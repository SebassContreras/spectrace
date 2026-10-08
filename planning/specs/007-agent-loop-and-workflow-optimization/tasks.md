# 007 — agent-loop-and-workflow-optimization — Tasks

- [x] T001 [agent] [status:done] `trace.py`: `start` prints resolved covered items and `done` prints the next task prompt
      covers: D2@1, D3@1
      changes: .gitignore (+1 -0), skills/spectrace-start/assets/trace.py (+11 -15)
- [x] T002 [agent] [status:done] Tests: verify `trace start` item print and `trace done` next task print; verify line count budget
      covers: R2@1, R3@1
      kind: test
      changes: tests/test_trace.py (+12 -1)
- [x] T003 [agent] [status:done] Protocol updates: document loop execution, single check at session end, and UI/browser testing guidance
      covers: D1@1, D4@1
      changes: AGENTS.md (+5 -4), skills/spectrace-plan/SKILL.md (+3 -1), skills/spectrace-start/assets/agents-protocol.md (+5 -4)
