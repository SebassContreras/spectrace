# Product

> Owns: why the project exists, who it serves and what it does today · Not here: status or order of work (planning/roadmap.md), technical choices (ARCHITECTURE.md), standards (ENGINEERING.md)

## Vision

One agent skill that scaffolds the contracts and playbooks a project needs, so coding agents decide well. Hooks and CI are suggestions, not part of the scaffold. It works with Claude Code and Antigravity, for software and non-software projects.

## Users and the problem

- **A developer starting a project with coding agents.** Every new project means rewriting the same rules (principles, tests, specs, way of working), and the agent forgets or skips them.
- **The same developer, mid-project.** Some rules must always hold, such as never adding Claude as co-author. Whether to back them with a hook or CI is the developer's call, so the skill suggests and does not install.

## Capabilities

- Scaffolds eight single-responsibility contracts, an `AGENTS.md` router, a roadmap and three playbooks (plan, change, review) into any project.
- Fits the contracts to the project by reading the repository, and writes only what the repository cannot show.
- Asks the language of the product text (UI or messages) apart from the language the agent speaks, and records it in `DESIGN.md`.
- Suggests optional extras (git and Claude hooks, `permissions.deny`, CI) and adds one only when the user says yes.
- Moves a repository that uses an earlier spectrace to this layout, with a diff per file.
