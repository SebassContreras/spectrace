# 031 — extract-engineering-principles

## Goal

Extract code quality and craftsmanship rules from `ARCHITECTURE.md` into a dedicated root-level `ENGINEERING.md` contract across `spectrace`, its skills (`spectrace-plan`, `spectrace-review`, `spectrace-change`), and starter assets, achieving complete separation of concerns between structural topology and engineering principles.

## Requirements

- R1: Provide a dedicated `ENGINEERING.md` at repository root defining the Core Engineering Principles (KISS/YAGNI, SRP, DRY by composition, Anti-Corruption Layer/DIP, stack conventions/casing, and documented trade-offs).
- R2: Purify `ARCHITECTURE.md` to focus strictly on structural blueprints, system topology, component communication, layer boundaries, and directory maps.
- R3: Provide a new starter template `skills/spectrace-plan/assets/engineering-template.md`, clean `architecture-template.md`, and update `agents-block.md`.
- R4: Update `spectrace-plan`, `spectrace-review`, and `spectrace-change` skills to recognize, scaffold, and audit against `ENGINEERING.md`.
- R5: Update `spectrace/AGENTS.md` and `planning/roadmap.md` to reflect the 7-contract progressive disclosure suite.

## Design

- D1 (R1, R2): Move `## 🏛️ Core Engineering Principles` from `ARCHITECTURE.md` into a new `ENGINEERING.md`. `ARCHITECTURE.md` retains overview, stack, directory map, topology diagram, and structural invariants.
- D2 (R3): Add `skills/spectrace-plan/assets/engineering-template.md`. Strip engineering principles from `skills/spectrace-plan/assets/architecture-template.md`. Add `ENGINEERING.md` to `skills/spectrace-plan/assets/agents-block.md`.
- D3 (R4): In `skills/spectrace-plan/SKILL.md`, add `ENGINEERING.md` to the File Responsibilities table and first-time setup scaffold. In `skills/spectrace-review/SKILL.md`, retarget principles 1-6 to `ENGINEERING.md`. In `skills/spectrace-change/SKILL.md`, include `ENGINEERING.md` in pivot reviews.
- D4 (R5): Update `spectrace/AGENTS.md` blueprint and rules to cite `ENGINEERING.md`.

## Tasks

- [x] 031/T001 [agent] Create `skills/spectrace-plan/assets/engineering-template.md`, clean `architecture-template.md`, and update `agents-block.md` — covers R3, D2
- [x] 031/T002 [agent] Create root `ENGINEERING.md` and purify `ARCHITECTURE.md` in `spectrace` — covers R1, R2, D1
- [x] 031/T003 [agent] Update `skills/spectrace-plan/SKILL.md` to scaffold `ENGINEERING.md` and explain its specific role — covers R4, D3
- [x] 031/T004 [agent] Update `skills/spectrace-review/SKILL.md` and `skills/spectrace-change/SKILL.md` to audit and track `ENGINEERING.md` — covers R4, D3
- [x] 031/T005 [agent] Update `spectrace/AGENTS.md` and `planning/roadmap.md` to integrate `ENGINEERING.md` — covers R5, D4
- [x] 031/T006 Verify: verify all skills, templates, and root markdown documents for consistency, valid frontmatter, and non-overlapping responsibilities — covers R1, R2, R3, R4, R5
      verified: all 3 skills validated with valid frontmatter; all assets verified in skills/spectrace-plan/assets; ARCHITECTURE.md, ENGINEERING.md, DESIGN.md, TESTING.md, AGENTS.md aligned.
