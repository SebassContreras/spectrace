# 014 — locate-packet-fix — Tasks

- [x] T001 [agent] [status:done] Add the tokens table and the tokenizer (camelCase and snake_case split, accent folding, simple plural stripping) to the index
      covers: D1@1, A12@1
      changes: skills/spectrace-start/assets/spectrace/facts.py (+19 -7), skills/spectrace-start/assets/spectrace/index.py (+8 -3), skills/spectrace-start/assets/spectrace/tokens.py (+37 -0)
- [x] T002 [agent] [status:done] Add `trace locate` with weighted ranking, expansion through `why` and matched-token output
      covers: D1@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+2 -0), skills/spectrace-start/assets/spectrace/views/locate.py (+65 -0)
- [x] T003 [agent] [status:done] Add the packet for a task — decisions, symbols, dependents, tests, incidents and what was not analysed — as Markdown and `--json`
      covers: D2@1
      changes: skills/spectrace-start/assets/spectrace/cli.py (+2 -0), skills/spectrace-start/assets/spectrace/commands.py (+4 -1), skills/spectrace-start/assets/spectrace/views/packet.py (+82 -0)
- [x] T004 [agent] [status:done] Add `packet --diff [--base ref]` over a git ref or the working tree, taking the tasks the diff adds under `.spectrace/changes/` as its decisions
      covers: D2@1
      changes: skills/spectrace-start/assets/spectrace/commands.py (+1 -1), skills/spectrace-start/assets/spectrace/index.py (+7 -3), skills/spectrace-start/assets/spectrace/views/index_view.py (+2 -2), skills/spectrace-start/assets/spectrace/views/packet.py (+33 -4)
- [x] T005 [agent] [status:done] Add the severity signals to the packet
      covers: D3@1, A11@1
      changes: skills/spectrace-start/assets/spectrace/records.py (+3 -0), skills/spectrace-start/assets/spectrace/views/packet.py (+40 -11)
- [x] T006 [agent] [status:done] Test `locate` on at least 20 golden queries over this repo and a fixture project, and report the comparison with `rg`
      covers: R1@1
      kind: test
      changes: tests/test_locate.py (+125 -0)
- [x] T007 [agent] [status:done] Test `packet`: identical output for identical input, `--diff --base` on a clean clone with no state and no index, and the severity signals on a fixture
      covers: R2@1, R6@1
      kind: test
      changes: tests/test_packet.py (+100 -0)
- [x] T008 [agent] [status:done] Document `kind: fix` and the `locate`, `packet` and `index` commands in `format.md`
      covers: D4@1
      changes: skills/spectrace-start/assets/format.md (+25 -1)
- [x] T009 [agent] [status:done] Write `skills/spectrace-fix/SKILL.md`, at most 200 lines
      covers: D4@1, A1@3
      changes: skills/spectrace-fix/SKILL.md (+97 -0)
- [x] T010 [agent] [status:done] Update `README.md`: four skills, the code map, the CI recipe and its limits
      covers: D5@1, A1@3
      changes: README.md (+41 -2)
- [x] T011 [agent] [status:done] Update `spectrace-plan`, `spectrace-change`, `spectrace-start` (question-bank dimension `codebase`) and the protocol block to use the new commands
      covers: D6@1
      changes: skills/spectrace-change/SKILL.md (+3 -2), skills/spectrace-plan/SKILL.md (+3 -1), skills/spectrace-start/SKILL.md (+4 -2), skills/spectrace-start/assets/agents-protocol.md (+1 -1), skills/spectrace-start/references/question-bank.md (+1 -0)
- [x] T012 [agent] [status:done] Add the packet step to this repo's `ci.yml` for pull requests
      covers: D7@1
      changes: .github/workflows/ci.yml (+10 -1), README.md (+1 -1)
- [x] T013 [agent] [status:done] Run `tests/test_skills.py` and the full suite
      covers: R3@1, R4@1
      kind: test
      changes: none
- [x] T014 [agent] [status:done] Check in `tests/test_skills.py` that `README.md` names the CI recipe commands and the four skills
      covers: R5@1
      kind: test
      changes: tests/test_skills.py (+17 -0)
