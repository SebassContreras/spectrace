---
name: spectrace-review
description: >-
  Audits code changes, pull requests, or completed spec tasks against the repository's
  10 core engineering and testing principles (KISS/YAGNI, SRP, Anti-Corruption Layer,
  Invariant Testing, Input Partitioning, Clean Table-Driven Test Bodies) defined in
  DESIGN.md. Generates an actionable findings report without modifying code. Use when:
  "review this code", "audit this spec", "check code quality", "run review", "review tasks",
  "audit PR", "verify engineering standards".
---

# spectrace-review

Run **inside the target repo**. This skill performs an objective, read-only architectural and testing audit of recent changes or completed tasks before a spec is finalized.

---

## Step 1 — Gather Diff & Context

1. Identify the changes under review:
   - For working tree changes: `git diff` and `git diff --cached`.
   - For recent commits: `git diff HEAD~1` (or the branch divergence `git diff main...HEAD`).
2. Read the governing documents:
   - [DESIGN.md](../../DESIGN.md) (the 10 engineering and testing principles).
   - [ARCHITECTURE.md](../../ARCHITECTURE.md) (layer boundaries and dependencies).
   - The active spec in `planning/specs/NNN-name.md` (verifying requirement coverage).

---

## Step 2 — Execute the 10-Point Audit

Audit the diff systematically against each principle. For each violation, cite the exact file and line number.

### 1. KISS / YAGNI — Proportionality
- [ ] **No Premature Abstractions:** Are there interfaces, adapters, or factory classes created for a single consumer or vendor?
- [ ] **No Speculative Flexibility:** Is there code written for hypothetical future requirements?
- [ ] **Simple > Clever:** Is the implementation direct and readable without unnecessary metaprogramming?

### 2. SRP / Separation of Concerns
- [ ] **Single Responsibility:** Does each new or modified file have a single, well-defined purpose?
- [ ] **Layer Isolation:** Is domain logic cleanly separated from persistence, external APIs, and presentation?

### 3. Composition over Inheritance
- [ ] **Composition First:** Is shared logic extracted into injectable utilities, services, or functions?
- [ ] **No Deep Inheritance:** Are class hierarchies shallow? (Inheritance allowed only for genuine is-a or Template Method).

### 4. Service Layer & Anti-Corruption (DIP)
- [ ] **Vendor Isolation:** Are third-party SDKs, libraries, or APIs called directly from business logic? (Must be wrapped in `services/` or `adapters/`).
- [ ] **Swappable Interface:** Does the domain depend on project-owned interfaces rather than external vendor types?

### 5. Design Simplicity
- [ ] **Minimal Seams:** Are newly introduced interfaces minimal and focused?
- [ ] **Pure Functions:** Are state transformations pure and deterministic where feasible?

### 6. Testing Invariants, Contracts & Input Space
- [ ] **Systematic Input Partitioning:**
  - Are valid nominal cases covered?
  - Are boundary values explicitly tested (min, max, off-by-one)?
  - Are empty/malformed payloads covered (null, empty strings, invalid structures)?
  - Are compound errors tested (multiple invalid fields simultaneously)?
- [ ] **Contract Suites over Ad-Hoc Tests:** If multiple writers modify the same state or share validation rules, is there a shared contract test suite rather than scattered individual tests?
- [ ] **Root-Cause Regressions:** If fixing a bug, does the test cover the general equivalence class across all entry points rather than just the exact reported payload?
- [ ] **State Machine & Lifecycle Transitions:** Are state transitions (idempotency, uniqueness, serialization round-trips) asserted?

### 7. Testing Hygiene & Parameterization
- [ ] **AAA Structure:** Are tests structured as Arrange-Act-Assert with descriptive behavioral names?
- [ ] **Parameterized / Table-Driven Tests:** Are matrices of inputs and boundaries expressed via data tables (`test.each`, `@pytest.mark.parametrize`) rather than copy-pasted test functions?
- [ ] **Clean Test Bodies:** Are test bodies free of `if`/`else` branches, ternary operators, and manual loops?
- [ ] **Boundary Mocking Only:** Is the unit under test completely unmocked? Are only external boundaries (I/O, network) mocked?

### 8. Stack Standards & Idioms
- [ ] **Official Conventions:** Does the code strictly follow the idiomatic style, naming conventions, and lint standards of the language/framework?

### 9. Validation Evidence
- [ ] **Verification:** Are test suite runs or verification commands recorded with passing evidence?

### 10. Documented Trade-offs
- [ ] **Trade-off Notes:** If a complex design choice was made, are pros, cons, and mitigations documented in comments or spec notes?

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
