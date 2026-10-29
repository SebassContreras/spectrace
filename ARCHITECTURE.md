# Architecture Blueprint

## System Overview

Spectrace provides a lightweight, spec-driven development methodology tailored for autonomous and semi-autonomous AI coding agents. It transforms unstructured plans and ideas into verifiable thin-slice specifications while maintaining living architectural, testing, and design contracts at the repository root.

The framework operates through three core Agent Skills:
- **`spectrace-plan`**: Ingests plans, creates root contracts (with context-aware design), and cuts thin-slice specs.
- **`spectrace-change`**: Handles pivots, refactors, and clean deprecations without stale code.
- **`spectrace-review`**: Audits changes against Core Engineering Principles in `ARCHITECTURE.md`, Testing Standards in `TESTING.md`, and Design Compliance in `DESIGN.md`.

```mermaid
graph TD
    A[Human / High-Level Plan] -->|spectrace-plan| B[Root Directives & planning/]
    B --> C[Root Decision Layer]
    B --> D[planning/ Execution Layer]
    
    subgraph "Root Decision Layer (Context Contracts)"
        C1[AGENTS.md - Operational manual]
        C2[PRODUCT.md - Scope & vision]
        C3[ARCHITECTURE.md - Structural blueprints & Engineering principles]
        C4[DESIGN.md - UI/UX or Content design guidelines]
        C5[TESTING.md - Test invariants & hygiene]
        C6[CHANGES.md - Pivot & deprecation ledger]
    end

    subgraph "planning/ Execution Layer (Action Plan)"
        D1[roadmap.md - Ordered specs & status]
        D2[specs/NNN-name.md - Thin slices with tasks]
    end

    D2 -->|Agent executes task| E[Codebase Changes]
    E -->|spectrace-review| R[Audit Principles]
    R -->|Pass| F[Verify & Test]
    F -->|Check task box [x]| G[Update roadmap.md to done]
    
    H[Pivot or New Requirement] -->|spectrace-change| C6
    H -->|spectrace-change| D2
```

---

## Directory Organization

The repository strictly isolates **governance/decision contracts** at the project root from **transient action plans** in `planning/`.

```text
├── AGENTS.md               # Primary agent entrypoint (< 150 lines, pointers & DoD)
├── PRODUCT.md              # Vision, target users, problem statement, and scope boundaries
├── ARCHITECTURE.md         # Structural patterns, boundaries, and Core Engineering Principles
├── DESIGN.md               # Context-aware design: content/editorial rules or UI/UX tokens
├── TESTING.md              # Test invariants, input partitioning, and test hygiene
├── CHANGES.md              # Historical ledger of pivots, replacements, and deprecations
├── README.md               # Human-oriented overview, installation, and usage
│
├── planning/               # Pure execution and scheduling layer
│   ├── roadmap.md          # Specs sequence, dependencies, statuses, and idea backlog
│   └── specs/              # Atomic specification slices
│       ├── 001-scaffold.md
│       └── 002-feature.md
│
└── skills/                 # Agent Skills (agentskills.io specification)
    ├── spectrace-plan/     # Skill to generate specs, roadmap, and foundational docs
    ├── spectrace-change/   # Skill to manage architectural pivots and refactor cleanup
    └── spectrace-review/   # Skill to audit code against engineering and testing principles
```

---

## 🏛️ Core Engineering Principles

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
  - `PascalCase`: classes, types, interfaces, React components.
  - `camelCase`: functions, methods, variables, properties.
  - `UPPER_SNAKE_CASE`: true constants, configuration globals, enum keys.

### 6. Document Trade-offs
- Every significant technical choice has trade-offs.
- Document pros, cons, and active mitigations directly in the relevant spec, code comments, or `CHANGES.md`.

---

## Structural Boundaries & Invariants

1. **Root-Level Discovery:**
   - AI tools (Claude Code, Cursor, Copilot, Antigravity) automatically inspect root directory context on startup.
   - Core decisions (`ARCHITECTURE.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`) live at the root so agents instantly acquire boundaries without deep directory traversal.

2. **Execution Isolation in `planning/`:**
   - `planning/` contains **only** execution artifacts (`roadmap.md` and `specs/`).
   - Broad architecture discussions must never be siloed inside individual specs; when a spec introduces a durable architectural pattern, it must be documented in `ARCHITECTURE.md`.

3. **Zero Runtime & Zero Hook Dependency:**
   - Development is driven by Markdown checkboxes (`- [ ]` / `- [x]`) and standard Git commits.
   - No platform-dependent shell scripts or Git commit-message hooks are enforced, preventing tool breakage across operating systems.

4. **Skill Standards:**
   - Every skill in `skills/` complies with the Agent Skills specification (`SKILL.md` with YAML frontmatter `name` and `description` under 1024 characters).
