# 032 — spectrace-init-and-upgrade

## Goal

Provide a streamlined mechanism (a dedicated `spectrace-init` skill and a zero-dependency CLI utility) to initialize `spectrace` in a new repository or upgrade an existing repository from legacy spectrace versions to the latest 7-contract progressive disclosure governance model (`PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`, `AGENTS.md`, and `planning/`).

## Requirements

- R1a: Detect unmanaged codebases, determine context-aware design archetype (UI vs. Docs vs. Backend), and scaffold the 7 root contracts, `planning/roadmap.md`, and `.agentignore`.
- R1b: Detect legacy Spectrace repositories, preserve existing content, extract missing contracts (`ENGINEERING.md`, `TESTING.md`), retire obsolete git hooks/trailers, and record the migration in `CHANGES.md`.
- R2: Provide a dedicated skill `spectrace-init` (in `skills/spectrace-init/SKILL.md`) that agents can run directly or invoke via prompt (e.g., "init spectrace", "upgrade spectrace", "migrate to latest spectrace").
- R3: Provide a single zero-dependency Node.js CLI script (`bin/spectrace-init.mjs`) using native `node:fs` to initialize or upgrade contracts without extra dependencies or shell wrappers.
- R4: Update existing skills (`spectrace-plan`, `spectrace-change`, `spectrace-review`) and README documentation to acknowledge the migration/init tooling and guide users on how to install and execute it.
- R5: Maintain zero external runtime dependencies and zero git hook daemons, performing all migrations via standard filesystem operations (`node:fs`) and Git-native files.
- R6: Verification must prove domain invariants across 4 input partitions: (1) Greenfield blank directory, (2) Legacy repo with partial contracts, (3) Repeated invocation (idempotency: zero clobbering of existing content), and (4) Invalid target directory path.

## Design

- D1 (R1a, R1b, R2): Create `skills/spectrace-init/SKILL.md` following the Agent Skills open standard ([agentskills.io](https://agentskills.io), requiring name, description with triggers, and standalone instructions compatible with Claude, Cursor, and Antigravity).
  - Categorize trigger phrases: "init spectrace", "setup spectrace", "upgrade spectrace", "migrate spectrace".
  - Step 1: Detect target repo status (Empty / Unmanaged codebase / Legacy spectrace v1-v2).
  - Step 2: In legacy repositories, identify deprecated items (e.g., git hooks in `.git/hooks` or `.spectrace/hooks`, trailers in commit scripts, missing `ENGINEERING.md`, legacy monolithic `DESIGN.md`).
  - Step 3: Run migration safely: preserve project-specific information, extract engineering principles from architecture/design docs into `ENGINEERING.md`, create missing contracts (`TESTING.md`, `CHANGES.md`, `PRODUCT.md`), refresh `AGENTS.md` and `.agentignore`, and log the upgrade in `CHANGES.md`.
  - Step 4: In fresh repositories, perform automated stack inspection and scaffold context-aware starter contracts using templates from `skills/spectrace-plan/assets/`.
- D2 (R1a, R1b, R3, R5): Provide `bin/spectrace-init.mjs` reusing canonical starter assets from `skills/spectrace-plan/assets/` via relative path resolution, avoiding duplicated templates. Support flags `--type <ui|docs|backend>`, `--upgrade`, and `--dry-run`.
- D3 (R4): Update `README.md` with an "Upgrade & Migration" section and instructions for both new repos and existing repos. Add cross-references in `skills/spectrace-plan/SKILL.md`, `spectrace-change/SKILL.md`, and `spectrace-review/SKILL.md`.

### Trade-offs & Mitigations (P10)
- Choice: Single-file ESM script (`bin/spectrace-init.mjs`) without build step vs. TypeScript/bundled binary.
  - Pros: Zero build step, zero npm install dependencies, instant execution via `node` or `npx`.
  - Cons: Requires Node.js >= 18 runtime on host machine.
  - Mitigation: Target environments for AI coding agents already include Node.js; agents can also follow `skills/spectrace-init/SKILL.md` natively in pure markdown if Node is absent.

## Tasks

- [x] 032/T001 [agent] Create `skills/spectrace-init/SKILL.md` defining the agent skill for greenfield init and legacy upgrade — covers R1a, R1b, R2, D1
- [x] 032/T002a [agent] Implement `bin/spectrace-init.mjs` scaffolding engine for greenfield initialization reusing canonical assets — covers R1a, R3, R5, D2
- [x] 032/T002b [agent] Implement migration and ledger recording logic in `bin/spectrace-init.mjs` for legacy repositories — covers R1b, R3, R5, D2
- [x] 032/T003 [agent] Configure `package.json` with `"type": "module"` and bin entry point pointing to `bin/spectrace-init.mjs` — covers R3, D2
- [x] 032/T004a [agent] Update `README.md` with spectrace-init installation, quick start, and CLI options — covers R4, D3
- [x] 032/T004b [agent] Update `skills/spectrace-plan/SKILL.md`, `spectrace-change`, and `spectrace-review` with `spectrace-init` prerequisites — covers R4, D3
- [x] 032/T005 Verify: Test `bin/spectrace-init.mjs` across input partitions using parameterized cases: (P1) blank dir scaffolds all 7 contracts, (P2) legacy repo extracts missing contracts and logs to CHANGES.md, (P3) second run asserts idempotent non-destructive preservation, (P4) non-existent target path reports clean error without unhandled exception — covers R1a, R1b, R3, R5, R6
      verified: executed tests across P1 (blank directory), P2 (legacy repo with old AGENTS/CHANGES), P3 (idempotent repeated run preserving files), and P4 (invalid directory handling). All 4 partitions passed cleanly.
