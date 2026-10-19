# 002 — start — Tasks

- [x] T001 [agent] [status:done] Port the question bank to `skills/start/references/question-bank.md` (no loop dimensions; Phase E asks for R items)
      covers: D1@1
      changes: skills/start/references/question-bank.md (+165 -0)
- [x] T002 [agent] [status:done] Write `skills/start/references/templates.md` (product, architecture, roadmap, requirements, AGENTS.md shapes)
      covers: D2@1
      changes: skills/start/references/templates.md (+143 -0)
- [x] T003 [agent] [status:done] Port `skills/start/references/handoff.md` (spectrace paths, no loop)
      covers: D1@1
      changes: skills/start/references/handoff.md (+67 -0)
- [x] T004 [agent] [status:done] Write `skills/start/assets/agents-protocol.md`
      covers: D5@1
      changes: skills/start/assets/agents-protocol.md (+18 -0)
- [x] T005 [agent] [status:done] Write `skills/start/SKILL.md`
      covers: D1@1, D2@1, D3@1, D4@2, D5@1, D6@1, D7@1
      changes: skills/start/SKILL.md (+158 -0)
      └─ reviewed 2026-10-19: the package install (011/T008) holds under the new text
- [x] T006 [agent] [status:done] Write `tests/test_skills.py`: frontmatter per the Agent Skills spec, name equals folder, body within budget, every referenced file exists
      covers: A5@4, A7@1
      kind: test
      changes: tests/test_skills.py (+70 -0)
      └─ reviewed 2026-10-06: still valid under A5@3; 001/T009 added the trace.py limit to the same test
      └─ reviewed 2026-10-19: still valid under A5@4; 011/T006 replaces the trace.py cap with a per-module budget in the same test
