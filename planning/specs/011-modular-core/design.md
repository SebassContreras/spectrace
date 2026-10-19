# 011 — modular-core — Design

## Approach

Code moves; it is not rewritten. The existing tests are the proof that nothing changed.

- D1@1 (implements R1): The code of `skills/spectrace-start/assets/trace.py` moves, function by function and unchanged, into `skills/spectrace-start/assets/spectrace/`: `model.py` (the file helpers, items, tasks, specs and `Repo`), `gitio.py` (git, snapshots, `refs/spectrace/`, diff, numstat), `state.py` (the state file and task edits), `patches.py` (`parse_patch`, `load_patches`, `follow`, `file_presence`), `commands.py` (the `cmd_*` handlers and `COMMANDS`) and `cli.py` (the parser and `main`). `VERSION` stays in `spectrace/__init__.py`, still `"1"`.
- D2@1 (implements R1): `trace.py` becomes a launcher: it puts its own folder on `sys.path`, imports `main` from `cli.py` and the regexes `tests/test_trace.py` uses from `model.py`, and exposes them under the same names, so that test file runs unchanged. Run as a script it calls `main()` as before.
- D3@1 (implements R2): `spectrace-start` Phase 3 and `references/upgrade.md` copy `assets/trace.py` and the whole `assets/spectrace/` folder, without `__pycache__`, into `.spectrace/`. An upgrade deletes the old folder before copying the new one, so a module dropped in a later version does not linger. The check still compares `VERSION` (probe a), which does not change here.
- D4@1 (implements R3): `tests/test_skills.py` replaces the single `trace.py` cap with one check per module under `assets/spectrace/`: at most 600 lines (A5@4). The `SKILL.md` body checks stay.
- D5@1 (implements R4): `state.py` gains `ensure_ignores(root)`, which appends any missing line (`state.json`, `index.db`, `__pycache__/`) to `.spectrace/.gitignore` and creates the file when absent; `save_state` calls it, replacing today's create-if-missing code.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Package and launcher, not one file or a zipapp | readable modules; the same command; installing is still a copy | a folder to copy, not a file | one unit with `VERSION`; an upgrade replaces the whole folder (D3) |
| Move without rewriting | the unchanged tests prove nothing changed | awkward seams stay for now | later specs touch only the modules they extend |
| A budget per module, not one cap | each file stays readable as the trace grows | no limit on the total | revisit A5 if the package outgrows its purpose |

## Deliverables

- `skills/spectrace-start/assets/spectrace/` (new) and `skills/spectrace-start/assets/trace.py`
- `tests/test_skills.py`
- `skills/spectrace-start/SKILL.md`, `skills/spectrace-start/references/upgrade.md`,
  `skills/spectrace-start/assets/format.md`, `README.md`, `AGENTS.md`

## Sequencing

Package modules first — the old `trace.py` keeps working until the launcher replaces it, and
the tests pass after every task — then the launcher with the unchanged test suite, then the
budgets and the ignores, then install and docs, then the equivalence run and the install check.

## Trade-offs context

Costs of decisions the table above does not cover.

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| D3 replaces the old folder on upgrade | no module lingers after a version drops it | files lost if the copy fails midway | copy the new folder to a temporary name, then swap it in |
| D5 appends to `.spectrace/.gitignore` | adopted repos get the new ignores | touches an existing file | only missing lines, only in the file the trace owns |
