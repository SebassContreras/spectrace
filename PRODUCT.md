# Product

> Owns: why the project exists, who it serves and what it does today · Not here: status or order of work (planning/roadmap.md), technical choices (ARCHITECTURE.md), standards (ENGINEERING.md)

## Vision

One agent skill that scaffolds the contracts, playbooks and guard a project needs, so coding agents decide well and cannot skip the rules that must always hold. It works with Claude Code and Antigravity, for software and non-software projects.

## Users and the problem

- **A developer starting a project with coding agents.** Every new project means rewriting the same rules (principles, tests, specs, way of working), and the agent forgets or skips them.
- **The same developer, mid-project.** Written rules are advisory text. The ones that must always hold, such as never adding Claude as co-author, need a hook or a CI check behind them.

## Capabilities

- Scaffolds eight single-responsibility contracts, an `AGENTS.md` router, a roadmap and three playbooks (plan, change, review) into any project.
- Fits the contracts to the project by reading the repository, and writes only what the repository cannot show.
- Blocks Claude attribution in commits and pull requests, `--no-verify`, force-push to `main` and staging `.env` files, from Claude Code and Antigravity hooks.
- Lints specs and the roadmap: every requirement is covered by a task and by a `[test]` task, every checked task carries evidence, and the roadmap matches the specs.
- Runs the same checks in CI, the one layer an agent cannot skip.
