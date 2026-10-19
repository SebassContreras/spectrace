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

## 2026-10-19 — the code map joins the trace
Why: the MVP is approved and works; the next goal is a code map — which symbols each task changed, which decision stands behind a piece of code, what depends on it. It needs more than one file in the trace, a fourth skill, and decisions about how facts about code are recorded and trusted. Plan: `planning/graph-plan.md`; specs 011–015.
- MODIFIED A1@2 → A1@3 (adds `spectrace-fix`, which arrives with spec 014)
- MODIFIED A2@1 → A2@2 (`trace.py` plus its `spectrace/` package, one unit)
- MODIFIED A5@3 → A5@4 (a budget per module of `spectrace/` instead of 900 lines for `trace.py`)
- ADDED A10@1, A11@1, A12@1, A13@1
- Tasks: 001/T009 is retired by 011/T006 (redo: the single-file cap test is replaced by a per-module budget test); 001/T014 and 002/T006 re-pointed to A5@4 and 005/T009 to A1@3 (still valid, noted as reviewed). No task covered A2@1, so `trace impact A2` finds nothing: the statements about "one script" are in the install text of `spectrace-start`, `references/upgrade.md`, `format.md` and the README, and are edited in place by 011/T008–T009 and 014/T010. Refactor in place, because that text keeps its structure and gains the package folder, so deleting and rewriting it would restate the same passages.

## 2026-10-19 — decisions change by conflict, not by workaround
Why: the code map will keep running into earlier decisions; building around them would leave over-engineering the next change has to undo. Decisions stay binding, but when one gets in the way the user decides — keep, edit or retire — instead of the code bending. Spec 016.
- ADDED A14@1, A15@1
- Tasks: 016/T001–T009 cover them. No task covered an earlier item they replace, so nothing is retired.
