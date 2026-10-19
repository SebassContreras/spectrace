# 014 — locate-packet-fix — Tasks

- [ ] T001 [agent] [status:todo] Add the tokens table and the tokenizer (camelCase and snake_case split, accent folding, simple plural stripping) to the index
      covers: D1@1, A12@1
- [ ] T002 [agent] [status:todo] Add `trace locate` with weighted ranking, expansion through `why` and matched-token output
      covers: D1@1
- [ ] T003 [agent] [status:todo] Add the packet for a task — decisions, symbols, dependents, tests, incidents and what was not analysed — as Markdown and `--json`
      covers: D2@1
- [ ] T004 [agent] [status:todo] Add `packet --diff [--base ref]` over a git ref or the working tree, taking the tasks the diff adds under `.spectrace/changes/` as its decisions
      covers: D2@1
- [ ] T005 [agent] [status:todo] Add the severity signals to the packet
      covers: D3@1, A11@1
- [ ] T006 [agent] [status:todo] Test `locate` on at least 20 golden queries over this repo and a fixture project, and report the comparison with `rg`
      covers: R1@1
      kind: test
- [ ] T007 [agent] [status:todo] Test `packet`: identical output for identical input, `--diff --base` on a clean clone with no state and no index, and the severity signals on a fixture
      covers: R2@1, R6@1
      kind: test
- [ ] T008 [agent] [status:todo] Document `kind: fix` and the `locate`, `packet` and `index` commands in `format.md`
      covers: D4@1
- [ ] T009 [agent] [status:todo] Write `skills/spectrace-fix/SKILL.md`, at most 200 lines
      covers: D4@1, A1@3
- [ ] T010 [agent] [status:todo] Update `README.md`: four skills, the code map, the CI recipe and its limits
      covers: D5@1, A1@3
- [ ] T011 [agent] [status:todo] Update `spectrace-plan`, `spectrace-change`, `spectrace-start` (question-bank dimension `codebase`) and the protocol block to use the new commands
      covers: D6@1
- [ ] T012 [agent] [status:todo] Add the packet step to this repo's `ci.yml` for pull requests
      covers: D7@1
- [ ] T013 [agent] [status:todo] Run `tests/test_skills.py` and the full suite
      covers: R3@1, R4@1
      kind: test
