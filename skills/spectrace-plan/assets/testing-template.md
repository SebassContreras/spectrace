# Testing Standards & Verification Guidelines

This document governs testing philosophy, contract invariants, test partitioning, and test hygiene. AI agents must follow these rules when writing automated tests or auditing test suites.

---

## 🧪 Testing Invariants & Input Partitioning

AI agents must write deterministic tests that assert domain contracts rather than surface-level happy-path anecdotes.

### 1. Systematic Input Partitioning
Cover the observable input space systematically:
- **Valid Nominal Cases:** Typical valid inputs and expected permutations.
- **Boundary Values:** Minimum, maximum, `boundary - 1`, `boundary + 1`, and off-by-one conditions.
- **Malformed & Empty Inputs:** Empty strings, empty collections, `null` / `undefined`, and unexpected types.
- **Compound Errors:** Simultaneous invalid fields to verify error aggregation without premature crashes.

### 2. Contract Suites over Fragmented Tests
- If multiple components or services modify the same state or share validation rules, write a shared contract test suite that runs uniformly against all writers.
- Assert rules at the invariant boundary rather than duplicating tests across entry points.

### 3. Root-Cause Regressions via Equivalence Classes
- When fixing a bug, never write a test that only asserts the single reported failing payload.
- Identify the underlying missing equivalence class or violated invariant, and assert the generalized invariant across all entry points that accept that shape.

### 4. Property & State Transitions
- Assert state machine lifecycles and invariants (uniqueness, idempotency, monotonic counters, serialization/deserialization round-trips) rather than isolated static properties.

---

## 🧼 Test Hygiene & Parameterization

### 1. AAA / Given-When-Then Structure
- Organize every test into three distinct phases: **Arrange** (set up preconditions), **Act** (execute the target behavior), and **Assert** (verify observable outcomes).
- Use descriptive behavioral test names stating the expected outcome under specific conditions (e.g., `test_rejects_expired_token_with_unauthorized_status`).

### 2. Parameterized & Table-Driven Tests
- Use native test table capabilities (`test.each`, `@pytest.mark.parametrize`, Go test tables) to test matrices of inputs and boundary values compactly.
- Keep table rows readable with explicit test case descriptions.

### 3. Clean Test Bodies
- No conditional branching (`if`/`else`), ternary operators, or manual loops inside test execution blocks. Branching in tests hides unexercised paths.

### 4. Isolate & Mock at Boundaries
- **Never mock the unit under test:** Test the real component logic.
- **Mock only external boundaries:** Network requests, external third-party APIs, disk I/O, or clock/timers when non-deterministic.
