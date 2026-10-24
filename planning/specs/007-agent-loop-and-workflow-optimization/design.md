# 007 — agent-loop-and-workflow-optimization — Design

## Approach

- D1@2 (implements R1, R4): Update `skills/spectrace-start/assets/agents-protocol.md`, `skills/spectrace-start/references/templates.md`, and repository `AGENTS.md` to document repository sync (`git pull` / `git status`) before querying next tasks/status, the multi-task loop (steps 1–5), no edits without an open task, closing with `done`, and running step 6 (`trace check`) once at the end of the session.
- D2@1 (implements R2): In the `start` handler, inspect `task.covers` against `repo.resolve(raw, task.spec)`; for each resolved item, print its reference and text so agents immediately receive the exact specification without opening full requirement/design files.
- D3@1 (implements R3): In the `done` handler, re-load/re-check `repo.next_task()` and print the next task prompt (`next: <ref> <text> -> run: trace start <ref>`), keeping agents on track in multi-task scenarios.
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
