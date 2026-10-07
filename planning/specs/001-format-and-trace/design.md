# 001 — format-and-trace — Design

## Approach

- D1@2 (implements R1): `format.md` defines R/D/A items, references, task lines and fields, the roadmap table, and the history files — `changes.md` per spec, `planning/changes.md` for A items; `trace.py` parses exactly that and ignores fenced examples.
- D2@2 (implements R2, R3): `trace start` snapshots the working tree through a temporary index and `git write-tree`, kept alive under `refs/spectrace/`; `trace done` diffs that snapshot against the current tree with rename detection (a moved file is recorded as `old → new`), excluding `planning/` and `.spectrace/`, and writes `.spectrace/changes/NNN-TNNN.patch` plus the task's `changes:` line. One task open at a time; changes made with no task open are refused until adopted or ignored.
- D3@2 (implements R3): `trace check` computes suspect, orphan and uncovered states; `trace impact` walks R → D → tasks across specs and reports, per recorded patch, how many added lines are still present, following each file through the renames recorded in later patches (or inferred from a delete and an add of the same content within one patch).
- D4@1 (implements R4): `trace status --write` rewrites only the `Status` and `Stage` cells; `trace check` reports any cell that disagrees with the files.
- D5@1 (implements R5): Python standard library only; git through `subprocess`.
- D6@1 (implements R6): `trace check` collects the files task patches deleted (not renamed) that no longer exist, and scans the repo's text files — except history (`tasks.md`, `changes.md`, `.spectrace/`) and retired item lines — for their paths; each mention is pending on the deleting task's spec.
- D7@1 (implements R7): `.spectrace/fingerprints.json` maps each `item@revision` to a hash of its whitespace-normalized text. `status --write` records items it hasn't seen and re-baselines items no finished task covers; `check` reports a covered item whose text no longer matches (pending, on its spec); `trace review <ref>` accepts the current text as a wording-only edit.
- D8@1 (implements R8): `trace restore NNN/TNNN` reverse-applies that task's recorded patch to the working tree (`git apply -R`, checked first, nothing applied on conflict). It needs an open task, so the restored code is recorded as that task's change.
- D9@1 (implements R3): A task that `retires:` a finished task is pending until it is done, so `trace check --strict` fails while any cleanup is left.

## Deliverables

- `skills/spectrace-start/assets/format.md`
- `skills/spectrace-start/assets/trace.py`
- `tests/test_trace.py`
