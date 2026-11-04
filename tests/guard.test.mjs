import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { after, test } from 'node:test';
import {
  checkAll,
  checkCommand,
  checkContract,
  checkRoadmap,
  handleHook,
  lintSpec,
  main,
  parseShell,
  parseSpec,
  render,
} from '../skills/spectrace/assets/guard/guard.mjs';

const made = [];
after(() => made.forEach((dir) => rmSync(dir, { recursive: true, force: true })));

function makeRepo(files = {}, { git = false } = {}) {
  const root = mkdtempSync(join(tmpdir(), 'guard-'));
  made.push(root);
  for (const [name, content] of Object.entries(files)) {
    mkdirSync(dirname(join(root, name)), { recursive: true });
    writeFileSync(join(root, name), content);
  }
  if (git) execFileSync('git', ['init', '-q'], { cwd: root });
  return root;
}

const commit = (root, message) =>
  execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '--allow-empty', '-m', message], { cwd: root });

const ids = (findings) => findings.map((f) => `${f.level}:${f.rule}`).sort();
const rules = (findings) => findings.map((f) => f.rule).sort();

// ---------------------------------------------------------------------------
// Shell parsing
// ---------------------------------------------------------------------------

const HEREDOC_CLEAN = `git commit -m "$(cat <<'EOF'
fix: handle a (partial "quoted" case, do not use --no-verify here

Body with ) and ( unbalanced.
EOF
)"`;

const HEREDOC_TRAILER = `git commit -m "$(cat <<'EOF'
feat: add x

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
EOF
)"`;

const parseCases = [
  { name: 'splits on && and ;', cmd: 'a && b; c', statements: 3 },
  { name: 'keeps a quoted message as one word', cmd: 'git commit -m "feat: add x"', words: ['git', 'commit', '-m', 'feat: add x'] },
  { name: 'single quotes are literal', cmd: "echo 'a && b'", words: ['echo', 'a && b'] },
  { name: 'an escaped quote stays inside the word', cmd: 'echo "say \\"hi\\""', words: ['echo', 'say "hi"'] },
  { name: 'a heredoc inside $() stays one statement', cmd: HEREDOC_CLEAN, statements: 1 },
  { name: '2>&1 does not split the statement', cmd: 'npm test 2>&1 | tee out.log', statements: 2 },
  { name: 'an empty string is an empty word', cmd: 'echo ""', words: ['echo', ''] },
];

for (const row of parseCases) {
  test(`parseShell: ${row.name}`, () => {
    const statements = parseShell(row.cmd);
    assert.equal(row.statements ?? statements.length, statements.length);
    assert.deepEqual(row.words ?? statements[0].words, statements[0].words);
  });
}

// ---------------------------------------------------------------------------
// Command rules
// ---------------------------------------------------------------------------

const commandCases = [
  { name: 'plain commit', cmd: 'git commit -m "feat: add x"', expect: [] },
  { name: 'flag text inside the message is not a flag', cmd: 'git commit -m "docs: explain --no-verify"', expect: [] },
  { name: '-m with attached text containing n is not -n', cmd: 'git commit -mnone', expect: [] },
  { name: '-am cluster without n', cmd: 'git commit -am "handle none"', expect: [] },
  { name: '--no-verify', cmd: 'git commit --no-verify -m x', expect: ['no-verify'] },
  { name: '-n short flag', cmd: 'git commit -n -m x', expect: ['no-verify'] },
  { name: '-n inside a cluster', cmd: 'git commit -anm x', expect: ['no-verify'] },
  { name: 'after && in a chain', cmd: 'git add src && git commit --no-verify -m x', expect: ['no-verify'] },
  { name: 'behind env assignments and -C', cmd: 'A=1 git -C repo commit --no-verify -m x', expect: ['no-verify'] },
  { name: 'push --no-verify', cmd: 'git push --no-verify origin feature', expect: ['no-verify'] },
  { name: 'echo is not git', cmd: 'echo git commit --no-verify', expect: [] },
  { name: 'trailer in a second -m', cmd: 'git commit -m "feat: x" -m "Co-Authored-By: Claude <noreply@anthropic.com>"', expect: ['no-claude-attribution'] },
  { name: 'trailer inside a heredoc', cmd: HEREDOC_TRAILER, expect: ['no-claude-attribution'] },
  { name: 'heredoc with parens, quotes and --no-verify text is clean', cmd: HEREDOC_CLEAN, expect: [] },
  { name: 'a human co-author is allowed', cmd: 'git commit -m x -m "Co-Authored-By: Ana <ana@example.com>"', expect: [] },
  { name: 'Generated with Claude Code line', cmd: 'git commit -m "x" -m "Generated with [Claude Code](https://claude.com/claude-code)"', expect: ['no-claude-attribution'] },
  { name: 'pull request body with attribution', cmd: 'gh pr create --title t --body "🤖 Generated with [Claude Code](https://claude.com/claude-code)"', expect: ['no-claude-attribution'] },
  { name: 'clean pull request', cmd: 'gh pr create --title t --body "Adds guard"', expect: [] },
  { name: 'force push to main', cmd: 'git push --force origin main', expect: ['force-push-main'] },
  { name: '-f to master', cmd: 'git push -f origin master', expect: ['force-push-main'] },
  { name: 'plus refspec', cmd: 'git push origin +main', expect: ['force-push-main'] },
  { name: 'force-with-lease to main', cmd: 'git push --force-with-lease origin main', expect: ['force-push-main'] },
  { name: 'force push to a feature branch', cmd: 'git push --force origin feature/x', expect: [] },
  { name: 'normal push to main', cmd: 'git push origin main', expect: [] },
  { name: 'bare -f on main', cmd: 'git push -f', branch: 'main', expect: ['force-push-main'] },
  { name: 'bare -f on a feature branch', cmd: 'git push -f', branch: 'feat/a', expect: [] },
  { name: 'staging .env', cmd: 'git add .env', expect: ['env-add'] },
  { name: 'staging a nested .env.local', cmd: 'git add src/.env.local', expect: ['env-add'] },
  { name: '.env.example is allowed', cmd: 'git add .env.example', expect: [] },
  { name: 'git add -A is not inspected', cmd: 'git add -A', expect: [] },
  { name: 'compound violation reports both', cmd: 'git add .env && git commit --no-verify -m x', expect: ['env-add', 'no-verify'] },
];

for (const row of commandCases) {
  test(`checkCommand: ${row.name}`, () => {
    assert.deepEqual(rules(checkCommand(row.cmd, { branch: () => row.branch ?? '' })), row.expect);
  });
}

// ---------------------------------------------------------------------------
// Spec lint
// ---------------------------------------------------------------------------

const VALID_SPEC = `# 007 — sample

## Goal
Something works.

## Requirements
- R1: First thing.
- R2: Second thing.

## Design
- D1 (R1): Decision one.
- D2 (R2): Decision two.

## Tasks
- [x] 007/T001 [agent] Build it — covers D1
      verified: ran it
- [ ] 007/T002 [agent][test] Test the first — covers R1
- [ ] 007/T003 [agent][test] Test the second — covers D2
`;
const SPEC_FILE = 'planning/specs/007-sample.md';

const specCases = [
  { name: 'valid spec', mutate: (s) => s, expect: [] },
  { name: 'valid spec with CRLF line endings', mutate: (s) => s.replace(/\n/g, '\r\n'), expect: [] },
  { name: 'a range in covers reaches every id', mutate: (s) => s.replace('covers R1\n', 'covers R1–R2\n').replace(/- \[ \] 007\/T003.*\n/, ''), expect: [] },
  { name: 'a struck requirement needs no task', mutate: (s) => s.replace('## Design', '- ~~R3: gone~~\n\n## Design'), expect: [] },
  { name: 'a struck design pointing at an existing item', mutate: (s) => s.replace('## Tasks', '- ~~D3 (R1): old~~ → D1\n\n## Tasks'), expect: [] },
  { name: 'missing Tasks section', mutate: (s) => s.slice(0, s.indexOf('## Tasks')), expect: ['error:req-covered', 'error:req-covered', 'error:spec-section', 'error:spec-test'] },
  { name: 'requirement with no task', mutate: (s) => s.replace(/- \[ \] 007\/T003.*\n/, ''), expect: ['error:req-covered'] },
  { name: 'requirement with no [test] task', mutate: (s) => s.replace('T003 [agent][test]', 'T003 [agent]'), expect: ['error:req-test'] },
  { name: 'no [test] task at all', mutate: (s) => s.replaceAll('[agent][test]', '[agent]'), expect: ['error:req-test', 'error:req-test', 'error:spec-test'] },
  { name: 'checked task without verified:', mutate: (s) => s.replace(/ {6}verified: ran it\n/, ''), expect: ['error:task-verified'] },
  { name: 'task id from another spec', mutate: (s) => s.replace('007/T002', '008/T002'), expect: ['error:task-id'] },
  { name: 'duplicate requirement', mutate: (s) => s.replace('- R2: Second thing.', '- R2: Second thing.\n- R2: again.'), expect: ['error:duplicate-id'] },
  { name: 'task without [agent] or [human]', mutate: (s) => s.replace('[agent] Build it', 'Build it'), expect: ['error:task-tag'] },
  { name: 'struck design pointing nowhere', mutate: (s) => s.replace('## Tasks', '- ~~D3 (R1): old~~ → D9\n\n## Tasks'), expect: ['error:struck-target'] },
  { name: 'title number differs from the file', mutate: (s) => s.replace('# 007', '# 008'), expect: ['error:spec-title'] },
  { name: 'task without covers is a warning', mutate: (s) => s.replace('Build it — covers D1', 'Build it'), expect: ['warn:task-covers'] },
  { name: 'a long spec is a warning, not an error', mutate: (s) => `${s}\n## Changes\n${'- note\n'.repeat(80)}`, expect: ['warn:spec-length'] },
];

for (const row of specCases) {
  test(`lintSpec: ${row.name}`, () => {
    assert.deepEqual(ids(lintSpec(row.mutate(VALID_SPEC), SPEC_FILE)), row.expect);
  });
}

test('parseSpec: a design item maps to the requirements in its parentheses', () => {
  const spec = parseSpec(VALID_SPEC, SPEC_FILE);
  assert.deepEqual(spec.designs.map((d) => [d.id, d.reqs]), [['D1', ['R1']], ['D2', ['R2']]]);
});

// ---------------------------------------------------------------------------
// Roadmap
// ---------------------------------------------------------------------------

const taskLines = (...states) => states.map((s, i) => `- [${s.done ? 'x' : ' '}] 009/T00${i + 1} [${s.kind ?? 'agent'}] t — covers R1`).join('\n');
const specOf = (...states) => ({ file: 'planning/specs/009-x.md', spec: parseSpec(`# 009 — x\n\n## Tasks\n${taskLines(...states)}\n`) });
const table = (status) => `| ID | Spec | Status | Depends on |\n|---|---|---|---|\n| 009 | x | ${status} | — |\n`;
const DONE = { done: true };
const OPEN = { done: false };

const roadmapCases = [
  { name: 'done with every agent task done', text: table('done'), specs: [specOf(DONE)], expect: [] },
  { name: 'done with an open agent task', text: table('done'), specs: [specOf(DONE, OPEN)], expect: ['error:roadmap-done'] },
  { name: 'an open human task does not block done', text: table('done'), specs: [specOf(DONE, { done: false, kind: 'human' })], expect: [] },
  { name: 'done and the spec file was deleted', text: table('done'), specs: [], expect: [] },
  { name: 'todo with a completed task', text: table('todo'), specs: [specOf(DONE, OPEN)], expect: ['error:roadmap-todo'] },
  { name: 'todo without a file', text: table('todo'), specs: [], expect: ['error:roadmap-file'] },
  { name: 'in progress with everything done', text: table('in progress'), specs: [specOf(DONE)], expect: ['warn:roadmap-close'] },
  { name: 'in progress with work left', text: table('in progress'), specs: [specOf(DONE, OPEN)], expect: [] },
  { name: 'invalid status', text: table('blocked'), specs: [specOf(OPEN)], expect: ['error:roadmap-status'] },
  { name: 'duplicate row', text: `${table('todo')}| 009 | x | todo | — |\n`, specs: [specOf(OPEN)], expect: ['error:roadmap-duplicate'] },
  { name: 'spec file with no row', text: '| ID | Spec | Status | Depends on |\n|---|---|---|---|\n', specs: [specOf(OPEN)], expect: ['error:roadmap-missing'] },
];

for (const row of roadmapCases) {
  test(`checkRoadmap: ${row.name}`, () => {
    const specs = new Map(row.specs.map((s) => ['009', s]));
    assert.deepEqual(ids(checkRoadmap(row.text, specs)), row.expect);
  });
}

// ---------------------------------------------------------------------------
// Contracts
// ---------------------------------------------------------------------------

const HEADER = '# T\n\n> Owns: a · Not here: b → see X\n';
const withLines = (n) => `${HEADER}${'line\n'.repeat(n - 3)}`;

const contractCases = [
  { name: 'header present', file: 'PRODUCT.md', text: HEADER, expect: [] },
  { name: 'header missing', file: 'PRODUCT.md', text: '# T\n\nbody\n', expect: ['error:contract-header'] },
  { name: 'AGENTS.md at the warning boundary', file: 'AGENTS.md', text: withLines(100), expect: [] },
  { name: 'AGENTS.md one line over', file: 'AGENTS.md', text: withLines(101), expect: ['warn:agents-length'] },
  { name: 'AGENTS.md at the hard cap', file: 'AGENTS.md', text: withLines(200), expect: ['warn:agents-length'] },
  { name: 'AGENTS.md over the hard cap', file: 'AGENTS.md', text: withLines(201), expect: ['error:agents-length'] },
  { name: 'other contracts have no length limit', file: 'TESTING.md', text: withLines(400), expect: [] },
  { name: 'a <fill:> marker left behind is a warning', file: 'PRODUCT.md', text: `${HEADER}<fill: users>\n`, expect: ['warn:contract-unfilled'] },
  { name: 'a {{TOKEN}} left behind is a warning', file: 'PRODUCT.md', text: `${HEADER}{{GOAL}}\n`, expect: ['warn:contract-unfilled'] },
];

for (const row of contractCases) {
  test(`checkContract: ${row.name}`, () => {
    assert.deepEqual(ids(checkContract(row.file, row.text)), row.expect);
  });
}

// ---------------------------------------------------------------------------
// Whole repository
// ---------------------------------------------------------------------------

const contractFiles = Object.fromEntries(
  ['AGENTS', 'PRODUCT', 'ARCHITECTURE', 'ENGINEERING', 'DESIGN', 'TESTING', 'CHANGES', 'OPERATIONS'].map((n) => [`${n}.md`, HEADER]),
);
const goodRepo = (extra = {}) =>
  makeRepo({ ...contractFiles, 'planning/roadmap.md': `${table('in progress').replace('009', '007').replace('| x |', '| sample |')}`, [SPEC_FILE]: VALID_SPEC, ...extra }, { git: true });

const repoCases = [
  { name: 'a consistent repository passes', files: {}, expect: [] },
  { name: 'a broken spec is reported', files: { [SPEC_FILE]: VALID_SPEC.replace(/ {6}verified: ran it\n/, '') }, expect: ['error:task-verified'] },
  { name: 'a missing contract is a warning', files: { 'OPERATIONS.md': null }, expect: ['warn:contract-missing'] },
  { name: 'a missing AGENTS.md is an error', files: { 'AGENTS.md': null }, expect: ['error:contract-missing'] },
];

for (const row of repoCases) {
  test(`checkAll: ${row.name}`, () => {
    const root = goodRepo();
    for (const [name, content] of Object.entries(row.files)) {
      if (content === null) rmSync(join(root, name));
      else writeFileSync(join(root, name), content);
    }
    assert.deepEqual(ids(checkAll(root)), row.expect);
  });
}

test('checkAll: a commit range with a Claude trailer is an error', () => {
  const root = goodRepo();
  commit(root, 'chore: first');
  commit(root, 'feat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>');
  assert.deepEqual(ids(checkAll(root, { range: 'HEAD~1..HEAD' })), ['error:no-claude-attribution']);
});

test('checkAll: a clean commit range passes', () => {
  const root = goodRepo();
  commit(root, 'chore: first');
  commit(root, 'feat: x');
  assert.deepEqual(ids(checkAll(root, { range: 'HEAD~1..HEAD' })), []);
});

// ---------------------------------------------------------------------------
// Agent adapters
// ---------------------------------------------------------------------------

const claudePre = (cwd, command) => ({ hook_event_name: 'PreToolUse', tool_name: 'Bash', tool_input: { command }, cwd });
const claudePost = (cwd, file) => ({ hook_event_name: 'PostToolUse', tool_name: 'Write', tool_input: { file_path: file }, cwd });
const BROKEN = VALID_SPEC.replace(/ {6}verified: ran it\n/, '');

const adapterCases = [
  { name: 'claude blocks a bad commit with exit 2', agent: 'claude', event: 'PreToolUse', payload: (r) => claudePre(r, 'git commit --no-verify -m x'), code: 2, stdout: /^$/, stderr: /no-verify/ },
  { name: 'claude allows a clean commit', agent: 'claude', event: 'PreToolUse', payload: (r) => claudePre(r, 'git commit -m "feat: x"'), code: 0, stdout: /^$/, stderr: /^$/ },
  { name: 'claude ignores a non-shell tool on PreToolUse', agent: 'claude', event: 'PreToolUse', payload: (r) => ({ ...claudePost(r, 'a.md'), hook_event_name: 'PreToolUse' }), code: 0, stdout: /^$/, stderr: /^$/ },
  { name: 'claude reports a broken spec after a write', agent: 'claude', event: 'PostToolUse', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => claudePost(r, join(r, SPEC_FILE)), code: 2, stdout: /^$/, stderr: /task-verified/ },
  { name: 'claude ignores a write outside planning', agent: 'claude', event: 'PostToolUse', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => claudePost(r, join(r, 'notes.md')), code: 0, stdout: /^$/, stderr: /^$/ },
  { name: 'claude Stop blocks while a changed spec is broken', agent: 'claude', event: 'Stop', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => ({ hook_event_name: 'Stop', cwd: r, stop_hook_active: false }), code: 2, stdout: /^$/, stderr: /task-verified/ },
  { name: 'claude Stop lets go when it is already continuing', agent: 'claude', event: 'Stop', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => ({ hook_event_name: 'Stop', cwd: r, stop_hook_active: true }), code: 0, stdout: /^$/, stderr: /^$/ },
  { name: 'antigravity denies a force push', agent: 'antigravity', event: 'PreToolUse', payload: (r) => ({ toolCall: { name: 'run_command', args: { CommandLine: 'git push --force origin main' } }, workspacePaths: [r] }), code: 0, stdout: /"decision":"deny"/, stderr: /^$/ },
  { name: 'antigravity allows a clean command', agent: 'antigravity', event: 'PreToolUse', payload: (r) => ({ toolCall: { name: 'run_command', args: { CommandLine: 'npm test' } }, workspacePaths: [r] }), code: 0, stdout: /"decision":"allow"/, stderr: /^$/ },
  { name: 'antigravity Stop asks to continue on a broken spec', agent: 'antigravity', event: 'Stop', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => ({ workspacePaths: [r], terminationReason: 'done' }), code: 0, stdout: /"decision":"continue"/, stderr: /^$/ },
  { name: 'antigravity PostToolUse only informs', agent: 'antigravity', event: 'PostToolUse', repo: { [SPEC_FILE]: BROKEN }, payload: (r) => ({ toolCall: { name: 'write_to_file', args: { TargetFile: join(r, SPEC_FILE) } }, workspacePaths: [r] }), code: 0, stdout: /^$/, stderr: /task-verified/ },
];

for (const row of adapterCases) {
  test(`adapter: ${row.name}`, () => {
    const root = goodRepo(row.repo);
    const payload = row.payload(root);
    const out = render(row.agent, row.event, handleHook(row.agent, payload, { event: row.event, root }));
    assert.equal(out.code, row.code);
    assert.match(out.stdout, row.stdout);
    assert.match(out.stderr, row.stderr);
  });
}

test('main: a payload that is not JSON blocks nothing', () => {
  assert.equal(main(['--agent', 'claude', '--event', 'PreToolUse'], () => 'not json'), 0);
});

test('main: --record saves the raw payload', () => {
  const root = goodRepo();
  const raw = JSON.stringify(claudePre(root, 'ls'));
  main(['--agent', 'claude', '--event', 'PreToolUse', '--record', '--root', root], () => raw);
  assert.equal(readdirSync(join(root, '.agents', 'guard', 'records')).length, 1);
});

test('main: --all exits 1 on an error and 0 when clean', () => {
  const broken = goodRepo({ [SPEC_FILE]: BROKEN });
  const clean = goodRepo();
  assert.deepEqual([main(['--all', '--root', broken]), main(['--all', '--root', clean])], [1, 0]);
});

test('records directory is not created without --record', () => {
  const root = goodRepo();
  main(['--agent', 'claude', '--event', 'PreToolUse', '--root', root], () => JSON.stringify(claudePre(root, 'ls')));
  assert.equal(existsSync(join(root, '.agents', 'guard', 'records')), false);
});
