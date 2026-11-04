# spectrace

One agent skill that scaffolds the files a coding agent needs to decide well in a new project. It only copies files; hooks, CI and other extras are offered as questions, never installed by default. It works with Claude Code and Antigravity, for software and non-software projects.

## Install

```sh
pnpm dlx skills add SebassContreras/spectrace
```

## Use

1. **"Initialize spectrace in this repo."** The skill asks a few questions, copies the scaffold and fits it to the repository.
2. **"Plan this project."** `AGENTS.md` routes the agent to `.agents/playbooks/plan.md`: specs, plus a diff of the contract changes the plan implies.
3. **"Execute the specs."** The agent takes the next open task, reads the contract the router names, runs the checks, marks `[x]` with a `verified:` line and commits.
4. **Pivots, bugs and reviews** go through `change.md` and `review.md`.

The skill only scaffolds. After that the repository owns everything. In a repository that already has a setup, including one from the previous four-skill spectrace, the skill enters update mode and moves it over with a diff per file.

## What you get

| File | Owns |
|---|---|
| `AGENTS.md` | The router to the other files, the hard rules and the working flow |
| `PRODUCT.md` | Why the project exists, who it serves and what it does |
| `ARCHITECTURE.md` | Layers, dependency direction and boundaries |
| `ENGINEERING.md` | How code is written |
| `DESIGN.md` | By project kind: UI (language of the interface, tokens, components, accessibility), interface shape (CLI, API) or editorial rules (content) |
| `TESTING.md` | What "done" means and the command that verifies it |
| `CHANGES.md` | Changes of direction and why |
| `OPERATIONS.md` | Exact procedures to set up, run, build, release and recover |
| `planning/` | The roadmap and the next spec |
| `.agents/playbooks/` | `plan`, `change` and `review` |

## Optional extras

The skill ships no hooks, scripts or CI. After scaffolding it asks whether you want any of these, and writes only what you pick, small and in your stack:

- Block risky git commands (`--no-verify`, force-push `main`, staging `.env`, Claude trailers) with a hook.
- Keep secrets unread with Claude Code's `permissions.deny`.
- Drop Claude attribution with the `attribution` setting.
- Run the verify command from `TESTING.md` in CI.
- Lint specs, once there are many.

Text in the contracts is advisory; an extra makes a rule hold at the cost of something to maintain.

## License

[MIT](LICENSE)
