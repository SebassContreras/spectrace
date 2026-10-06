# 005 — distribution — Changes

## 2026-10-06 — install through the skills CLI only
Why: the plugin, the installer scripts and the release pipeline made installation harder to explain and to maintain, and it's unknown whether anyone installs through the marketplace. The `skills` CLI installs from the repo into the right folder for each agent (75+), with no release needed.
- MODIFIED R1@1 → R1@2
- REMOVED R3@1, D1@1, D3@1
- ADDED D5@1
- Tasks: T010 retires T001, T011 retires T002, T012 retires T004/T005/T006 (redo: deleted, not adapted — T005 tested a retired requirement); T008 re-pointed to R1@2 (still valid); T013 rewrites the install section; T009 renames the skills (A1@2)

## 2026-10-06 — sweep after removing the plugin
Why: the first pass used only the trace, which can't see mentions written by tasks that covered other items or by no task (004 R7@1, 001 R6@1 came out of this).
- No item changes.
- Context edited: what's built, who it serves, owner split, deliverables; 006's "who it serves" no longer mentions a release.
- Tasks: T014 drops the release-helper mention from the CI comment.

## 2026-10-06 — publish-ready
Why: the repository is being published; the README needs status badges and an honest limits section, CI must prove the Python 3.9 floor, and the repo must be findable.
- MODIFIED R4@1 → R4@2, D4@1 → D4@2
- ADDED R5@1, R6@1, D6@1, D7@1
- Tasks: T007 re-pointed to D4@2 (still valid); T008 also covers R6@1; T015–T017 added. T008 is done by the agent on the maintainer's explicit go-ahead.
