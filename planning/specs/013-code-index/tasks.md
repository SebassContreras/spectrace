# 013 — code-index — Tasks

- [ ] T001 [agent] [status:todo] Add the index store: schema, per-file content hash, incremental refresh, and `index.db` handled by `ensure_ignores`
      covers: D1@1, A12@1
- [ ] T002 [agent] [status:todo] Extract per-file Python facts — definitions, imports and the names each symbol uses — from the adapter's AST
      covers: D2@1
- [ ] T003 [agent] [status:todo] Add the linker: imports to repo files, same-module and `self` binding, and attribute names with candidate counts
      covers: D2@1, A11@1
- [ ] T004 [agent] [status:todo] Add `trace index` with `--status`, `--rebuild` and `--dump`, and the lazy refresh used by the commands that need the index
      covers: D1@1
- [ ] T005 [agent] [status:todo] Classify test files and link each test to the symbols it references
      covers: D4@1
- [ ] T006 [agent] [status:todo] Extend `trace impact` to `path[::symbol]` with `--direction` and `--depth`, grouped by confidence and ending with the "not analysed" line
      covers: D3@1, A11@1
- [ ] T007 [agent] [status:todo] Add `--deep` to the decision form of `impact`
      covers: D3@1
- [ ] T008 [agent] [status:todo] Add the removed-symbol mention warning to `check`
      covers: D5@1, A11@1
- [ ] T009 [agent] [status:todo] Add the trace coverage and the resolution rate to `index --status`
      covers: D6@1
- [ ] T010 [agent] [status:todo] Add `tests/eval_index.py`: recall and precision of the dependents against the co-changes in git history
      covers: D7@1
- [ ] T011 [agent] [status:todo] Test the index on a fixture project: a refresh re-reads only the changed file, each resolution tier, `impact` in and out, tests linking, warnings that never hold a spec open, and unparsed files reported
      covers: R1@1, R2@1, R3@1, R4@1, R5@1, R6@1
      kind: test
- [ ] T012 [agent] [status:todo] Run `index --status` and the evaluation on this repo, write the numbers and the limits into the README's Limits section
      covers: R7@1, R8@1
