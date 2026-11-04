import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { LIMITS, checkContract, errorsOf, lintSpec } from '../skills/spectrace/assets/guard/guard.mjs';

const ASSETS = join(dirname(fileURLToPath(import.meta.url)), '..', 'skills', 'spectrace', 'assets');
// Git on Windows may check files out with CRLF (core.autocrlf); the tests read them as LF.
const read = (...parts) => readFileSync(join(ASSETS, ...parts), 'utf8').replace(/\r\n/g, '\n');

const CONTRACT_FILES = ['AGENTS', 'PRODUCT', 'ARCHITECTURE', 'ENGINEERING', 'TESTING', 'CHANGES', 'OPERATIONS', 'design-ui', 'design-content', 'design-interface'];
const PLAYBOOKS = ['plan', 'change', 'review'];
const contractName = (file) => (file.startsWith('design-') ? 'DESIGN.md' : `${file}.md`);
const ownsOf = (text) => /^>\s*Owns:(.*?)·/m.exec(text)?.[1].trim();
const headingsOf = (text) => text.split('\n').filter((l) => l.startsWith('## ')).map((l) => l.slice(3).trim());

for (const file of CONTRACT_FILES) {
  test(`template ${file}: passes the guard's contract check with no errors`, () => {
    assert.deepEqual(errorsOf(checkContract(contractName(file), read('contracts', `${file}.md`))), []);
  });
}

for (const file of CONTRACT_FILES) {
  test(`template ${file}: says what it must not contain`, () => {
    assert.match(read('contracts', `${file}.md`), /^>\s*Owns:.*·\s*Not here:/m);
  });
}

test('every template owns a different responsibility, apart from the three DESIGN variants', () => {
  const owners = CONTRACT_FILES.filter((f) => !f.startsWith('design-')).map((f) => ownsOf(read('contracts', f + '.md')));
  assert.equal(new Set(owners).size, owners.length);
});

const ownerOfSection = [
  { section: 'Verify', owner: 'TESTING' },
  { section: 'Run', owner: 'OPERATIONS' },
  { section: 'Setup', owner: 'OPERATIONS' },
  { section: 'Build and release', owner: 'OPERATIONS' },
  { section: 'Layers', owner: 'ARCHITECTURE' },
  { section: 'Principles', owner: 'ENGINEERING' },
];

for (const row of ownerOfSection) {
  test(`the "${row.section}" section exists only in ${row.owner}`, () => {
    const holders = CONTRACT_FILES.filter((f) => headingsOf(read('contracts', `${f}.md`)).includes(row.section));
    assert.deepEqual(holders, [row.owner]);
  });
}

// One fact, one owner: each statement below appears in a single contract (the three DESIGN variants count as one).
const oneOwner = [
  { fact: 'never weaken, skip or delete a test', pattern: /skip or delete a test/i, owner: 'TESTING' },
  { fact: 'file and identifier casing', pattern: /kebab-case/i, owner: 'ENGINEERING' },
  { fact: 'docs travel with behavior', pattern: /docs travel with behavior/i, owner: 'ENGINEERING' },
  { fact: 'commit format', pattern: /conventional commits/i, owner: 'AGENTS' },
  { fact: 'no Claude attribution', pattern: /co-author/i, owner: 'AGENTS' },
  { fact: 'the language of code and commits', pattern: /docs and commits in/i, owner: 'AGENTS' },
  { fact: 'the guard script', pattern: /guard\.mjs/i, owner: 'AGENTS' },
  { fact: 'the verification evidence line', pattern: /`verified:`/, owner: 'AGENTS' },
  { fact: 'what a layer may import', pattern: /never imports/i, owner: 'ARCHITECTURE' },
  { fact: 'accessibility', pattern: /WCAG/, owner: 'DESIGN' },
];

const holdersOf = (pattern) => [
  ...new Set(CONTRACT_FILES.filter((f) => pattern.test(read('contracts', `${f}.md`))).map((f) => contractName(f).replace('.md', ''))),
];

for (const row of oneOwner) {
  test(`${row.fact} is stated in ${row.owner} only`, () => {
    assert.deepEqual(holdersOf(row.pattern), [row.owner]);
  });
}

test('PRODUCT has no non-goals section', () => {
  assert.doesNotMatch(read('contracts', 'PRODUCT.md'), /non-?goals?|out of scope/i);
});

test('AGENTS.md stays inside the length the guard enforces', () => {
  const lines = read('contracts', 'AGENTS.md').trimEnd().split('\n').length;
  assert.ok(lines <= LIMITS.agentsWarn, `${lines} lines`);
});

const routerTargets = [...read('contracts', 'AGENTS.md').matchAll(/^\|[^|]+\|\s*([^|\s]+\.md)\s*\|$/gm)].map((m) => m[1]);

test('the router names every contract and playbook', () => {
  assert.deepEqual(
    routerTargets.sort(),
    ['.agents/playbooks/change.md', '.agents/playbooks/plan.md', '.agents/playbooks/review.md', 'ARCHITECTURE.md', 'CHANGES.md', 'DESIGN.md', 'ENGINEERING.md', 'OPERATIONS.md', 'PRODUCT.md', 'TESTING.md'],
  );
});

// Where the template for a router target lives under assets/.
const templatePathFor = (target) => {
  const inPlaybooks = /^\.agents\/playbooks\/(.+)$/.exec(target);
  if (inPlaybooks) return ['playbooks', inPlaybooks[1]];
  return ['contracts', target === 'DESIGN.md' ? 'design-ui.md' : target];
};

for (const target of routerTargets) {
  test(`router target ${target} has a template`, () => {
    assert.ok(read(...templatePathFor(target)).length > 0);
  });
}

for (const name of PLAYBOOKS) {
  test(`playbook ${name}: states what it owns and does not`, () => {
    assert.match(read('playbooks', `${name}.md`), /^>\s*Owns:.*·\s*Not here:/m);
  });
}

for (const name of PLAYBOOKS) {
  test(`playbook ${name}: only points at files that exist`, () => {
    const refs = [...read('playbooks', `${name}.md`).matchAll(/\b([A-Z]+\.md|(?:plan|change|review)\.md)\b/g)].map((m) => m[1]);
    const known = [...CONTRACT_FILES.map(contractName), ...PLAYBOOKS.map((p) => `${p}.md`), 'README.md'];
    assert.deepEqual(refs.filter((r) => !known.includes(r)), []);
  });
}

test('the spec example in plan.md passes the guard', () => {
  const example = /```markdown\n([\s\S]*?)```/.exec(read('playbooks', 'plan.md'))[1];
  assert.deepEqual(lintSpec(example, 'planning/specs/003-login.md'), []);
});

test('the roadmap template has the columns the guard reads', () => {
  assert.match(read('planning', 'roadmap.md'), /\| ID\s+\| Spec\s+\| Status\s+\| Depends on\s+\|/);
});
