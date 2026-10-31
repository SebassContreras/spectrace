# Architecture & Decision Changes

This document maintains a permanent ledger of architectural pivots, deprecated decisions, and significant scope modifications. It prevents agents from reintroducing rejected patterns and provides context on why the system evolved.

---

## 🔄 Change Protocol

When an existing architectural design or requirement needs to change:

1. **Document the Rationale:** Add a new entry to the [Change Log](#change-log) below with date, what changed, why, and what was replaced.
2. **Update the Spec:** In the affected spec (`planning/specs/NNN-name.md`):
   - Strike through the obsolete item and point to the replacement (e.g., `- ~~D1: Sessions in localStorage~~ → D2`).
   - Add explicit cleanup tasks to remove obsolete code, tests, and documentation.
3. **Update Root Context:** If the change modifies system boundaries or visual guidelines, update [PRODUCT.md](./PRODUCT.md), [ARCHITECTURE.md](./ARCHITECTURE.md), or [DESIGN.md](./DESIGN.md) accordingly.

---

## 📜 Change Log

### 2026-10-31 — Principle 7: Validate with Research, Propagated to Every Entry Point

- **Scope:** Engineering standards, starter asset, `spectrace-init`, `spectrace-plan`, `spectrace-review`, `bin/spectrace-init.mjs`, and `ARCHITECTURE.md` invariant 4.
- **What Changed:**
  - Added `### 7. Validate with Research — Only When It Changes the Decision` to `ENGINEERING.md`: research only when the choice is hard to reverse, depends on a fact outside the repository, or breaks a factual tie; fixed source order; citations as `Source: <url> (accessed YYYY-MM-DD)`.
  - Mirrored the section in `skills/spectrace-plan/assets/engineering-template.md`, so every scaffolded repository inherits it.
  - Upgrade and adoption paths now reconcile an existing `ENGINEERING.md` instead of skipping it: `spectrace-init` Step 3, `spectrace-plan` Step 4 and `bin/spectrace-init.mjs` append the principle sections the file lacks, keep repository-specific principles, and never overwrite.
  - `spectrace-review` flags an uncited hard-to-reverse choice and contract drift: a principle the skill lists, missing from `ENGINEERING.md`, with no excusing entry here.
  - Every enumeration now lists the same seven principles: init table and Step 2, plan table and Step 4, the review read-list, `assets/agents-block.md` and this repository's `AGENTS.md`.
- **Why:**
  - Research had no home after the extraction of six principles, so agents either guessed platform facts or browsed ritualistically.
  - A principle that lives only in this repository never reaches repositories that already carry `ENGINEERING.md`. The enumerations had already drifted: four of six lists omitted trade-offs.
- **Rejected Alternative — do not reintroduce:** Mandatory research on every task (invites invented citations and ritual browsing); overwriting `ENGINEERING.md` from the template on upgrade (destroys repository-specific principles); leaving propagation to memory without an invariant (it fails silently, as the trade-offs omission shows).

### 2026-10-31 — Small Fixes Tracked by Git, Not by a Fix List

- **Scope:** Bug and correction routing (`spectrace-change`, `AGENTS.md` block).
- **What Changed:**
  - `spectrace-change` Step 4 now routes by size: a **trivial correction** (breaks no `R`/`D`, one commit) gets no `planning/` entry — the `fix:`/`docs:` commit is the record; a **bug against a requirement** adds regression and fix tasks to the owning spec, reopening it (`done` → `in progress`) when needed; a fix that needs a different `R`/`D` goes through the change-of-direction protocol.
  - Added a `Small Fixes` section to the `AGENTS.md` block and to this repo's `AGENTS.md`.
  - `## Ideas` explicitly accepts small fixes that won't be done right away.
- **Why:**
  - The bug route told agents to add tasks to a spec, but "done specs stay done" (spec 021) left no place for bugs in finished specs, so agents either inflated fixes into new specs or recorded nothing.
  - Corrections that violate no requirement (typos, stale docs) did not fit any category.
- **Rejected Alternative — do not reintroduce:** A `## Fixes` checklist in `planning/roadmap.md` (or a `planning/fixes.md` file, or a `spectrace-fix` skill). It duplicates what `git log` already records, needs manual cleanup, and turns spectrace into an issue tracker, which `PRODUCT.md` lists as a non-goal. Spec 021 already removed `spectrace-fix` and moved tracking to git for the same reason.
- **Replaced Items:** "Done specs stay done" now applies only to changes of direction; bugs reopen their spec.

### 2026-10-28 — Engineering Standards & spectrace-review Skill Integration

- **Scope:** Code quality governance and testing discipline.
- **What Changed:**
  - Codified the 10 Core Engineering & Testing Principles in `DESIGN.md` (KISS/YAGNI, SRP, Anti-Corruption Layer/DIP, Invariant Testing, Input Partitioning, Clean Table-Driven Tests).
  - Created the read-only audit skill `spectrace-review` to evaluate code changes and task completions against these 10 principles without modifying code.
  - Added engineering constraints and anti-abstraction rules directly into `AGENTS.md`.
- **Why:**
  - Autonomous agents frequently introduce premature abstractions (single-use interfaces/factories) or shallow, anecdotal happy-path tests that fail to catch boundary regressions.
  - Providing explicit invariant standards and an auditing tool ensures code cleanliness without manual human micromanagement.

### 2026-10-28 — Foundation Realignment: Pure Markdown & Root Architecture

- **Scope:** Repository foundation & execution mechanics.
- **What Changed:**
  - Removed all POSIX Git hooks (`.githooks/`), trailer verification scripts (`check-trailers`), and CI trailer enforcement workflows.
  - Eliminated the mandatory `Spec: NNN/TNNN` commit trailer requirement in favor of standard Conventional Commits.
  - Relocated core decision contracts to the repository root: `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `CHANGES.md`.
  - Established `PRODUCT.md` at root to cleanly isolate vision, personas, and product scope boundaries from structural architecture, deprecating `planning/product.md`.
  - Focused `planning/` strictly on actionable execution (`roadmap.md` and `specs/NNN-*.md`).
  - Updated skills (`spectrace-plan` and `spectrace-change`) to generate and manage this streamlined structure.
- **Why:**
  - Shell-based Git hooks caused persistent friction and blocking errors across cross-platform environments (notably Windows path/CRLF discrepancies).
  - Enforcing rigid trailers on every micro-commit interrupted natural agent workflows and created friction without improving code quality.
  - Moving architecture and design contracts to the root maximizes immediate discovery for modern AI agents (Cursor, Claude Code, Copilot, Antigravity) via progressive disclosure.
- **Replaced Items:**
  - `~~Specs 021–027~~`: Git hooks, trailer checkers, and CI trailer validations retired.
