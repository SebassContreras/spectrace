# 006 — e2e-verification — Tasks

- [x] T001 [agent] [status:done] Write `e2e/scenario.md`: the to-do project, the interview answers, the two specs, the item retired and reinstated, the two edits, and the exact prompt for each step
      covers: D2@1, D3@1, D4@1
      changes: e2e/scenario.md (+196 -0)
- [x] T002 [agent] [status:done] Add the verification procedure to `e2e/scenario.md`: `write-tree` snapshots, `impact`, `check --strict`, `git grep`, post-restore tree compare, edit checks
      covers: D5@1, D6@1, D7@1, D8@1
      changes: e2e/scenario.md (+79 -0)
- [x] T003 [agent] [status:done] Claude Code, R1: set up the throwaway repo, install the skills, run `spectrace-start` and `spectrace-plan`, execute three tasks, verify exactness; record the result in `e2e/report.md`
      covers: R1@1, D1@1, D3@1, D4@1, D5@1, D10@1
      kind: test
      changes: e2e/report.md (+61 -0), e2e/scenario.md (+1 -1)
- [x] T004 [agent] [status:done] Claude Code, R2: retire the design item, check the manifest, `check --strict` before and after cleanup, `git grep`; record the result in `e2e/report.md`
      covers: R2@1, D6@1
      kind: test
      changes: e2e/report.md (+32 -0)
- [ ] T005 [agent] [status:todo] Claude Code, R4: reinstate the decision with `trace restore`, verify the tree and `changes:`; record the result in `e2e/report.md`
      covers: R4@1, D7@1
      kind: test
- [ ] T006 [agent] [status:todo] Claude Code, R5: wording edit vs. meaning edit; record the result in `e2e/report.md`
      covers: R5@1, D8@1
      kind: test
- [ ] T007 [agent] [status:todo] agy, R1: as T003, first verifying the open questions (project `AGENTS.md`, conversation ID, `skills` CLI agent name)
      covers: R1@1, D1@1, D3@1, D4@1, D5@1, D10@1
      kind: test
- [ ] T008 [agent] [status:todo] agy, R2: as T004
      covers: R2@1, D6@1
      kind: test
- [ ] T009 [agent] [status:todo] agy, R4: as T005
      covers: R4@1, D7@1
      kind: test
- [ ] T010 [agent] [status:todo] agy, R5: as T006
      covers: R5@1, D8@1
      kind: test
- [ ] T011 [agent] [status:todo] Summary table in `e2e/report.md`: pass/fail per R item and harness, plus gaps
      covers: R3@1, D9@1
      kind: test
- [x] T012 [agent] [status:done] `trace.py`: record a task's patch from `git diff`'s raw output (no `strip()`), with `--binary`
      covers: 001/D2@2, 001/D8@1, D9@1
      changes: skills/spectrace-start/assets/trace.py (+4 -4)
- [x] T013 [agent] [status:done] `tests/test_trace.py`: a change whose last hunk ends in blank context lines, and a binary change, are recorded exactly and `restore` reverses both
      covers: 001/R8@1
      kind: test
      changes: tests/test_trace.py (+23 -0)
- [x] T014 [agent] [status:done] `e2e/scenario.md`: every `git grep` uses `--untracked` and excludes `*.pyc`
      covers: D6@1
      changes: e2e/scenario.md (+5 -2)
- [x] T015 [agent] [status:done] Push `main` to origin, so the rerun installs the fix from the published repo
      covers: D1@1
      changes: none
- [x] T016 [agent] [status:done] Claude Code: rerun steps 0–4 on a fresh throwaway repo with the fix; update R1 and R2 in `e2e/report.md` (T005 and T006 continue on that run)
      covers: R1@1, R2@1, D5@1, D6@1
      kind: test
      changes: e2e/report.md (+49 -2), e2e/scenario.md (+1 -1)
- [x] T017 [agent] [status:done] `trace.py`: a not-done task that `retires:` a finished task is pending
      covers: 001/D9@1
      changes: skills/spectrace-start/assets/trace.py (+4 -4)
- [x] T018 [agent] [status:done] `format.md`: add the cleanup-pending state to "Trace states"
      covers: 001/D9@1
      changes: skills/spectrace-start/assets/format.md (+2 -0)
- [x] T019 [agent] [status:done] `tests/test_trace.py`: `check --strict` fails until a retiring task is done, even when the task it retires isn't suspect
      covers: 001/R3@2
      kind: test
      changes: tests/test_trace.py (+12 -0)
- [ ] T020 [agent] [status:in_progress] Push `main` to origin with the strict-gate change
      covers: D1@1
- [ ] T021 [agent] [status:todo] Claude Code run 2: reset the throwaway repo to its pre-change snapshot, update its `.spectrace/trace.py`, rerun step 4; update R2 in `e2e/report.md`
      covers: R2@1, D6@1
      kind: test
- [x] T022 [agent] [status:done] `spectrace-change` Phase 5: accept "cleanup pending" for the cleanup tasks it just wrote
      covers: 001/D9@1
      changes: skills/spectrace-change/SKILL.md (+3 -2)
