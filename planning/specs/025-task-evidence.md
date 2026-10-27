# 025 — task-evidence

## Goal
A task closes in its own commit when its only output is project docs in `AGENTS.md`
or a check that changes no files, and an `--amend` that ticks a task is judged on the
whole commit. Check: in a scratch repo the hook accepts a conventions-only `AGENTS.md`
change, refuses a block-only one, accepts a `Verify:` task only with its `verified:`
note, and accepts an amend of a task's commit.

## Requirements
- R1: `AGENTS.md` lines outside the spectrace block count as a task's work; the block,
  `.githooks/` and `.gitattributes` don't. The missing-trailer warning still ignores
  all of `AGENTS.md`.
- R2: A `Verify:` task needs no work and closes only with an indented `verified:` note.
- R3: Amending a commit that already names one of the message's tasks compares the
  index with the commit's parent.

## Design
- D1 (R1): `commit-msg` adds one to the work count when `AGENTS.md` differs from the
  base once the `<!-- spectrace -->` block is stripped from both.
- D2 (R2): `commit-msg` exempts `Verify:` like `Review:`; `pre-commit` requires
  `verified:` under a ticked `Verify:`.
- ~~D3 (R3): When HEAD's trailers share a `Spec:` with the message, the base is `HEAD^`
  (the empty tree for a root commit). Other amends can't be told apart; the block says
  to use `git reset --soft HEAD~1` to fold a task into an earlier commit.~~ → 026/D1

## Tasks
- [x] 025/T001 [agent] `commit-msg` counts `AGENTS.md` outside the block and diffs an amend against its parent (assets and this repo) — covers D1, D3
- [x] 025/T002 [agent] `Verify:` tasks: exempt in `commit-msg`, `verified:` required in `pre-commit` — covers D2
- [x] 025/T003 [agent] Block, `AGENTS.md` copy and README describe what counts as work, `Verify:`, and `reset --soft` — covers R1, R2, D3
