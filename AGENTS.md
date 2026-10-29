# AGENTS.md

Instructions and operational constraints for AI coding agents.

## 🚀 Quick Reference & Commands
- **Environment:** Pure Markdown and Git. No runtime or custom binary needed.
- **Verification:** Always verify changes locally before marking any task as complete.
- **Clean Commits:** Use standard Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`). No rigid hook trailers or custom formats required.

## 🧭 Repository Blueprint & Pointers
This codebase uses a progressive disclosure model with clear separation of concerns:
- **[PRODUCT.md](./PRODUCT.md):** Product vision, target audience, core user problems, and functional boundaries. Read before proposing scope changes or features.
- **[ARCHITECTURE.md](./ARCHITECTURE.md):** System topology, directory layout, layer boundaries, and structural patterns. Read before modifying structural code.
- **[ENGINEERING.md](./ENGINEERING.md):** Code quality standards, craftsmanship principles (KISS/YAGNI, SRP, DRY, DIP), and stack conventions. Read before writing or refactoring modules.
- **[DESIGN.md](./DESIGN.md):** UI/UX principles, design tokens, or content/documentation design guidelines. Read before writing user interfaces or documentation.
- **[TESTING.md](./TESTING.md):** Testing standards, contract invariants, input partitioning, table-driven tests, and test hygiene. Read before writing or auditing tests.
- **[CHANGES.md](./CHANGES.md):** Historical log of architecture pivots, deprecated decisions, and migration reasons. Consult when altering existing behavior.
- **[planning/roadmap.md](./planning/roadmap.md):** Ordered roadmap of specs, dependencies, current statuses, and backlog ideas.

---

## 📋 Task Execution Workflow

Agents execute work incrementally using the specs in `planning/`:

1. **Find Next Task:**
   - Open `planning/roadmap.md`. Find the first spec with status `todo` or `in progress` whose dependencies are `done`.
   - Open the corresponding spec file in `planning/specs/NNN-name.md`.
   - Take the first uncompleted agent task: `- [ ] NNN/TNNN [agent] ...`.
   - Note: Skip `[human]` tasks and notify the user if one blocks execution.

2. **Execute & Follow Constraints:**
   - Implement only the scope described by the task.
   - Respect boundaries defined in `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, and `TESTING.md`.
   - Maintain documentation integrity: do not delete or alter comments/docstrings unrelated to your changes.

3. **Verify:**
   - Run the relevant test suite, build, or type check.
   - For `Verify:` tasks, perform the explicit check and record results under the task (e.g., `verified: <summary>`).

4. **Close Task & Commit:**
   - Mark the checkbox as completed: `- [x] NNN/TNNN [agent] ...`.
   - If all tasks in the spec are complete, update the spec's status to `done` in `planning/roadmap.md`.
   - Stage touched files by name and commit with a clear Conventional Commit message.

---

## ⚠️ Critical Rules & Boundary Conditions
1. **Never Bypass Checks:** Never use `--no-verify` or bypass lint/test checks.
2. **Never Break Working Specs:** If an existing requirement needs to change, follow the protocol in [CHANGES.md](./CHANGES.md) instead of silently breaking old assumptions.
3. **Keep `planning/` Clean:** Only actionable specs and the roadmap belong in `planning/`. Broad system design belongs in `ARCHITECTURE.md`.
4. **When Blocked:** Add an indented `blocked: <reason>` line below the task, commit the note, inform the user, and move to unblocked work.
5. **Enforce Engineering & Testing Invariants:** Adhere strictly to the Core Engineering Principles in [ENGINEERING.md](./ENGINEERING.md) (KISS/YAGNI, Anti-Corruption Layer, SRP) and the Testing Standards in [TESTING.md](./TESTING.md) (Table-Driven Testing, Input Partitioning, Clean Test Bodies).
6. **No Speculative Abstractions:** Never introduce premature interfaces, adapters, or base classes for single-use cases. Abstract only for 2+ concrete consumers or vendors.
