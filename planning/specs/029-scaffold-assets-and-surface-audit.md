# 029 — scaffold-assets-and-surface-audit

## Goal

Equip `spectrace-plan` with deterministic starter templates (including the 10 engineering principles in `DESIGN.md`, `PRODUCT.md`, `CHANGES.md`, and `.agentignore`) and integrate Surface Alignment verification into `spectrace-review`.

## Requirements

- R1: Provide reusable starter templates in `skills/spectrace-plan/assets/` for `PRODUCT.md`, `DESIGN.md` (containing the 10 principles), `CHANGES.md`, and `.agentignore`.
- R2: Update `skills/spectrace-plan/SKILL.md` to instruct agents to use these assets during first-time project setup.
- R3: Update `skills/spectrace-review/SKILL.md` to enforce Surface Alignment (verifying that new public surfaces, commands, or layer boundaries are documented in `ARCHITECTURE.md` or `DESIGN.md`).
- R4: Update `planning/roadmap.md` to track spec 029 and retire the converted Surface Alignment idea from the backlog.

## Design

- D1 (R1): Create clean, standard templates in `skills/spectrace-plan/assets/`:
  - `product-template.md`: vision, audience, core problems, capabilities, and non-goals.
  - `design-template.md`: tokens, UI/UX conventions, and the 10 Core Engineering & Testing Principles.
  - `changes-template.md`: change protocol and ledger log table.
  - `agentignore-template`: standard context exclusion patterns for AI coding tools.
- D2 (R2): Update Step 4 of `skills/spectrace-plan/SKILL.md` so the first-time setup step references the asset templates.
- D3 (R3): Add a dedicated "Surface Alignment & Architectural Integrity" check in Step 2 of `skills/spectrace-review/SKILL.md`.
- D4 (R4): Add spec 029 to `planning/roadmap.md` with status `in progress` and remove the Surface Alignment idea from `## Ideas`.

## Tasks

- [x] 029/T001 [agent] Create starter templates in `skills/spectrace-plan/assets/` — covers R1, D1
- [x] 029/T002 [agent] Update `skills/spectrace-plan/SKILL.md` to scaffold with assets — covers R2, D2
- [x] 029/T003 [agent] Add surface alignment audit to `skills/spectrace-review/SKILL.md` — covers R3, D3
- [x] 029/T004 [agent] Update `planning/roadmap.md` with spec 029 and idea retirement — covers R4, D4
- [x] 029/T005 [agent] Verify all skills and files locally against spectrace standards — covers R1, R2, R3, R4
      verified: all asset files verified in skills/spectrace-plan/assets/, YAML frontmatter validated, and surface alignment rule added to spectrace-review.
