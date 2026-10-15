# 009 — testing-policy — Requirements

## What's being built

A testing policy that spectrace writes into every target repo's `AGENTS.md`, so an agent
knows which command to run in each case and how many tests to create:
1. A command map recorded at setup: the narrowest command (one file or module), the
   affected-only command and the full-suite command.
2. A run rule: each task runs only the narrowest command covering the files it touched;
   the full suite runs only at the end of the session or when a shared module changed.
3. A creation rule: tests are minimal and proportional to the requirements; e2e and smoke
   tests exist only when the user asks for them at setup.

## Who it serves

Developers whose small projects end with hundreds of tests, and agents that spend time
and tokens running the whole suite after every task.

## Requirements

- R1@1: The `toolchain` question in `skills/spectrace-start/references/question-bank.md`
  asks for three commands — single file or module, affected only, full suite — and records
  only commands the toolchain actually accepts.
- R2@1: `skills/spectrace-start/references/templates.md` gives `AGENTS.md` a "Testing"
  section holding that command map and the run and creation rules below, marked as hard
  rules.
- R3@1: `skills/spectrace-start/assets/agents-protocol.md` step 4 tells the agent to run
  the narrowest command for the files the task changed, and the full suite only when the
  task touched a shared module (config, core, public interfaces) or at session end.
- R4@1: `skills/spectrace-plan/SKILL.md` Phase 3 creates at most one `kind: test` task per
  checkable R, at the lowest level that proves it: a unit test with a fake adapter before
  an integration test.
- R5@1: `skills/spectrace-plan/SKILL.md` creates e2e, smoke or browser-driven test tasks
  only when the `verification` answer asks for them; the "prefer headless scripts" line
  applies only then.
- R6@1: The `verification` question in `question-bank.md` states that unit tests are the
  default and asks whether e2e or smoke tests are wanted at all.
- R7@1: The "Testing" section tells the agent not to test code without logic (wrappers,
  config, getters) nor a vendor's own behavior.
- R8@1: The "Testing" section tells the agent to stop and justify in the task's report when
  a spec's tests exceed three times its R items; it is a tripwire, not a cap.
- R9@1: All skills still pass `tests/test_skills.py` (bodies at most 200 lines, valid
  frontmatter).
- R10@1: For a `software` project, `spectrace-start` Phase 4 writes the verified test commands and the `verification` answer into `AGENTS.md` "Testing", so that section holds no placeholder once Phase 4 ends; for other project types the section is not written.

## Out of scope

- Changing `trace.py` (for example, making `start` print the test command).
- A hard numeric cap on tests per project.
- Rewriting the tests of repos already scaffolded.

## Dependencies

002, 003, 008.

## Owner split

All agent.
