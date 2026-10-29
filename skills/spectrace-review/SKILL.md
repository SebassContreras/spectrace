---
name: spectrace-review
description: >-
  Audits code changes, pull requests, or completed spec tasks against the repository's
  Core Engineering Principles in ENGINEERING.md, Testing Standards in TESTING.md,
  Structural Boundaries in ARCHITECTURE.md, and Visual/Content standards in DESIGN.md.
  Generates an actionable findings report without modifying code. Use when:
  "review this code", "audit this spec", "check code quality", "run review",
  "review tasks", "audit PR", "verify engineering standards".
---

# spectrace-review

Run **inside the target repo**. This skill performs an objective, read-only architectural, engineering, testing, and design audit of recent changes or completed tasks before a spec is finalized.

---

## Step 1 — Gather Diff & Context

1. Identify the changes under review:
   - For working tree changes: `git diff` and `git diff --cached`.
   - For recent commits: `git diff HEAD~1` (or the branch divergence `git diff main...HEAD`).
2. Read the governing documents:
   - [ENGINEERING.md](../../ENGINEERING.md) (Core Engineering Principles: KISS/YAGNI, SRP, DRY, DIP/ACL, stack casing).
   - [ARCHITECTURE.md](../../ARCHITECTURE.md) (system topology, layer boundaries, and public surfaces).
   - [TESTING.md](../../TESTING.md) (testing invariants, input partitioning, table tests, and mocking boundaries).
   - [DESIGN.md](../../DESIGN.md) (UI tokens/a11y for frontend apps; content/editorial conventions for docs repos).
   - The active spec in `planning/specs/NNN-name.md` (verifying requirement coverage).

---

## Step 2 — Execute the Audit Checklist

Audit the diff systematically against each document. For each violation, cite the exact file and line number.

### ⚙️ Engineering Principles (Governed by ENGINEERING.md)

#### 1. KISS / YAGNI — Proportionality
- [ ] **No Premature Abstractions:** Are there interfaces, adapters, or factory classes created for a single consumer or vendor?
- [ ] **No Speculative Flexibility:** Is there code written for hypothetical future requirements?
- [ ] **Simple > Clever:** Is the implementation direct and readable without unnecessary metaprogramming?

#### 2. SRP / Separation of Concerns
- [ ] **Single Responsibility:** Does each new or modified file have a single, well-defined purpose?
- [ ] **Layer Isolation:** Is domain logic cleanly separated from persistence, external APIs, and presentation?

#### 3. Composition over Inheritance
- [ ] **Composition First:** Is shared logic extracted into injectable utilities, services, or functions?
- [ ] **No Deep Inheritance:** Are class hierarchies shallow? (Inheritance allowed only for genuine is-a or Template Method).

#### 4. Service Layer & Anti-Corruption (DIP)
- [ ] **Vendor Isolation:** Are third-party SDKs, libraries, or APIs called directly from business logic? (Must be wrapped in `services/` or `adapters/`).
- [ ] **Swappable Interface:** Does the domain depend on project-owned interfaces rather than external vendor types?

#### 5. Design Simplicity & Stack Conventions
- [ ] **Minimal Seams:** Are newly introduced interfaces minimal and focused?
- [ ] **Pure Functions:** Are state transformations pure and deterministic where feasible?
- [ ] **Official Conventions:** Does the code strictly follow the idiomatic style, naming conventions, and lint standards of the language/framework?

#### 6. Documented Trade-offs
- [ ] **Trade-off Notes:** If a complex design choice was made, are pros, cons, and mitigations documented in comments, `CHANGES.md`, or spec notes?

---

### 🏛️ Structural & Layer Boundaries (Governed by ARCHITECTURE.md)

#### 7. Architecture & Dependency Flow
- [ ] **Dependency Inversion:** Do dependencies point inward toward domain models? Are adapters prohibited from leaking into domain code?
- [ ] **Directory Integrity:** Are new files placed strictly within the declared directory map?

---

### 🧪 Testing Standards (Governed by TESTING.md)

#### 8. Testing Invariants, Contracts & Input Space
- [ ] **Systematic Input Partitioning:**
  - Are valid nominal cases covered?
  - Are boundary values explicitly tested (min, max, off-by-one)?
  - Are empty/malformed payloads covered (null, empty strings, invalid structures)?
  - Are compound errors tested (multiple invalid fields simultaneously)?
- [ ] **Contract Suites over Ad-Hoc Tests:** If multiple writers modify the same state or share validation rules, is there a shared contract test suite rather than scattered individual tests?
- [ ] **Root-Cause Regressions:** If fixing a bug, does the test cover the general equivalence class across all entry points rather than just the exact reported payload?
- [ ] **State Machine & Lifecycle Transitions:** Are state transitions (idempotency, uniqueness, serialization round-trips) asserted?

#### 9. Testing Hygiene & Parameterization
- [ ] **AAA Structure:** Are tests structured as Arrange-Act-Assert with descriptive behavioral names?
- [ ] **Parameterized / Table-Driven Tests:** Are matrices of inputs and boundaries expressed via data tables (`test.each`, `@pytest.mark.parametrize`, Go tables) rather than copy-pasted test functions?
- [ ] **Clean Test Bodies:** Are test bodies free of `if`/`else` branches, ternary operators, and manual loops?
- [ ] **Boundary Mocking Only:** Is the unit under test completely unmocked? Are only external boundaries (I/O, network) mocked?

---

### 🎨 Design & Content Alignment (Governed by DESIGN.md)

#### 10. Context-Aware Design Compliance
- [ ] **UI Projects (Frontend / Web / Mobile):**
  - **Tokens over Raw Values:** Are colors, spacing, and font sizes using semantic tokens (no hardcoded hex/px)?
  - **Component States:** Do interactive controls support hover, focus, active, disabled, loading?
  - **Accessibility (A11y):** Are WCAG AA contrast, keyboard navigation, and `aria-label` attributes respected?
- [ ] **Documentation / Governance Repos:**
  - **Hierarchy & Format:** Is frontmatter metadata complete? Are standard alert callouts (`> [!NOTE]`) and Mermaid syntax valid?
  - **No UI Fluff:** Confirm that no inappropriate CSS tokens or HTML component styles have been injected.

---

### 🔍 Surface Alignment & Spec Traceability

#### 11. Public Surface Documentation & Scope Integrity
- [ ] **Public Surface Documentation:** If a public API, endpoint, CLI command, tool, or domain model was introduced or changed, is it documented in `ARCHITECTURE.md`, `ENGINEERING.md`, or `DESIGN.md`?
- [ ] **Strict Spec Coverage:** Does the diff align with the active task scope (`— covers R/D` or `— replaces D`) without undocumented side-effects?

---

## Step 3 — Report Findings

Output the audit report in the conversation:

```markdown
# Engineering & Architecture Audit Report

**Target:** <Spec ID or commit range>
**Verdict:** [PASS | NEEDS_REFACTOR | BLOCKED]

### 🚨 Blockers (Must fix before closing spec)
- **Principle [X] - [Name]:** `path/to/file.ext:L12-L18` — Explanation of violation and required fix.

### ⚠️ Warnings (Clean up to prevent tech debt)
- **Principle [X] - [Name]:** `path/to/file.ext:L45` — Explanation of recommended improvement.

### 💡 Commendations / Highlights
- Notable adherence to invariants, clean table tests, or anti-corruption layers.

### 📋 Recommended Remediation Tasks
- [ ] NNN/TNNN [agent] Refactor <component> to remove premature interface — covers D1
- [ ] NNN/TNNN [agent] Parameterize test matrix for <function> using table tests — covers R2
```

**Stop.** Do not make code edits during the review. Allow the user or executing agent to implement the remediation tasks.
