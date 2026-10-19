# 011 — modular-core — Tasks

- [ ] T001 [agent] [status:todo] Create the `spectrace/` package with `model.py` (file helpers, items, tasks, specs, `Repo`) and import it back into `trace.py`
      covers: D1@1, A2@2
- [ ] T002 [agent] [status:todo] Move the git helpers into `gitio.py` and the state file and task edits into `state.py`
      covers: D1@1
- [ ] T003 [agent] [status:todo] Move `parse_patch`, `load_patches`, `follow` and `file_presence` into `patches.py`
      covers: D1@1
- [ ] T004 [agent] [status:todo] Move the command handlers and the parser into `commands.py` and `cli.py`
      covers: D1@1
- [ ] T005 [agent] [status:todo] Reduce `trace.py` to the launcher that re-exports `main` and the regexes the tests use, and confirm `tests/test_trace.py` passes unchanged
      covers: D2@1
- [ ] T006 [agent] [status:todo] Replace the single `trace.py` cap in `tests/test_skills.py` with one budget per module
      covers: R3@1, D4@1, A5@4
      kind: test
      retires: 001/T009
- [ ] T007 [agent] [status:todo] Add `ensure_ignores()` to `state.py`, call it from `save_state`, and test it on a repo whose `.spectrace/.gitignore` already exists
      covers: R4@1, D5@1
      kind: test
- [ ] T008 [agent] [status:todo] Update `spectrace-start` Phase 3 and "Owns only", and `references/upgrade.md`, to copy and replace the package as one unit
      covers: D3@1, A2@2
- [ ] T009 [agent] [status:todo] Update `README.md`, `format.md` "Files" and the `AGENTS.md` doc map (with `planning/graph-plan.md`), and fix the two stale statements: the README's e2e status and the AGENTS.md remote rule
      covers: D3@1, A2@2
- [ ] T010 [agent] [status:todo] Verify equivalence: run `status`, `check` and `impact` with the previous `trace.py` and the new one on this repo, diff the outputs, and run the full suite
      covers: R1@1
      kind: test
- [ ] T011 [agent] [status:todo] Verify install and upgrade: follow Phase 3 into a temporary repo, upgrade a single-file install with `upgrade.md`, and run `--version`, `status` and `check` in both
      covers: R2@1
      kind: test
