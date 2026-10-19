# 016 — decision-conflicts — Tasks

- [ ] T001 [agent] [status:todo] Make `cmd_block` accept `conflicts <ref>: <why>`, refusing a reference that names no item and writing nothing
      covers: D1@1, A14@1
- [ ] T002 [agent] [status:todo] Keep a task's conflict note when parsing and report one pending per blocked agent task that has it
      covers: D2@1, A14@1
- [ ] T003 [agent] [status:todo] Test the conflict flow: block names the item, `check` is pending and `--strict` exits 1, `start` clears it, and an unknown reference is refused
      covers: R1@1, R2@1
      kind: test
- [ ] T011 [agent] [status:todo] Baseline every A item and every item ID seen in `fingerprints.json`, silently the first time, and report a changed A item, a missing ID that was not retired, and a bump or retirement with no `changes.md` entry
      covers: D7@1, A14@1
- [ ] T012 [agent] [status:todo] Test the record guard: an A item edited without a bump, deleted, bumped with no entry and retired with no entry are pending; the same changes with an entry are clean; a repo with existing items is adopted with no findings
      covers: R7@1
      kind: test
- [ ] T004 [agent] [status:todo] Document the conflict note, the pending state and the freedom to edit an unbuilt item in `format.md`, with an example `FormatDocTest` parses
      covers: D5@1, A4@1
- [ ] T005 [agent] [status:todo] Add "Phase 0b — Start from a conflict" to `spectrace-change` and extend its Phase 5 gate
      covers: D3@1
- [ ] T006 [agent] [status:todo] Add the "When a decision is in the way" paragraph to `agents-protocol.md`
      covers: D5@1, A14@1, A15@1
- [ ] T007 [agent] [status:todo] Change `spectrace-plan` Phase 0 step 4 and its Phase 1 rule on a contradicting A item to propose the change
      covers: D5@1
- [ ] T008 [agent] [status:todo] Give the `product.md` template "Current MVP scope" and "Not for now" and map the `mvp` answers to them in `spectrace-start` Phase 3
      covers: D4@1
- [ ] T009 [agent] [status:todo] Add the protocol's paragraph to this repo's `AGENTS.md` and turn `product.md` "Scope filter" into a pointer to it
      covers: D6@1, A14@1, A15@1
- [ ] T010 [human] [status:todo] Run a `spectrace-change` session, with no task open, for 002/R4, 002/D4, 010/R4, 010/D5, 010/D7 (include the package) and the wording of 007/D2 and D3
      covers: D6@1
