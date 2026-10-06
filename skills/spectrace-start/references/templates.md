# File templates

The shapes of the files `spectrace-start` writes. Item, task and roadmap grammar is defined in
`.spectrace/format.md` — not here. Write content only from the ledger; anything not
yet answered stays `TBD`.

## `AGENTS.md`

```markdown
# <project>

<one-line goal> For: <audience>. Type: <project-type>.

## Doc map

- `planning/product.md` — what this is, who it's for, out of scope.
- `planning/architecture.md` — project-wide decisions (A items).
- `planning/styles.md` — style detail (if present).
- `planning/roadmap.md` — specs, order, status.
- `planning/specs/NNN-name/` — requirements (R), design (D), tasks, changes.
- `.spectrace/format.md` — how all of the above is written.

## Stack & conventions

<short operative form of each A item: "Node 22 (A1)">

## Style

<operative summary from Phase D; hard rules marked as such; points to planning/styles.md>

## Rules for agents

<agent-rules answers>

<protocol block from assets/agents-protocol.md>
```

`AGENTS.md` is the only instructions file. Never create `CLAUDE.md`. If the repo
already has an `AGENTS.md`, add the sections that are missing and the protocol block;
change nothing else without asking.

## `planning/product.md`

```markdown
# Product

## What this is

## Who uses it

## Out of scope
```

## `planning/architecture.md`

```markdown
# Architecture

Project-wide decisions. Grammar: `.spectrace/format.md`.

## <type-keyed headers>

## Still to define
```

Headers by `project-type` (only the category picks the set):

| Type | Headers |
|---|---|
| software | `Container`, `Stack`, `Conventions` |
| marketing/content | `Channels`, `Tools`, `Data sources` |
| operations/process | `Systems`, `Cadence`, `Handoffs` |
| research | `Sources`, `Method`, `Output` |
| other / skipped | `Tools`, `Inputs/Outputs` |

Each decision is an A item under the header it belongs to:
`- A3@1: PostgreSQL 16 — why: relational data, team knows it.`
An undecided dimension is a bullet under `Still to define`, never an invented A item.

## `planning/roadmap.md`

```markdown
# Roadmap

Index of every spec. `Status` and `Stage` are written only by `trace`. Grammar:
`.spectrace/format.md`.

| ID  | Spec | Status | Depends on | Stage | Priority |
|-----|------|--------|------------|-------|----------|
```

Nothing else goes in this file — no history, no prose ordering.

## `planning/specs/NNN-name/requirements.md`

```markdown
# NNN — name — Requirements

## What's being built

## Who it serves

## Requirements

- R1@1: <one checkable statement>

## Out of scope

## Dependencies

## Owner split
```

Every R item is observably checkable: someone could tell, by looking or running
something, whether it holds. A hard constraint is an R item too. `## Dependencies` is
written even when the answer is "None."

## `planning/specs/NNN-name/design.md` and `tasks.md` (stubs)

```markdown
# NNN — name — Design

TBD — closed by the `spectrace-plan` skill.
```

```markdown
# NNN — name — Tasks

TBD — written by the `spectrace-plan` skill.
```

## `.spectrace/interview.md`

```markdown
# Interview ledger

| dimension | status | answer |
|-----------|--------|--------|
| idea-detail | open | |
```

One row per question-bank dimension, in phase order; per-spec rows prefixed with the
spec ID (`002.requirements`). Write the user's own words in `answer`, not a paraphrase.
