# Design & Style Guidelines

This document governs visual UI/UX conventions, engineering architecture principles, and rigorous testing standards. AI agents must follow these rules when implementing interfaces, writing code, or auditing changes.

---

## 🎨 Visual & UI/UX Standards

### 1. Design Token Strategy
- **Tokens over Raw Values:** Always use semantic design tokens or CSS variables. Never hardcode arbitrary hex codes, pixel margins, or magic numbers.
- **Color Semantics:**
  - `primary`: Core actions, primary buttons, and key interactive focal points.
  - `surface` / `background`: Background tiers for cards, panels, and body.
  - `muted`: Subdued text, secondary borders, and placeholders.
  - `destructive` / `danger`: Destructive actions, error states, and warnings.
- **Spacing Scale:** Adhere to a standard 4px / 8px incremental scale (`4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`).

### 2. Component Hierarchy & Layout
- **Composition over Inheritance:** Build composite components from tested primitives.
- **Responsive Layout:** Design mobile-first or fluid layout using Flexbox and Grid. Avoid fixed viewport widths.
- **State Feedback:** Every interactive control must declare clear hover, focus, active, disabled, and loading states.

### 3. Accessibility (A11y)
- **Contrast:** Maintain WCAG AA compliant contrast ratios for all text elements.
- **Keyboard Navigation:** All interactive elements must be focusable with visible focus rings.
- **Semantics:** Use standard HTML tags (`<button>`, `<nav>`, `<main>`, `<dialog>`) instead of nested `<div>`s with click handlers. Include `aria-label` when visual labels are omitted.

---

## 🏛️ Core Engineering Principles

AI agents must apply these 10 principles proportionally to prevent code rot, over-engineering, and architectural drift.

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

### 5. When in Doubt
When facing uncertainty in design:
- Prefer a **small interface**.
- Prefer a **pure function** (deterministic, no hidden side-effects).
- Prefer an **injected, easily testable dependency**.

### 6. Follow the Stack's Standards
- Strictly adhere to official conventions, idiomatic patterns, and style guides of the language and framework in use.
- Harmonize with the existing codebase before introducing external stylistic preferences.
- Standard casing: `kebab-case` for files; `PascalCase` for classes/types/components; `camelCase` for functions/variables; `UPPER_SNAKE_CASE` for constants.

### 7. Validate with Research
- Before committing to an approach, library choice, or unfamiliar API design, search documentation and real-world examples to verify current best practices. Do not guess API signatures.

### 8. Document Trade-offs
- Every significant technical choice has trade-offs.
- Document pros, cons, and active mitigations directly in the relevant spec, code comments, or `CHANGES.md`.

---

## 🧪 Testing Standards — Invariants, Contracts & Hygiene

AI agents must write robust, deterministic tests that assert domain contracts rather than surface-level happy-path anecdotes.

### 9. Testing Invariants, Contracts & Input Space (Not Anecdotal Examples)
Test observable behavior and business invariants through systematic input partitioning:
- **Input Partitioning:**
  - **Valid cases:** Typical nominal inputs and valid permutations.
  - **Boundary values:** Min, max, boundary - 1, boundary + 1, off-by-one conditions.
  - **Malformed / Empty inputs:** Empty strings, empty collections, null/undefined, unexpected types.
  - **Compound errors:** Simultaneous invalid fields to verify error aggregation without premature crashes.
- **Contract Suites over Manual Combinations:**
  - If multiple tools or services modify the same state or share validation rules, write a shared contract suite that runs uniformly against every writer.
- **Root-Cause Regressions via Equivalence Classes:**
  - When fixing a bug, identify the underlying missing equivalence class or violated invariant, and test the generalized rule across all entry points that accept that shape.
- **Property & State Transitions:**
  - Test state machine lifecycles and invariants (uniqueness, idempotency, monotonic counters, serialization/deserialization round-trips).

### 10. Testing Hygiene & Parameterization
- **Given-When-Then / Arrange-Act-Assert (AAA):** Structure all test functions with clear arrange, act, and assert blocks using behavior-descriptive test names.
- **Parameterized / Table-Driven Tests:**
  - Use native data tables (`test.each`, `@pytest.mark.parametrize`, Go test tables) to test matrices of inputs and boundary values compactly.
- **Clean Test Bodies:**
  - No branching logic (`if`/`else`) or manual loops inside test execution blocks.
- **Isolate & Mock at Boundaries:**
  - Never mock the unit under test. Mock only external boundaries (network, filesystem, databases, third-party APIs).
