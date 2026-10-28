# 028 — streamlined-foundation

## Goal
Establish a streamlined, hook-free foundation where core architectural and design decisions live at the repository root (`AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`) and `planning/` is strictly reserved for the execution plan (`roadmap.md` and `specs/`).

## Requirements
- R1: Eliminate all shell git hooks, trailer checkers, and CI trailer enforcement.
- R2: Relocate and create root-level governance files in English: `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`.
- R3: Ensure `planning/` strictly contains the action plan (`roadmap.md`, `specs/`).
- R4: Update `spectrace-plan` and `spectrace-change` skills to support this streamlined structure without hooks.
- R5: Update `README.md` to reflect the pure Markdown architecture.

## Design
- D1 (R1): Remove `.githooks/`, `tests/hooks.sh`, `.github/workflows/spectrace.yml`, and unset `core.hooksPath`.
- D2 (R2): Write concise, progressive-disclosure root documents in English adhering to modern AI coding agent best practices.
- D3 (R3): Remove `planning/product.md` and keep only `roadmap.md` and `specs/` in `planning/`.
- D4 (R4): Update `skills/spectrace-plan/` and `skills/spectrace-change/` instructions to initialize root documents and avoid git hooks.
- D5 (R5): Rewrite `README.md` in English.

## Tasks
- [x] 028/T001 [agent] Remove git hooks, trailer scripts, and unset `core.hooksPath` — covers R1, D1
- [x] 028/T002 [agent] Create `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md` at root in English — covers R2, D2
- [x] 028/T003 [agent] Clean up `planning/` directory to contain only `roadmap.md` and `specs/` — covers R3, D3
- [x] 028/T004 [agent] Update `skills/spectrace-plan` and `skills/spectrace-change` skills — covers R4, D4
- [x] 028/T005 [agent] Update `README.md` documentation — covers R5, D5
