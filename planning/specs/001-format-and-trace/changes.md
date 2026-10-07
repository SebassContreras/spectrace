# 001 — format-and-trace — Changes

## 2026-10-06 — history for project-wide decisions
Why: revising A5 showed the format had no place to record why an A item changed; `changes.md` exists only per spec.
- MODIFIED D1@1 → D1@2 (adds `planning/changes.md` for A items)
- Tasks: T001, T002 re-pointed to D1@2 (still valid); T004 added for the missing part

## 2026-10-06 — follow renames; report mentions of deleted files
Why: renaming the skill folders (005/T009) was recorded as delete + add, so `impact` reported moved files as deleted; and removing the plugin left mentions of deleted files (spec context, a CI comment) that no task covered, so nothing reported them.
- MODIFIED R3@1 → R3@2, D2@1 → D2@2, D3@1 → D3@2
- ADDED R6@1, D6@1
- Tasks: T002, T003 re-pointed (still valid as the base); T006, T007, T008 added. Refactor in place: rename handling extends `done`/`impact` in `trace.py`; rewriting the script to add it would change nothing else.

## 2026-10-06 — item fingerprints and restore
Why: two gaps left after the trace review — an item's text could change without a revision bump and nothing noticed; and a retired approach could be removed but not brought back.
- ADDED R7@1, R8@1, D7@1, D8@1
- Tasks: T010–T013 added
- Tasks (later the same day): T014 brought `trace.py` back within A5@3 (one command table, unused `--json` on `check`/`impact` dropped); T013's tests found that `review` never saved, fixed inside T013.

## 2026-10-07 — cleanup tasks hold the strict gate
Why: in the end-to-end run (006) `check --strict` passed while a task that `retires:` a finished one was still to do, because the retired task covered an item that hadn't changed; nothing else made it pending.
- ADDED D9@1
- Tasks: 006/T017 implements it in `trace.py`; 006/T018 adds it to `format.md`; 006/T019 tests it
