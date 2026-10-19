# 013 — code-index — Design

## Approach

Two steps, as in the tools that index code for navigation: the facts of each file are
extracted and cached by file hash, and the relations are linked across files on every run,
because one changed file can change what its neighbours resolve to. Only exact relations may
ever gate (A11@1); a static analysis of Python misses roughly 30% of the call edges even in
the best published tools, so the rest is labelled and never claims "no impact".

- D1@1 (implements R1): The index is `.spectrace/index.db`, one `sqlite3` file (A12@1) with the tables `files` (path, content hash, size, language, test flag, parse status), `symbols`, `imports` and `refs`. A command that needs the index refreshes it first: files whose size or modification time changed are re-hashed, and only those whose hash changed are re-extracted. `trace index --rebuild` starts over and `--dump` prints JSON for inspection. `ensure_ignores` already lists `index.db`.
- D2@1 (implements R2, R6): For Python, a file's facts are its definitions (reusing the 012 adapter), its imports and the names its symbols use. Linking: an import resolves to a file of the repo (roots: the repo root, `src/` and every directory with a chain of `__init__.py`); a name bound by an import, or defined in the same module, is exact; `self.method` resolves through the class and its bases, exact when unique; an attribute name matched across the repo is inferred, with its candidate count; a name that resolves to nothing is dropped and counted in the resolution rate. Files that do not parse and languages without an adapter are listed under "not analysed".
- D3@1 (implements R3, R4): `trace impact` accepts a code address. Dependents go up to `--depth` (default 2), grouped by confidence, each with its path and the reference line; a longer list ends in `+N more`. `--direction in|out` picks dependents or dependencies. The decision form with `--deep` runs the same query from each symbol its tasks introduced (the 012 records). The output never says "no impact": it says "no dependents found among the analysed files" and counts what was not analysed.
- D4@1 (implements R3): A file is a test by path or name (`tests/`, `test_*.py`, `*_test.py`) or because a task with `kind: test` recorded it. "Tests that reference S" are the test symbols whose resolved references include S.
- D5@1 (implements R5): `trace check` collects the names of classes, functions and variables that tasks removed (the 012 records), keeps those no longer defined anywhere in the index, and looks for them as whole words in non-history text files — a nested name needs its qualified form, and a bare name needs six characters or more. Each hit is a warning, capped per name; an inferred finding never holds a spec open.
- D6@1 (implements R7): `index --status` prints files, symbols, parse failures, the trace coverage (symbols whose file has an exact record, an anchored answer, or none) and the resolution rate per language.
- D7@1 (implements R8): `tests/eval_index.py` — not collected as a test — walks the git history; for each commit that changed at least two files it asks whether the dependents of the changed symbols include the other files of that commit (recall) and how many predicted dependents were not co-changed (a precision proxy). It prints the numbers and sets no threshold.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| A `sqlite3` index, not JSON | atomic writes; indexed queries; nothing to reload per call | an opaque binary; the module can be missing in minimal Pythons | a disposable cache with `--dump`; `why` and `check` do not need it |
| Facts cached per file, linking redone every run | correct when a neighbour changes; simple invalidation | linking cost on each refresh | linking runs in memory over cached facts; measured in T012 |
| Name-based resolution, no types | standard library only; deterministic | recall is limited for dynamic code | confidence labels and candidate counts; never "no impact"; recall measured (R8) |
| Warnings for mentions of removed symbols | catches stale docs and code | noise from common names | length and qualification rules; capped; warnings only |

## Deliverables

- `skills/spectrace-start/assets/spectrace/index.py`, `facts.py` and `linker.py` (new), and
  changes to `views/impact.py`, `commands.py` and `model.py`
- `tests/test_index.py` and `tests/eval_index.py` (new)
- `README.md` (the limits of the code map)

## Sequencing

The store and its refresh first, then the extractor and the linker (pure and testable on a
fixture project), then the commands that read the index, then the evaluation, run last on this
repo's real history.

## Trade-offs context

Costs of decisions the table above does not cover.

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| D4 classifies tests by path or name | simple, no config | an oddly named test is missed | a task with `kind: test` that recorded the file makes it exact |
