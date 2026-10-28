# Architecture & Decision Changes

This document maintains a permanent ledger of architectural pivots, deprecated decisions, and significant scope modifications. It prevents agents from reintroducing rejected patterns and provides context on why the system evolved.

---

## 🔄 Change Protocol

When an existing architectural design or requirement needs to change:

1. **Document the Rationale:** Add a new entry to the [Change Log](#change-log) below with date, what changed, why, and what was replaced.
2. **Update the Spec:** In the affected spec (`planning/specs/NNN-name.md`):
   - Strike through the obsolete item and point to the replacement (e.g., `- ~~D1: Sessions in localStorage~~ → D2`).
   - Add explicit cleanup tasks to remove obsolete code, tests, and documentation.
3. **Update Root Context:** If the change modifies system boundaries or visual guidelines, update [ARCHITECTURE.md](./ARCHITECTURE.md) or [DESIGN.md](./DESIGN.md) accordingly.

---

## 📜 Change Log

### 2026-10-28 — Foundation Realignment: Pure Markdown & Root Architecture

- **Scope:** Repository foundation & execution mechanics.
- **What Changed:**
  - Removed all POSIX Git hooks (`.githooks/`), trailer verification scripts (`check-trailers`), and CI trailer enforcement workflows.
  - Eliminated the mandatory `Spec: NNN/TNNN` commit trailer requirement in favor of standard Conventional Commits.
  - Relocated core decision contracts to the repository root: `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `CHANGES.md`.
  - Focused `planning/` strictly on actionable execution (`roadmap.md` and `specs/NNN-*.md`), deprecating `planning/product.md`.
  - Updated skills (`spectrace-plan` and `spectrace-change`) to generate and manage this streamlined structure.
- **Why:**
  - Shell-based Git hooks caused persistent friction and blocking errors across cross-platform environments (notably Windows path/CRLF discrepancies).
  - Enforcing rigid trailers on every micro-commit interrupted natural agent workflows and created friction without improving code quality.
  - Moving architecture and design contracts to the root maximizes immediate discovery for modern AI agents (Cursor, Claude Code, Copilot, Antigravity) via progressive disclosure.
- **Replaced Items:**
  - `~~Specs 022–027~~`: Git hooks, trailer checkers, and CI trailer validations retired.
