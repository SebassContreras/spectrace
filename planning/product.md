# Product

## What this is

spectrace is a pair of Agent Skills that turn a plan into small, ordered specs in
`planning/`, so any coding agent can execute them task by task and anyone can see what
is done, what is next and why. Tracking lives in git: one task, one commit, with a
`Spec: NNN/TNNN` trailer, enforced by two short git hooks and, on GitHub, a CI check.
No runtime.

## Who uses it

Developers who plan a project with an AI agent and then have agents build it, and who
keep changing direction, adding ideas and growing the product after the first version.

## Stack

- Skills in the open Agent Skills format (agentskills.io), written in English.
- Plain Markdown and git. A target repo gets the `AGENTS.md` block, two POSIX sh
  hooks and `check-trailers` in `.githooks/`, and on GitHub a workflow in
  `.github/workflows/spectrace.yml`.
- Distributed with the `skills` CLI: `pnpm dlx skills add SebassContreras/spectrace`.
- Test: `sh tests/hooks.sh` — behavior tests for the git hooks: each builds a
  throwaway repo, makes a commit and checks that it is accepted or refused. It also
  checks that `.githooks/` matches `skills/spectrace-plan/assets/hooks/`.

## Docs

- `README.md` — what spectrace is, install, quick start, the skills table, the spec
  format, how tasks close (trailers, hooks), principles, limits.
- `AGENTS.md` — doc map of this repo and the spectrace block (a copy of
  `skills/spectrace-plan/assets/agents-block.md`).
- `skills/*/SKILL.md` — what each skill does, step by step.
