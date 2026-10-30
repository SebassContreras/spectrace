# 028 — streamlined-foundation

## Goal
Establish a streamlined, hook-free foundation where core architectural and design decisions live at the repository root (`AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`) and `planning/` is strictly reserved for the execution plan (`roadmap.md` and `specs/`).

## Requirements
- R1: Eliminate hook machinery across 2 input partitions: (a) repo with `.githooks/`, `tests/hooks.sh`, and `.github/workflows/spectrace.yml` present; (b) repo where hooks or config are already absent (no-op idempotency).
- R2: Scaffold the 4 root governance contracts (`AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`) in English, asserting invariant preservation of existing historical change logs.
- R3: Purify `planning/` to retain strictly `roadmap.md` and `specs/`, cleanly removing `planning/product.md` if present without affecting existing spec files.
- R4: Update `spectrace-plan` and `spectrace-change` skills to support this streamlined structure without hooks.
- R5: Update `README.md` to reflect the pure Markdown architecture.

## Design
- D1 (R1): Remove `.githooks/`, `tests/hooks.sh`, `.github/workflows/spectrace.yml`, and unset `core.hooksPath`.
- D2 (R2): Write concise, progressive-disclosure root documents in English adhering to modern AI coding agent best practices.
- D3 (R3): Remove `planning/product.md` and keep only `roadmap.md` and `specs/` in `planning/`.
- D4a (R4): Update `skills/spectrace-plan/SKILL.md` to scaffold root-level governance files during initial planning without generating git hooks.
- D4b (R4): Update `skills/spectrace-change/SKILL.md` to reference root contracts and remove all trailer validation guidance.
- D5 (R5): Rewrite `README.md` in English.

### Trade-offs & Mitigations (P10)
- Choice: Removing automated git hooks and trailer scripts in favor of agent-enforced verification and conventions.
  - Pros: Eliminates fragile runtime environments, cross-platform hook issues, and shell script dependencies. Pure Git and Markdown.
  - Cons: Requires AI agents and human contributors to verify contracts voluntarily through workflow guidelines.
  - Mitigation: Codify workflow constraints and step-by-step checklists directly in `AGENTS.md` and skill instructions.

## Tasks
- [x] 028/T001 [agent] Remove git hooks, trailer scripts, and unset `core.hooksPath` — covers R1, D1
- [x] 028/T002 [agent] Create `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md` at root in English — covers R2, D2
- [x] 028/T003 [agent] Clean up `planning/` directory to contain only `roadmap.md` and `specs/` — covers R3, D3
- [x] 028/T004a [agent] Update `skills/spectrace-plan` instructions to scaffold root documents without hooks — covers R4, D4a
- [x] 028/T004b [agent] Update `skills/spectrace-change` instructions to reference root documents and remove trailers — covers R4, D4b
- [x] 028/T005 [agent] Update `README.md` documentation — covers R5, D5
- [x] 028/T006 Verify: Assert repository structure across 3 input partitions: (P1) verify `.githooks/` and CI hook workflows are absent and git config has no `core.hooksPath`; (P2) verify `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md` exist at root and contain valid Markdown; (P3) verify `planning/` contains exclusively `roadmap.md` and `specs/` — covers R1, R2, R3, R4, R5
      verified: all hook files removed, core.hooksPath unset, root documents created, and planning/ purified to roadmap.md and specs/.
