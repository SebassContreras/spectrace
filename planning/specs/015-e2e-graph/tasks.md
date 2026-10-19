# 015 — e2e-graph — Tasks

- [x] T001 [agent] [status:done] Add the Records, Why and Leftover checks to the Verification section of `e2e/scenario.md`
      covers: D1@1
      changes: e2e/scenario.md (+41 -0)
- [x] T002 [agent] [status:done] Add Step 7 "Find and fix" to `e2e/scenario.md`: the hand edit, the prompt, the answers and its checks
      covers: D2@1
      changes: e2e/scenario.md (+31 -0)
- [ ] T003 [agent] [status:blocked] Claude Code: run steps 0–7 of the extended scenario and record R1–R4 in `e2e/report.md`
      covers: R1@1, R2@1, R3@1, R4@1, D1@1, D2@1
      kind: test
      └─ blocked: needs real harness runs: step 0 installs the skills from the published repo, which lacks 011-016 until the maintainer pushes; then 20+ fresh claude/agy conversations
- [ ] T004 [agent] [status:blocked] agy: the same run, recorded in `e2e/report.md`
      covers: R1@1, R2@1, R3@1, R4@1, D1@1, D2@1
      kind: test
      └─ blocked: needs real harness runs: step 0 installs the skills from the published repo, which lacks 011-016 until the maintainer pushes; then 20+ fresh claude/agy conversations
- [ ] T005 [agent] [status:blocked] Add the "Code map" summary table to `e2e/report.md`: the result of each check per harness, plus the gaps
      covers: R5@1, D3@1
      kind: test
      └─ blocked: waits for the results of 015/T003 and 015/T004
