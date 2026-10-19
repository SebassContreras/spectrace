# Product

## What this is

spectrace turns a natural-language interview into specs — requirements, design,
tasks — where every decision has an ID and a revision, and it records exactly what
each task changed, down to the symbols it touched. When a decision changes, it lists
what implemented the old one (tasks, files, symbols, lines, tests) and won't let the
spec read as done until that is removed or redone. Asked about a piece of code, it
names the decision behind it and what depends on it. Any agent can execute the tasks;
there is no orchestrator.

## Who uses it

Developers working with AI coding agents (any harness that reads Agent Skills and
`AGENTS.md`) on projects where direction changes and old decisions must not leave
dead code, stale docs or obsolete tests behind.

## Current MVP scope

What must work today:

- The interview writes specs (requirements, design, tasks) with IDs and revisions.
- `trace.py` keeps the ledger: `status`, `start`, `done`, `block`, `check`, `impact`.
- A change of direction lists exactly what to remove or redo (`spectrace-change`).
- Installing and upgrading `.spectrace/` in a target repo.
- Next, in order: the code map's first step — symbols recorded at `done`, and `why` and
  `impact` down to the symbol (specs 011–012).

## Not for now

- Task orchestration: no loop, no parallel dispatch, no worker configuration.
- Dashboards and status pages: `trace status` and the roadmap table are the view.
- Per-harness adapters.
- Tags inside source code: the trace links decisions to code through each task's
  recorded diff.
- Semantic (LLM) drift detection; mutation testing.

## Scope filter

Is it needed for the MVP to work? Yes: it goes in by the simplest route, adjusting earlier
decisions if they are in the way. No: it is dropped or postponed, without debate.

When an earlier decision (architecture or design) gets in the way of the current spec, do
not build a workaround. Propose changing it directly: "this decision forces
over-engineering; I propose X, which is direct. Approved?" The user chooses to keep it,
edit it or retire it, and the change goes through `spectrace-change`.
