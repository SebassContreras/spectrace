# Engineering Principles & Code Standards

This document defines the craftsmanship, code quality standards, and software engineering principles for this repository. AI agents must apply these principles proportionally to prevent code rot, over-engineering, and architectural drift.

---

## ⚙️ Core Engineering Principles

### 1. KISS / YAGNI — No Over-Engineering
- Apply every principle with proportionality.
- Do not create premature interfaces, adapters, or abstractions for a single use case or a hypothetical future.
- Introduce an abstraction **only** when there are 2+ concrete uses, 2+ distinct vendors/implementations, or when automated testing genuinely requires a boundary seam.
- **Simple > clever:** Prefer readable, straightforward code over complex metaprogramming or speculative design patterns.

### 2. SRP / Separation of Concerns
- One file / module / class = one single responsibility.
- Maximize cohesion, minimize coupling. If a unit does two unrelated things, split it cleanly.
- Keep business domain logic, data persistence, and transport/presentation layers strictly separated.

### 3. DRY via Composition, Not Inheritance
- Avoid code duplication by extracting shared logic into small, injectable utilities, services, or helper functions.
- Avoid deep inheritance hierarchies. Default to **composition + dependency injection**.

### 4. Service Layer + Anti-Corruption / Dependency Inversion (DIP)
- Never call third-party libraries, vendor SDKs, or external APIs directly from domain business logic.
- Place an anti-corruption layer in `services/` or `adapters/` declaring your own project-scoped interface wrapper.
- Inject that interface into domain logic. Vendors must be swappable without altering domain code.

### 5. Follow the Stack's Standards
- Strictly adhere to official conventions, idiomatic patterns, and style guides of the language and framework in use.
- Harmonize with the existing codebase before introducing external stylistic preferences.
- Standard casing:
  - `kebab-case`: files, directories, Markdown documents.
  - `PascalCase`: classes, types, interfaces, components.
  - `camelCase`: functions, methods, variables, properties.
  - `UPPER_SNAKE_CASE`: true constants, configuration globals, enum keys.

### 6. Document Trade-offs
- Every significant technical choice has trade-offs.
- Document pros, cons, and active mitigations directly in the relevant spec, code comments, or `CHANGES.md`.
