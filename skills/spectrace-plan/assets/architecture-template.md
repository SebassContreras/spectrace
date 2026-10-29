# Architecture Blueprint & Engineering Principles

This document defines system architecture, directory boundaries, core technical patterns, and engineering principles. AI agents must consult this document before modifying system structure or implementing new modules.

---

## 🏛️ System Overview & Boundaries

### 1. Overview
[Brief description of the system, primary components, runtime, and infrastructure boundaries.]

### 2. Tech Stack & Dependencies
- **Runtime & Language:** [e.g. Node 20+, Python 3.12+, .NET 8, etc.]
- **Frameworks & Libraries:** [Core frameworks]
- **Storage & Infrastructure:** [Databases, caches, message queues]

### 3. Layer Boundaries & Directory Map
```text
src/
├── domain/         # Pure business logic and domain entities (zero external dependencies)
├── services/       # Application services and anti-corruption wrappers
├── adapters/       # Persistence, external APIs, and transport handlers
└── entrypoints/    # CLI, HTTP controllers, or message consumers
```

---

## ⚙️ Core Engineering Principles

AI agents must apply these principles proportionally to prevent code rot, over-engineering, and architectural drift.

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
