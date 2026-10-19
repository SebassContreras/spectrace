# 012 — change-records — Tasks

- [x] T001 [agent] [status:done] Add the adapter interface and the file-level adapter in `spectrace/symbols/`
      covers: D2@1, A13@1
      changes: skills/spectrace-start/assets/spectrace/symbols/__init__.py (+28 -0)
- [x] T002 [agent] [status:done] Add the Python adapter: functions, classes, methods, module variables, class attributes and imports; decorators inside the span; duplicate names merged; `sig`
      covers: D2@1, A13@1
      changes: skills/spectrace-start/assets/spectrace/symbols/__init__.py (+3 -0), skills/spectrace-start/assets/spectrace/symbols/python.py (+57 -0)
- [x] T003 [agent] [status:done] Add the Markdown adapter: headings outside fences, `(frontmatter)` and `(preamble)`
      covers: D2@1, A13@1
      changes: skills/spectrace-start/assets/spectrace/symbols/__init__.py (+1 -1), skills/spectrace-start/assets/spectrace/symbols/markdown.py (+38 -0)
- [x] T004 [agent] [status:done] Test the adapters: Python (decorators, nested definitions, class attributes, a property and its setter, a syntax error) and Markdown (fences, front matter)
      covers: R7@1
      kind: test
      changes: tests/test_symbols.py (+116 -0)
- [x] T005 [agent] [status:done] Add the recorder: hunks between two trees, attribution by position, buckets, `renamed_from` and per-file totals
      covers: D1@1, A10@1
      changes: skills/spectrace-start/assets/spectrace/patches.py (+26 -10), skills/spectrace-start/assets/spectrace/records.py (+160 -0)
- [x] T006 [agent] [status:done] Add the caps, the `skipped` and `partial` fields, and the guard that keeps the recorder from ever raising
      covers: D3@1
      changes: skills/spectrace-start/assets/spectrace/records.py (+29 -10)
- [x] T007 [agent] [status:done] Hook the recorder into `done` before `drop("base")`: write `NNN-TNNN.touch.json` and print the accounting line
      covers: D1@1, D3@1, D8@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+7 -1), skills/spectrace-start/assets/spectrace/records.py (+17 -5)
- [x] T008 [agent] [status:done] Test recording through `done`: totals add up, a rename, a removed symbol, a syntax error skipped, a binary file, and a task over the caps
      covers: R1@1, R6@1, R8@1
      kind: test
      changes: skills/spectrace-start/assets/spectrace/patches.py (+6 -4), tests/test_records.py (+134 -0)
- [x] T009 [agent] [status:done] Bump `VERSION` to 2 and document the record, the `path[::symbol]` address and "Format version: 2" in `format.md`
      covers: D10@1
      changes: skills/spectrace-start/assets/format.md (+39 -1), skills/spectrace-start/assets/spectrace/__init__.py (+1 -1)
- [x] T010 [agent] [status:done] Make `FormatDocTest` parse the record's example from `format.md`
      covers: D10@1
      kind: test
      changes: tests/test_trace.py (+8 -0)
- [x] T011 [agent] [status:done] Add `trace why` for live code, deleted code and code outside the trace
      covers: D4@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+2 -0), skills/spectrace-start/assets/spectrace/model.py (+14 -0), skills/spectrace-start/assets/spectrace/views/__init__.py (+17 -0), skills/spectrace-start/assets/spectrace/views/why.py (+40 -0)
- [x] T012 [agent] [status:done] Extend `trace impact` with each task's symbols, their unchanged, changed or gone status, and the in-symbol line counts
      covers: D5@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+2 -52), skills/spectrace-start/assets/spectrace/model.py (+13 -0), skills/spectrace-start/assets/spectrace/records.py (+30 -0), skills/spectrace-start/assets/spectrace/views/impact.py (+80 -0)
- [x] T013 [agent] [status:done] Add the `leftover` check, `trace keep` and `keeps.json`
      covers: D6@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+2 -0), skills/spectrace-start/assets/spectrace/leftover.py (+55 -0), skills/spectrace-start/assets/spectrace/model.py (+9 -1)
- [x] T014 [agent] [status:done] Add the anchored fallback for tasks without a record
      covers: D7@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/records.py (+27 -1), skills/spectrace-start/assets/spectrace/views/impact.py (+7 -1), skills/spectrace-start/assets/spectrace/views/why.py (+15 -1)
- [x] T015 [agent] [status:done] Add the totals check to `check` (`unaccounted`, a warning)
      covers: D8@1
      changes: skills/spectrace-start/assets/spectrace/model.py (+10 -1)
- [x] T016 [agent] [status:done] Name the changed symbols in the outside-any-task messages of `start` and `check`
      covers: D9@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+7 -2), skills/spectrace-start/assets/spectrace/records.py (+6 -0)
- [x] T017 [agent] [status:done] Test `why`, `impact`, `leftover` with `keep`, the anchored fallback, code outside the trace, outside-the-task symbols, and a version 1 repo with patches and no records
      covers: R2@1, R3@1, R4@1, R5@1, R9@1
      kind: test
      changes: tests/test_records.py (+53 -0)
- [x] T018 [agent] [status:done] Update `spectrace-change` Phase 3 to use `why` and `leftover` instead of `git blame`, and add the `trace why` line to `agents-protocol.md`
      covers: D11@1
      changes: skills/spectrace-change/SKILL.md (+10 -4), skills/spectrace-start/assets/agents-protocol.md (+1 -1)
- [x] T019 [agent] [status:done] Run the recorder between every pair of consecutive commits of this repo, confirm the totals add up and that at least 98% of the Python code lines fall inside a named symbol, check `why` on five hand-picked symbols, and time `done` on a typical task
      covers: D8@1
      changes: none
