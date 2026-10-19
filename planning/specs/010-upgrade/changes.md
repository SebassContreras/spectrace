# 010 — upgrade — Changes

## 2026-10-19 — the upgrade replaces the package as one unit
Why: 011 moved the trace into the `spectrace/` package; these items named only `trace.py` and `format.md` as what is copied (016/D6).
- MODIFIED R4@1 → R4@2
- MODIFIED D5@1 → D5@2
- MODIFIED D7@1 → D7@2
- Tasks: T002 and T006 re-pointed to D5@2, T004 to D7@2 (still valid, 011/T008). Refactor in place: the text keeps its structure and gains the package folder, and the code already does it (011/T008).
