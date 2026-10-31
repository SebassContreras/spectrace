# AGENTS.md

Instructions and operational constraints for AI coding agents.

## 🚀 Quick Reference & Commands
- **Environment:** Pure Markdown and Git. No runtime, daemons, or custom binaries needed.
- **Verification:** Always verify changes locally before marking any task as complete.
- **Clean Commits:** Use standard Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`). No rigid hook trailers or custom formats required.

## 🧭 Repository Blueprint & Pointers
This codebase uses a progressive disclosure model with clear separation of concerns across 7 root contracts:
- **[PRODUCT.md](./PRODUCT.md):** Product vision, target audience, core user problems, and functional boundaries (including explicit non-goals). Read before proposing scope changes or features.
- **[ARCHITECTURE.md](./ARCHITECTURE.md):** System topology, directory layout, layer boundaries, and structural patterns. Read before modifying structural code.
- **[ENGINEERING.md](./ENGINEERING.md):** Code quality standards, craftsmanship principles (KISS/YAGNI, SRP, DRY, DIP/ACL, research when it pays, trade-offs), and stack conventions. Read before writing or refactoring modules.
- **[DESIGN.md](./DESIGN.md):** Context-aware design: visual UI/UX tokens and component states for frontend apps, or content/editorial design guidelines for documentation/governance repos. Read before writing user interfaces or documentation.
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
   - Respect structural boundaries in [ARCHITECTURE.md](./ARCHITECTURE.md), craftsmanship principles in [ENGINEERING.md](./ENGINEERING.md), design guidelines in [DESIGN.md](./DESIGN.md), and test requirements in [TESTING.md](./TESTING.md).
   - Maintain documentation integrity: do not delete or alter comments/docstrings unrelated to your changes.

3. **Verify:**
   - Run the relevant test suite, build, or type check.
   - For `Verify:` tasks, perform the explicit check and record results under the task (e.g., `verified: <summary>`).

4. **Close Task & Commit:**
   - Mark the checkbox as completed: `- [x] NNN/TNNN [agent] ...`.
   - If all tasks in the spec are complete, update the spec's status to `done` in `planning/roadmap.md`.
   - Stage touched files by name and commit with a clear Conventional Commit message.

### Small Fixes

Never create a spec just to hold a fix, and keep no separate fix list — git is the record (see [CHANGES.md](./CHANGES.md), 2026-10-31).

- **Trivial correction** (breaks no `R`/`D`, fits in one commit — typo, stale doc, wrong message, small defect): commit it directly as `fix:` or `docs:`, with a regression test if behavior changes. Not doing it now? One bullet under `## Ideas` in [planning/roadmap.md](./planning/roadmap.md).
- **Bug against a requirement:** add a regression test task and a fix task to the spec that owns it. If that spec is `done`, set it back to `in progress` and note the reopening under its `## Changes`.
- **The fix needs a different `R` or `D`:** it is a change of direction — use `spectrace-change`.

---

## ⚠️ Critical Rules & Boundary Conditions
1. **Never Bypass Checks:** Never use `--no-verify` or bypass lint/test checks.
2. **Never Break Working Specs:** If an existing requirement needs to change, follow the protocol in [CHANGES.md](./CHANGES.md) instead of silently breaking old assumptions.
3. **Keep `planning/` Clean:** Only actionable specs and the roadmap belong in `planning/`. Broad system design belongs in `ARCHITECTURE.md` and `ENGINEERING.md`.
4. **When Blocked:** Add an indented `blocked: <reason>` line below the task, commit the note, inform the user, and move to unblocked work.
5. **Enforce Engineering & Testing Invariants:** Adhere strictly to the Core Engineering Principles in [ENGINEERING.md](./ENGINEERING.md) (KISS/YAGNI, Anti-Corruption Layer, SRP, research only when the decision requires it, trade-offs) and the Testing Standards in [TESTING.md](./TESTING.md) (Table-Driven Testing, Input Partitioning, Clean Test Bodies).
6. **No Speculative Abstractions:** Never introduce premature interfaces, adapters, or base classes for single-use cases. Abstract only for 2+ concrete consumers or vendors.
7. **Context-Aware Design:** Never inject CSS tokens, component states, or HTML tags into non-UI repositories. Use [DESIGN.md](./DESIGN.md) for editorial and document standards in documentation or governance repos.
