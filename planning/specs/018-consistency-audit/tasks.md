# 018 — consistency-audit — Tasks

- [x] T001 [agent] [status:done] Create `spectrace/audit.py` with pure audit check functions (`check_architecture_alignment`, `check_scope_alignment`, `check_interview_alignment`, `run_audit`)
      covers: D1@1, D2@1, D3@1, D4@1, R1@1, R2@1, R3@1, R4@1
      changes: skills/spectrace-start/assets/spectrace/audit.py (+159 -0)
- [x] T002 [agent] [status:done] Integrate `cmd_audit` and `trace check --audit` into `commands.py` and `cli.py`
      covers: D1@1, D5@1, R1@1, R5@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+24 -1)
- [x] T003 [agent] [status:done] Add unit and integration tests in `tests/test_audit.py` covering all audit checks, `--json`, and `--strict`
      covers: D1@1, D2@1, D3@1, D4@1, D5@1, R1@1, R2@1, R3@1, R4@1, R5@1
      kind: test
      changes: tests/test_audit.py (+124 -0)
- [x] T004 [agent] [status:done] Document `trace audit` and `trace check --audit` in `skills/spectrace-start/assets/format.md`
      covers: D1@1, R1@1
      changes: skills/spectrace-start/assets/format.md (+4 -0)
- [x] T005 [agent] [status:done] Verify module line budgets (A5 cap: 600 lines), run full test suite with `uv run pytest tests -q`, and verify `trace check`
      covers: D1@1, R1@1, R5@1
      kind: test
      changes: none
