# 001 — format-and-trace — Tasks

- [x] T001 [agent] [status:done] Write `skills/start/assets/format.md`
      covers: D1@2
      changes: skills/start/assets/format.md (+145 -0)
      └─ reviewed 2026-10-06: still valid under D1@2; T004 adds the missing part
- [x] T002 [agent] [status:done] Write `skills/start/assets/trace.py` (status, start, done, abort, block, check, impact)
      covers: D1@2, D2@2, D3@2, D4@1, D5@1
      changes: skills/start/assets/trace.py (+748 -0)
      └─ reviewed 2026-10-06: still valid under D1@2 (history files are not parsed)
      └─ reviewed 2026-10-06: still the base for D2@2/D3@2; T006 adds rename handling in place
- [x] T003 [agent] [status:done] Write `tests/test_trace.py`, including a check that `format.md`'s examples parse
      covers: R1@1, R2@1, R3@2, R4@1, R5@1
      kind: test
      changes: tests/test_trace.py (+288 -0)
      └─ reviewed 2026-10-06: still valid; T008 adds the rename and deleted-file cases
- [x] T004 [agent] [status:done] Add `planning/changes.md` (history of A items) to `format.md`'s file list and History section
      covers: D1@2
      changes: skills/start/assets/format.md (+4 -1)
- [x] T005 [agent] [status:done] `format.md` "Who writes what": the `change` skill may re-point `covers:`, add review notes and delete not-started tasks
      covers: D1@2
      changes: skills/start/assets/format.md (+3 -1)
- [x] T006 [agent] [status:done] `trace done` records renames; `trace impact` follows a file through recorded or inferred renames
      covers: D2@2, D3@2
      changes: skills/spectrace-start/assets/trace.py (+81 -29)
- [x] T007 [agent] [status:done] `trace check` reports mentions of files deleted by a task, pending on that task's spec
      covers: D6@1
      changes: skills/spectrace-start/assets/trace.py (+27 -0)
- [x] T008 [agent] [status:done] Tests: impact across a rename (recorded and inferred); mention of a deleted file blocks the spec until removed
      covers: R3@2, R6@1
      kind: test
      changes: tests/test_trace.py (+45 -0)
- [x] T009 [agent] [status:done] Test that enforces A5's size budgets for `trace.py` and every `SKILL.md`
      covers: A5@3
      kind: test
      changes: tests/test_skills.py (+12 -5)
- [x] T010 [agent] [status:done] Item fingerprints: record in `status --write`, report in `check`, accept with `trace review`
      covers: D7@1
      changes: skills/spectrace-start/assets/trace.py (+77 -11)
- [x] T011 [agent] [status:done] `trace restore NNN/TNNN`: reverse-apply a task's patch inside an open task
      covers: D8@1
      changes: skills/spectrace-start/assets/trace.py (+24 -1)
- [x] T012 [agent] [status:done] `format.md`: the fingerprints file and the `review` and `restore` commands
      covers: D7@1, D8@1
      changes: skills/spectrace-start/assets/format.md (+18 -3)
- [x] T013 [agent] [status:done] Tests: wording vs meaning edits of a built-on item; restoring a retired task's work
      covers: R7@1, R8@1
      kind: test
      changes: skills/spectrace-start/assets/trace.py (+2 -1), tests/test_trace.py (+44 -0)
- [x] T014 [agent] [status:done] Bring `trace.py` back within A5: one command table for dispatch and parsing, drop the unused `--json` from `check` and `impact`, simplify `file_presence`
      covers: A5@3
      changes: skills/spectrace-start/assets/trace.py (+28 -46)
- [x] T015 [agent] [status:done] Keep recorded patches byte-exact across clones (`.spectrace/.gitattributes`: `changes/*.patch -text`) so `restore` works on any OS
      covers: D8@1
      changes: skills/spectrace-start/assets/trace.py (+5 -4), tests/test_trace.py (+2 -0)
