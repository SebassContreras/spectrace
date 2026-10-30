# 029 — scaffold-assets-and-surface-audit

## Goal

Equip `spectrace-plan` with deterministic starter templates (including the 10 engineering principles in `DESIGN.md`, `PRODUCT.md`, `CHANGES.md`, and `.agentignore`) and integrate Surface Alignment verification into `spectrace-review`.

## Requirements

- R1: Provide reusable starter templates in `skills/spectrace-plan/assets/` (`product-template.md`, `design-template.md`, `changes-template.md`, `.agentignore`) asserting the invariant that each template contains valid GitHub Flavored Markdown and complete section placeholders.
- R2: Update `skills/spectrace-plan/SKILL.md` to instruct agents to use these assets during first-time project setup.
- R3: Update `skills/spectrace-review/SKILL.md` to enforce Surface Alignment verification across 2 input partitions: (1) changes introducing or altering a public CLI/API/boundary surface, asserting documentation in `ARCHITECTURE.md` or `DESIGN.md`; (2) internal-only implementation changes where no public surface changes are asserted.
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

### Trade-offs & Mitigations (P10)
- Choice: Local bundled static templates in `skills/spectrace-plan/assets/` vs. network fetching or LLM dynamic generation.
  - Pros: 100% offline reliability, zero external network failure modes, deterministic contract baseline.
  - Cons: Assets must be maintained directly within the git repository.
  - Mitigation: Keep templates lean and unopinionated; domain-specific rules are filled in during project initialization.

## Tasks

- [x] 029/T001 [agent] Create starter templates in `skills/spectrace-plan/assets/` — covers R1, D1
- [x] 029/T002 [agent] Update `skills/spectrace-plan/SKILL.md` to scaffold with assets — covers R2, D2
- [x] 029/T003 [agent] Add surface alignment audit to `skills/spectrace-review/SKILL.md` — covers R3, D3
- [x] 029/T004 [agent] Update `planning/roadmap.md` with spec 029 and idea retirement — covers R4, D4
- [x] 029/T005 Verify: Validate assets and skills across input partitions using parameterized checks: (P1) valid YAML frontmatter and triggers in `spectrace-plan` and `spectrace-review`; (P2) all 4 asset templates exist and render without Markdown parse errors; (P3) surface alignment checklist correctly triggers on public API diffs — covers R1, R2, R3, R4
      verified: all asset files verified in skills/spectrace-plan/assets/, YAML frontmatter validated, and surface alignment rule added to spectrace-review.
