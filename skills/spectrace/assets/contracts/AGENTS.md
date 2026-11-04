# {{PROJECT_NAME}}

> Owns: the router to every other contract, the hard rules and the working flow · Not here: standards, commands, vision or history → see the contract the router names

{{GOAL}}

## Hard rules (always)

1. Never add Claude as co-author or "Generated with Claude Code" to commits or pull requests. Commits are Conventional Commits with no trailers.
2. Never bypass hooks (`--no-verify`), force-push `main`, or stage `.env` files or secrets.
3. Never weaken, skip or delete a test to make a change pass.
4. A task is done only after a check you ran passes; write the evidence as `verified: …` under the task.
5. Code, comments, docs and commits in English. <fill: the language you speak with the user>
6. If a rule here is wrong, say so and propose the change. Do not work around it.

## Before you act, open the contract

| You are about to… | Read first |
|---|---|
| write or change code | ENGINEERING.md |
| add or move a module, layer or dependency | ARCHITECTURE.md |
| write or change a test, or decide what "done" means | TESTING.md |
| touch UI, copy, tone or an interface shape | DESIGN.md |
| accept or propose a feature, or change scope | PRODUCT.md |
| run, build, configure or release the project | OPERATIONS.md |
| reverse or question an earlier decision | CHANGES.md |
| plan a feature or a project | .agents/playbooks/plan.md |
| fix a bug, change direction or record a decision | .agents/playbooks/change.md |
| review a diff or close a spec | .agents/playbooks/review.md |

When you decide something, name the contract and section you used ("per ENGINEERING.md §2"). If none applied, say so.

## Working flow

1. `planning/roadmap.md` lists specs in order with a status. Take the first open `[agent]` task of the first spec that is not `done`.
2. Read the contract the router names for that task. Implement only that task.
3. Run the checks from TESTING.md. Mark `[x]`, add the `verified:` line, commit.
4. Stuck? Add an indented `blocked: <reason>` under the task, commit it, tell the user and move on.

The spec format and its rules are in `.agents/playbooks/plan.md`.

## Enforcement

`.agents/guard/guard.mjs` blocks rules 1 and 2 and lints specs in the Claude Code and Antigravity hooks and in CI. A hook that crashes does not block, so CI is the backstop: do not rely on the hook alone.
