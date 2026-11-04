# Architecture

> Owns: the layers, the allowed direction of dependencies and the boundaries · Not here: how code is written (ENGINEERING.md), procedures (OPERATIONS.md), history (CHANGES.md); no file listings, they go stale

## Layers

- **Skill** (`skills/spectrace/SKILL.md`): the procedure an agent follows to scaffold or update a project. Depends on the assets only.
- **Assets** (`skills/spectrace/assets/`): files copied verbatim into a target repository, in `contracts/`, `playbooks/`, `planning/`, `adapters/` and `guard/`. At runtime they depend on nothing except the guard script.
- **Guard** (`assets/guard/guard.mjs`): pure rule functions (shell parsing, command rules, spec lint, roadmap, contracts) behind a thin CLI, plus one translator per agent. No dependencies.
- **Tests** (`tests/`): run the guard and inspect the assets. Nothing depends on them.

## Boundaries

- A target repository receives copies. After init the skill does not link back, so the project owns what it was given and `update` shows a diff.
- Claude Code and Antigravity reach the guard through their own hook files; git and CI call the same script.
- Facts the design relies on come from outside this repository: Claude Code hooks and settings, and Antigravity hooks, rules and skills. Their sources are cited in the decisions of spec 035.

## Invariants

- Rules live only in the guard. An adapter translates a payload or an answer and decides nothing.
- A hook that fails does not block (Claude Code: any exit code other than 2), so every rule a hook enforces is also run by CI.
- Every asset is accounted for in `SKILL.md`.
- The guard has no dependencies and runs on Node 20 or later.
