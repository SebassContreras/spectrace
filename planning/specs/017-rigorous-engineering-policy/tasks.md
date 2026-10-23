# 017 — rigorous-engineering-policy — Tasks

- [x] T001 [agent] [status:done] Record universal architecture decisions (Service Layer / Anti-Corruption, YAGNI proportionality, SRP, injected testable dependencies) in `planning/architecture.md`
      covers: D1@1, R2@1
      changes: none
- [x] T002 [agent] [status:done] Update `AGENTS.md` and `skills/spectrace-start/references/templates.md` under "Rules for agents" to enforce all 10 Engineering Principles
      covers: D2@1, R1@1
      changes: AGENTS.md (+11 -4), skills/spectrace-start/references/templates.md (+11 -4)
- [x] T003 [agent] [status:done] Add critical inquiry, anti-sycophancy prompts, and failure-mode probing to `skills/spectrace-start/references/question-bank.md` and `skills/spectrace-start/SKILL.md`
      covers: D3@1, R3@1
      changes: skills/spectrace-start/SKILL.md (+1 -0), skills/spectrace-start/references/question-bank.md (+2 -2)
- [x] T004 [agent] [status:done] Update `skills/spectrace-plan/SKILL.md` Phase 1 and Phase 3 to evaluate designs against the 10 principles and require behavior-driven, non-vacuous test tasks
      covers: D4@1, R4@1
      changes: skills/spectrace-plan/SKILL.md (+4 -3)
- [x] T005 [agent] [status:done] Verify skill size budgets (A5 line caps) with `pytest tests/test_skills.py` and run full spectrace check
      covers: D5@1, R5@1
      kind: test
      changes: none
