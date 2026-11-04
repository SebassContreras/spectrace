import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

test('this repository passes its own guard', () => {
  const guard = join(ROOT, 'skills', 'spectrace', 'assets', 'guard', 'guard.mjs');
  const result = spawnSync('node', [guard, '--all'], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stdout);
});

test('this repository uses the shipped Claude settings, only with the guard path of its own checkout', () => {
  const shipped = readFileSync(join(ROOT, 'skills', 'spectrace', 'assets', 'adapters', 'claude-settings.json'), 'utf8');
  const own = readFileSync(join(ROOT, '.claude', 'settings.json'), 'utf8');
  assert.deepEqual(JSON.parse(own), JSON.parse(shipped.replaceAll('/.agents/guard/guard.mjs', '/skills/spectrace/assets/guard/guard.mjs')));
});

test('this repository ships exactly one skill', () => {
  const listed = spawnSync('git', ['ls-files', '--cached', '--others', '--exclude-standard', 'skills'], { cwd: ROOT, encoding: 'utf8' }).stdout;
  const skills = listed.split('\n').filter((path) => path.endsWith('/SKILL.md'));
  assert.deepEqual(skills, ['skills/spectrace/SKILL.md']);
});
