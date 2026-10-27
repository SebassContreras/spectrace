---
name: spectrace-plan
description: >-
  Turns a plan that already exists — written with another agent, pasted in the chat,
  or in a file — into small ordered specs in planning/ (product.md, roadmap.md, one
  specs/NNN-name.md per spec with goal, requirements, design and tasks), and writes the
  spectrace block into AGENTS.md so any agent executes the tasks and closes each one
  with a git commit carrying a `Spec: NNN/TNNN` trailer. No interview. Also adds new
  specs to an existing project at any time, including after the first version ships.
  Use when: "turn this plan into specs", "plan this project", "add a spec for X",
  "new feature: Y", "pasa este plan a specs", "arma las specs", "nueva spec para Z".
---

# spectrace-plan

Run **inside the target repo**. The format and the execution protocol are defined once,
in `assets/agents-block.md`; once installed, the copy in the repo's `AGENTS.md` is the
reference. Read it before writing anything.

## Step 1 — Find the plan

1. The plan is in the conversation, or in a file the user names. If neither, ask for it
   in one sentence — don't interview. A rough plan is enough.
2. Read what exists: `planning/product.md`, `planning/roadmap.md`, every
   `planning/specs/NNN-*.md` (spec files found directly in `planning/` come from an
   earlier layout: `git mv` them into `planning/specs/`), `AGENTS.md`, the code layout
   if there is code (top-level files, the manifest, the test command), and whether this is a git repo. An existing
   `planning/` means you are **adding** specs.
3. Ask **one round** of questions, only about what blocks writing the specs (a stack
   choice the plan leaves open, an account only the user has, `git init` when there is
   no repo). Everything else: pick
   the simplest reasonable option and say so in the spec's Design. If the plan already
   answers everything, ask nothing.

## Step 2 — Cut it into specs

- Each spec is a **thin slice** that ends in something that runs and can be checked:
  a page that loads, a command that answers, a job that writes a row. Prefer three small
  specs over one large one.
- The first spec reaches a running skeleton fast (project scaffold + one real path end
  to end). Polish, scale and extras come later, as their own specs.
- Order by dependency; record dependencies in the roadmap's `Depends on`.
- No over-engineering: no abstraction, layer or config the slice doesn't use today.
  Later specs adjust it when they need to.
- Anything the plan mentions that isn't needed to get value soon goes to the roadmap's
  `## Ideas`, not into a spec. Don't argue scope with the user — a new idea is always
  welcome, it just waits its turn.

## Step 3 — Write each spec

`planning/specs/NNN-name.md`, where `NNN` is the highest existing spec ID + 1 (start at 001)
and `name` is kebab-case. Sections, in English:

- **Goal** — what works when it's done and how to check it, in two or three lines.
- **Requirements** — `R1:`, `R2:`… one checkable outcome each. Only what the slice needs.
- **Design** — `D1 (R1):`… one decision each, naming the R it serves. Stack, files or
  modules, the approach. Mark a guess as `(assumed)` so it's easy to revisit.
- **Tasks** — `- [ ] NNN/T001 [agent] <one verifiable action> — covers D1`, naming
  the R or D items it implements (one or more, comma-separated).
  - One action each (a file, a function, an endpoint, a config change), not "build the
    feature". Each says how you know it's done if that's not obvious.
  - `[human]` for anything needing a credential, a payment, an approval or a physical
    act; `[agent]` for the rest.
  - Tests: one test task per requirement worth checking, at the lowest level that
    proves it, and only as many as the slice needs.
  - Docs: when the spec changes what a doc in `## Docs` describes, add a task for it
    (`Update README.md: add the export command — covers D2`). A spec that creates a
    new doc also adds its line to `## Docs`.
Leave out a section that would be empty (a spec with nothing to decide has no Design).
There is no Changes section yet; `spectrace-change` adds it with the first change.

## Step 4 — Confirm, then write

1. Show the roadmap rows and, per spec, its goal and task list in one message. Ask for
   yes / changes — and, if the plan came from a file, whether to delete that file once
   the specs exist (it goes stale as they change). Write nothing before a yes.
   No git repo and the user agreed → `git init` first.
2. First time in the repo (no `planning/`):
   - `planning/product.md`: `# Product`, then `## What this is`, `## Who uses it`,
     `## Stack` (including how to run and test it, marked `(assumed)` when the plan
     doesn't say) and `## Docs` — from the plan, a few lines each. It describes; it
     doesn't restrict. `## Docs` lists each doc the project keeps and what it
     describes (`README.md — install, usage, commands`); `AGENTS.md` is always one.
   - `planning/roadmap.md`: `# Roadmap`, the table from the block, then `## Ideas`.
3. Add each spec file and its roadmap row with `Status` `todo` (from then on the hook
   writes it). Append new rows; never renumber.
4. **Hooks.** Copy `assets/hooks/pre-commit` and `assets/hooks/commit-msg` to
   `.githooks/` with LF line endings (convert if the copy came out CRLF — `sh` fails on
   CRLF), add `.githooks/* text eol=lf` to `.gitattributes`, stage both hooks with
   `git add --chmod=+x .githooks/pre-commit .githooks/commit-msg` (the only reliable
   executable bit on Windows), and run `git config core.hooksPath .githooks`. If
   `core.hooksPath` already points elsewhere (husky, another tool), ask before changing
   it. If the files exist and differ from the assets, show the diff and replace them on
   a yes. This step also repairs a project whose `.githooks/` went missing.
5. `AGENTS.md`: if it has no `<!-- spectrace -->` block, append the content of
   `assets/agents-block.md` in the file's line endings (create the file if missing,
   with a `# <project>` title). If the block exists and differs from the asset, show
   the diff and replace it on a yes. Touch nothing outside the markers.
6. Delete the source plan file if the user said so. Don't commit: the executing agent
   commits `planning/`, `AGENTS.md` and the hooks before its first task.

## Step 5 — Report and stop

List what was written, the `[human]` tasks (they are the user's), and the next step:
"tell any agent to execute the specs". **Stop** — don't start executing tasks here.

## Style

- Terse. The user's language in the conversation; English in the files.
- Never invent a fact only the user knows (an account, a budget, a name) — ask, or
  leave `TBD`.
