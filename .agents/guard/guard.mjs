#!/usr/bin/env node
/**
 * guard: deterministic checks for a spectrace repository. Zero dependencies.
 *
 * One script behind Claude Code hooks, Antigravity hooks, git and CI. The rules live
 * here; the per-agent adapters only translate payloads and answers.
 *
 *   node guard.mjs --agent claude --event PreToolUse      (hook; payload JSON on stdin)
 *   node guard.mjs --all [--commits origin/main..HEAD]    (CI and manual run)
 *   add --record to save the raw payload under .agents/guard/records/
 *
 * Antigravity details marked "provisional" are not documented yet (error behaviour,
 * the field names inside toolCall.args). They are confirmed with --record (spec 035 T014).
 */
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, join, relative, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

export const CONTRACTS = [
  'AGENTS.md',
  'PRODUCT.md',
  'ARCHITECTURE.md',
  'ENGINEERING.md',
  'DESIGN.md',
  'TESTING.md',
  'CHANGES.md',
  'OPERATIONS.md',
];
export const LIMITS = { agentsWarn: 100, agentsError: 200, specWarn: 80, stopNudges: 2 };
const STATUSES = ['todo', 'in progress', 'done'];
const PROTECTED = /(^|[:+]|refs\/heads\/)(main|master)$/;

const error = (rule, message, where = {}) => ({ level: 'error', rule, message, ...where });
const warn = (rule, message, where = {}) => ({ level: 'warn', rule, message, ...where });
export const errorsOf = (findings) => findings.filter((f) => f.level === 'error');
export const formatFinding = (f) =>
  `${f.level} [${f.rule}] ${f.file ? f.file + (f.line ? `:${f.line}` : '') + ' ' : ''}${f.message}`;

// ---------------------------------------------------------------------------
// Shell parsing. Quote-aware so that text inside a commit message never counts
// as a flag: `git commit -m "explain --no-verify"` is fine.
// ---------------------------------------------------------------------------

function parseHeredocStart(src, at) {
  const m = /^<<(-?)[ \t]*(?:'([^']*)'|"([^"]*)"|\\?([A-Za-z_]\w*))/.exec(src.slice(at, at + 200));
  if (!m) return null;
  return { delim: m[2] ?? m[3] ?? m[4], strip: m[1] === '-', next: at + m[0].length };
}

function readHeredocBody(src, at, heredoc) {
  let i = at;
  let body = '';
  while (i < src.length) {
    let eol = src.indexOf('\n', i);
    if (eol < 0) eol = src.length;
    const line = src.slice(i, eol);
    const probe = heredoc.strip ? line.replace(/^\t+/, '') : line;
    i = eol + 1;
    if (probe.trimEnd() === heredoc.delim) return { body, next: i };
    body += `${line}\n`;
  }
  return { body, next: src.length };
}

function readDouble(src, at) {
  let out = '';
  let i = at;
  while (i < src.length) {
    const c = src[i];
    if (c === '"') return { text: out, next: i + 1 };
    if (c === '\\' && i + 1 < src.length) {
      out += '"\\$`'.includes(src[i + 1]) ? src[i + 1] : c + src[i + 1];
      i += 2;
    } else if (c === '$' && src[i + 1] === '(') {
      const sub = readSubstitution(src, i + 2);
      out += `$(${sub.text})`;
      i = sub.next;
    } else {
      out += c;
      i += 1;
    }
  }
  return { text: out, next: i };
}

function readSubstitution(src, at) {
  let depth = 1;
  let i = at;
  let out = '';
  const pending = [];
  while (i < src.length) {
    const c = src[i];
    if (c === "'") {
      const close = src.indexOf("'", i + 1);
      const end = close < 0 ? src.length : close + 1;
      out += src.slice(i, end);
      i = end;
    } else if (c === '"') {
      const dq = readDouble(src, i + 1);
      out += `"${dq.text}"`;
      i = dq.next;
    } else if (c === '\\') {
      out += src.slice(i, i + 2);
      i += 2;
    } else if (c === '<' && src[i + 1] === '<' && src[i + 2] !== '<') {
      const h = parseHeredocStart(src, i);
      if (h) {
        pending.push(h);
        out += src.slice(i, h.next);
        i = h.next;
      } else {
        out += c;
        i += 1;
      }
    } else if (c === '\n' && pending.length > 0) {
      out += '\n';
      i += 1;
      for (const h of pending) {
        const b = readHeredocBody(src, i, h);
        out += b.body;
        i = b.next;
      }
      pending.length = 0;
    } else {
      if (c === '(') depth += 1;
      if (c === ')' && --depth === 0) return { text: out, next: i + 1 };
      out += c;
      i += 1;
    }
  }
  return { text: out, next: i };
}

/** Splits a shell command into statements: { words, text } (text includes heredoc bodies). */
export function parseShell(src) {
  const statements = [];
  const pending = [];
  let words = [];
  let extra = [];
  let cur = '';
  let started = false;
  const endWord = () => {
    if (started) words.push(cur);
    cur = '';
    started = false;
  };
  const endStatement = () => {
    endWord();
    if (words.length > 0) statements.push({ words, text: [...words, ...extra].join('\n') });
    words = [];
    extra = [];
  };
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === "'") {
      const close = src.indexOf("'", i + 1);
      const end = close < 0 ? src.length : close;
      cur += src.slice(i + 1, end);
      started = true;
      i = end + 1;
    } else if (c === '"') {
      const dq = readDouble(src, i + 1);
      cur += dq.text;
      started = true;
      i = dq.next;
    } else if (c === '\\') {
      if (src[i + 1] !== '\n') cur += src[i + 1] ?? '';
      started = true;
      i += 2;
    } else if (c === '$' && src[i + 1] === '(') {
      const sub = readSubstitution(src, i + 2);
      cur += `$(${sub.text})`;
      started = true;
      i = sub.next;
    } else if (c === '@' && (src[i + 1] === "'" || src[i + 1] === '"') && /^\r?\n/.test(src.slice(i + 2, i + 4))) {
      // PowerShell here-string: @'  ...  '@ (or with double quotes), closed by a line that starts with '@
      const end = src.indexOf(`\n${src[i + 1]}@`, i + 2);
      cur += src.slice(i + 2, end < 0 ? src.length : end);
      started = true;
      i = end < 0 ? src.length : end + 3;
    } else if (c === '<' && src[i + 1] === '<' && src[i + 2] !== '<') {
      const h = parseHeredocStart(src, i);
      if (h) {
        pending.push(h);
        i = h.next;
      } else {
        cur += c;
        started = true;
        i += 1;
      }
    } else if (c === '\n') {
      i += 1;
      for (const h of pending) {
        const b = readHeredocBody(src, i, h);
        extra.push(b.body);
        i = b.next;
      }
      pending.length = 0;
      endStatement();
    } else if (c === ';' || c === '|' || c === '(' || c === ')') {
      endStatement();
      i += 1;
    } else if (c === '&') {
      if (src[i - 1] === '>' || src[i + 1] === '>') {
        cur += c;
        started = true;
      } else {
        endStatement();
      }
      i += 1;
    } else if (c === ' ' || c === '\t' || c === '\r') {
      endWord();
      i += 1;
    } else {
      cur += c;
      started = true;
      i += 1;
    }
  }
  endStatement();
  return statements;
}

// ---------------------------------------------------------------------------
// Command rules (PreToolUse on the shell tool, and commit message scans).
// ---------------------------------------------------------------------------

const WRAPPERS = new Set(['command', 'env', 'exec', 'time', 'sudo', 'nohup']);
const GIT_OPTS_WITH_ARG = new Set(['-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path']);
const PUSH_OPTS_WITH_ARG = new Set(['-o', '--push-option', '--repo', '--receive-pack', '--exec']);

function gitInvocation(words) {
  let i = 0;
  while (i < words.length && (/^\w+=/.test(words[i]) || WRAPPERS.has(words[i]))) i += 1;
  if (!/(^|[\\/])git(\.exe)?$/.test(words[i] ?? '')) return null;
  i += 1;
  while (i < words.length && words[i].startsWith('-')) i += GIT_OPTS_WITH_ARG.has(words[i]) ? 2 : 1;
  return i < words.length ? { sub: words[i], args: words.slice(i + 1) } : null;
}

/** Letters of a short-flag cluster, stopping at the first letter that takes an argument. */
function shortFlags(token, argLetters) {
  const flags = new Set();
  if (!/^-[A-Za-z]/.test(token)) return flags;
  for (const ch of token.slice(1)) {
    flags.add(ch);
    if (argLetters.includes(ch)) break;
  }
  return flags;
}

export function claudeAttribution(text) {
  return /^\s*co-authored-by:\s*(claude\b|.*@anthropic\.com)/im.test(text) || /generated with\b.*\bclaude\b/i.test(text);
}

function pushTargets(args) {
  const positional = [];
  for (let i = 0; i < args.length; i += 1) {
    if (PUSH_OPTS_WITH_ARG.has(args[i])) i += 1;
    else if (!args[i].startsWith('-')) positional.push(args[i]);
  }
  return positional;
}

/** `branch` is the current branch, read lazily by the caller; it matters for a bare `git push -f`. */
export function checkCommand(command, { branch = () => '' } = {}) {
  const findings = [];
  for (const stmt of parseShell(command)) {
    const git = gitInvocation(stmt.words);
    const isGhPr = stmt.words[0] === 'gh' && stmt.words[1] === 'pr';
    if (isGhPr && claudeAttribution(stmt.text)) {
      findings.push(error('no-claude-attribution', 'Do not add Claude attribution to pull requests.'));
    }
    if (!git) continue;
    const { sub, args } = git;
    if (sub === 'commit' && claudeAttribution(stmt.text)) {
      findings.push(error('no-claude-attribution', 'Do not add Co-Authored-By or "Generated with" Claude lines to commits.'));
    }
    const skipsHooks =
      args.includes('--no-verify') || (sub === 'commit' && args.some((a) => shortFlags(a, 'mFcCStu').has('n')));
    if (['commit', 'push', 'merge'].includes(sub) && skipsHooks) {
      findings.push(error('no-verify', `Do not bypass hooks (git ${sub} --no-verify).`));
    }
    if (sub === 'push') {
      const forced =
        args.some((a) => /^--force(-with-lease|-if-includes)?(=|$)/.test(a) || shortFlags(a, 'o').has('f')) ||
        pushTargets(args).slice(1).some((t) => t.startsWith('+'));
      const targets = pushTargets(args).slice(1);
      const toProtected = targets.length > 0 ? targets.some((t) => PROTECTED.test(t)) : PROTECTED.test(branch());
      if (forced && toProtected) findings.push(error('force-push-main', 'Do not force-push to main or master.'));
    }
    if (sub === 'add') {
      const secret = args.some((a) => /(^|[\\/])\.env(\.[\w.-]+)?$/.test(a) && !/\.(example|sample|template)$/.test(a));
      if (secret) findings.push(error('env-add', 'Do not stage .env files; they hold secrets.'));
    }
  }
  return findings;
}

export function checkCommitMessages(commits) {
  return commits
    .filter((c) => claudeAttribution(c.message))
    .map((c) => error('no-claude-attribution', `commit ${c.hash.slice(0, 8)} carries Claude attribution.`));
}

// ---------------------------------------------------------------------------
// Specs and roadmap.
// ---------------------------------------------------------------------------

function expandIds(text) {
  const ids = new Set(text.match(/[RD]\d+/g) ?? []);
  for (const m of text.matchAll(/([RD])(\d+)\s*[–-]\s*\1?(\d+)/g)) {
    for (let n = Number(m[2]); n <= Number(m[3]); n += 1) ids.add(`${m[1]}${n}`);
  }
  return [...ids];
}

export function parseSpec(text, file = '') {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  while (lines.length > 0 && lines.at(-1) === '') lines.pop();
  const spec = { file, lineCount: lines.length, title: null, sections: new Set(), reqs: [], designs: [], tasks: [] };
  let section = '';
  let current = null;
  lines.forEach((raw, index) => {
    const line = index + 1;
    const h1 = /^#\s+(.+)$/.exec(raw);
    if (h1 && !spec.title) {
      spec.title = { text: h1[1], line };
      return;
    }
    const h2 = /^##\s+(.+?)\s*$/.exec(raw);
    if (h2) {
      section = h2[1].toLowerCase();
      spec.sections.add(section);
      current = null;
      return;
    }
    if (section === 'requirements') {
      const m = /^\s*-\s*(~~)?\s*R(\d+)\b/.exec(raw);
      if (m) spec.reqs.push({ id: `R${m[2]}`, struck: Boolean(m[1]), line });
    } else if (section === 'design') {
      const m = /^\s*-\s*(~~)?\s*D(\d+)\b\s*(?:\(([^)]*)\))?/.exec(raw);
      if (m) {
        spec.designs.push({
          id: `D${m[2]}`,
          struck: Boolean(m[1]),
          reqs: expandIds(m[3] ?? '').filter((id) => id.startsWith('R')),
          arrow: /→\s*([DR]\d+)/.exec(raw)?.[1] ?? null,
          line,
        });
      }
    } else if (section === 'tasks') {
      const m = /^\s*-\s*(~~)?\[( |x)\]\s+(\d+)\/T(\d+[a-z]?)\s+(.*)$/i.exec(raw);
      if (m) {
        const rest = m[5];
        const tagText = /^((?:\[[a-z]+\])+)\s*/i.exec(rest)?.[1] ?? '';
        const covers = /[—–]\s*(?:covers|replaces)\s+(.+)$/i.exec(rest)?.[1] ?? '';
        current = {
          id: `${m[3]}/T${m[4]}`,
          specNumber: Number(m[3]),
          struck: Boolean(m[1]),
          done: m[2].toLowerCase() === 'x',
          tags: (tagText.match(/[a-z]+/gi) ?? []).map((t) => t.toLowerCase()),
          covers: expandIds(covers),
          verified: false,
          line,
        };
        spec.tasks.push(current);
      } else if (current && /^\s+verified:/i.test(raw)) {
        current.verified = true;
      }
    }
  });
  return spec;
}

export function lintSpec(text, file = '') {
  const spec = parseSpec(text, file);
  const where = (line) => ({ file, line });
  const findings = [];
  const fileNumber = /^(\d+)-/.exec(basename(file))?.[1];

  const titleNumber = /^(\d+)\s*[—–-]/.exec(spec.title?.text ?? '')?.[1];
  if (!titleNumber) findings.push(error('spec-title', 'The H1 must be "# NNN — name".', where(spec.title?.line ?? 1)));
  else if (fileNumber && Number(titleNumber) !== Number(fileNumber)) {
    findings.push(error('spec-title', `Title number ${titleNumber} does not match the file name.`, where(spec.title.line)));
  }
  for (const needed of ['goal', 'requirements', 'tasks']) {
    if (!spec.sections.has(needed)) findings.push(error('spec-section', `Missing "## ${needed[0].toUpperCase()}${needed.slice(1)}".`, where(1)));
  }

  const reqs = spec.reqs.filter((r) => !r.struck);
  const designs = spec.designs;
  const tasks = spec.tasks.filter((t) => !t.struck);
  const known = new Set([...spec.reqs, ...designs].map((i) => i.id));
  for (const [list, label] of [[spec.reqs, 'requirement'], [designs, 'design']]) {
    const seen = new Set();
    for (const item of list) {
      if (seen.has(item.id)) findings.push(error('duplicate-id', `Duplicate ${label} ${item.id}.`, where(item.line)));
      seen.add(item.id);
    }
  }
  for (const d of designs.filter((x) => x.struck)) {
    if (!d.arrow || !known.has(d.arrow)) {
      findings.push(error('struck-target', `Struck ${d.id} must point to an existing item with "→".`, where(d.line)));
    }
  }

  const seenTasks = new Set();
  for (const t of tasks) {
    if (seenTasks.has(t.id)) findings.push(error('duplicate-id', `Duplicate task ${t.id}.`, where(t.line)));
    seenTasks.add(t.id);
    if (fileNumber && t.specNumber !== Number(fileNumber)) {
      findings.push(error('task-id', `Task ${t.id} does not belong to spec ${fileNumber}.`, where(t.line)));
    }
    if (!t.tags.includes('agent') && !t.tags.includes('human')) {
      findings.push(error('task-tag', `Task ${t.id} needs [agent] or [human].`, where(t.line)));
    }
    if (t.covers.length === 0) findings.push(warn('task-covers', `Task ${t.id} has no "— covers …".`, where(t.line)));
    if (t.done && !t.verified) findings.push(error('task-verified', `Checked task ${t.id} needs a "verified:" line.`, where(t.line)));
  }

  const reach = (task) => new Set(task.covers.flatMap((id) => [id, ...designs.filter((d) => d.id === id).flatMap((d) => d.reqs)]));
  if (!tasks.some((t) => t.tags.includes('test'))) {
    findings.push(error('spec-test', 'The spec has no [test] task.', where(1)));
  }
  for (const r of reqs) {
    if (!tasks.some((t) => reach(t).has(r.id))) findings.push(error('req-covered', `${r.id} is not covered by any task.`, where(r.line)));
    else if (!tasks.some((t) => t.tags.includes('test') && reach(t).has(r.id))) {
      findings.push(error('req-test', `${r.id} has no [test] task.`, where(r.line)));
    }
  }

  if (spec.lineCount > LIMITS.specWarn) {
    findings.push(warn('spec-length', `${spec.lineCount} lines; keep a spec under ${LIMITS.specWarn}.`, where(1)));
  }
  return findings;
}

const normalizeId = (id) => String(Number.parseInt(id, 10)).padStart(3, '0');

export function parseRoadmap(text) {
  const rows = [];
  text.replace(/\r\n/g, '\n').split('\n').forEach((raw, index) => {
    const m = /^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|/.exec(raw);
    if (m) rows.push({ id: normalizeId(m[1]), name: m[2], status: m[3].toLowerCase(), deps: m[4], line: index + 1 });
  });
  return rows;
}

/** `specs` maps a normalized id to { file, spec } for every spec file present. */
export function checkRoadmap(text, specs, file = 'planning/roadmap.md') {
  const findings = [];
  const rows = parseRoadmap(text);
  const listed = new Set();
  for (const row of rows) {
    const where = { file, line: row.line };
    if (listed.has(row.id)) findings.push(error('roadmap-duplicate', `Spec ${row.id} is listed twice.`, where));
    listed.add(row.id);
    if (!STATUSES.includes(row.status)) {
      findings.push(error('roadmap-status', `Status "${row.status}" must be todo, in progress or done.`, where));
      continue;
    }
    const entry = specs.get(row.id);
    const tasks = entry ? entry.spec.tasks.filter((t) => !t.struck && t.tags.includes('agent')) : [];
    if (!entry && row.status !== 'done') findings.push(error('roadmap-file', `Spec ${row.id} is ${row.status} but has no file.`, where));
    if (row.status === 'done' && tasks.some((t) => !t.done)) {
      findings.push(error('roadmap-done', `Spec ${row.id} is done but has open [agent] tasks.`, where));
    }
    if (row.status === 'todo' && tasks.some((t) => t.done)) {
      findings.push(error('roadmap-todo', `Spec ${row.id} has completed tasks; mark it in progress.`, where));
    }
    const everything = entry ? entry.spec.tasks.filter((t) => !t.struck) : [];
    if (row.status === 'in progress' && everything.length > 0 && everything.every((t) => t.done)) {
      findings.push(warn('roadmap-close', `Spec ${row.id}: every task is done; mark it done.`, where));
    }
  }
  for (const [id, entry] of specs) {
    if (!listed.has(id)) findings.push(error('roadmap-missing', `Spec ${id} has no row in the roadmap.`, { file: entry.file }));
  }
  return findings;
}

// ---------------------------------------------------------------------------
// Contracts.
// ---------------------------------------------------------------------------

/** The files named in the second column of the router table in AGENTS.md. */
export function routerTargets(text) {
  return [...text.replace(/\r\n/g, '\n').matchAll(/^\|[^|]+\|\s*([^|\s]+\.md)\s*\|$/gm)].map((m) => m[1]);
}

/** `root`, when given, lets AGENTS.md be checked against the files it routes to. */
export function checkContract(name, text, root = null) {
  const head = text.replace(/\r\n/g, '\n').split('\n').slice(0, 8);
  const findings = [];
  if (name === 'AGENTS.md' && root) {
    for (const target of routerTargets(text).filter((t) => !existsSync(join(root, t)))) {
      findings.push(error('router-target', `The router points at ${target}, which does not exist.`, { file: name }));
    }
  }
  if (!head.some((l) => /^>\s*Owns:.*Not here:/i.test(l))) {
    findings.push(error('contract-header', 'Open with "> Owns: … · Not here: …".', { file: name, line: 1 }));
  }
  const unfilled = (text.match(/<fill:|\{\{[A-Z_]+\}\}/g) ?? []).length;
  if (unfilled > 0) findings.push(warn('contract-unfilled', `${unfilled} placeholder(s) left to fill.`, { file: name }));
  if (name === 'AGENTS.md') {
    const count = text.replace(/\r\n/g, '\n').replace(/\n+$/, '').split('\n').length;
    if (count > LIMITS.agentsError) findings.push(error('agents-length', `${count} lines; the hard cap is ${LIMITS.agentsError}.`, { file: name }));
    else if (count > LIMITS.agentsWarn) findings.push(warn('agents-length', `${count} lines; keep AGENTS.md under ${LIMITS.agentsWarn}.`, { file: name }));
  }
  return findings;
}

export function checkContracts(root) {
  const findings = [];
  for (const name of CONTRACTS) {
    const path = join(root, name);
    if (!existsSync(path)) {
      findings.push((name === 'AGENTS.md' ? error : warn)('contract-missing', `${name} is missing.`, { file: name }));
    } else {
      findings.push(...checkContract(name, readFileSync(path, 'utf8'), root));
    }
  }
  return findings;
}

// ---------------------------------------------------------------------------
// Repository-level runs.
// ---------------------------------------------------------------------------

function loadSpecs(root) {
  const dir = join(root, 'planning', 'specs');
  const specs = new Map();
  if (!existsSync(dir)) return specs;
  for (const name of readdirSync(dir).filter((n) => /^\d+-.+\.md$/.test(n))) {
    const file = `planning/specs/${name}`;
    specs.set(normalizeId(name), { file, text: readFileSync(join(dir, name), 'utf8') });
  }
  for (const entry of specs.values()) entry.spec = parseSpec(entry.text, entry.file);
  return specs;
}

const roadmapOf = (root) => {
  const path = join(root, 'planning', 'roadmap.md');
  return existsSync(path) ? readFileSync(path, 'utf8') : null;
};

/** Checks a set of repo-relative paths; the hook handlers and the Stop gate use it. */
export function checkPaths(root, paths) {
  const findings = [];
  const specs = loadSpecs(root);
  const roadmap = roadmapOf(root);
  let roadmapChecked = false;
  for (const rel of new Set(paths)) {
    if (/^planning\/specs\/\d+-.+\.md$/.test(rel) && existsSync(join(root, rel))) {
      findings.push(...lintSpec(readFileSync(join(root, rel), 'utf8'), rel));
      roadmapChecked ||= roadmap !== null;
    } else if (rel === 'planning/roadmap.md') {
      roadmapChecked ||= roadmap !== null;
    } else if (CONTRACTS.includes(rel) && existsSync(join(root, rel))) {
      findings.push(...checkContract(rel, readFileSync(join(root, rel), 'utf8'), root));
    }
  }
  if (roadmapChecked) findings.push(...checkRoadmap(roadmap, specs));
  return findings;
}

const git = (root, args) => {
  try {
    return execFileSync('git', args, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch {
    return '';
  }
};

export function commitsInRange(root, range) {
  return git(root, ['log', '--format=%H%x1f%B%x1e', range])
    .split('\x1e')
    .map((chunk) => chunk.trim())
    .filter(Boolean)
    .map((chunk) => {
      const [hash, message = ''] = chunk.split('\x1f');
      return { hash, message };
    });
}

export function checkAll(root, { range } = {}) {
  const findings = checkContracts(root);
  const specs = loadSpecs(root);
  for (const entry of specs.values()) findings.push(...lintSpec(entry.text, entry.file));
  const roadmap = roadmapOf(root);
  if (roadmap !== null) findings.push(...checkRoadmap(roadmap, specs));
  else findings.push(warn('roadmap-missing', 'planning/roadmap.md is missing.', { file: 'planning/roadmap.md' }));
  if (range) findings.push(...checkCommitMessages(commitsInRange(root, range)));
  return findings;
}

const changedPlanningFiles = (root) =>
  git(root, ['status', '--porcelain', '-uall'])
    .split('\n')
    .map((l) => l.slice(3).split(' -> ').at(-1).trim())
    .filter((p) => p.startsWith('planning/') || CONTRACTS.includes(p));

// ---------------------------------------------------------------------------
// Agent adapters: translate each payload into one context, then render the answer.
// ---------------------------------------------------------------------------

const stringsOf = (input) => Object.values(input).filter((v) => typeof v === 'string');

export function contextOf(agent, payload, eventArg) {
  if (agent === 'antigravity') {
    const call = payload.toolCall ?? {};
    return {
      event: eventArg,
      tool: call.name ?? '',
      input: call.args ?? {},
      root: payload.workspacePaths?.[0],
      stopActive: false,
      shell: /run_command|bash|shell|terminal|exec/i.test(call.name ?? ''),
    };
  }
  return {
    event: eventArg ?? payload.hook_event_name,
    tool: payload.tool_name ?? '',
    input: payload.tool_input ?? {},
    root: payload.cwd,
    stopActive: Boolean(payload.stop_hook_active),
    // On Windows Claude Code routes shell commands through the PowerShell tool, and a hook that
    // matches only Bash never fires there.
    shell: payload.tool_name === 'Bash' || payload.tool_name === 'PowerShell',
  };
}

export const commandOf = (input) =>
  input.command ?? input.CommandLine ?? input.commandLine ?? input.cmd ?? stringsOf(input).sort((a, b) => b.length - a.length)[0] ?? '';

export function editedPaths(root, input) {
  return stringsOf(input)
    .filter((v) => v.endsWith('.md'))
    .map((v) => relative(root, resolve(root, v)).split('\\').join('/'))
    .filter((p) => !p.startsWith('..'));
}

/**
 * Antigravity sends no stop_hook_active, so a Stop hook that keeps answering "continue" could loop
 * forever on a problem the agent cannot fix. After the same errors were reported LIMITS.stopNudges
 * times in a conversation, report a warning instead and let the agent stop; CI still fails.
 */
export function limitRepeats(findings, key, dir = tmpdir()) {
  const file = join(dir, `spectrace-guard-${String(key).replace(/[^\w-]/g, '_')}.json`);
  const errors = errorsOf(findings);
  if (errors.length === 0) {
    rmSync(file, { force: true });
    return findings;
  }
  const signature = errors.map(formatFinding).join('\n');
  let previous = { signature: '', count: 0 };
  try {
    previous = JSON.parse(readFileSync(file, 'utf8'));
  } catch {
    // first report in this conversation
  }
  const count = previous.signature === signature ? previous.count + 1 : 1;
  writeFileSync(file, JSON.stringify({ signature, count }), 'utf8');
  if (count <= LIMITS.stopNudges) return findings;
  return [warn('stop-budget', `The same ${errors.length} problem(s) were reported ${LIMITS.stopNudges} times; letting the agent stop. CI will still fail.`)];
}

export function handleHook(agent, payload, { event: eventArg, root: rootArg, stateDir } = {}) {
  const ctx = contextOf(agent, payload, eventArg);
  const root = resolve(rootArg ?? ctx.root ?? process.cwd());
  if (ctx.event === 'PreToolUse' && ctx.shell) {
    return checkCommand(commandOf(ctx.input), { branch: () => git(root, ['rev-parse', '--abbrev-ref', 'HEAD']).trim() });
  }
  if (ctx.event === 'PostToolUse') return checkPaths(root, editedPaths(root, ctx.input));
  if (ctx.event === 'Stop' && !ctx.stopActive) {
    const found = checkPaths(root, changedPlanningFiles(root));
    return agent === 'antigravity' ? limitRepeats(found, payload.conversationId ?? root, stateDir) : found;
  }
  return [];
}

/** Returns { code, stdout, stderr }. Claude blocks with exit 2; Antigravity answers with JSON (provisional). */
export function render(agent, event, findings) {
  const errors = errorsOf(findings);
  const message = findings.map(formatFinding).join('\n');
  if (agent === 'antigravity') {
    if (event === 'PreToolUse') {
      return { code: 0, stdout: JSON.stringify(errors.length > 0 ? { decision: 'deny', reason: message } : { decision: 'allow' }), stderr: '' };
    }
    if (event === 'Stop') {
      return { code: 0, stdout: JSON.stringify(errors.length > 0 ? { decision: 'continue', reason: message } : { decision: 'allow' }), stderr: '' };
    }
    return { code: 0, stdout: '', stderr: message };
  }
  return errors.length > 0 ? { code: 2, stdout: '', stderr: message } : { code: 0, stdout: '', stderr: message };
}

// ---------------------------------------------------------------------------
// CLI.
// ---------------------------------------------------------------------------

const USAGE = `Usage:
  guard.mjs --all [--commits <range>] [--root <dir>]
      check contracts, specs, roadmap and, with --commits, commit messages
  guard.mjs --agent claude|antigravity --event PreToolUse|PostToolUse|Stop [--record] [--root <dir>]
      hook mode: the agent's payload JSON arrives on stdin`;

/** Reads the hook payload; returns null on a terminal, where there is nothing to read and waiting would hang. */
const stdinText = () => (process.stdin.isTTY ? null : readFileSync(0, 'utf8'));

function parseArgs(argv) {
  const opts = { all: false, record: false, help: false };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--help' || a === '-h') opts.help = true;
    else if (a === '--all') opts.all = true;
    else if (a === '--record') opts.record = true;
    else if (['--agent', '--event', '--commits', '--root'].includes(a)) opts[a.slice(2)] = argv[(i += 1)];
  }
  return opts;
}

function record(root, agent, event, raw) {
  const dir = join(root, '.agents', 'guard', 'records');
  mkdirSync(dir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  writeFileSync(join(dir, `${agent}-${event ?? 'event'}-${stamp}.json`), raw, 'utf8');
}

export function main(argv, readStdin = stdinText) {
  const opts = parseArgs(argv);
  const root = resolve(opts.root ?? process.cwd());
  if (opts.help) {
    console.log(USAGE);
    return 0;
  }
  if (opts.all || opts.commits) {
    const findings = checkAll(root, { range: opts.commits });
    for (const f of findings) console.log(formatFinding(f));
    const failed = errorsOf(findings).length;
    console.log(`guard: ${failed} error(s), ${findings.length - failed} warning(s).`);
    return failed > 0 ? 1 : 0;
  }
  const agent = opts.agent ?? 'claude';
  const raw = readStdin();
  if (raw === null) {
    console.error(USAGE);
    return 2;
  }
  if (opts.record) record(root, agent, opts.event, raw);
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    console.error('guard: payload is not JSON; nothing checked.');
    return 0;
  }
  const event = opts.event ?? contextOf(agent, payload).event;
  const out = render(agent, event, handleHook(agent, payload, { event, root: opts.root }));
  if (out.stdout) console.log(out.stdout);
  if (out.stderr) console.error(out.stderr);
  return out.code;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = main(process.argv.slice(2));
}
