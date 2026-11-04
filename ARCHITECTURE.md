# Architecture

> Owns: the layers, the allowed direction of dependencies and the boundaries · Not here: how code is written (ENGINEERING.md), procedures (OPERATIONS.md), history (CHANGES.md); no file listings, they go stale

## Layers

- **Skill** (`skills/spectrace/SKILL.md`): the procedure an agent follows to scaffold or update a project. Depends on the assets only.
- **Assets** (`skills/spectrace/assets/`): files copied verbatim into a target repository, in `contracts/`, `playbooks/` and `planning/`. They are Markdown only: no script, hook or workflow.
- **Installed copy** (`.agents/playbooks/`): this repository installs what it ships, the way any project that runs the skill would.
- **Tests** (`tests/`): inspect the assets. Nothing depends on them.

## Boundaries

- A target repository receives copies. After init the skill does not link back, so the project owns what it was given and `update` shows a diff.
- Extras (hooks, CI) are suggestions in `SKILL.md`; the skill writes one only when the user asks, and the project owns it afterwards.

## Invariants

- Every asset is accounted for in `SKILL.md`.
- The installed copy of the playbooks is identical to the asset it comes from; a test fails when they drift.
- Every file the router in `AGENTS.md` names has a template; a test checks it.
- Nothing under `skills/spectrace/assets/` is executable.
