---
name: spectrace-plan
description: >-
  Closes a spectrace spec's design and breaks it into tasks in one flow: design
  decisions become D items that name the requirements (R items) they implement,
  project-wide decisions become A items, and every task declares what it covers, so
  later changes can be traced to the code each task produced. Use when a spec has
  requirements but no design or no tasks yet: "plan spec 002", "design and break down
  the auth spec", "close the design for X", "make the tasks for NNN", "planifica la
  spec 003", "arma las tareas". Requires the spectrace-start skill to have run (.spectrace/).
---

# spectrace-plan

Run **inside the target repo**. Grammar of items and tasks: `.spectrace/format.md` —
read it first; never restate it to the user from memory. Run the trace with `python3`
(`python` on Windows): `python3 .spectrace/trace.py <command>`.

## Phase 0 — Pick the spec, refuse if not ready

1. The user named a spec → use it. Otherwise run `trace status` and ask which spec at
   stage `design` or `tasks` to plan.
2. **Refuse** if `.spectrace/trace.py` is missing (point to the `spectrace-start` skill), or the
   spec's `requirements.md` has no active R item (point to `spectrace-start`, which writes or
   drafts them).
3. **Refuse** if the spec already has D items *and* tasks: changing a closed design or
   an existing task list is the `spectrace-change` skill's job.
4. Read `requirements.md`, `planning/product.md` (project type), `planning/architecture.md`,
   `AGENTS.md`, and `.spectrace/interview.md` if present. The design must stay
   consistent with existing A items.

## Phase 1 — Design (skip if the spec already has D items)

Ask once: close the design here, one question at a time, or have it **drafted** for
approval. Draft mode uses the same rules as `spectrace-start`'s draft mode: every line the user
didn't give is marked `_(standard: <name> — <url>)_` or `_(judgement, no standard)_`,
the full draft is shown for yes / changes / defer, and only a fact the user alone knows
is asked live.

Q&A mode — one at a time, phrased for the project type, writing `design.md` after
each answer:

1. **Approach** — "How should this get built, in plain terms?"
2. **Deliverables** — "What does this create or change?" (files/modules; assets/pages;
   runbook steps; datasets/analyses).
3. **Sequencing** — "Does anything here have to happen in a specific order, or need
   something from another spec the roadmap doesn't record?"
4. **Decisions settled** — "Does this settle any stack, tooling or convention question
   not recorded yet?"
5. **Open questions** — "Anything genuinely undecided that should be flagged rather
   than guessed?"

Write `design.md` as:

```markdown
# NNN — name — Design

## Approach

- D1@1 (implements R1, R3): <one decision>

## Deliverables

## Sequencing

## Open questions
```

- Each D item is **one** decision and names the R items it serves. Deliverables,
  sequencing and open questions are context, not items. Omit an empty section.
- A project-wide decision (answer 4) is appended to `planning/architecture.md` as the
  next A item under its header, with its operative line in `AGENTS.md` → "Stack &
  conventions". Append only: if it contradicts an existing A item, stop and point to
  the `spectrace-change` skill.
- Never invent a decision the user didn't make — it goes under "Open questions".

## Phase 2 — Design gate

1. Run `trace check`. For each `uncovered: NNN/Rn` in this spec, ask how the design
   addresses it — a new D item, or a task that covers the R directly — until none is
   left. Fix any `error` in the files this skill wrote.
2. Ask once: **"What haven't we covered in this design?"** Address anything new, then
   ask again; stop when a pass returns nothing.

## Phase 3 — Tasks

Draft a numbered list from `requirements.md` and `design.md`:

- **Single-action** (one file, function, asset, decision or config change — not
  "implement the feature") and **verifiable** (an unambiguous way to tell it's done).
  Phrase it for the project type.
- Each task's `covers:` names the D (or R) items it implements. Every task traces to
  something written in the spec — never invent scope.
- A task that installs, configures or encodes a project-wide decision (an A item: the
  runtime, a framework, a convention enforced in code) lists that A item in `covers:`
  too — otherwise changing the decision later can't find the task.
- Every R item that states a checkable outcome gets a `kind: test` task covering it:
  the executable form of the spec's definition of done.
- Owner: `human` for anything needing a credential, an approval, a purchase, a physical
  act or a live session; `agent` otherwise. Use the ledger's `owner-split` and
  `automatability` answers; ask when unsure.
- Order follows the design's sequencing.

Show the list (ID, owner, text, covers) in one message. Ask the user to approve or
add / remove / reorder, then ask once: **"Anything in this design that no task
covers?"** Write nothing before confirmation.

Then write `tasks.md` in the format's task grammar, every task `[status:todo]`, IDs
`T001`, `T002`, …, task lines at column 0, fields indented six spaces.

## Phase 4 — Task gate, report, stop

1. Run `trace status --write`, then `trace check`. No `uncovered` D may remain in this
   spec and no `error` in the files this skill wrote; fix and re-check.
2. Report: the spec is at stage `build`; list its `[human]` tasks — they are the
   user's. Any agent can now execute the rest by following the protocol in
   `AGENTS.md` (or the user can just say "execute the specs").
3. **Stop.** Never start executing a task here.

## Style

- Terse and structural; the user's language in conversation, the project's in files.
- One question at a time, always waiting for the reply.
- Never edit `Status`/`Stage`, a task's status or a `changes:` line — the trace owns them.
