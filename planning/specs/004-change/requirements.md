# 004 — change — Requirements

## What's being built

The `spectrace-change` skill: the only way to change a decision once it exists. Replaces
specloop's `amend` and `fix`.

## Who it serves

Anyone who changed their mind, or found the approach was wrong, after requirements,
design or code already exist.

## Requirements

- R1@1: From a natural-language description of what changed, it identifies the affected R, D and A items and, after confirmation, revises them (revision bump), retires them (struck through, dated, with a replacement) or adds new ones.
- R2@1: Every change is recorded in the spec's `changes.md` as ADDED / MODIFIED / REMOVED with the reason.
- R3@1: It runs `trace impact` on every revised or retired item and shows the result as the retirement manifest: tasks, files, lines still present, tests.
- R4@1: Each affected finished task is classified with the user: still valid (re-point `covers:` to the new revision), redo (default: a task that `retires:` it plus a new one), or refactor in place (only with a written justification in `changes.md`). A test covering a retired requirement gets a task that deletes it.
- R5@1: The spec cannot read as done until every suspect task is resolved; it ends with `trace status --write`.
- R6@1: It refuses while a task is open.
- R7@1: Beyond the trace, every other mention of the old decision — docs, comments, config, spec context — is found by a search for its terms and, case by case, updated, removed or kept as history.
- R8@1: A retired decision can be reinstated: it comes back as a new item, and the work that removed it is undone with `trace restore` where it still applies, redone where it doesn't.
- R9@1: A wording-only edit to an item is confirmed with `trace review` and recorded as such, instead of a revision bump.

## Out of scope

- Logging corrections outside a spec (specloop's `fix`): a correction is a change to a spec.

## Dependencies

001, 003.

## Owner split

All agent; every edit is confirmed by the user first.
