# 014 — locate-packet-fix — Requirements

## What's being built

The three ways people and agents use the code map day to day: finding code from a free-text
request (`trace locate`), a review packet for a task or a diff (`trace packet`), and a skill,
`spectrace-fix`, that takes a bug report to a traced task. The existing skills and the agent
protocol use the new commands where they replace manual steps, and the README documents a CI
recipe.

## Who it serves

Developers and agents working on code that already has specs: a bug report, a small
correction, a review in a pull request.

## Requirements

- R1@1: `trace locate "<text>"` ranks the decisions, tasks, files and symbols that match a free-text request, and says why each one matched.
- R2@1: `trace packet <task>` and `trace packet --diff [--base <ref>]` render a review packet — decisions, symbols, dependents, tests, incidents, severity signals and what was not analysed — deterministically, as Markdown or `--json`.
- R3@1: The skill `spectrace-fix` takes a bug report to a traced task under the decision it violates, or hands over to `spectrace-change` when the decision is wrong or missing.
- R4@1: The existing skills and the agent protocol use `locate`, `why` and `impact` where they replace manual steps.
- R5@1: `README.md` documents a CI recipe — `trace check --strict` and `trace packet --diff` — and the limits of the code map.
- R6@1: `trace packet --diff --base <ref>` works on a clean CI checkout, with no `state.json` and no index file.

## Out of scope

- Semantic (LLM) search: `locate` is lexical, and the agent rephrases.
- Languages without an adapter (A13@1).
- Posting the packet anywhere: the recipe pipes it to the CI job summary; the trace sends nothing.

## Dependencies

012, 013.

## Owner split

All agent.
