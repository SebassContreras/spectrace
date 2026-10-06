# Changes to project-wide decisions

## 2026-10-06 — trace.py size budget
Why: 650 lines was an estimate made before `trace.py` existed; the finished script (spec 001) is 748 lines with no dead code.
- MODIFIED A5@1 → A5@2 (`trace.py` at most 800 lines; the SKILL.md budget is unchanged)

## 2026-10-06 — prefixed skill names
Why: without a plugin there is no `spectrace:` namespace; installed as bare folders, `start`/`plan`/`change` would collide with other skills of the same name. See 005's change of the same date.
- MODIFIED A1@1 → A1@2 (`spectrace-start`, `spectrace-plan`, `spectrace-change`)
- Tasks: 005/T009. No task covered A1@1, so `trace impact A1` finds nothing: the rename's reach is found by searching for the old names.

## 2026-10-06 — trace.py budget, second revision
Why: following renames and reporting mentions of deleted files (001 R3@2, R6@1) added 79 lines (748 → 827). Squeezing it under 800 would mean compacting readable code or dropping blank lines — gaming the number, not reducing complexity. Nothing enforced the budget either.
- MODIFIED A5@2 → A5@3 (`trace.py` at most 900; now enforced by a test)
- Tasks: 001/T009 rewritten before any work — it had been opened and aborted with no changes; 002/T006 re-pointed to A5@3 (still valid; found by `trace check`, missed when the budget was revised).
