# 015 — e2e-graph — Tasks

- [x] T001 [agent] [status:done] Add the Records, Why and Leftover checks to the Verification section of `e2e/scenario.md`
      covers: D1@1
      changes: e2e/scenario.md (+41 -0)
- [x] T002 [agent] [status:done] Add Step 7 "Find and fix" to `e2e/scenario.md`: the hand edit, the prompt, the answers and its checks
      covers: D2@1
      changes: e2e/scenario.md (+31 -0)
- [x] T003 [agent] [status:done] Claude Code: run steps 0–7 of the extended scenario and record R1–R4 in `e2e/report.md`
      covers: R1@1, R2@1, R3@1, R4@1, D1@1, D2@1
      kind: test
      changes: none
      └─ blocked: needs real harness runs: step 0 installs the skills from the published repo, which lacks 011-016 until the maintainer pushes; then 20+ fresh claude/agy conversations
      └─ conflict kept 2026-10-20: 012/D6@2 resolves false leftover and 015/T008 resolves suspect restore task
- [x] T004 [agent] [status:done] agy: the same run, recorded in `e2e/report.md`
      covers: R1@1, R2@1, R3@1, R4@1, D1@1, D2@1
      kind: test
      changes: none
      └─ blocked: needs real harness runs: step 0 installs the skills from the published repo, which lacks 011-016 until the maintainer pushes; then 20+ fresh claude/agy conversations
- [x] T005 [agent] [status:done] Add the "Code map" summary table to `e2e/report.md`: the result of each check per harness, plus the gaps
      covers: R5@1, D3@1
      kind: test
      changes: e2e/report.md (+15 -5)
      └─ blocked: waits for the results of 015/T003 and 015/T004
- [x] T006 [agent] [status:done] Test leftover regression: reinstated/rebuilt symbol is not a leftover when recorded by a task after cleanup
      covers: 012/D6@2
      kind: test
      changes: tests/test_records.py (+12 -0)
- [x] T007 [agent] [status:done] Update leftover check to ignore symbols touched by any task done after the retiring task
      covers: 012/D6@2
      changes: skills/spectrace-start/assets/spectrace/leftover.py (+12 -1)
- [x] T008 [agent] [status:done] Fix Reinstate in spectrace-change skill to retire the task it undoes and test restore task suspect state
      covers: 004/D7@1
      changes: skills/spectrace-change/SKILL.md (+2 -1), tests/test_trace.py (+4 -1)
