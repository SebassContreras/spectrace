# 017 — rigorous-engineering-policy — Design

## Approach

Embed and enforce the 10 Engineering Principles (KISS/YAGNI, SRP/Separation of Concerns, DRY via Composition, Service Layer & Anti-Corruption, Small & Testable Dependencies, Behavior-driven Testing, AAA Testing Hygiene, Stack Idiom Standards, Web Research Verification, Documented Trade-offs with Mitigations) directly across Spectrace's core operational documents, skill instructions, question banks, and templates.

- D1@1 (implements R1, R2): Record universal architectural decisions in `planning/architecture.md` (and propagate to `skills/spectrace-start/references/templates.md` and `AGENTS.md`) establishing that:
  - Third-party SDKs, APIs, and libraries must never be coupled directly to core business logic; they must be wrapped behind a service/adapter interface and injected (Service Layer / Anti-Corruption Layer / Dependency Inversion).
  - Single-use abstractions, speculative interfaces, and premature adapters are prohibited (KISS / YAGNI proportionality: abstract only with 2+ concrete uses/vendors or when testing boundaries strictly require it).
  - High cohesion, single responsibility (SRP), composition over inheritance, and small, pure functions with testable injected dependencies are mandatory conventions.
- D2@1 (implements R1): Update `AGENTS.md` and the `AGENTS.md` template in `skills/spectrace-start/references/templates.md` under "Rules for agents" to formally mandate all 10 Engineering Principles:
  1. KISS / YAGNI — No Over-Engineering: Proportionality; start simple and direct; abstract only for 2+ uses/vendors or isolation for testing.
  2. SRP / Separation of Concerns: One responsibility per file/module/class; split multi-concern units.
  3. DRY via Composition, not Inheritance: Extract shared logic into injectable helpers/services; avoid deep inheritance.
  4. Service Layer + Anti-Corruption / Dependency Inversion: Wrap external libraries/APIs in adapter interfaces; business logic depends on interfaces, not vendors.
  5. Small interface, pure function, injected and testable dependency.
  6. Testing — Behavior, not Coverage: Test observable behavior and explicit failure modes; regression test before every bug fix; never weaken tests to pass code.
  7. Testing Hygiene: Strict Given-When-Then / Arrange-Act-Assert; clear behavior-stating test names; no conditionals/loops in tests; mock boundary dependencies only.
  8. Follow the Stack's Standards: Idiomatic conventions, official style guides, and codebase consistency.
  9. Web Research for Verification: Confirm choices, libraries, and APIs with official documentation and research before committing.
  10. Documented Trade-offs & Mitigations: Detail pros and cons of technical decisions; specify and implement concrete mitigations.
- D3@1 (implements R3): Update `skills/spectrace-start/SKILL.md` and `skills/spectrace-start/references/question-bank.md` to establish anti-sycophancy and active probing behaviors during the interview:
  - Add explicit probing directives to Phase A (`idea-detail`, `goal`, `mvp`) and Phase B (`framework`, `interface`, `datastore`) instructing the agent to challenge vague requirements, probe underlying problems and measurable success criteria, question premature abstractions/dependencies, and actively inquire about failure modes and edge cases.
- D4@1 (implements R4): Update `skills/spectrace-plan/SKILL.md` in Phase 1 (Design) and Phase 3 (Tasks) to require design review against the 10 engineering principles, ensure adapter interfaces isolate third-party dependencies, and enforce that task generation strictly produces behavior-driven test tasks covering real failure modes and observable outcomes (rejecting trivial getter/mock tests).
- D5@1 (implements R5): Audit and verify line counts across all modified skill files (`skills/spectrace-start/SKILL.md`, `skills/spectrace-plan/SKILL.md`) to guarantee strict compliance with the 200-line size budget (A5), and ensure `tests/test_skills.py` passes cleanly.

## Deliverables

- `AGENTS.md`: Update "Rules for agents" with the complete 10 principles.
- `planning/architecture.md`: Record new universal architecture decisions (A16, A17).
- `skills/spectrace-start/references/templates.md`: Update `AGENTS.md` and architecture templates.
- `skills/spectrace-start/references/question-bank.md`: Add active inquiry and anti-sycophancy probing prompts.
- `skills/spectrace-start/SKILL.md`: Incorporate critical requirement evaluation guidance while adhering to line budgets.
- `skills/spectrace-plan/SKILL.md`: Enforce principles in Phase 1 and Phase 3 task breakdown while adhering to line budgets.
- `tests/test_skills.py`: Verification that all skills adhere to A5 line budgets.

## Sequencing

1. Record architecture decisions in `planning/architecture.md`.
2. Update templates in `skills/spectrace-start/references/templates.md` and project rules in `AGENTS.md`.
3. Update `skills/spectrace-start/references/question-bank.md` and `skills/spectrace-start/SKILL.md`.
4. Update `skills/spectrace-plan/SKILL.md`.
5. Run line-budget and skill tests (`tests/test_skills.py`) to confirm zero budget regressions.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Enforce principles via skill prompts and templates rather than code linters | Universal across languages and project types without heavyweight AST parsing | Relies on LLM adherence to instructions in `AGENTS.md` and skills | Prompts are made explicit, directive, and embedded in task review gates (Phase 2 & Phase 4) |
| Add comprehensive engineering principles to `AGENTS.md` rules | Agents automatically adopt the 10 principles in every task prompt context | Increases token size of `AGENTS.md` slightly | Keep phrasing concise, bulleted, and actionable |
| Compress additions in `SKILL.md` files | Guarantees compliance with strict 200-line budget (A5) | Less room for extensive narrative explanations in `SKILL.md` | Place detailed explanations in `references/question-bank.md` and `references/templates.md` which have separate line budgets |
