# spectrace format

The single definition of how specs, decisions and tasks are written. Skills cite this
file; `trace.py` implements it. If the two ever disagree, `trace.py` is wrong — fix it
and add a test. Format version: 2.

## Files

```
AGENTS.md                         instructions for any agent (one file, no CLAUDE.md)
planning/product.md               what this is, who it's for, out of scope
planning/architecture.md          project-wide decisions (A items)
planning/styles.md                preferences (optional)
planning/roadmap.md               index of specs
planning/changes.md               history of changes to A items
planning/specs/NNN-name/
  requirements.md                 R items
  design.md                       D items
  tasks.md                        tasks
  changes.md                      history of changes to this spec
.spectrace/
  trace.py  spectrace/  format.md copied in by `spectrace-start` (the script and its package)
  interview.md                    interview ledger
  changes/NNN-TNNN.patch          exact diff of each finished task (committed)
  changes/NNN-TNNN.touch.json     symbols the task added, changed or removed (committed, v2)
  fingerprints.json               item text hashes and IDs seen, written by trace (committed)
  keeps.json                      leftovers accepted with a reason, by `trace keep` (committed)
  index.db                        code index, disposable (git-ignored)
  state.json                      open task (git-ignored, with `__pycache__/`)
```

## Items: R, D, A

An item is one normative statement with an ID and a revision. Anything that is not an
item line is context and is never traced.

```
- R2@1: A user signs in with email and password.
- D3@1 (implements R2): Sessions live in an httpOnly cookie.
- A4@1: Runtime is Node 22 — why: LTS, team knows it.
- ~~D1@1 (implements R2): Sessions live in localStorage.~~ retired 2026-10-12 → D3
```

- `R` items live only in a spec's `requirements.md`, `D` items only in its `design.md`,
  `A` items only in `planning/architecture.md`.
- IDs are numbered per file kind and never reused: a retired item stays, struck through.
- `@N` is the revision. Bump it when the meaning changes; never for a wording fix.
- `(implements R2, R5)` on a D item names the requirements it serves (same spec).
- Retired: the whole statement wrapped in `~~`, then `retired YYYY-MM-DD`, optionally
  `→ <replacement ID>`.
- Never edit an item's meaning by hand — the `spectrace-change` skill does it, so the history in
  `changes.md` and the trace stay right.

## References

| Written as | Means |
|---|---|
| `R2@1`, `D3@1` | item in the same spec |
| `001/D3@1` | item in spec 001 |
| `A4@1` | project-wide item in `architecture.md` |
| `001/T005` | task 5 of spec 001 |

## Tasks (`tasks.md`)

```
- [ ] T005 [agent] [status:todo] Session middleware
      covers: D3@1
- [x] T006 [agent] [status:done] Session expiry test
      covers: R2@1
      kind: test
      changes: src/auth/session.ts (+42 -3), test/session.test.ts (+30)
- [ ] T009 [agent] [status:todo] Remove the localStorage session code
      covers: D3@1
      retires: T002
- [ ] T010 [human] [status:blocked] Create the mail provider account
      covers: R4@1
      └─ blocked: waiting for billing approval
- [ ] T011 [agent] [status:blocked] Store sessions in two places
      covers: D3@1
      └─ blocked: conflicts 001/D3: a cookie alone cannot hold the offline session
```

- A task line starts at column 0: checkbox, `T` + 3 digits, owner, status, text.
  The checkbox is `[x]` exactly when the status is `done`.
- Owner: `agent` (any agent may do it) or `human` (the user does it; agents report and
  skip it).
- Status: `todo` · `in_progress` · `blocked` · `done`.
- Fields are indented lines under the task:
  - `covers:` — required. The items this task implements or verifies.
  - `kind: test` — the task writes a test for the R items it covers.
  - `kind: fix` — the task brings code back in line with the items it covers, after a
    bug report (the `spectrace-fix` skill); a `kind: test` task with a failing
    regression test comes before it.
  - `retires: T002` — the task removes what an earlier task built.
  - `changes:` — written only by `trace done`. Never by hand.
  - `└─ <note>` — free text. `trace block` writes `└─ blocked: <reason>`; a reason of the
    form `conflicts <ref>: <why>` records a **decision conflict** — the task cannot be done
    without contradicting that item (`A5`, `001/D3`; revision optional). `block` refuses a
    reference that names no item. The latest block note of a task is the one that counts.
- Who writes what: `trace` writes `in_progress`, `done`, `blocked`, the checkbox and
  `changes:`. The `spectrace-plan` and `spectrace-change` skills write new task lines;
  `spectrace-change` may also
  re-point a `covers:` to a new revision (adding a `└─ reviewed YYYY-MM-DD: …` note)
  and delete a task that was never started. Nobody else edits a task line.

## Roadmap (`planning/roadmap.md`)

```
| ID  | Spec  | Status      | Depends on | Stage | Priority |
|-----|-------|-------------|------------|-------|----------|
| 001 | auth  | done        | —          | —     | 1        |
| 002 | feed  | in_progress | 001        | build | 2        |
```

- People and skills write `ID`, `Spec`, `Depends on`, `Priority`. Only `trace` writes
  `Status` and `Stage`; `trace check` fails if they differ from what the files say.
- `Spec` is exactly the folder name after `NNN-`.
- `Depends on`: comma-separated spec IDs, or `—`.
- `Priority`: a number, lower first among specs the dependencies don't already order;
  `—` if unranked.
- Stage — what the spec needs next:
  `requirements` (no R items) · `design` (no D items) · `tasks` (no tasks) ·
  `build` (tasks left) · `—` (done).
- Status: `todo` (nothing started) · `in_progress` · `blocked` (an agent task is
  blocked) · `done` (every agent task done, nothing suspect or uncovered). `human`
  tasks never hold a spec open.

## Trace states (computed, never written)

- **suspect** — a done task covers an older revision of an item, or a retired item, and
  no done task retires it. Resolved by the `spectrace-change` skill: re-point `covers:` to the
  new revision (the task is still right) or add a task that `retires:` it.
- **cleanup pending** — a task that `retires:` a finished task isn't done yet. Holds the
  spec open, so `trace check --strict` fails until every cleanup task is done.
- **orphan** — a reference to an item or task that doesn't exist.
- **uncovered** — an active R that no active D implements and no task covers (checked
  once the spec has D items); an active D no task covers (checked once it has tasks).
- **changed** — the text of an A item, or of an item a done task covers, differs from when that work was
  built, and the revision wasn't bumped. Resolved by bumping the revision (a meaning
  change: the `spectrace-change` skill), or by `trace review <ref>` (wording only).
- **decision conflict** — an agent task is `blocked` and its latest block note is a
  conflict. Keep the item, edit it or retire it (the `spectrace-change` skill), then resume
  the task with `start`. Once the task leaves `blocked`, the note is history.
- **unrecorded change** — a guarded item (every A item, and every item a finished task
  covers) disappeared without being struck through, or got a new revision or was retired
  with no `changes.md` entry naming its new `ID@rev`. An R or D item nothing has been
  built on is free to edit: the trace re-baselines it. The first time the trace sees an
  item it records it silently, so adopting an existing repo flags nothing.
- **mentions a deleted file** — a file a task deleted is still named somewhere outside
  history (`tasks.md`, `changes.md`, `.spectrace/`, retired item lines). Pending on the
  spec of the task that deleted it.

## Change records (`changes/NNN-TNNN.touch.json`)

Written by `trace done` beside the patch, from the task's base and the working tree, so it
does not depend on the patch or its size limit. Sorted keys, no dates. Per changed file:
`status` (`new`, `modified`, `deleted`, `renamed` with `from`), `lang` (`python`,
`markdown` or `file`), `lines` (`[added, removed]`, as `git diff --numstat`; `null` for a
binary file), `symbols` and `other`. A symbol has `name`, `kind`, `change` (`added`,
`modified`, `removed`, or `renamed` with `from`), `lines`, the `body` hash of its text and,
in Python, `sig` (and `sig_from` when a change altered it). Every added and removed line belongs to the innermost symbol holding it,
or to a bucket in `other`: `imports`, `module` (outside any symbol) or `file` (a file read
at file level). Per task: `partial` (a file over 1 MB or a task over 400 files was read at
file level) and `skipped` (files that could not be parsed, with the reason). The symbols
and buckets of a file always add up to its `lines`.

```json
{
 "files": {
  "src/store.py": {
   "lang": "python",
   "lines": [5, 2],
   "other": {"imports": [1, 0], "module": [1, 0]},
   "status": "modified",
   "symbols": [
    {"body": "3f1c9a0d5e7b2a64", "change": "added", "kind": "function", "lines": [3, 0], "name": "save", "sig": "(path, data)"},
    {"body": "9b2e4f61c0a8d375", "change": "renamed", "from": "read", "kind": "function", "lines": [0, 2], "name": "load", "sig": "(path)"}
   ]
  }
 },
 "partial": false,
 "skipped": []
}
```

A **code address** is a path, or `path::Qualified.name`: `src/store.py::Store.save`, or
`docs/usage.md::Usage > Install` for a Markdown section. Version 1 projects stay valid: a
task without a record is answered from its patch and labelled `anchored`.

## History (`changes.md`)

One entry per change, newest last, written by the `spectrace-change` skill: in the spec's
`changes.md` for R and D items, in `planning/changes.md` for A items. A change that
touches both gets an entry in each.

```
## 2026-10-12 — sessions move to cookies
Why: localStorage sessions are readable by any script on the page.
- MODIFIED R2@1 → R2@2
- REMOVED D1@1
- ADDED D3@1
- Tasks: T009 retires T002; T006 re-pointed to R2@2 (still valid)
```

## Executing tasks

```
python3 .spectrace/trace.py status            # (python on Windows)
python3 .spectrace/trace.py start 001/T005    # before editing anything
python3 .spectrace/trace.py done 001/T005     # writes changes: and the patch
python3 .spectrace/trace.py check             # must exit 0 before you finish
python3 .spectrace/trace.py check --audit     # trace verification plus consistency audit
python3 .spectrace/trace.py audit             # consistency audit across architecture, product and interview
python3 .spectrace/trace.py audit --strict    # exit 1 on audit warnings (CI / release gates)
python3 .spectrace/trace.py audit --json      # machine-readable JSON output
```

`start` snapshots the working tree without committing or touching the staging area;
`done` diffs against that snapshot (detecting renames), so each task's changes are exact
even if several tasks share one commit or none. One task is open at a time. Changes
under `planning/` and `.spectrace/` are never counted as task changes.

Used by the `spectrace-change` skill:

```
python3 .spectrace/trace.py impact 001/D3      # what implemented it, and what's still in the code
python3 .spectrace/trace.py impact 001/D3 --deep  # plus the dependents and tests of its symbols
python3 .spectrace/trace.py review 001/D3      # accept a wording-only edit of its text
python3 .spectrace/trace.py restore 001/T009   # undo that task's changes, inside the open task
python3 .spectrace/trace.py keep src/store.py::save "the CLI still needs it"  # a leftover that stays
```

The code map, for any skill or agent:

```
python3 .spectrace/trace.py why src/store.py::Store.save        # the tasks and decisions behind code
python3 .spectrace/trace.py locate "session expiry"             # rank items, tasks, files, symbols
python3 .spectrace/trace.py impact src/store.py::Store --depth 2  # dependents (--direction out: dependencies)
python3 .spectrace/trace.py packet 001/T005 --json              # review packet of a task
python3 .spectrace/trace.py packet --diff --base origin/main    # review packet of a diff (CI)
python3 .spectrace/trace.py index --status                      # what the index holds and misses
```

`index` keeps `.spectrace/index.db` (git-ignored, disposable: delete it any time); the
commands that need it refresh it first, and `packet --diff` builds it in memory. Every
relation is `exact` or `inferred` (with its number of candidates); only exact findings
hold a spec open. `.spectrace/keeps.json` (committed) lists the symbols `keep` accepted,
each with the task that added it and the reason.
