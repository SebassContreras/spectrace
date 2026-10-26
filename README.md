# spectrace

**Plans you can change your mind about.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2.svg)](https://agentskills.io)

spectrace turns a plan you already have — made with another agent, or in the chat —
into small, ordered specs in `planning/`. Any coding agent executes them task by task
and closes each task with a git commit that names it. When you change direction, find a
bug or have a new idea, it updates the specs and adds the tasks that clean up what the
old approach left behind. It's just Markdown and git, plus two short git hooks: no
runtime to install.

## Install

From your project's folder:

```sh
pnpm dlx skills add SebassContreras/spectrace
```

The [`skills` CLI](https://github.com/vercel-labs/skills) copies the two skills into the
folder your agent reads (`.claude/skills/` for Claude Code, `.agents/skills/` for most
others). Add `-g` to install for every project.

## Quick start

1. Install the skills (above) in your project's folder.
2. Paste or point to your plan: *"turn this plan into specs"*. `spectrace-plan` writes
   `planning/`, the block in `AGENTS.md` and the hooks in `.githooks/` (and runs
   `git init` if you agree).
3. *"Execute the specs."* Any agent takes it from there, one commit per task.

Later, anything new — an idea, a change of mind, a bug — goes through
`spectrace-change`.

## The two skills

| Skill | What it does |
|---|---|
| `spectrace-plan` | Takes your plan and writes `planning/product.md`, `planning/roadmap.md` and one `planning/NNN-name.md` per spec — thin slices that each end in something that runs. Adds the spectrace block to `AGENTS.md` and installs the git hooks (also repairs them if missing). Use it again any time to add specs. |
| `spectrace-change` | Changes of direction, bugs, new ideas, and conventions that get in the way. Replaces the old item, finds what it built (`git log --grep`, `git grep`, and the old approach's assumptions), and adds cleanup tasks ending in a review. A change that spans specs becomes a new spec, so finished specs stay finished. |

## A spec

```markdown
# 003 — login

## Goal
A user can sign in and stay signed in across reloads.

## Requirements
- R1: A user signs in with email and password.

## Design
- ~~D1 (R1): Sessions live in localStorage.~~ → D2
- D2 (R1): Sessions live in an httpOnly cookie.

## Tasks
- [x] 003/T001 [agent] Login form — covers R1
- [ ] 003/T002 [agent] Session cookie middleware — covers D2
- [ ] 003/T003 [agent] Remove the localStorage session code — replaces D1
- [ ] 003/T004 [human] Create the mail provider account — covers R1

## Changes
- 2026-10-12: D1 → D2. Why: localStorage is readable by any script. Work: T003.
```

## Executing

Tell your agent to "execute the specs". The block in `AGENTS.md` makes it take the next
open task, do only that, verify it, and close it with one commit holding the change, the
ticked box and a trailer:

```
feat(login): session cookie middleware

Spec: 003/T002
```

The `Spec:` line must sit in the message's last paragraph, with any other trailer
(`Co-Authored-By:`…) and no blank line between them — git reads only that paragraph as
trailers.

Two small git hooks, installed to `.githooks/` by `spectrace-plan`, make this hard to
skip: `commit-msg` refuses a `Spec:` trailer whose task isn't ticked, or a ticked task
with no work in the commit; `pre-commit` writes each spec's `Status` in the roadmap from
its checkboxes — nobody types it.

After a change of direction, `spectrace-change` lists what the old approach *assumed*
(not just its names), turns the reason for the change into a requirement with a test,
and ends with a `Review:` task — run by a fresh agent when possible — that the hook
won't let close without a `reviewed:` note saying what was read and found.

What a spec built is then one command away:

```sh
git log --grep "Spec: 003/" --stat
```

## Docs follow the specs

`planning/product.md` lists the docs the project keeps and what each describes:

```markdown
## Docs
- README.md — install, usage, the commands
- AGENTS.md — the protocol agents follow
```

When a spec changes something a listed doc describes, `spectrace-plan` adds a task to
update it, so the doc changes in a commit with a `Spec:` trailer like any code:

```sh
git blame README.md          # the line → commit a1b2c3
git show -s a1b2c3           # → Spec: 003/T002 → the decision behind it
```

When that decision changes, `git log --grep "Spec: 003/"` lists the doc commits next to
the code, and `spectrace-change` re-reads every listed doc for sentences that describe
the old way without naming it. A change that belongs to no spec on purpose — a typo, a
chore — carries `Spec: none`; a commit with no trailer at all gets a warning.

## Principles

- **Plan elsewhere, spec here.** No interview; one round of questions at most.
- **Thin specs first.** Get something running, validate it, then adjust.
- **Nothing is out of scope.** New ideas go to the roadmap's `## Ideas` and wait their
  turn.
- **Conventions describe, they don't bind.** When one blocks the best solution, the
  agent proposes changing it instead of working around it.
- **The commit is the record.** No ledger to keep in sync.

## Limits

- The trace is as good as the commits: a task closed without its `Spec:` trailer is
  invisible to `git log --grep`.
- A squash merge folds several tasks into one commit; the trailers survive in the
  message, but per-task diffs don't. Prefer merge or rebase for spec branches.
- Finding leftovers after a change of direction is the agent's search and reading,
  not a checker. It is backed by a test of the reason for the change and a recorded
  review, but code that breaks neither can still slip through.
- Hooks are local: a fresh clone runs `git config core.hooksPath .githooks` once (the
  protocol tells agents to). `--no-verify` bypasses them.

## Coming from the old spectrace

Earlier versions had an interview, `trace.py` and `.spectrace/`. They are gone and
there is no automatic migration: delete `.spectrace/` and the old protocol block in
`AGENTS.md`, then run `spectrace-plan` on what is still pending.

## This repository

spectrace is planned with itself: see [`planning/`](planning/roadmap.md) and
[`AGENTS.md`](AGENTS.md). After cloning, run `git config core.hooksPath .githooks`.

## License

[MIT](LICENSE)
