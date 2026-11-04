import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const lf = (path) => readFileSync(join(ROOT, path), 'utf8').replace(/\r\n/g, '\n');

// This repository installs what it ships, so a project that runs the skill and this repository behave alike.
const INSTALLED = [
  ['skills/spectrace/assets/playbooks/plan.md', '.agents/playbooks/plan.md'],
  ['skills/spectrace/assets/playbooks/change.md', '.agents/playbooks/change.md'],
  ['skills/spectrace/assets/playbooks/review.md', '.agents/playbooks/review.md'],
];

for (const [shipped, installed] of INSTALLED) {
  test(`${installed} is identical to the shipped ${shipped}`, () => {
    assert.equal(lf(installed), lf(shipped));
  });
}

test('this repository ships exactly one skill', () => {
  const listed = spawnSync('git', ['ls-files', '--cached', '--others', '--exclude-standard', 'skills'], { cwd: ROOT, encoding: 'utf8' }).stdout;
  const skills = listed.split('\n').filter((path) => path.endsWith('/SKILL.md'));
  assert.deepEqual(skills, ['skills/spectrace/SKILL.md']);
});
