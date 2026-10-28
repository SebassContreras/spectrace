# Architecture & Decision Changes

This document maintains a permanent ledger of architectural pivots, deprecated decisions, and significant scope modifications. It prevents agents from reintroducing rejected patterns and provides context on why the system evolved.

---

## 🔄 Change Protocol

When an existing architectural design or requirement needs to change:

1. **Document the Rationale:** Add a new entry to the [Change Log](#change-log) below with date, what changed, why, and what was replaced.
2. **Update the Spec:** In the affected spec (`planning/specs/NNN-name.md`):
   - Strike through the obsolete item and point to the replacement (e.g., `- ~~D1: Sessions in localStorage~~ → D2`).
   - Add explicit cleanup tasks to remove obsolete code, tests, and documentation.
3. **Update Root Context:** If the change modifies system boundaries or visual guidelines, update `PRODUCT.md`, `ARCHITECTURE.md`, or `DESIGN.md` accordingly.

---

## 📜 Change Log

<!-- 
### YYYY-MM-DD — Title of Pivot or Decision Change

- **Scope:** <!-- Affected subsystem or area -->
- **What Changed:** <!-- Specific architectural shifts -->
- **Why:** <!-- Underlying reason, constraint, or bug discovered -->
- **Replaced Items:** <!-- Struck decisions or superseded specs -->
-->
