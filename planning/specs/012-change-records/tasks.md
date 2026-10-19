# 012 — change-records — Tasks

- [ ] T001 [agent] [status:todo] Add the adapter interface and the file-level adapter in `spectrace/symbols/`
      covers: D2@1, A13@1
- [ ] T002 [agent] [status:todo] Add the Python adapter: functions, classes, methods, module variables, class attributes and imports; decorators inside the span; duplicate names merged; `sig`
      covers: D2@1, A13@1
- [ ] T003 [agent] [status:todo] Add the Markdown adapter: headings outside fences, `(frontmatter)` and `(preamble)`
      covers: D2@1, A13@1
- [ ] T004 [agent] [status:todo] Test the adapters: Python (decorators, nested definitions, class attributes, a property and its setter, a syntax error) and Markdown (fences, front matter)
      covers: R7@1
      kind: test
- [ ] T005 [agent] [status:todo] Add the recorder: hunks between two trees, attribution by position, buckets, `renamed_from` and per-file totals
      covers: D1@1, A10@1
- [ ] T006 [agent] [status:todo] Add the caps, the `skipped` and `partial` fields, and the guard that keeps the recorder from ever raising
      covers: D3@1
- [ ] T007 [agent] [status:todo] Hook the recorder into `done` before `drop("base")`: write `NNN-TNNN.touch.json` and print the accounting line
      covers: D1@1, D3@1, D8@1
- [ ] T008 [agent] [status:todo] Test recording through `done`: totals add up, a rename, a removed symbol, a syntax error skipped, a binary file, and a task over the caps
      covers: R1@1, R6@1, R8@1
      kind: test
- [ ] T009 [agent] [status:todo] Bump `VERSION` to 2 and document the record, the `path[::symbol]` address and "Format version: 2" in `format.md`
      covers: D10@1
- [ ] T010 [agent] [status:todo] Make `FormatDocTest` parse the record's example from `format.md`
      covers: D10@1
      kind: test
- [ ] T011 [agent] [status:todo] Add `trace why` for live code, deleted code and code outside the trace
      covers: D4@1
- [ ] T012 [agent] [status:todo] Extend `trace impact` with each task's symbols, their unchanged, changed or gone status, and the in-symbol line counts
      covers: D5@1
- [ ] T013 [agent] [status:todo] Add the `leftover` check, `trace keep` and `keeps.json`
      covers: D6@1, A11@1
- [ ] T014 [agent] [status:todo] Add the anchored fallback for tasks without a record
      covers: D7@1, A11@1
- [ ] T015 [agent] [status:todo] Add the totals check to `check` (`unaccounted`, a warning)
      covers: D8@1
- [ ] T016 [agent] [status:todo] Name the changed symbols in the outside-any-task messages of `start` and `check`
      covers: D9@1
- [ ] T017 [agent] [status:todo] Test `why`, `impact`, `leftover` with `keep`, the anchored fallback, code outside the trace, outside-the-task symbols, and a version 1 repo with patches and no records
      covers: R2@1, R3@1, R4@1, R5@1, R9@1
      kind: test
- [ ] T018 [agent] [status:todo] Update `spectrace-change` Phase 3 to use `why` and `leftover` instead of `git blame`, and add the `trace why` line to `agents-protocol.md`
      covers: D11@1
- [ ] T019 [agent] [status:todo] Run the recorder between every pair of consecutive commits of this repo, confirm the totals add up and that at least 98% of the Python code lines fall inside a named symbol, check `why` on five hand-picked symbols, and time `done` on a typical task
      covers: D8@1
