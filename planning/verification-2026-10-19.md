# Verification — 2026-10-19 (audit of specs 011–016 and `graph-plan.md`)

Audited against the ten engineering principles. Applied, with no revision bump (the items are unbuilt):

- 014 D4 and 015 D2: a `kind: fix` task is always preceded by a `kind: test` regression task.
- "Trade-offs context" added to the designs of 011, 012, 013 and 014.
- One module per view in `views/` (012, 013, 014 Deliverables and `graph-plan.md`).
- 012 D1/D5 reuse the `patches.py` hunk parser (`parse_patch` minimum length becomes a parameter).
- 013/T012 is no longer `kind: test`.

Checks: `python -m pytest tests -q` → 29 passed, 12 subtests; `trace.py check` exit 0 (2 pending, 1 warning); `check --strict` exit 1 (011/T006 cleanup of 001/T009 not done). No linter configured.

## Pending for the next session

- Execute 011 first (`trace.py status` → `next: 011/T001`), then 016, 012, 013, 014, 015.
- 011/T006 retires 001/T009 (clears the suspect and the strict failure).
- Human: 016/T010 `spectrace-change` session for 002/R4, 002/D4, 010/R4, 010/D5, 010/D7 and the wording of 007/D2, D3.
- Not pushed: `AGENTS.md` says no push until the maintainer asks.

## 012/T019 — recorder over this repo's history (2026-10-19)

- 13 consecutive commit pairs (root included): every record adds up (0 unaccounted, totals equal `git diff --numstat`), nothing skipped.
- Python code lines (added, non-blank, not comments or imports): 1180 of 1198 inside a named symbol, 98.5%.
- `trace why` checked on `commands.py::cmd_done`, `model.py::Repo.record_guard`, `records.py::record`, `state.py::ensure_ignores`, `patches.py::parse_patch`: each lists the tasks that wrote it (exact for tasks after 012/T007, `anchored` before).
- Slowest single record: 0.93 s (the root commit).

## 014/T006 — `locate` against `rg` (2026-10-19)

`python tests/test_locate.py --compare`: 21 golden queries (16 over this repo, 5 over a fixture).
`locate` ranks the expected code in the top 5 for 21/21 (rank 1 for 12). `rg -i -l` with the
query words lists 22–95 files per query on this repo (it has the file in 15/16) and finds
nothing for "sesiones expiradas" against "La sesión expira" (no accent folding, no plurals).
