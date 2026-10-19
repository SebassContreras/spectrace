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
