# spectrace

> Owns: the router to every other contract, the hard rules and the working flow · Not here: standards, commands, vision or history → see the contract the router names

One agent skill that scaffolds a project's contracts and playbooks, and offers optional extras only when asked.

## Hard rules (always)

1. Never add Claude as co-author or "Generated with Claude Code" to commits or pull requests. Commits are Conventional Commits with no trailers.
2. Never bypass git hooks (`--no-verify`), force-push `main`, or stage `.env` files or secrets.
3. Write code, comments, docs and commits in English. Talk to the user in Spanish. The language of the product's own text (interface, messages) is set in DESIGN.md, not here.
4. If a rule here is wrong, say so and propose the change. Do not work around it.

## Before you act, open the contract

| You are about to… | Read first |
|---|---|
| write or change code | ENGINEERING.md |
| add or move a module, layer or dependency | ARCHITECTURE.md |
| write or change a test, make a failing check pass, or decide what "done" means | TESTING.md |
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
3. Run the checks from TESTING.md. Mark `[x]`, add a `verified:` line with the evidence, commit.
4. Stuck? Add an indented `blocked: <reason>` under the task, commit it, tell the user and move on.

The spec format and its rules are in `.agents/playbooks/plan.md`.