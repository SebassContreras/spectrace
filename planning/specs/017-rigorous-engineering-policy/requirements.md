# 017 — rigorous-engineering-policy — Requirements

## What's being built

An enforcement mechanism and guideline update across Spectrace skills (`spectrace-start`, `spectrace-plan`, `spectrace-change`, `spectrace-fix`) and project core documentation (`AGENTS.md`, `planning/architecture.md`, `references/templates.md`, `references/question-bank.md`) that prevents passive, uncritical agent agreement ("sycophancy") during interviewing and planning. It establishes 10 strict engineering principles (KISS/YAGNI, SRP, DRY via composition, Service Layer / Anti-Corruption, small testable dependencies, behavior-driven testing without trivial coverage, test hygiene AAA, idiomatic stack standards, research verification, and explicit trade-off / mitigation analysis) and requires agents to challenge assumptions, inquire about failure modes and real goals, and actively prevent accidental complexity before creating specs and tasks.

## Who it serves

Developers and engineering leads who rely on Spectrace to guide autonomous agents through discovery, architecture, planning, and task execution without taking premature or over-engineered architectural detours.

## Requirements

- R1@1: `AGENTS.md` and `skills/spectrace-start/references/templates.md` enforce the 10 Engineering Principles (KISS/YAGNI, SRP, DRY via Composition, Service Layer / Anti-Corruption, Injected Testable Dependency, Behavior-Focused Testing, AAA Testing Hygiene, Stack Idiom Standards, Research Verification, Documented Trade-offs & Mitigations) as mandatory agent rules.
- R2@1: `planning/architecture.md` records universal architecture decisions establishing that business logic must never couple directly to third-party SDKs/APIs (anti-corruption wrapper required) and that single-use abstractions are forbidden (proportionality / YAGNI).
- R3@1: `skills/spectrace-start/SKILL.md` and `skills/spectrace-start/references/question-bank.md` require the agent during the interview to critically evaluate requests, actively probe problem statements ("what exact problem does this solve and what observable outcome defines success?"), challenge unnecessary abstractions or premature scope, and inquire about failure modes and edge cases rather than accepting answers passively.
- R4@1: `skills/spectrace-plan/SKILL.md` requires that during Phase 1 (Design) and Phase 3 (Tasks), designs are verified against the 10 principles; tasks for tests must validate observable behavior or explicit failure modes (no vacuous getter/mock tests), and external vendor dependencies must be isolated behind an adapter/interface.
- R5@1: All modified skills conform to the size budget (body at most 200 lines per A5) and `tests/test_skills.py` passes.

## Out of scope

- Creating an external automated linter for conversational tone.
- Modifying SQLite index schemas or `trace.py` binary protocols.

## Dependencies

- 008 (architecture-defaults)
- 009 (testing-policy)

## Owner split

- `agent`: Update skills, templates, question bank, architectural rules, and verify skill limits and test suites.
- `human`: Review the resulting policy and interview prompts.
