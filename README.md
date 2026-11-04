# spectrace

One agent skill that scaffolds the files a coding agent needs to decide well in a new project, plus a guard that stops it from skipping the rules that must always hold. It works with Claude Code and Antigravity, for software and non-software projects.

## Install

```sh
pnpm dlx skills add SebassContreras/spectrace
```

## Use

1. **"Initialize spectrace in this repo."** The skill asks a few questions, copies the scaffold and fits it to the repository.
2. **"Plan this project."** `AGENTS.md` routes the agent to `.agents/playbooks/plan.md`: specs, plus a diff of the contract changes the plan implies.
3. **"Execute the specs."** The agent takes the next open task, reads the contract the router names, runs the checks, marks `[x]` with a `verified:` line and commits.
4. **Pivots, bugs and reviews** go through `change.md` and `review.md`.

The skill only scaffolds. After that the repository owns everything.

## What you get

| File | Owns |
|---|---|
| `AGENTS.md` | The router to the other files, the hard rules and the working flow |
| `PRODUCT.md` | Why the project exists, who it serves and what it does |
| `ARCHITECTURE.md` | Layers, dependency direction and boundaries |
| `ENGINEERING.md` | How code is written |
| `DESIGN.md` | UI tokens, or the interface shape, or editorial rules, by project kind |
| `TESTING.md` | What "done" means and the command that verifies it |
| `CHANGES.md` | Changes of direction and why |
| `OPERATIONS.md` | Exact procedures to set up, run, build, release and recover |
| `planning/` | The roadmap and the next spec |
| `.agents/playbooks/` | `plan`, `change` and `review` |
| `.agents/guard/guard.mjs` | The enforcement script |

## How the rules are enforced

Text is advisory, so the rules that must always hold are checked by one script, `guard.mjs`:

- **Hooks** in Claude Code (`.claude/settings.json`) and Antigravity (`.agents/hooks.json`) block Claude attribution in commits and pull requests, `--no-verify`, force-push to `main` and staging `.env` files, and lint specs as they are edited.
- **CI** runs `guard --all` over contracts, specs, the roadmap and commit messages. It is the only layer an agent cannot skip.
- **Specs** must cover every requirement with a task and a `[test]` task, and every checked task needs a `verified:` line.

## Limits

- The hooks protect Claude Code and Antigravity only, and a hook that crashes does not block.
- Antigravity's answer format and tool names are only partly documented; `guard --record` captures real payloads to confirm them.
- The guard checks structure. Whether a spec respects KISS or a test partitions its inputs well still needs a review.

## License

[MIT](LICENSE)
