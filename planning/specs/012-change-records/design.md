# 012 — change-records — Design

## Approach

The record is made when a task closes, because that is the only moment both the pre- and the
post-image of every file exist: `refs/spectrace/base` and the working tree. Mapping a patch's
line numbers onto today's code instead hits the right symbol 35% of the time (measured on this
repo's own history: 340 of 979 unambiguous lines), and the patch can be missing altogether when
it exceeds `PATCH_LIMIT`.

- D1@1 (implements R1, R8): `trace done` writes `.spectrace/changes/NNN-TNNN.touch.json` beside the patch (sorted keys, no dates). Per changed file: `status`, `lang`, `lines` (`[added, removed]`, the same totals as `numstat`), `symbols` (`name`, `kind`, `change` — added, modified, removed, or renamed with `from` —, `sig` for Python, `lines`, `body` hash) and `other` buckets (imports, module, file). Per task: `skipped` and `partial`. It is computed, reusing the hunk parser of `patches.py`, from `git diff -U0 -M` between the `base` and `current` trees and from the AST of each file's pre- and post-image, so it depends neither on the patch nor on its size limit.
- D2@1 (implements R7): Adapters sit behind one interface, `symbols(text) -> list of spans`, chosen by file extension. Python (`ast`): functions, classes, methods, module variables, class attributes and imports; decorators belong to the span; duplicate names at one level merge (a `property` and its setter are one symbol). Markdown: headings outside fences as `Section > Subsection`, plus `(frontmatter)` and `(preamble)`. Every other file is one file-level span.
- D3@1 (implements R1, R6): The recorder runs in `done` before `drop("base")` and is wrapped so that no exception stops `done`. Caps: a file over 1 MB, or a task over 400 changed files, is recorded at file level and the record is marked `partial`; a file that cannot be parsed — a `SyntaxError`, including syntax newer than the Python running the trace — goes to `skipped` with the reason.
- D4@1 (implements R2): `trace why <path[::symbol]>` reads the records newest first, following `renamed_from` and the file renames recorded in later patches. For each task that touched the code it prints the task, the items it covers (with revision and `retired` flag) and the task that retired it, if any. Code removed by a task is answered from that task's record; code no record names is reported as outside the trace.
- D5@1 (implements R3): `trace impact <decision>` adds, under each task, the symbols of its record. A symbol is `unchanged` when its current body hash equals the recorded one, `changed` when it exists with another body, and `gone` when it no longer exists (`renamed to` when a later record says so). For a changed symbol it counts the lines the task added that are still inside that symbol, as a multiset of whole lines read from the task's patch with `parse_patch`, whose minimum line length becomes a parameter (0 here) instead of the fixed 4-character filter. The file-level lines (`N/M added lines still present`) stay.
- D6@2 (implements R4): `trace check` reports `leftover` — pending, on the spec of the retiring task — for each done task C with `retires: T` and each symbol T added whose current body hash equals the recorded one, unless a task done after C recorded that symbol again (added, modified or renamed). `trace keep <path::symbol> "<reason>"` writes `.spectrace/keeps.json` (symbol, task, reason; a reason is required) and `check` skips what it lists.
- D7@1 (implements R5): A task without a record is answered by anchoring its patch: each added line is matched by text to the current file; a line found exactly once gives its current symbol, ambiguous or missing lines stay unmapped. Everything derived this way is labelled `anchored` and never gates (A11@1).
- D8@1 (implements R8): `done` prints `accounted A/A added, R/R removed lines`, and `check` recomputes every record's totals; a record whose symbols and buckets do not add up to `lines` is reported as `unaccounted: n` (a warning: it is the recorder's fault, not the code's).
- D9@1 (implements R9): `start` and `check` run the recorder between `reference_tree` and the working tree, and name the changed symbols in their existing "changed outside any task" messages.
- D10@1 (implements R1, R2): `VERSION` becomes `2` and `format.md` states `Format version: 2`; it defines the record and the code address — `path`, or `path::Qualified.name` (`docs/usage.md::Usage > Install` for Markdown). Version 1 projects stay valid, and a version 1 trace ignores the records (it reads only `NNN-TNNN.patch`). `FormatDocTest` parses the record's example.
- D11@1 (implements R2, R4): `spectrace-change` Phase 3 uses the symbols of `impact`, `why` and `leftover` in place of the manual `git blame` step, and `agents-protocol.md` gains one line: before editing code you did not write, run `trace why <path[::symbol]>`.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Record at `done`, not derive from patches | exact by construction; independent of the 200 KB patch limit | a new ledger file; only for tasks from now on | the anchored fallback for older tasks (D7), labelled; a version 1 trace ignores records |
| A sidecar file, not a field in the patch or in `changes:` | `git apply` and the version 1 parsers stay untouched; the task line stays short | one more file per task | same name stem as the patch; both committed |
| Python and Markdown by name, the rest at file level | precision first; no dependencies | JS and TS stay file-level for now | A13@1: another language enters with a measured gate |
| Only exact findings may gate | a heuristic never holds a spec open | anchored answers cannot block | they are labelled; `check` keeps its exit codes |
| `leftover` compares the body hash | no alarm when the code was rewritten | code changed slightly still passes | rewriting is the redo path (A6); `impact` shows what remains |

## Deliverables

- `skills/spectrace-start/assets/spectrace/symbols/` (new), `records.py` (new), one module per view in `views/` (`why.py`, `impact.py`; new),
  and changes to `commands.py` and `model.py`
- `skills/spectrace-start/assets/format.md`, `skills/spectrace-start/assets/agents-protocol.md`,
  `skills/spectrace-change/SKILL.md`
- `tests/test_symbols.py` and `tests/test_records.py` (new, with their own temporary-repo helper)

## Sequencing

Adapters first (pure functions, tested alone), then the recorder, then the `done` hook, then the
format and version, then the views that read the records (`why`, `impact`, `leftover`, `keep`),
then the fallback and the outside-the-task reports, then the tests and the verification over this
repo's real history.

## Trade-offs context

Costs of decisions the table above does not cover.

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| D9 runs the recorder in `start` and `check` | symbols named outside any task | cost on every call | time it in T019; the recorder reads only changed files |
| D10 bumps `VERSION` to 2 | the record is a declared contract | every install is asked to upgrade though v1 still reads | 010's compare-by-version path does it in one step |
| D3 caps a file at 1 MB and a task at 400 files | `done` stays fast on huge changes | the limits are guesses | T019 times `done`; the caps are named constants, changed in one place |
| D5 counts surviving lines as a multiset | survives moves inside a symbol | a repeated line can be counted twice | the counts are labelled and never gate (A11) |
| D8 reports `unaccounted` as a warning | a recorder bug never blocks a spec | a warning can be ignored | T019 runs the recorder over this repo's whole history |
