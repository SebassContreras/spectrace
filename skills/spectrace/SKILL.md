---
name: spectrace
description: >-
  Scaffolds the agent contracts of a project, software or not: an AGENTS.md router, seven
  single-responsibility contracts plus DESIGN.md (PRODUCT, ARCHITECTURE, ENGINEERING, DESIGN, TESTING,
  CHANGES, OPERATIONS), three playbooks (plan, change, review) and a roadmap. It only copies files;
  hooks, CI and other extras are suggested and added only if the user asks.
  Use when: "init spectrace", "set up the agent contracts", "scaffold this project",
  "start a new project with spectrace", "update spectrace", "upgrade spectrace".
---

# spectrace

Run **inside the target repository**. This skill copies and fits the scaffold; it does not plan, change or review. Once it has run, the repository carries everything: `AGENTS.md` routes the agent to the contract or playbook that applies.

## Step 0 — Pick the mode

- No `AGENTS.md` and no `planning/` → **init**.
- Either one exists (an earlier spectrace, or another setup) → **update**. Never overwrite silently.

## Init

1. **Ask once** (skip what the user already said): project name; the goal in one or two sentences; the language the user speaks; the language of the product's own text if it has a UI or messages (not the same as the language the user speaks); which agents they use (default Claude Code and Antigravity); and the kind of project: *software with a UI*, *software without a UI* (CLI, API, library), or *content* (docs, video, writing, research). Do not guess the kind: `DESIGN.md` depends on it.
2. **Copy** from `${CLAUDE_SKILL_DIR}/assets/` with a file copy, not by retyping:

   | From `assets/` | To the repository |
   |---|---|
   | `contracts/AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `TESTING.md`, `CHANGES.md`, `OPERATIONS.md` | the root, same names |
   | `contracts/design-ui.md` or `design-interface.md` or `design-content.md` (by kind) | `DESIGN.md` |
   | `planning/roadmap.md` | `planning/roadmap.md`, and create `planning/specs/` with an empty `.gitkeep` so git keeps the folder |
   | `playbooks/*.md` | `.agents/playbooks/` |
   | `CLAUDE.md` (Claude Code) | `CLAUDE.md` |

3. **Fill the contracts.** Replace `{{PROJECT_NAME}}` and `{{GOAL}}`. For each `<fill: …>` marker, read the repository first (manifests and scripts, lockfiles, CI, folders, the README, existing docs) and write only what the repository cannot show on its own. If you cannot know it yet, leave the marker: the plan playbook fills it. Do not invent. Keep `AGENTS.md` under 100 lines and put the user's language in its language rule (hard rule 3) and the product's language in `DESIGN.md`. Each fact lives in one contract only: if another contract already owns it (see the `Owns` line), link to it instead of repeating it.

   For a project that is not software (video, writing, research), keep the same files and change what they hold: `ENGINEERING.md` holds the production standards (tools, file naming, review steps) and drops the code principles that do not apply; `TESTING.md` holds the review checklist that says when a piece is done; `DESIGN.md` is the content variant.
4. **Report** the files created and the unfilled markers, and suggest the first commit as `chore: add agent contracts` (no trailers). Tell the user the next step is to ask the agent to plan the project; `AGENTS.md` routes that to `.agents/playbooks/plan.md`. Then offer the optional extras below as a question, not as something already installed. Stop there.

## Update

For each shipped file (contracts, playbooks, `CLAUDE.md`) compare it with the repository's copy and show a diff per file; apply only what the user approves.

- A contract the repository has edited: propose only sections or rules it lacks. Never replace its text.
- The playbooks: replace only when the user approves the diff.
- Record the update in `CHANGES.md` with what changed and why.

### A repository from the previous four-skill spectrace

Move it over with diffs. Leave the user's own uncommitted changes alone: the migration goes in its own commit. Edit files in place instead of rewriting them, so line endings and unrelated lines stay, and check `git diff --stat` as you go. This procedure has been run once, on a copy of a real repository; report what did not fit.

1. Add the `> Owns: … · Not here: …` line to each existing contract, then move each project rule to the contract whose `Owns` line fits it: code rules to `ENGINEERING.md`, layers and invariants to `ARCHITECTURE.md`, test rules and the verify commands to `TESTING.md`, run and release steps to `OPERATIONS.md`. Only a rule that must hold on every task and that no contract owns stays in `AGENTS.md`.
2. Create `OPERATIONS.md`. Replace the old `<!-- spectrace -->` block in `AGENTS.md` with the router. Remove a non-goals section from `PRODUCT.md` and keep its text in the migration entry of `CHANGES.md`; the new design has none.
3. Install the playbooks and `CLAUDE.md` as in Init.
4. Old specs must match the format in `plan.md`. Never invent evidence: for a task already checked write `verified: carried over from the previous format, not re-run`; for a requirement with no test task add a real `[agent][test]` task that names the test file or behavior it covers, not one task for "all requirements". A finished spec that gains an open task goes back to `in progress`; a finished spec with nothing open is deleted and keeps its roadmap row. Keep a spec under 80 lines.
5. Remove what the new design drops: the four `spectrace-*` skills (in `.agents/skills/` and `.claude/skills/`) and their entries in `skills-lock.json`, `.agentignore`, retired git hooks, `.agents/guard/`, `.agents/hooks.json`, spectrace hook entries in `.claude/settings.json`, the guard CI workflow and commit-trailer checks. Record the migration in `CHANGES.md`.

## Optional extras (suggest, never install by default)

Spectrace ships no hooks, scripts or CI. After scaffolding, ask the user which of these they want, if any. If they say yes, write only that one, small, in the project's own stack, and explain what it does. Prose in the contracts is advisory; these make a rule hold, at the cost of something to maintain.

- **Block risky git commands** (`--no-verify`, force-push `main`, `git add .env`, Claude trailers in commits): a Claude Code `PreToolUse` hook, or a plain git hook. On Windows Claude Code runs shell commands through its PowerShell tool, so match both `Bash` and `PowerShell`. A hook that crashes does not block.
- **Keep secrets unread:** `permissions.deny` in `.claude/settings.json` for `.env`, `secrets/` and key files. Antigravity has no repository-level equivalent.
- **Drop Claude attribution:** the `attribution` setting in `.claude/settings.json` (`commit` and `pr` empty, `sessionUrl` false).
- **CI:** run the verify command from `TESTING.md` on every push. It is the one layer an agent cannot skip.
- **Spec lint:** a short script that checks specs against the format in `plan.md`. Only worth it once specs are many.

Record any extra the user adds in `OPERATIONS.md`.
