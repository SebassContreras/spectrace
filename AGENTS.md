# AGENTS.md

Instructions and operational constraints for AI coding agents.

## 🚀 Quick Reference & Commands
- **Environment:** Pure Markdown and Git. No runtime or custom binary needed.
- **Verification:** Always verify changes locally before marking any task as complete.
- **Clean Commits:** Use standard Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`). No rigid hook trailers or custom formats required.

## 🧭 Repository Blueprint & Pointers
This codebase uses a two-tier progressive disclosure model:
- **[PRODUCT.md](./PRODUCT.md):** Product vision, target audience, core user problems, and functional boundaries. Read before proposing scope changes or features.
- **[ARCHITECTURE.md](./ARCHITECTURE.md):** System architecture, directory layout, core dependencies, and technical patterns. Read before modifying structural code.
- **[DESIGN.md](./DESIGN.md):** UI/UX principles, design tokens, visual hierarchy, and code style standards. Read before writing user interfaces or new modules.
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
   - Respect boundaries defined in `ARCHITECTURE.md` and `DESIGN.md`.
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
