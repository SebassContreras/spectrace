---
name: spectrace
description: >-
  Scaffolds the agent contracts of a project, software or not: an AGENTS.md router, eight
  single-responsibility contracts (PRODUCT, ARCHITECTURE, ENGINEERING, DESIGN, TESTING, CHANGES,
  OPERATIONS), three playbooks (plan, change, review), a roadmap, and a guard script wired into
  Claude Code and Antigravity hooks and into CI. It only scaffolds; planning, changes and reviews
  run from the repository's own playbooks afterwards.
  Use when: "init spectrace", "set up the agent contracts", "scaffold this project",
  "start a new project with spectrace", "update spectrace", "upgrade spectrace".
---

# spectrace

Run **inside the target repository**. This skill copies and fits the scaffold; it does not plan, change or review. Once it has run, the repository carries everything: `AGENTS.md` routes the agent to the contract or playbook that applies.

## Step 0 — Pick the mode

- No `AGENTS.md` and no `planning/` → **init**.
- Either one exists (an earlier spectrace, or another setup) → **update**. Never overwrite silently.

## Init

1. **Ask once** (skip what the user already said): project name; the goal in one or two sentences; the language the user speaks; which agents they use (default Claude Code and Antigravity); and the kind of project: *software with a UI*, *software without a UI* (CLI, API, library), or *content* (docs, video, writing, research). Do not guess the kind: `DESIGN.md` depends on it.
2. **Copy** from `${CLAUDE_SKILL_DIR}/assets/` with a file copy, not by retyping:

   | From `assets/` | To the repository |
   |---|---|
   | `contracts/AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `TESTING.md`, `CHANGES.md`, `OPERATIONS.md` | the root, same names |
   | `contracts/design-ui.md` or `design-interface.md` or `design-content.md` (by kind) | `DESIGN.md` |
   | `planning/roadmap.md` | `planning/roadmap.md`, and create `planning/specs/` with an empty `.gitkeep` so git keeps the folder |
   | `playbooks/*.md` | `.agents/playbooks/` |
   | `guard/guard.mjs` | `.agents/guard/guard.mjs` |
   | `adapters/claude-settings.json` (Claude Code) | merged into `.claude/settings.json` |
   | `adapters/CLAUDE.md` (Claude Code) | `CLAUDE.md` |
   | `adapters/antigravity-hooks.json` (Antigravity) | merged into `.agents/hooks.json` |
   | `adapters/guard.yml` (repository on GitHub) | `.github/workflows/guard.yml` |

   Add `.agents/guard/records/` to `.gitignore`. When a settings or hooks file already exists, merge by key (join the arrays, such as `permissions.deny`), keep what the user has, and show the diff. After writing JSON, parse it to confirm it is valid.
3. **Fill the contracts.** Replace `{{PROJECT_NAME}}` and `{{GOAL}}`. For each `<fill: …>` marker, read the repository first (manifests and scripts, lockfiles, CI, folders, the README, existing docs) and write only what the repository cannot show on its own. If you cannot know it yet, leave the marker: the guard lists it as unfilled and the plan playbook fills it. Do not invent. Keep `AGENTS.md` under 100 lines and put the user's language in its language rule (hard rule 3). Each fact lives in one contract only: if another contract already owns it (see the `Owns` line), link to it instead of repeating it.

   For a project that is not software (video, writing, research), keep the same files and change what they hold: `ENGINEERING.md` holds the production standards (tools, file naming, review steps) and drops the code principles that do not apply; `TESTING.md` holds the review checklist that says when a piece is done; `DESIGN.md` is the content variant.
4. **Check.** Run `node .agents/guard/guard.mjs --all`. Fix every error; unfilled markers are warnings you report.
5. **Report** the files created and the unfilled markers, and suggest the first commit as `chore: add agent contracts` (no trailers). Tell the user the next step is to ask the agent to plan the project; `AGENTS.md` routes that to `.agents/playbooks/plan.md`. Stop there.

## Update

For each shipped file (contracts, playbooks, `guard.mjs`, adapters) compare it with the repository's copy and show a diff per file; apply only what the user approves.

- A contract the repository has edited: propose only sections or rules it lacks. Never replace its text.
- `guard.mjs` and the playbooks: replace only when the user approves the diff.
- Record the update in `CHANGES.md` with what changed and why.

### A repository from the previous four-skill spectrace

Move it over with diffs. Leave the user's own uncommitted changes alone: the migration goes in its own commit. Edit files in place instead of rewriting them, so line endings and unrelated lines stay, and check `git diff --stat` as you go. This procedure has been run once, on a copy of a real repository; report what did not fit.

1. Add the `> Owns: … · Not here: …` line to each existing contract, then move each project rule to the contract whose `Owns` line fits it: code rules to `ENGINEERING.md`, layers and invariants to `ARCHITECTURE.md`, test rules and the verify commands to `TESTING.md`, run and release steps to `OPERATIONS.md`. Only a rule that must hold on every task and that no contract owns stays in `AGENTS.md`.
2. Create `OPERATIONS.md`. Replace the old `<!-- spectrace -->` block in `AGENTS.md` with the router. Remove a non-goals section from `PRODUCT.md` and keep its text in the migration entry of `CHANGES.md`; the new design has none.
3. Install the playbooks, `guard.mjs` and the adapters as in Init, then run the guard.
4. Old specs fail the lint. Never invent evidence: for a task already checked write `verified: carried over from the previous format, not re-run`; for a requirement with no test task add a real `[agent][test]` task that names the test file or behavior it covers, not one task for "all requirements". A finished spec that gains an open task goes back to `in progress`; a finished spec with nothing open is deleted and keeps its roadmap row. A spec over 80 lines is only a warning.
5. Remove what the new design drops: the four `spectrace-*` skills (in `.agents/skills/` and `.claude/skills/`) and their entries in `skills-lock.json`, `.agentignore`, retired git hooks and commit-trailer checks. Record the migration in `CHANGES.md`.

## Limits to tell the user

- The hooks protect Claude Code and Antigravity only. A hook that crashes does not block, so the CI workflow is the backstop.
- `permissions.deny` keeps Claude Code from reading `.env` and key files. Antigravity has no repository-level equivalent.
- Antigravity's answer format and tool names are not fully documented. After the first real session, add `--record` to one hook command, read `.agents/guard/records/`, and adjust. Those recordings hold raw commands and payloads: they are git-ignored, so delete them when done.
