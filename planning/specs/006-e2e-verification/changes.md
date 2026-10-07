# 006 — e2e-verification — Changes

## 2026-10-06 — cover restore and fingerprints
Why: 001 gained `trace restore` and item fingerprints; the end-to-end run must exercise both.
- ADDED R4@1, R5@1

## 2026-10-07 — fix trace.py patch recording found by the Claude Code run
Why: the run's T011 patch lost its trailing blank context lines (`git()` strips stdout) and binary changes were recorded without data, so `trace restore` — R4 — cannot reverse them. Defects against 001/R8, fixed here per D9; no item's meaning changes.
- Tasks: T012 fixes patch recording; T013 tests it; T014 fixes the scenario's `git grep`; T015 publishes the fix; T016 reruns steps 0–4 under Claude Code

## 2026-10-07 — strict gate for cleanup tasks
Why: run 2 failed R2's strict criterion: `check --strict` passed while 001/T012 (`retires: T003`) was still to do. Recorded as 001/D9@1.
- Tasks: T017–T019 implement and test 001/D9@1; T022 teaches `spectrace-change` the new state; T020 publishes it; T021 reruns step 4 on run 2
