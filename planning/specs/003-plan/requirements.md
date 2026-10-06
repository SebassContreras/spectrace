# 003 — plan — Requirements

## What's being built

The `spectrace-plan` skill: closes a spec's design and breaks it into tasks, in one flow.
Merges specloop's `design-closing` and `task-breakdown` (and `advance` Phases 1–2).

## Who it serves

A spec whose `requirements.md` has R items; the agent that later executes its tasks.

## Requirements

- R1@1: The design is written as D items, each naming the R items it implements; project-wide decisions settled on the way are appended to `architecture.md` as A items.
- R2@1: The design can be closed through a one-question-at-a-time Q&A or drafted from the requirements and interview for approval.
- R3@1: Tasks are single-action and verifiable, each with `covers:`; every R item that states an acceptance check gets a `kind: test` task covering it; owners are `agent` or `human`.
- R4@1: The task list is confirmed with the user before it is written.
- R5@1: It does not finish while `trace check` reports an uncovered R or D in the spec, and it ends with `trace status --write`.
- R6@1: A task that sets up or directly embodies a project-wide decision also covers its A item, so changing that decision reaches the task.

## Out of scope

- Executing tasks.
- Changing an already-closed design (004).

## Dependencies

001, 002.

## Owner split

All agent.
