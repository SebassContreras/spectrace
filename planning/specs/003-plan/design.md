# 003 — plan — Design

## Approach

- D1@1 (implements R1, R2): Design phase ported from specloop `design-closing` (five questions: approach, deliverables, sequencing, decisions settled, open questions) with a draft alternative using `spectrace-start`'s marking rules; each design statement is a D item naming the R items it implements; project-wide decisions are appended to `architecture.md` as A items, with the operative line in `AGENTS.md`.
- D2@1 (implements R5): Design gate — `trace check` shows no `uncovered` R for the spec before tasks are drafted.
- D3@1 (implements R3, R4): Task phase ported from specloop `task-breakdown`: single-action, verifiable tasks with owner and `covers:`, a `kind: test` task for each R that states a checkable outcome, the full list confirmed before writing.
- D4@1 (implements R5): Task gate — `trace check` shows no `uncovered` D; the skill ends with `trace status --write`.
- D5@1 (implements R6): Task-phase rule: a task that installs, configures or encodes an A item (a runtime, a framework, a convention enforced in code) lists that A item in `covers:` too.

## Deliverables

- `skills/spectrace-plan/SKILL.md`
