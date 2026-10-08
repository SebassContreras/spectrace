# 007 — agent-loop-and-workflow-optimization — Design

## Approach

- D1@1 (implements R1, R4): Update `skills/spectrace-start/assets/agents-protocol.md` and repository `AGENTS.md` to document the multi-task loop: iterate steps 1–5 for each task, never edit files without an open task, close with `done` before moving to the next task or spec, and run step 6 (`trace check`) only once at the conclusion of the session.
- D2@1 (implements R2): In `trace.py`'s `cmd_start`, inspect `task.covers` against `repo.resolve(raw, task.spec)`; for each resolved item, print its reference and text so agents immediately receive the exact specification without opening full requirement/design files.
- D3@1 (implements R3): In `trace.py`'s `cmd_done`, re-load/re-check `repo.next_task()` and print the next task prompt (`next: <ref> <text> -> run: trace start <ref>`), keeping agents on track in multi-task scenarios.
- D4@1 (implements R5): In `skills/spectrace-plan/SKILL.md` (and related references), add guidance for browser and UI verification tasks: prefer executable headless tests (`kind: test`, owner `[agent]`), and reserve `[human]` for manual visual acceptance or credentialed access.

## Deliverables

- `skills/spectrace-start/assets/agents-protocol.md`
- `AGENTS.md`
- `skills/spectrace-start/assets/trace.py`
- `skills/spectrace-plan/SKILL.md`
- `tests/test_trace.py`
- `tests/test_skills.py`

## Sequencing

1. Update `trace.py` for start/done output enhancements.
2. Update unit tests in `test_trace.py` and verify size budget (`test_skills.py`).
3. Update `agents-protocol.md` and `AGENTS.md`.
4. Update `spectrace-plan/SKILL.md`.
