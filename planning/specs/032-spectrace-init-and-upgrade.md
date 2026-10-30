# 032 — spectrace-init-and-upgrade

## Goal

Provide a streamlined mechanism (a dedicated `spectrace-init` skill, and optionally a CLI/script utility) to initialize `spectrace` in a new repository or upgrade an existing repository from legacy spectrace versions to the latest 7-contract progressive disclosure governance model (`PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`, `AGENTS.md`, and `planning/`).

## Requirements

- R1: Define the operational workflows for two primary scenarios:
  - **Fresh adoption (greenfield / unmanaged repo):** Detect existing codebase structure, inspect technologies/stack, determine appropriate context-aware design archetype (UI vs. Doc/Governance vs. CLI/Backend), and scaffold the 7 root decision contracts alongside `planning/roadmap.md` and `.agentignore`.
  - **Upgrade / Migration (legacy spectrace repo):** Identify obsolete spectrace artifacts (e.g. legacy git hooks, `.husky`, trailers, outdated combined docs like old `DESIGN.md` holding engineering rules or missing `ENGINEERING.md`, outdated `AGENTS.md`), migrate content safely into the 7 root contracts without losing historical context, and record the migration in `CHANGES.md`.
- R2: Provide a dedicated skill `spectrace-init` (in `skills/spectrace-init/SKILL.md`) that agents can run directly or invoke via prompt (e.g., "init spectrace", "upgrade spectrace", "migrate to latest spectrace").
- R3: Include a standalone, zero-dependency helper script (e.g., Node.js / shell / PowerShell or cross-platform npx command) that can quickly copy template assets or scaffold files directly into a target repository if executed from CLI.
- R4: Update existing skills (`spectrace-plan`, `spectrace-change`, `spectrace-review`) and README documentation to acknowledge the migration/init tooling and guide users on how to install and execute it.
- R5: Maintain pure Markdown, Git-native principles with zero mandatory runtime daemons or fragile git hooks.

## Design

- D1 (R1, R2): Create `skills/spectrace-init/SKILL.md` following Agent Skills specification standard (`agentskills.io` compatible).
  - Categorize trigger phrases: "init spectrace", "setup spectrace", "upgrade spectrace", "migrate spectrace".
  - Step 1: Detect target repo status (Empty / Unmanaged codebase / Legacy spectrace v1-v2).
  - Step 2: In legacy repositories, identify deprecated items (e.g., git hooks in `.git/hooks` or `.spectrace/hooks`, trailers in commit scripts, missing `ENGINEERING.md`, legacy monolithic `DESIGN.md`).
  - Step 3: Run migration safely: preserve project-specific information, extract engineering principles from architecture/design docs into `ENGINEERING.md`, create missing contracts (`TESTING.md`, `CHANGES.md`, `PRODUCT.md`), refresh `AGENTS.md` and `.agentignore`, and log the upgrade in `CHANGES.md`.
  - Step 4: In fresh repositories, perform automated stack inspection and scaffold context-aware starter contracts using templates from `skills/spectrace-plan/assets/`.
- D2 (R3): Provide a lightweight Node.js script (e.g., `bin/spectrace-init.mjs` or `scripts/init.mjs`) compatible with `npx` / `pnpm dlx` or direct execution (`node bin/spectrace-init.mjs [path]`), supporting `--upgrade` and `--dry-run` modes to automate physical scaffolding for developers who prefer a CLI command in addition to the AI skill.
- D3 (R4): Update `README.md` with an "Upgrade & Migration" section and instructions for both new repos and existing repos. Add cross-references in `skills/spectrace-plan/SKILL.md`.

## Tasks

- [x] 032/T001 [agent] Create `skills/spectrace-init/SKILL.md` defining the agent skill for both greenfield init and legacy upgrade — covers R1, R2, D1
- [x] 032/T002 [agent] Create zero-dependency scaffolding and migration script `bin/spectrace-init.mjs` (or `scripts/init.mjs`) with support for target path detection and template copying — covers R3, D2
- [x] 032/T003 [agent] Add package configuration / executable entry point if applicable or ensure clean CLI invocation — covers R3, D2
- [x] 032/T004 [agent] Update `README.md` and `skills/spectrace-plan/SKILL.md` to reference `spectrace-init` and migration instructions — covers R4, D3
- [x] 032/T005 Verify: Test `spectrace-init` on a mock blank repo and a mock legacy repo (with old hooks/docs) to verify clean scaffolding and non-destructive migration — covers R1, R2, R3, R5
      verified: tested bin/spectrace-init.mjs on temporary greenfield repo and legacy spectrace mock; verified non-destructive updates, template copying, and CHANGES.md ledger recording. Checked SKILL.md frontmatter for spectrace-init.
