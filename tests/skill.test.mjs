import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { after, test } from 'node:test';
import { fileURLToPath } from 'node:url';

const SKILL = join(dirname(fileURLToPath(import.meta.url)), '..', 'skills', 'spectrace');
const ASSETS = join(SKILL, 'assets');
// Git on Windows may check files out with CRLF (core.autocrlf); the tests read them as LF.
const lf = (text) => text.replace(/\r\n/g, '\n');
const read = (...parts) => lf(readFileSync(join(ASSETS, ...parts), 'utf8'));
const skillText = lf(readFileSync(join(SKILL, 'SKILL.md'), 'utf8'));

const made = [];
after(() => made.forEach((dir) => rmSync(dir, { recursive: true, force: true })));

const ROOT_CONTRACTS = ['AGENTS', 'PRODUCT', 'ARCHITECTURE', 'ENGINEERING', 'TESTING', 'CHANGES', 'OPERATIONS'];
const DESIGN_BY_KIND = { ui: 'design-ui', interface: 'design-interface', content: 'design-content' };

/** Performs the copy table of SKILL.md "Init" step 2 for a repository that uses Claude Code, Antigravity and GitHub. */
function scaffold(kind) {
  const root = mkdtempSync(join(tmpdir(), 'scaffold-'));
  made.push(root);
  for (const name of ROOT_CONTRACTS) cpSync(join(ASSETS, 'contracts', `${name}.md`), join(root, `${name}.md`));
  cpSync(join(ASSETS, 'contracts', `${DESIGN_BY_KIND[kind]}.md`), join(root, 'DESIGN.md'));
  mkdirSync(join(root, 'planning', 'specs'), { recursive: true });
  cpSync(join(ASSETS, 'planning', 'roadmap.md'), join(root, 'planning', 'roadmap.md'));
  cpSync(join(ASSETS, 'playbooks'), join(root, '.agents', 'playbooks'), { recursive: true });
  cpSync(join(ASSETS, 'guard', 'guard.mjs'), join(root, '.agents', 'guard', 'guard.mjs'));
  mkdirSync(join(root, '.claude'), { recursive: true });
  cpSync(join(ASSETS, 'adapters', 'claude-settings.json'), join(root, '.claude', 'settings.json'));
  cpSync(join(ASSETS, 'adapters', 'CLAUDE.md'), join(root, 'CLAUDE.md'));
  cpSync(join(ASSETS, 'adapters', 'antigravity-hooks.json'), join(root, '.agents', 'hooks.json'));
  mkdirSync(join(root, '.github', 'workflows'), { recursive: true });
  cpSync(join(ASSETS, 'adapters', 'guard.yml'), join(root, '.github', 'workflows', 'guard.yml'));
  spawnSync('git', ['init', '-q'], { cwd: root });
  return root;
}

const guard = (root, args, input) => spawnSync('node', [join(root, '.agents', 'guard', 'guard.mjs'), ...args], { cwd: root, input, encoding: 'utf8' });

// ---------------------------------------------------------------------------
// The skill itself
// ---------------------------------------------------------------------------

test('SKILL.md: frontmatter names the skill after its directory', () => {
  assert.match(skillText, /^---\nname: spectrace\ndescription: >-\n/);
});

test('SKILL.md: the description stays under the 1024 characters the spec allows', () => {
  const description = /description: >-\n([\s\S]*?)\n---/.exec(skillText)[1].replace(/\s+/g, ' ');
  assert.ok(description.length < 1024, `${description.length} characters`);
});

test('SKILL.md: stays short enough to read in one go', () => {
  assert.ok(skillText.trimEnd().split('\n').length <= 150);
});

const migrationSteps = [
  { name: 'adds the ownership header to existing contracts', needle: '> Owns: … · Not here: …' },
  { name: 'creates OPERATIONS.md', needle: 'Create `OPERATIONS.md`' },
  { name: 'says what to do with old specs', needle: 'Old specs fail the lint' },
  { name: 'removes what the new design drops', needle: '`.agentignore`' },
  { name: 'removes the old skills and their lock entries', needle: '`skills-lock.json`' },
  { name: 'forbids inventing evidence for old tasks', needle: 'Never invent evidence' },
  { name: 'says where project rules go', needle: 'whose `Owns` line fits it' },
  { name: 'asks to edit in place', needle: 'Edit files in place' },
  { name: 'adapts the contracts to a project that is not software', needle: 'not software' },
];

for (const row of migrationSteps) {
  test(`SKILL.md: the migration path ${row.name}`, () => {
    assert.ok(skillText.includes(row.needle));
  });
}

const assetFiles = readdirSync(ASSETS, { recursive: true, withFileTypes: true })
  .filter((entry) => entry.isFile())
  .map((entry) => ({ dir: entry.parentPath.slice(ASSETS.length + 1).split('\\').join('/'), name: entry.name }));

for (const file of assetFiles) {
  test(`SKILL.md accounts for asset ${file.dir}/${file.name}`, () => {
    assert.ok(skillText.includes(file.name) || skillText.includes(`${file.dir}/*`));
  });
}

// ---------------------------------------------------------------------------
// Scaffold, then the guard
// ---------------------------------------------------------------------------

for (const kind of Object.keys(DESIGN_BY_KIND)) {
  test(`a ${kind} scaffold passes the guard, with unfilled markers only as warnings`, () => {
    const result = guard(scaffold(kind), ['--all']);
    assert.equal(result.status, 0, result.stdout);
    assert.match(result.stdout, /warn \[contract-unfilled\] AGENTS\.md/);
  });
}

test('a scaffold fails the guard after a contract loses its ownership header', () => {
  const root = scaffold('ui');
  const path = join(root, 'PRODUCT.md');
  writeFileSync(path, lf(readFileSync(path, 'utf8')).replace(/^> Owns:.*\n/m, ''));
  const result = guard(root, ['--all']);
  assert.deepEqual([result.status, /error \[contract-header\] PRODUCT\.md/.test(result.stdout)], [1, true]);
});

test('a scaffold fails the guard when a spec has no test task', () => {
  const root = scaffold('ui');
  writeFileSync(join(root, 'planning', 'specs', '001-x.md'), '# 001 — x\n\n## Goal\ng\n\n## Requirements\n- R1: a\n\n## Tasks\n- [ ] 001/T001 [agent] do — covers R1\n');
  writeFileSync(join(root, 'planning', 'roadmap.md'), read('planning', 'roadmap.md') .replace('|------|\n', '|------|\n| 001 | x | todo | — |\n'));
  const result = guard(root, ['--all']);
  assert.deepEqual([result.status, /\[spec-test\]/.test(result.stdout)], [1, true]);
});

// ---------------------------------------------------------------------------
// Adapters, run the way each agent would run them
// ---------------------------------------------------------------------------

const claudeSettings = JSON.parse(read('adapters', 'claude-settings.json'));
const antigravityHooks = JSON.parse(read('adapters', 'antigravity-hooks.json'));

test('claude settings: attribution uses the form older Claude Code versions accept', () => {
  assert.deepEqual(claudeSettings.attribution, { commit: '', pr: '', sessionUrl: false });
});

const deny = claudeSettings.permissions.deny;

for (const rule of ['Read(.env)', 'Read(.env.*)', 'Read(secrets/**)', 'Read(*.pem)', 'Read(*.key)']) {
  test(`claude settings: denies ${rule}`, () => {
    assert.ok(deny.includes(rule));
  });
}

for (const keep of ['Read(!.env.example)', 'Read(!.env.sample)', 'Read(!.env.template)']) {
  test(`claude settings: ${keep} comes after the .env.* rule it carves out of`, () => {
    assert.ok(deny.indexOf(keep) > deny.indexOf('Read(.env.*)') && deny.indexOf('Read(.env.*)') >= 0);
  });
}

test('claude settings: no rule denies the .env.example files outright', () => {
  assert.deepEqual(deny.filter((rule) => /example|sample|template/.test(rule) && !rule.startsWith('Read(!')), []);
});

test('claude settings: hooks cover exactly PreToolUse, PostToolUse and Stop', () => {
  assert.deepEqual(Object.keys(claudeSettings.hooks).sort(), ['PostToolUse', 'PreToolUse', 'Stop']);
});

for (const [event, groups] of Object.entries(claudeSettings.hooks)) {
  test(`claude settings: the ${event} hook is exec form and names its own event`, () => {
    const hook = groups[0].hooks[0];
    assert.deepEqual([hook.type, hook.command, hook.args[0], hook.args.slice(1)], ['command', 'node', '${CLAUDE_PROJECT_DIR}/.agents/guard/guard.mjs', ['--agent', 'claude', '--event', event]]);
  });
}

const DOCUMENTED_ANTIGRAVITY_EVENTS = ['SessionStart', 'PreToolUse', 'PostToolUse', 'PreInvocation', 'PostInvocation', 'Stop'];

for (const [event, groups] of Object.entries(antigravityHooks['spectrace-guard'])) {
  test(`antigravity hooks: ${event} is a documented event with a command handler`, () => {
    const hook = groups[0].hooks[0];
    assert.deepEqual(
      [DOCUMENTED_ANTIGRAVITY_EVENTS.includes(event), hook.type, hook.command, typeof hook.timeout],
      [true, 'command', `node .agents/guard/guard.mjs --agent antigravity --event ${event}`, 'number'],
    );
  });
}

test('CLAUDE.md only imports AGENTS.md', () => {
  assert.equal(read('adapters', 'CLAUDE.md').trim(), '@AGENTS.md');
});

test('the CI workflow runs the guard over files and commits', () => {
  assert.match(read('adapters', 'guard.yml'), /guard\.mjs --all --commits/);
});

// On Windows Claude Code routes shell commands through the PowerShell tool; a matcher of Bash alone never fires there.
test('claude settings: the PreToolUse matcher covers both shell tools', () => {
  assert.deepEqual(claudeSettings.hooks.PreToolUse[0].matcher.split('|'), ['Bash', 'PowerShell']);
});

const hookRuns = [
  { name: 'blocks --no-verify with a real exit code 2', tool: 'Bash', command: 'git commit --no-verify -m x', status: 2 },
  { name: 'lets a clean commit through', tool: 'Bash', command: 'git commit -m "feat: x"', status: 0 },
  { name: 'blocks a Claude co-author trailer', tool: 'Bash', command: 'git commit -m "x" -m "Co-Authored-By: Claude <noreply@anthropic.com>"', status: 2 },
  { name: 'blocks --no-verify through the PowerShell tool', tool: 'PowerShell', command: 'git commit --no-verify -m x', status: 2 },
  { name: 'blocks a co-author trailer in a PowerShell here-string', tool: 'PowerShell', command: "git commit -m @'\nfeat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n'@", status: 2 },
  { name: 'lets a clean PowerShell commit through', tool: 'PowerShell', command: 'git commit -m "feat: x"', status: 0 },
];

for (const row of hookRuns) {
  test(`hook as claude runs it, from the scaffolded settings: ${row.name}`, () => {
    const root = scaffold('ui');
    const installed = JSON.parse(readFileSync(join(root, '.claude', 'settings.json'), 'utf8'));
    const args = installed.hooks.PreToolUse[0].hooks[0].args.map((a) => a.replace('${CLAUDE_PROJECT_DIR}', root));
    const payload = JSON.stringify({ hook_event_name: 'PreToolUse', tool_name: row.tool, tool_input: { command: row.command }, cwd: root });
    const result = spawnSync('node', args, { cwd: root, input: payload, encoding: 'utf8' });
    assert.equal(result.status, row.status, result.stderr);
  });
}

test('the guard prints its usage and exits 0 on --help', () => {
  const result = guard(scaffold('ui'), ['--help']);
  assert.deepEqual([result.status, /Usage:/.test(result.stdout)], [0, true]);
});

test('hook as antigravity runs it: a force push to main is denied in JSON', () => {
  const root = scaffold('ui');
  const payload = JSON.stringify({ toolCall: { name: 'run_command', args: { CommandLine: 'git push --force origin main' } }, workspacePaths: [root] });
  const result = guard(root, ['--agent', 'antigravity', '--event', 'PreToolUse'], payload);
  assert.deepEqual([result.status, JSON.parse(result.stdout).decision], [0, 'deny']);
});
