# 026 — hook-tests

## Goal
The hooks have behavior tests that fail when a rule breaks, and an amend is told
apart from a new commit without guessing from trailers. Check: `sh tests/hooks.sh`
passes on the current hooks and fails on the 025 and pre-025 versions for the cases
each one got wrong.

## Requirements
- R1: One test per hook rule, each in its own throwaway repo, named after the
  behavior it expects; the suite also checks `.githooks/` against the assets.
- R2: A new commit that names an already closed task is judged on its own changes,
  never on those of the commit before it.
- R3: `AGENTS.md` lines after an unclosed spectrace block still count as work.
- R4: The install path list lives once in `commit-msg`.

## Design
- D1 (R2, 025/R3): `commit-msg` treats the commit as an amend when `GIT_AUTHOR_DATE`
  (exported by git to hooks) equals the author date of HEAD; an amend keeps it, a new
  commit gets the current time. Checked on git 2.56: `prepare-commit-msg` gets
  `message` for `--amend -m`, the same as a plain commit, so it can't tell them apart.
  Trade-off: a new commit in the same second as HEAD, or `-C HEAD`, is judged against
  HEAD's parent; the tests space their commits a minute apart.
- D2 (R3): `outside_block` holds the block's lines and puts them back if no
  `<!-- /spectrace -->` follows.
- D3 (R4): `install_re` names the paths once, used by the warning and the work count.
- D4 (R1): `tests/hooks.sh`, POSIX sh, no dependencies; `HOOKS=<dir>` runs it on
  another copy of the hooks. `product.md` → `## Stack` names it; the doc map, the
  conventions, `spectrace-plan` (`Verify:` tasks) and README `## Limits` follow.

## Tasks
- [x] 026/T001 [agent] `commit-msg`: amend by author date, unclosed block kept, `install_re` (assets and this repo) — covers D1, D2, D3; replaces 025/D3
- [x] 026/T002 [agent] `tests/hooks.sh` and `product.md` → `## Stack`; block says `--amend` is judged as a whole — covers D4, R1
- [x] 026/T003 [agent] Verify: suite passes on the new hooks; fails on the 025 and pre-025 hooks for what each got wrong — covers R1, R2, R3
      verified: `sh tests/hooks.sh` (14 ok); `HOOKS=<025 hooks>` fails unclosed-block, amend-without-trailer and reused-task; `HOOKS=<pre-025 hooks>` fails conventions-change, verify-with-note, unclosed-block and amend — found nothing else
- [x] 026/T004 [agent] Docs: doc map and hook convention in `AGENTS.md`, `Verify:` in `spectrace-plan`, amend limit in README — covers D4

## Changes
- 2026-10-27: 025/D3 → D1. Why: the trailer heuristic let a new commit for an already
  closed task count the previous commit's work, and missed amends of a commit with no
  matching trailer. Work: T001.
