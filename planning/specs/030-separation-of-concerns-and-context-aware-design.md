# 030 — separation-of-concerns-and-context-aware-design

## Goal

Decouple mixed responsibilities across the root governance documents (`ARCHITECTURE.md`, `DESIGN.md`, `TESTING.md`) and equip Agent Skills (`spectrace-plan`, `spectrace-review`, `spectrace-change`) with clear file boundaries and context-aware design scaffolding (UI/UX design vs Content/Documentation design for non-UI repos).

## Requirements

- R1: Define the industry-standard boundaries for each root file (`PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`, `AGENTS.md`) in `spectrace-plan` instructions.
- R2: Provide decoupled starter templates in `skills/spectrace-plan/assets/`:
  - `design-template.md`: strictly UI/UX, Design Tokens, typography, colors, layout, component states, and accessibility.
  - `design-docs-template.md`: for non-UI / documentation / governance repos (editorial style, headings, callouts, Mermaid diagrams, tone/voice, bilingual policy).
  - `testing-template.md`: testing invariants, contracts, input partitioning, AAA, table-driven tests, and boundary mocking.
  - `architecture-template.md`: architecture blueprint incorporating the Core Engineering Principles (KISS/YAGNI, SRP, DRY, DIP/ACL, stack conventions, trade-offs).
  - `agents-block.md`: updated to reflect the decoupled document suite.
- R3: Implement **Context-Aware Design** in `skills/spectrace-plan/SKILL.md` so that non-UI repositories do not scaffold inappropriate visual/CSS tokens.
- R4: Update `skills/spectrace-review/SKILL.md` to audit engineering principles against `ARCHITECTURE.md`, testing standards against `TESTING.md`, and visual standards against `DESIGN.md` (only when UI applies).
- R5: Update `spectrace`'s own root files:
  - Migrate Core Engineering Principles from `DESIGN.md` to `ARCHITECTURE.md`.
  - Create `TESTING.md` containing the testing invariants and hygiene standards.
  - Refactor `DESIGN.md` to reflect `spectrace`'s true nature as a Markdown/Skill repo (editorial and content design, callouts, diagrams, frontmatter standards).
  - Update `AGENTS.md` and `planning/roadmap.md` to align with the new structure.

## Design

- D1 (R1, R3): In `skills/spectrace-plan/SKILL.md`, add an explicit section detailing the single-responsibility matrix for repository files. Add branching logic: if the project has UI/UX, use `design-template.md`; if it is a documentation/governance repo, use `design-docs-template.md`; if pure API/CLI/backend, use an API contract design or omit visual tokens.
- D2 (R2): Split `skills/spectrace-plan/assets/design-template.md` into single-responsibility templates (`design-template.md`, `design-docs-template.md`, `testing-template.md`, `architecture-template.md`). Update `assets/agents-block.md`.
- D3 (R4): In `skills/spectrace-review/SKILL.md`, retarget the 10-principle audit checklist to reference the corresponding files (`ARCHITECTURE.md` for principles 1-5 & 8, `TESTING.md` for principles 6-7, `DESIGN.md` for visual/UI when applicable).
- D4 (R5): Update `spectrace`'s own `ARCHITECTURE.md`, `DESIGN.md`, `TESTING.md`, and `AGENTS.md`.

## Tasks

- [x] 030/T001 [agent] Create decoupled starter templates (`testing-template.md`, `design-docs-template.md`, update `design-template.md`, `architecture-template.md`, `agents-block.md`) in `skills/spectrace-plan/assets/` — covers R2, D2
- [x] 030/T002 [agent] Update `skills/spectrace-plan/SKILL.md` with file boundaries, web findings, and context-aware design logic — covers R1, R3, D1
- [x] 030/T003 [agent] Update `skills/spectrace-review/SKILL.md` to audit principles against their respective files (`ARCHITECTURE.md`, `TESTING.md`, `DESIGN.md`) — covers R4, D3
- [x] 030/T004 [agent] Update `skills/spectrace-change/SKILL.md` to reference `TESTING.md` and the decoupled file responsibilities — covers R1, D1
- [x] 030/T005 [agent] Restructure `spectrace` root files: move engineering principles to `ARCHITECTURE.md`, create `TESTING.md`, refactor `DESIGN.md` to content design, and update `AGENTS.md` — covers R5, D4
- [x] 030/T006 Verify: verify all skills, templates, and root documents locally for consistency and frontmatter validity — covers R1, R2, R3, R4, R5
      verified: all 3 skills validated with valid frontmatter; all assets created in skills/spectrace-plan/assets; ARCHITECTURE.md, DESIGN.md, TESTING.md, AGENTS.md aligned.
