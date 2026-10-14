# 008 — architecture-defaults — Design

## Approach

- D1@1 (implements R1): `skills/spectrace-start/references/templates.md` defines default A items for software architecture in `planning/architecture.md` templates under `## Conventions`: SRP & High Cohesion, Service Layer & Anti-Corruption, Composition over inheritance, Testability by default, and Pragmatic KISS/YAGNI.
- D2@1 (implements R2): `skills/spectrace-start/references/templates.md` adds default rules in `AGENTS.md` under `## Rules for agents`: following industry standards, researching details/examples on the web, and weighing pros and cons with mitigations for any design trade-offs.
- D3@1 (implements R3): `skills/spectrace-start/references/question-bank.md` references the default architectural principles in `code-conventions` and agent evaluation habits in `agent-rules`.
- D4@1 (implements R4): `skills/spectrace-plan/SKILL.md` incorporates guidance in Phase 1 (Design) for agents to cross-examine proposals against architecture items (A items), verify standards on the web, and document pros/cons and mitigations.
- D5@1 (implements R5): Maintain strict size budgets and validation in `tests/test_skills.py` ensuring all skills stay under 200 lines and follow Agent Skills specification.

## Deliverables

- `skills/spectrace-start/references/templates.md`
- `skills/spectrace-start/references/question-bank.md`
- `skills/spectrace-plan/SKILL.md`
- `tests/test_skills.py`
