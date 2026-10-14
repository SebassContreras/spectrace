# 008 — architecture-defaults — Requirements

## What's being built

Default architecture and agent design guidelines embedded directly in spectrace skills:
1. Seed default software architecture principles in `planning/architecture.md` (SRP/cohesion, service layer/anti-corruption layer, composition over inheritance, pure/testable units, KISS/YAGNI).
2. Seed default research and trade-off rules in `AGENTS.md` (industry standards, web research, pro/con analysis with mitigation).
3. Ensure `spectrace-plan` enforces compliance with these architecture items when generating designs (`design.md`) and tasks (`tasks.md`).

## Who it serves

Developers and agents creating new projects or specs with spectrace, ensuring solid architectural foundations by default.

## Requirements

- R1@1: `skills/spectrace-start/references/templates.md` defines default A items for software architecture in `planning/architecture.md` (SRP, Service Layer/Anti-Corruption, Composition over inheritance, Testability, KISS/YAGNI).
- R2@1: `skills/spectrace-start/references/templates.md` includes default agent rules in `AGENTS.md` for industry standards, web search verification, and pros/cons analysis with trade-off mitigations.
- R3@1: `skills/spectrace-start/references/question-bank.md` notes in `code-conventions` and `agent-rules` that the architectural guide is provided by default.
- R4@1: `skills/spectrace-plan/SKILL.md` instructs agents during design to evaluate solutions against the architecture conventions, verify against web/industry standards, and detail trade-offs (pros, cons, and mitigations).
- R5@1: All skills continue to pass structural checks (`test_skills.py`), keeping bodies under 200 lines and valid frontmatter.

## Out of scope

- Creating separate skills for architecture reminders.
- Changing `trace.py` logic.

## Dependencies

002, 003.

## Owner split

All agent.
