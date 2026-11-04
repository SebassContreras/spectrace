import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const SKILL = join(dirname(fileURLToPath(import.meta.url)), '..', 'skills', 'spectrace');
const ASSETS = join(SKILL, 'assets');
// Git on Windows may check files out with CRLF (core.autocrlf); the tests read them as LF.
const lf = (text) => text.replace(/\r\n/g, '\n');
const read = (...parts) => lf(readFileSync(join(ASSETS, ...parts), 'utf8'));
const skillText = lf(readFileSync(join(SKILL, 'SKILL.md'), 'utf8'));

test('SKILL.md: frontmatter names the skill after its directory', () => {
  assert.match(skillText, /^---\nname: spectrace\ndescription: >-\n/);
});

test('SKILL.md: the description stays under 1024 characters', () => {
  const description = /description: >-\n([\s\S]*?)\n---/.exec(skillText)[1].replace(/\s+/g, ' ');
  assert.ok(description.length < 1024, `${description.length} characters`);
});

test('SKILL.md: stays short enough to read in one go', () => {
  assert.ok(skillText.trimEnd().split('\n').length <= 150);
});

const skillRows = [
  { name: 'asks for the language of the product apart from the user\'s', needle: 'not the same as the language the user speaks' },
  { name: 'ships no hooks', needle: 'Spectrace ships no hooks' },
  { name: 'presents extras as a question', needle: 'suggest, never install by default' },
  { name: 'adds the ownership header to existing contracts', needle: '> Owns: … · Not here: …' },
  { name: 'creates OPERATIONS.md when migrating', needle: 'Create `OPERATIONS.md`' },
  { name: 'says what to do with old specs', needle: 'Old specs must match the format' },
  { name: 'removes what the new design drops', needle: '`.agentignore`' },
  { name: 'removes the old guard', needle: '`.agents/guard/`' },
  { name: 'forbids inventing evidence for old tasks', needle: 'Never invent evidence' },
  { name: 'says where project rules go', needle: 'whose `Owns` line fits it' },
  { name: 'asks to edit in place', needle: 'Edit files in place' },
  { name: 'adapts the contracts to a project that is not software', needle: 'not software' },
];

for (const row of skillRows) {
  test(`SKILL.md: ${row.name}`, () => {
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

test('assets hold no script, workflow or settings file', () => {
  assert.deepEqual(assetFiles.filter((f) => /\.(mjs|js|yml|json)$/.test(f.name)), []);
});

for (const variant of ['design-ui', 'design-interface', 'design-content']) {
  test(`${variant} asks which language the text is written in`, () => {
    assert.match(read('contracts', `${variant}.md`), /language/i);
  });
}

test('CLAUDE.md only imports AGENTS.md', () => {
  assert.equal(read('CLAUDE.md').trim(), '@AGENTS.md');
});
