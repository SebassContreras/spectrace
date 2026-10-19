# Handoff — 2026-10-19

Where the work on specs 011–016 stands, what is verified, and what is left. Read this,
then `python skills/spectrace-start/assets/trace.py status` and `check`.

## Done and verified

Pushed to `origin/main` (`9a044d9..5c25589`), one commit per spec, each commit passing
the full suite on its own:

| Commit | Spec | What |
|---|---|---|
| `28e4e7d` | 011 | `trace.py` is a launcher; the code is the `spectrace/` package (model, gitio, state, patches, commands, cli). Same output as before on 10 commands; install and upgrade copy the package as one unit. |
| `0eff69c` | 016 | `block "conflicts <ref>: <why>"` and its pending state; record guard (an A item, or a built-on item, cannot change or disappear without a `changes.md` entry); `spectrace-change` Phase 0b; protocol paragraph "When a decision is in the way"; `product.md` MVP sections. |
| `fa79ea6` | 012 | Change records by symbol (`NNN-TNNN.touch.json`), `trace why`, symbols in `impact`, `leftover` + `trace keep`, anchored fallback, format version 2. History check: 13 commit pairs, 0 unaccounted, 98.5% of Python code lines in a named symbol. |
| `4eac7ee` | 013 | `sqlite3` code index, `trace index [--status]`, `impact path::symbol` with `--direction`, `--depth`, `--deep`, removed-symbol mention warnings, `tests/eval_index.py`. Resolution 99.7%; eval recall 0/8 (documented: the history pairs `trace.py` with a test that loads it by `importlib`). |
| `c43017e` | 014 | `trace locate` (21/21 golden queries in the top 5), `trace packet` (task or `--diff`, in memory on CI, severity signals), skill `spectrace-fix`, README code map and CI recipe, packet step in `ci.yml`. |
| `f900233` | 015 | `e2e/scenario.md`: Records, Why, Leftover checks and Step 7 "Find and fix". |
| `5c25589` | — | Planning audit of 011–016 (principles 1–10), trade-offs added, 011/D5@2 and 013/D1@2, and the 016/T010 `spectrace-change` session (002/R4@2, 002/D4@2, 010/R4@2, 010/D5@2, 010/D7@2; 007/D2, D3 reworded). |

Measurements and comparisons: `planning/verification-2026-10-19.md`.

## In progress: the e2e run of spec 015

### Claude Code (015/T003) — stopped at step 5, task blocked

`015/T003` is **blocked** with `conflicts 012/D6` (shows as a pending decision conflict in
`trace check`). Throwaway repo: `%TEMP%/spectrace-e2e/claude-code/` (not committed after
step 2, as the scenario says).

| Step | Result |
|---|---|
| 0 Set up | pass — published skills installed (4 skills, `spectrace/` package) |
| 1 Interview | pass — ~40 turns; 3 gaps answered consistently (see notes) |
| 2 Plan | pass — D1–D3, T001–T011 |
| 3 Three tasks | pass — EXACT patches, records add up, `check --strict` 0 |
| 4 Retire JSON | pass after an extra `spectrace-change` conversation (gap): strict 1 → 0, no JSON left, SQLite present, `why` newest first, tdo tests OK |
| 5 Reinstate JSON | **fail** — 7 pending: 6 false `leftover`, T012 `suspect` (defects 1 and 2 below) |
| 6 Wording/meaning | not run |
| 7 Find and fix | not run |

Snapshot before step 5: `pre-reinstate f7e78fad6f7e86b4282a773128c0fc91fe5411ac`
(all snapshots in `planning/e2e-driver/snaps-claude-code.txt`).

### agy (015/T004) and the summary table (015/T005)

Not started; both blocked until the Claude Code run passes.

## Defects the e2e found (to fix before repeating step 5)

1. **False `leftover` on reinstate** (012/D6@1, my code in `spectrace/leftover.py`):
   restored or rebuilt code identical to a retired task's is reported as leftover.
   Proposed **012/D6@2**: a symbol is not a leftover when a task done after the cleanup
   recorded it again (added, modified or renamed). **Needs the maintainer's yes**
   (`spectrace-change` on 012/D6), then a regression test task and a fix task.
2. **Restored task stays `suspect`**: the task that runs `trace restore NNN/TNNN` does
   not `retires:` it. Fix the Reinstate paragraph of `skills/spectrace-change/SKILL.md`
   (the restore task also `retires:` the task it undoes). 004/D7@1 still holds — no
   bump. Add a regression test in `tests/test_trace.py`.

## Findings that do not block (decide: now or a later spec)

- `next` ignores cleanup priority: after a change, agents built `list_tasks`/`complete`
  on the JSON helpers that a later cleanup removed (code broken until an extra change).
- A dangling same-file reference to a removed symbol only **warns**, and `_read`
  (bare, 5 chars < `MIN_BARE` 6) is not even searched; an exact dangling reference
  could be pending.
- The default A1–A5 principles template is written in Spanish (skills are English, A7).
- `__pycache__/*.pyc` are recorded as task changes in a repo with no `.gitignore`.
- Minor: the harness first wrote task lines without `[status:todo]`; `check` caught it.

Full notes: `planning/e2e-driver/e2e-notes.txt`.

## How to resume

1. Answer the 012/D6 question (edit as proposed, keep, or retire).
2. Run `spectrace-change` for 012/D6, add the fix tasks (regression test first, then
   `kind: fix`) for defects 1 and 2, execute them through the protocol, full suite,
   `trace check` exit 0; commit and push (no co-author trailer).
3. In the throwaway repo, update `.spectrace/` from the bundled assets (`spectrace-start`
   upgrade path) or reinstall the skills, then reset it to `pre-reinstate`:
   `git checkout f7e78fa -- . && git clean -fd -e .spectrace/state.json`, and set
   `refs/spectrace/last` to the tree of the last closed task. Log this in the report.
4. Resume `015/T003` (`trace start 015/T003`) and repeat steps 5–7 with the driver:
   `planning/e2e-driver/say.sh claude <log> <session|new> "<answer>"` for one turn,
   `exec_task.sh claude <label>` for an "Execute the next spectrace task" conversation
   (snapshots + EXACT/record checks). Answers come from `e2e/scenario.md`.
5. Write the Claude Code results into `e2e/report.md`, `trace done 015/T003`.
6. Same run under agy (015/T004, repo `%TEMP%/spectrace-e2e/agy/`; verify how agy
   exposes the conversation id first), then the "Code map" table (015/T005).
7. Decide the non-blocking findings (fix now or open a spec).

## Not committed

This file and `planning/e2e-driver/` (driver scripts, notes, snapshots) are uncommitted.
