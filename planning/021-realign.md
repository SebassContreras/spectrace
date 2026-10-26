# 021 — realign

## Goal

Keep only what worked in real projects — `planning/` with specs and a roadmap — and
drop everything that slowed work down: the interview, `trace.py`, the code graph,
architecture rules and scope limits. Tracking moves to git.

## Requirements

- R1: A plan made elsewhere (another agent, the chat) becomes a roadmap and specs with
  no interview.
- R2: Each spec is one English file holding goal, requirements, design, tasks and
  changes; tasks read `NNN/TNNN [agent]` or `[human]`.
- R3: An agent can't finish a task without leaving it traceable, using git only — no
  script.
- R4: New ideas, changes of direction and bugs enter at any time, also after the first
  version, without scope rules in the way.
- R5: Conventions describe the current state; when one blocks the best solution, the
  agent proposes changing it instead of working around it.
- R6: Nothing that no longer works stays in the repo.

## Design

- D1 (R1): `spectrace-plan` reads an existing plan, asks at most one round of
  questions, proposes thin specs (each ends in something runnable) and writes them on
  confirmation. It also adds specs later.
- D2 (R2): Spec file `planning/NNN-name.md` with `Goal`, `Requirements` (R1…),
  `Design` (D1…, naming the R it serves), `Tasks`, `Changes`. Labels without revisions;
  a replaced item is struck through with `→` its replacement.
- D3 (R3): Closing a task is one commit holding the code, the task's `[x]` and the
  trailer `Spec: NNN/TNNN`; the last task also sets the roadmap `Status` to `done`.
- D4 (R3, R5): The format and the protocol live once, in the `AGENTS.md` block that
  `spectrace-plan` writes from `assets/agents-block.md`.
- D5 (R4): `spectrace-change` handles new features (new spec), changes of direction
  (strike, replace, `git log --grep` + `git grep` sweep, cleanup tasks, reopen the spec)
  and bugs (regression test + fix tasks). The roadmap has a free `## Ideas` list.
- D6 (R6): Delete `spectrace-start`, `spectrace-fix`, `trace.py` and its package,
  `.spectrace/`, tests, CI, e2e, `architecture.md` and specs 001–020.

## Tasks

- [x] 021/T001 [agent] Write the new `product.md`, `roadmap.md` and this spec — covers D2
- [x] 021/T002 [agent] Delete everything D6 lists — covers D6
- [x] 021/T003 [agent] Write `skills/spectrace-plan/assets/agents-block.md` — covers D2, D3, D4
- [x] 021/T004 [agent] Rewrite `skills/spectrace-plan/SKILL.md` — covers D1
- [x] 021/T005 [agent] Rewrite `skills/spectrace-change/SKILL.md` — covers D5
- [x] 021/T006 [agent] Rewrite this repo's `AGENTS.md` with the new block — covers D4, R5
- [x] 021/T007 [agent] Rewrite `README.md` — covers R1, R2, R3, R4
- [x] 021/T008 [human] Try the skills in a scratch repo: plan → execute → change — covers R1, R3, R4
      done by agents on a made-up `bkm` CLI: 6 specs, 25 traced commits, 16 tests pass

## Changes

- 2026-10-26: Retired specs 001–020 (interview, `trace.py`, code graph, architecture
  rules, consistency audit). Why: in real use only `planning/` gave value; the rest was
  slow or skipped.
- 2026-10-26: Scratch-repo trial tightened the block and both skills: `covers` takes
  R or D lists, cross-spec refs `006/D1`, conflicts without the user → `blocked`,
  stage by name, a test may share its fix's commit, a cross-spec change of direction
  becomes a new spec (done specs stay done), build → switch → remove order.
