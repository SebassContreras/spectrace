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
   | `planning/roadmap.md` | `planning/roadmap.md`, and create `planning/specs/` |
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

Move it over with diffs and delete nothing on your own. This procedure has not been run on a real repository yet; report what did not fit.

1. Add the `> Owns: … · Not here: …` line to each existing contract, then move what is misplaced to its owner: commands to `OPERATIONS.md` or `TESTING.md`, layer rules to `ARCHITECTURE.md`, a non-goals section out of `PRODUCT.md` (show it first; the new design has none).
2. Create `OPERATIONS.md`. Replace the old `<!-- spectrace -->` block in `AGENTS.md` with the router, keeping the project's own commands by moving them to the contract that owns them.
3. Install the playbooks, `guard.mjs` and the adapters as in Init, then run the guard.
4. Old specs will fail the lint. For a spec still open, propose the missing `[test]` tasks and `verified:` lines. For a finished one, delete the file and keep its roadmap row.
5. Remove what the new design drops: `.agentignore`, retired git hooks and commit-trailer checks. Record the migration in `CHANGES.md`.

## Limits to tell the user

- The hooks protect Claude Code and Antigravity only. A hook that crashes does not block, so the CI workflow is the backstop.
- `permissions.deny` keeps Claude Code from reading `.env` and key files. Antigravity has no repository-level equivalent.
- Antigravity's answer format and tool names are not fully documented. After the first real session, add `--record` to one hook command, read `.agents/guard/records/`, and adjust. Those recordings hold raw commands and payloads: they are git-ignored, so delete them when done.
