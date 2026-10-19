# Plan: the code map as part of spectrace

Written 2026-10-19. Specs 011–015 carry it out; this file keeps the reasoning, so the specs
can stay short. Decisions it changes are recorded in `planning/changes.md` (2026-10-19) and
`planning/architecture.md` (A1@3, A2@2, A5@4, A10–A13).

## Order

011 modular-core → 016 decision-conflicts → 012 → 013 → 014 → 015. Spec 016 (not part of the code map)
makes earlier decisions change by a user's choice — keep, edit or retire — instead of being
worked around, so 012–015 can be built without bending code around old decisions. It runs
after 011 because the old test caps `trace.py` at 900 lines and A5@4 already chose per-module
budgets.

## Goal

The MVP is approved and works. The next goal is a code map: which symbols each task changed,
which decision stands behind a piece of code, what depends on it, and whether a change of
direction left anything behind. It is not a tool beside spectrace. Old and new become one
system: one ledger, one format, one CLI (`trace.py`), one install and upgrade, one test suite.

## Core idea

The code map is the **ledger taken down to the symbol**. spectrace already knows, exactly,
what each task changed and which decision it covered. It lacked (1) which symbols the task
touched, (2) the question the other way round — from code to decision — and (3) relations
between symbols.

```
planning/ (R, D, A, tasks) ──┐
.spectrace/changes/           │  ledger: NNN-TNNN.patch + NNN-TNNN.touch.json   (committed, exact)
code (working tree) ──────────┤
                              ▼
             .spectrace/index.db   (derived, git-ignored): files · symbols · imports · references
                              ▼
        views, all in `trace.py`:  why · impact · locate · packet · check
```

## What spectrace evaluates after this

Lines of a hunk. Until now `parse_patch` keeps only lines of four characters or more
(`trace.py:730`), `file_presence` looks them up as text anywhere in the file, and removed
lines are never validated. Measured on this repo's ledger:

| Hunk line | Before | Measured here | After |
|---|---|---|---|
| Added, 4+ characters | "still present" by text, anywhere in the file | 4,432 of 5,502 (80.6%) | all, inside their symbol |
| Added, blank or 1–3 characters | never | 1,070 (19.4%): 930 blank, 140 short | attributed to their symbol; covered by the body hash |
| Removed, any length | never (only used to detect renames) | 2,374 | recorded; `leftover`, mentions and `why` of deleted symbols |
| Added and repeated in the file | counts as present even if it is another copy | 18.4% ambiguous (in `.py`) | presence inside the symbol, not the file |
| Task whose patch is over 200 KB | no hunks: "search by hand" | none here; likely with JS lockfiles | the record comes from the trees, not the patch |
| Change outside a task (`--ignore`) | file-level warning | — | symbol-level warning; `why` says "outside the trace" |

Every added or removed line, of any length, is attributed to a symbol or an explicit bucket
(imports, module, file). The record keeps the per-file total, so **symbols plus buckets must
equal `numstat`**: `done` checks it when writing ("accounted 42/42 added, 7/7 removed") and
`check` when reading; a mismatch becomes `unaccounted: n`.

| Question | Mechanism | Spec | Guarantee |
|---|---|---|---|
| Is every changed line attributed to a task and a decision? | exact record + accounting | 012 | exact |
| Which decision stands behind this code, even if deleted? | `why` | 012 | exact; "outside the trace" if no task touched it |
| What did a decision build that is still there? | `impact` by symbol | 012 | exact |
| Is code of a retired decision still there? | `leftover` | 012 | exact → pending |
| What changed outside the tasks? | `start` and `check`, by symbol | 012 | exact |
| What depends on this change, which tests touch it? | `impact` with dependents and tests | 013 | exact for resolved imports; the rest inferred, with confidence and candidate count |
| How much of the repo is understood? | `index --status`: trace coverage and reference resolution rate | 013 | a metric, not a gate |
| How serious is a change? | `packet`: signature changed, removed symbols still referenced, dependents, no tests, not analysed | 014 | signals, not a score |

Large changes: the record does not depend on the patch limit. Over 400 files in a task, or a
file over 1 MB, are recorded at file level and the record is `partial: true`; `done` and
`packet` say so. What it still cannot validate, and says so in its output: whether behavior is
correct (tests do that); dynamic relations — reflection, `getattr`, registration by string —
because static analysis has limited recall (about 70% in the best published Python call-graph
tool, PyCG, ICSE 2021); languages without an adapter; edits made with `--ignore`; tasks
finished before records existed (answered by anchoring: about 74% of their lines resolve by
text without ambiguity here).

## Evidence that shaped the design (measured on this repo)

| Fact | Consequence |
|---|---|
| Mapping hunks by line number to today's code hits the right symbol 35% of the time (979 unambiguous lines, 18 patches); only 14.2% of lines still sit at their line. `trace` keeps only the last snapshot | The attribution is **recorded at `done`**, when the pre- and post-image exist; it is not derived later |
| Functions and classes cover 92.4% of code lines; with module variables and imports, 98.6% | A symbol can be a function, class, method, variable, class attribute or import (covers `Meta.fields`, `urlpatterns`, constants) |
| 57% of the ledger's lines are not Python (Markdown 49.5%) | A Markdown adapter (sections) from day one; other files at file level |
| The largest patch is 164,583 B of `PATCH_LIMIT`'s 200,000; past it, a task loses all its hunks | The record is computed from the `base` and `current` trees |
| `VERSION` is the trace's contract and `upgrade` compares only that (010 design) | Everything installs and upgrades as one unit |
| A hunk header names only column-0 lines (git) | It is not used to attribute |

## Architecture

Layers and durability:

| Layer | Content | Where | Committed | Rebuildable |
|---|---|---|---|---|
| Law | R, D, A, tasks, roadmap | `planning/` | yes | no, it is the source |
| Ledger | patch and symbol record per task, fingerprints, `keeps.json` | `.spectrace/` | yes | no: exact only when the task closes |
| Index | files, symbols, imports, references, tokens | `.spectrace/index.db` (`sqlite3`) | no | yes, always |
| Views | `why`, `impact`, `locate`, `packet`, `check` | computed | — | — |

Commands: `status start abort block restore review` unchanged; `done` also records symbols;
`impact <decision>` goes down to symbols (`--deep` adds dependents and tests);
`impact <path[::symbol]>` shows dependents and decisions (`--direction in|out`, `--depth`);
`why <path[::symbol]>` (012); `locate "<text>"` (014); `packet [NNN/TNNN] [--diff --base ref]`
(014); `index [--status|--rebuild|--dump]` (013); `keep <path::symbol> "<reason>"` (012);
`check` adds `leftover`, accounting, outside-the-task symbols and mentions of removed symbols.
Code address: `path`, or `path::Qualified.name` (`docs/usage.md::Usage > Install` for Markdown).

The record, `.spectrace/changes/NNN-TNNN.touch.json` (sorted keys, no dates):

```json
{"task": "001/T003",
 "files": [
  {"path": "tdo/store.py", "status": "modified", "lang": "python", "lines": [12, 2],
   "symbols": [
    {"name": "add", "kind": "function", "change": "modified", "sig": "same", "lines": [3, 1], "body": "9f2c1a…"},
    {"name": "Store.save", "kind": "method", "change": "added", "lines": [8, 0], "body": "41be07…"}],
   "other": {"imports": [1, 1]}},
  {"path": "docs/usage.md", "status": "modified", "lang": "markdown", "lines": [2, 1],
   "symbols": [{"name": "Usage > Install", "kind": "section", "change": "modified", "lines": [2, 1], "body": "c3d9…"}]},
  {"path": "assets/logo.png", "status": "new"}],
 "skipped": [{"path": "legacy.py", "why": "SyntaxError: line 12"}]}
```

`lines` is `[added, removed]`: the file's total (the same as `numstat`) and, per symbol and
bucket, its share — here 3 + 8 + 1 = 12 and 1 + 0 + 1 = 2. A version 1 trace ignores the file
(it reads only `NNN-TNNN.patch`).

Severity: exact findings (recorded or parsed) may be `pending`; inferred ones are `warning`
only; nothing claims "no impact" — `packet` lists "not analysed".

Installed layout:

```
.spectrace/
  trace.py            launcher (the same command as today)
  spectrace/          package: model, gitio, state, patches, commands, cli, symbols/, index, views/
  format.md
  changes/            NNN-TNNN.patch + NNN-TNNN.touch.json        (committed)
  fingerprints.json   keeps.json                                  (committed)
  index.db  state.json  __pycache__/                              (ignored)
```

Invariants of the whole: one command and one vocabulary (R/D/A, task, symbol); one format,
only extended (version 1 stays valid); one install and upgrade unit; one agent loop
(`status → start → done → check`, no new mandatory step — recording is automatic); one
criterion of truth (exact gates, inferred warns); one suite and one e2e; still no tags in code
and no orchestrator.

## What changes in each existing piece

| Piece | Before | After |
|---|---|---|
| `trace.py` | one 896-line file | launcher + `spectrace/` package; same commands and output |
| `trace impact` | tasks → files → lines present (by text) | + symbols; keeps `file_presence`; accepts `path::symbol` |
| `trace check` | suspect, changed, uncovered, orphan, mentions of deleted files | + `leftover`, accounting, outside-the-task symbols, mentions of removed symbols |
| `format.md` | format version 1 | version 2: the record, code addresses, `kind: fix`; example tests keep it honest (A4) |
| `spectrace-start` | copies `trace.py`; interview | copies the package; asks about existing code and languages |
| `spectrace-plan` | design and tasks | + `locate` to anchor tasks in existing code |
| `spectrace-change` | `impact` + a `git blame` sweep by hand | manifest with symbols and `why`; `check` verifies the cleanup |
| `agents-protocol.md` | status/start/done/check | + one line: find code before editing (`why`, `locate`) |
| `references/upgrade.md` | trace.py + format.md + protocol + sections | + the package as one unit |
| `tests/test_skills.py` | one 900-line cap | one budget per module |
| e2e (006) | JSON → SQLite → JSON | + records, `why`, cleanup check, `spectrace-fix` |

## Decisions: pros, cons, mitigation

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Package and launcher (not one file, not a zipapp) | readable modules; same command; installing is still a copy | a folder to copy | one unit with `VERSION`; upgrade replaces the whole folder |
| Record symbols at `done` (not derive from patches) | exact; independent of the 200 KB limit | a new ledger file; only from now on | anchored fallback for older tasks, labelled; version 1 ignores it |
| One CLI (not a separate `graph.py`) | one vocabulary; no version skew; one `impact` and one `check` | `trace.py` gains commands | one view per module; version 1 output unchanged by default |
| `sqlite3` index (not JSON) | atomic; indexed queries; no reload per call | opaque binary; module may be missing in minimal Pythons | disposable cache with `--dump`; `why` and `check` do not need it |
| Only exact findings gate | no false blocking | inferred findings stop nothing | `packet` shows them with confidence and "not analysed" |
| Python and Markdown in the core; others via measured adapters | precision before coverage; no dependencies | JS/TS stay at file level for now | entry criteria below; tree-sitter or SCIP only as optional providers (`scip-python` needs Node 16+ and Python 3.10+) |
| A fourth skill, `spectrace-fix` | fixes enter the ledger instead of landing outside any task | more surface | at most 200 lines; hands over to `spectrace-change` |

## The specs

Each leaves the project whole and `check --strict` at 0 when it closes.

| Spec | What | Size | Gate |
|---|---|---|---|
| 011 modular-core | the trace becomes a package; same behavior | M, 11 tasks | `tests/test_trace.py` unchanged and green; outputs identical to the previous version on this repo; install and upgrade checked |
| 012 change-records | the record, `why`, symbols in `impact`, `leftover`/`keep`, accounting, anchored fallback, outside-the-task symbols; `VERSION` 2 | L, 19 tasks | accounting at 100% over this repo's consecutive commits; at least 98% of Python code lines in a named symbol; a version 1 repo still works; `why` right on five symbols |
| 013 code-index | the derived index; dependents, dependencies, tests; coverage; recall and precision report | L, 12 tasks | incremental refresh re-reads only the changed file; numbers reported, no threshold until there is a baseline |
| 014 locate-packet-fix | `locate`, `packet`, `spectrace-fix`, skills and README, CI recipe | L, 13 tasks | at least 20 golden queries compared with `rg`; packet deterministic; `--diff --base` on a clean clone |
| 015 e2e-graph | the 006 scenario extended: records, `why`, cleanup check, find-and-fix | M, 5 tasks | passes under Claude Code and a second harness |

## After 015 — entry criteria

| Spec | What | Enters when |
|---|---|---|
| ts-adapter | symbols and imports for TS/JS; spike among regex, optional tree-sitter, the compiler API and SCIP | 012–014 used for at least two weeks on a real project with TS; exactness gate on a labelled sample |
| contracts | `contract` nodes derived from OpenAPI or JSON Schema, not from a hand-kept JSON; drift by schema comparison | a project with a schema file (for example one generated by drf-spectacular) |
| workspace | multi-repo first as a read-only map (a manifest of repos, each with its own `.spectrace`); one task per repo, linked by a contract | contracts in use |

## Risks

| Risk | Mitigation |
|---|---|
| Regression in the refactor | `tests/test_trace.py` untouched and green, plus output equivalence against the previous version |
| The record breaks `done` | try/except, caps, `skipped` with the reason; tests with invalid syntax, binaries and huge tasks |
| Symbol churn (renames, moves) | `renamed_from` by identical body; unchanged / changed / gone; `follow()` for files |
| Syntax newer than the running Python (A2: 3.9) | `skipped` with the reason; `packet` shows it as not analysed |
| `leftover` false positives | only with an identical body; `keep` with a written reason |
| Skill size (`spectrace-start` is at 164 of 200 lines) | detail goes to `references/` |
| Scope | a gate per spec; later specs only with entry criteria |
| Windows and CRLF | POSIX paths, UTF-8; CI already runs on Windows and Python 3.9 |

## Verification

- Per task, the narrowest test command; the full suite when each spec closes, and
  `python skills/spectrace-start/assets/trace.py check` at 0 (`AGENTS.md`).
- Tests stay proportional (spec 009; tripwire 3× the R items).
- 011: output equivalence between the previous and the new `trace.py` on this repo; install into
  a temporary repo and upgrade a single-file install.
- 012: the recorder against a real `git diff` on a fixture; a version-1 repo; the cost of `done`.
- 013–014: incremental refresh; the recall and precision report; golden queries against `rg`;
  packet determinism.
- 015: the extended e2e under two harnesses, as in spec 006.

## Relation to the first draft

| First draft | Here |
|---|---|
| 011 graph-core | 011 + 012 + 013 |
| 012 graph-queries | 012 + 013 + 014 |
| 013 ts-adapter | after 015, with entry criteria |
| 014 workspace-trace | after 015, as a read-only map first |
| 015 contracts | after 015, derived from OpenAPI or JSON Schema |
| `graph.py`, `graph.json` | commands of `trace.py`; `index.db` (derived) and `touch.json` (ledger) |
| skill `spectrace-graph` | `spectrace-fix` |
