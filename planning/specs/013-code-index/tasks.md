# 013 — code-index — Tasks

- [x] T001 [agent] [status:done] Add the index store: schema, per-file content hash, incremental refresh, and `index.db` handled by `ensure_ignores`
      covers: D1@2, A12@1
      changes: skills/spectrace-start/assets/spectrace/index.py (+94 -0), skills/spectrace-start/assets/spectrace/state.py (+1 -1)
- [x] T002 [agent] [status:done] Extract per-file Python facts — definitions, imports and the names each symbol uses — from the adapter's AST
      covers: D2@1
      changes: skills/spectrace-start/assets/spectrace/facts.py (+101 -0), skills/spectrace-start/assets/spectrace/index.py (+3 -6), tests/test_trace.py (+1 -1)
- [x] T003 [agent] [status:done] Add the linker: imports to repo files, same-module and `self` binding, and attribute names with candidate counts
      covers: D2@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/facts.py (+1 -1), skills/spectrace-start/assets/spectrace/linker.py (+137 -0)
- [x] T004 [agent] [status:done] Add `trace index` with `--status`, `--rebuild` and `--dump`, and the lazy refresh used by the commands that need the index
      covers: D1@2
      changes: skills/spectrace-start/assets/spectrace/commands.py (+3 -0), skills/spectrace-start/assets/spectrace/views/index_view.py (+39 -0)
- [x] T005 [agent] [status:done] Classify test files and link each test to the symbols it references
      covers: D4@1
      changes: skills/spectrace-start/assets/spectrace/linker.py (+21 -0), skills/spectrace-start/assets/spectrace/symbols/__init__.py (+5 -0), skills/spectrace-start/assets/spectrace/views/__init__.py (+1 -4), skills/spectrace-start/assets/spectrace/views/index_view.py (+11 -5)
- [x] T006 [agent] [status:done] Extend `trace impact` to `path[::symbol]` with `--direction` and `--depth`, grouped by confidence and ending with the "not analysed" line
      covers: D3@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/cli.py (+6 -1), skills/spectrace-start/assets/spectrace/commands.py (+3 -2), skills/spectrace-start/assets/spectrace/views/__init__.py (+0 -1), skills/spectrace-start/assets/spectrace/views/impact.py (+59 -2)
- [x] T007 [agent] [status:done] Add `--deep` to the decision form of `impact`
      covers: D3@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+1 -1), skills/spectrace-start/assets/spectrace/views/impact.py (+24 -0)
- [x] T008 [agent] [status:done] Add the removed-symbol mention warning to `check`
      covers: D5@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+8 -1), skills/spectrace-start/assets/spectrace/facts.py (+5 -2), skills/spectrace-start/assets/spectrace/index.py (+8 -0), skills/spectrace-start/assets/spectrace/mentions.py (+35 -0), skills/spectrace-start/assets/spectrace/model.py (+24 -17)
- [x] T009 [agent] [status:done] Add the trace coverage and the resolution rate to `index --status`
      covers: D6@1
      changes: skills/spectrace-start/assets/spectrace/views/index_view.py (+21 -0)
- [x] T010 [agent] [status:done] Add `tests/eval_index.py`: recall and precision of the dependents against the co-changes in git history
      covers: D7@1
      changes: tests/eval_index.py (+57 -0)
- [x] T011 [agent] [status:done] Test the index on a fixture project: a refresh re-reads only the changed file, each resolution tier, `impact` in and out, tests linking, warnings that never hold a spec open, and unparsed files reported
      covers: R1@1, R2@1, R3@1, R4@1, R5@1, R6@1
      kind: test
      changes: tests/test_index.py (+117 -0)
- [x] T012 [agent] [status:done] Run `index --status` and the evaluation on this repo, write the numbers and the limits into the README's Limits section
      covers: R7@1, R8@1
      changes: README.md (+10 -0)
- [x] T013 [agent] [status:done] Test `index --status` on a fixture project: the coverage counts (exact, anchored, outside the trace) and the resolution rate
      covers: R7@1
      kind: test
      changes: tests/test_index.py (+11 -0)
