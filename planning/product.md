# Product

## What this is

spectrace turns a natural-language interview into specs — requirements, design,
tasks — where every decision has an ID and a revision, and it records exactly what
each task changed. When a decision changes, it lists what implemented the old one
(tasks, files, lines, tests) and won't let the spec read as done until that is
removed or redone. Any agent can execute the tasks; there is no orchestrator.

## Who uses it

Developers working with AI coding agents (any harness that reads Agent Skills and
`AGENTS.md`) on projects where direction changes and old decisions must not leave
dead code, stale docs or obsolete tests behind.

## Out of scope

- Task orchestration: no loop, no parallel dispatch, no worker configuration.
- Dashboards and status pages: `trace status` and the roadmap table are the view.
- Per-harness adapters.
- Tags inside source code: the trace links decisions to code through each task's
  recorded diff.
- Semantic (LLM) drift detection; mutation testing.
