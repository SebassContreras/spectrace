# spectrace format

The single definition of how specs, decisions and tasks are written. Skills cite this
file; `trace.py` implements it. If the two ever disagree, `trace.py` is wrong — fix it
and add a test. Format version: 1.

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
  trace.py  format.md             copied in by `spectrace-start`
  interview.md                    interview ledger
  changes/NNN-TNNN.patch          exact diff of each finished task (committed)
  fingerprints.json               hash of each item's text, written by trace (committed)
  state.json                      open task (git-ignored)
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
```

- A task line starts at column 0: checkbox, `T` + 3 digits, owner, status, text.
  The checkbox is `[x]` exactly when the status is `done`.
- Owner: `agent` (any agent may do it) or `human` (the user does it; agents report and
  skip it).
- Status: `todo` · `in_progress` · `blocked` · `done`.
- Fields are indented lines under the task:
  - `covers:` — required. The items this task implements or verifies.
  - `kind: test` — the task writes a test for the R items it covers.
  - `retires: T002` — the task removes what an earlier task built.
  - `changes:` — written only by `trace done`. Never by hand.
  - `└─ <note>` — free text.
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
- **changed** — the text of an item a done task covers differs from when that work was
  built, and the revision wasn't bumped. Resolved by bumping the revision (a meaning
  change: the `spectrace-change` skill), or by `trace review <ref>` (wording only).
- **mentions a deleted file** — a file a task deleted is still named somewhere outside
  history (`tasks.md`, `changes.md`, `.spectrace/`, retired item lines). Pending on the
  spec of the task that deleted it.

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
```

`start` snapshots the working tree without committing or touching the staging area;
`done` diffs against that snapshot (detecting renames), so each task's changes are exact
even if several tasks share one commit or none. One task is open at a time. Changes
under `planning/` and `.spectrace/` are never counted as task changes.

Used by the `spectrace-change` skill:

```
python3 .spectrace/trace.py impact 001/D3      # what implemented it, and what's still in the code
python3 .spectrace/trace.py review 001/D3      # accept a wording-only edit of its text
python3 .spectrace/trace.py restore 001/T009   # undo that task's changes, inside the open task
```
