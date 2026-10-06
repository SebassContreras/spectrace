# 005 — distribution — Tasks

- [x] T001 [agent] [status:done] Write `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
      covers: D1@1
      changes: .claude-plugin/marketplace.json (+18 -0), .claude-plugin/plugin.json (+12 -0)
- [x] T002 [agent] [status:done] Write `install.sh` and `install.ps1`
      covers: D1@1
      changes: install.ps1 (+86 -0), install.sh (+103 -0)
- [x] T003 [agent] [status:done] Write `.github/workflows/ci.yml`
      covers: D2@1
      changes: .github/workflows/ci.yml (+25 -0)
- [x] T004 [agent] [status:done] Port `scripts/next_version.py`
      covers: D3@1
      changes: scripts/next_version.py (+56 -0)
- [x] T005 [agent] [status:done] Write `tests/test_next_version.py`
      covers: R3@1
      kind: test
      changes: tests/test_next_version.py (+38 -0)
- [x] T006 [agent] [status:done] Write `.github/workflows/release.yml`
      covers: D3@1
      changes: .github/workflows/release.yml (+148 -0)
- [x] T007 [agent] [status:done] Write `README.md`
      covers: D4@2
      changes: README.md (+83 -0)
      └─ reviewed 2026-10-06: still valid under D4@2; T016 adds badges and limits
- [x] T008 [human] [status:done] Create the GitHub repository `SebassContreras/spectrace` and push
      covers: R1@2, R6@1
      changes: none
      └─ reviewed 2026-10-06: still needed — the skills CLI installs from the GitHub repo
- [x] T009 [agent] [status:done] Rename the skills to `spectrace-start`, `spectrace-plan`, `spectrace-change` (folders, `name:`, every reference in skills, docs, tests and CI)
      covers: A1@2
      changes: .github/workflows/ci.yml (+1 -1), AGENTS.md (+8 -8), README.md (+5 -5), skills/change/SKILL.md (+0 -106), skills/plan/SKILL.md (+0 -121), skills/spectrace-change/SKILL.md (+106 -0), skills/spectrace-plan/SKILL.md (+121 -0), skills/spectrace-start/SKILL.md (+158 -0), skills/spectrace-start/assets/agents-protocol.md (+18 -0), skills/spectrace-start/assets/format.md (+151 -0), skills/spectrace-start/assets/trace.py (+748 -0), skills/spectrace-start/references/handoff.md (+67 -0), skills/spectrace-start/references/question-bank.md (+165 -0), skills/spectrace-start/references/templates.md (+143 -0), skills/start/SKILL.md (+0 -158), skills/start/assets/agents-protocol.md (+0 -18), skills/start/assets/format.md (+0 -150), skills/start/assets/trace.py (+0 -748), skills/start/references/handoff.md (+0 -67), skills/start/references/question-bank.md (+0 -165), skills/start/references/templates.md (+0 -143), tests/test_trace.py (+2 -2)
- [x] T010 [agent] [status:done] Delete `.claude-plugin/`
      covers: D5@1
      retires: T001
      changes: .claude-plugin/marketplace.json (+0 -18), .claude-plugin/plugin.json (+0 -12)
- [x] T011 [agent] [status:done] Delete `install.sh` and `install.ps1`
      covers: D5@1
      retires: T002
      changes: install.ps1 (+0 -86), install.sh (+0 -103)
- [x] T012 [agent] [status:done] Delete the release machinery: `.github/workflows/release.yml`, `scripts/next_version.py` and its test
      covers: R1@2
      retires: T004, T005, T006
      changes: .github/workflows/release.yml (+0 -148), scripts/next_version.py (+0 -56), tests/test_next_version.py (+0 -38)
- [x] T013 [agent] [status:done] Rewrite the README's install section for `pnpm dlx skills add SebassContreras/spectrace`
      covers: D5@1
      changes: README.md (+7 -13)
- [x] T014 [agent] [status:done] Drop the release-helper mention from `.github/workflows/ci.yml`'s comment
      covers: D2@1
      changes: .github/workflows/ci.yml (+1 -1)
- [x] T015 [agent] [status:done] `ci.yml`: test matrix (3.9 on ubuntu-24.04; 3.13 on ubuntu-latest and windows-latest)
      covers: D6@1
      changes: .github/workflows/ci.yml (+20 -6)
- [x] T016 [agent] [status:done] README: badges, limits, changing-direction and develop sections
      covers: D4@2
      changes: README.md (+70 -24)
- [x] T017 [agent] [status:done] Set the GitHub description and topics
      covers: D7@1
      changes: none
