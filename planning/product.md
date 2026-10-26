# Product

## What this is

spectrace is a pair of Agent Skills that turn a plan into small, ordered specs in
`planning/`, so any coding agent can execute them task by task and anyone can see what
is done, what is next and why. Tracking lives in git: one task, one commit, with a
`Spec: NNN/TNNN` trailer, enforced by two short git hooks. No runtime.

## Who uses it

Developers who plan a project with an AI agent and then have agents build it, and who
keep changing direction, adding ideas and growing the product after the first version.

## Stack

- Skills in the open Agent Skills format (agentskills.io), written in English.
- Plain Markdown and git. A target repo gets the `AGENTS.md` block and two POSIX sh
  hooks in `.githooks/`.
- Distributed with the `skills` CLI: `pnpm dlx skills add SebassContreras/spectrace`.
