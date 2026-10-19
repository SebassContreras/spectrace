# 011 — modular-core — Tasks

- [x] T001 [agent] [status:done] Create the `spectrace/` package with `model.py` (file helpers, items, tasks, specs, `Repo`) and import it back into `trace.py`
      covers: D1@1, A2@2
      changes: skills/spectrace-start/assets/spectrace/__init__.py (+7 -0), skills/spectrace-start/assets/spectrace/gitio.py (+12 -0), skills/spectrace-start/assets/spectrace/model.py (+429 -0), skills/spectrace-start/assets/spectrace/patches.py (+53 -0), skills/spectrace-start/assets/trace.py (+8 -485)
- [x] T002 [agent] [status:done] Move the git helpers into `gitio.py` and the state file and task edits into `state.py`
      covers: D1@1
      changes: skills/spectrace-start/assets/spectrace/gitio.py (+67 -1), skills/spectrace-start/assets/spectrace/state.py (+52 -0), skills/spectrace-start/assets/trace.py (+4 -126)
- [x] T003 [agent] [status:done] Move `parse_patch`, `load_patches`, `follow` and `file_presence` into `patches.py`
      covers: D1@1
      changes: skills/spectrace-start/assets/spectrace/patches.py (+24 -0), skills/spectrace-start/assets/trace.py (+1 -25)
- [x] T004 [agent] [status:done] Move the command handlers and the parser into `commands.py` and `cli.py`
      covers: D1@1
      changes: skills/spectrace-start/assets/spectrace/cli.py (+35 -0), skills/spectrace-start/assets/spectrace/commands.py (+234 -0), skills/spectrace-start/assets/trace.py (+2 -260)
- [x] T005 [agent] [status:done] Reduce `trace.py` to the launcher that re-exports `main` and the regexes the tests use, and confirm `tests/test_trace.py` passes unchanged
      covers: D2@1
      changes: skills/spectrace-start/assets/trace.py (+6 -6)
- [x] T006 [agent] [status:done] Replace the single `trace.py` cap in `tests/test_skills.py` with one budget per module
      covers: R3@1, D4@1, A5@4
      kind: test
      retires: 001/T009
      changes: tests/test_skills.py (+13 -9)
- [x] T007 [agent] [status:done] Add `ensure_ignores()` to `state.py`, call it from `save_state`, and test it on a repo whose `.spectrace/.gitignore` already exists
      covers: R4@1, D5@2
      kind: test
      changes: skills/spectrace-start/assets/spectrace/state.py (+21 -4), tests/test_trace.py (+5 -0)
- [x] T008 [agent] [status:done] Update `spectrace-start` Phase 3 and "Owns only", and `references/upgrade.md`, to copy and replace the package as one unit
      covers: D3@1, A2@2
      changes: skills/spectrace-start/SKILL.md (+4 -3), skills/spectrace-start/references/upgrade.md (+6 -3)
- [x] T009 [agent] [status:done] Update `README.md`, `format.md` "Files" and the `AGENTS.md` doc map (with `planning/graph-plan.md`), and fix the two stale statements: the README's e2e status and the AGENTS.md remote rule
      covers: D3@1, A2@2
      changes: AGENTS.md (+3 -1), README.md (+9 -5), skills/spectrace-start/assets/format.md (+2 -2)
- [x] T010 [agent] [status:done] Verify equivalence: run `status`, `check` and `impact` with the previous `trace.py` and the new one on this repo, diff the outputs, and run the full suite
      covers: R1@1
      kind: test
      changes: none
- [x] T011 [agent] [status:done] Verify install and upgrade: follow Phase 3 into a temporary repo, upgrade a single-file install with `upgrade.md`, and run `--version`, `status` and `check` in both
      covers: R2@1
      kind: test
      changes: none
