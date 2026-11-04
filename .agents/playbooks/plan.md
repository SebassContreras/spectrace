# Playbook: plan

> Owns: turning an idea into specs, and shaping the contracts to fit the project · Not here: standards (ENGINEERING.md, TESTING.md), the roadmap itself (planning/roadmap.md)

## Steps

1. Read `AGENTS.md`, every contract, `planning/roadmap.md` and `git log -20`. Read the code you will touch.
2. Ask only what blocks the plan: open stack choices, credentials. Decide the rest and record the decision in the spec's Design.
3. Cut the plan into thin slices that each end in something running. Add one roadmap row per spec, and write a full spec only for the next one; later specs stay one line in the roadmap.
4. Write the next spec in the format below. Keep it under 80 lines.
5. List the contract changes the plan implies: a layer in ARCHITECTURE.md, a command in OPERATIONS.md, a framework in TESTING.md. Show them as a diff, apply them once the user approves, and record the change in CHANGES.md. Write only what the repo cannot show, and add a rule only after a failure you saw.
6. Run `node .agents/guard/guard.mjs --all` and fix what it reports. Report, and stop: planning does not start executing.

## Spec format

```markdown
# 003 — login

## Goal
What works when this is done and how to check it, in 2–3 lines.

## Requirements
- R1: A checkable outcome.

## Design
- D1 (R1): A decision, with its trade-off when it is not obvious. This section is optional.

## Tasks
- [ ] 003/T001 [agent] Do one thing — covers D1
- [ ] 003/T002 [agent][test] Test R1 — covers R1
- [ ] 003/T003 [human] Create the account — covers R1
      blocked: waiting for approval

## Changes
- 2026-11-04: D1 → D2. Why: … Work: T004.
```

- Every requirement is covered by a task, and by a `[test]` task. A `[test]` task writes or runs a test.
- `[x]` needs a `verified:` line under it with the evidence.
- A replaced item is struck, `~~D1~~ → D2`, never renumbered.
- `[agent]` is for what an agent can do; `[human]` is for accounts, credentials and physical actions.
- Finished spec: mark the roadmap row `done` and delete the spec file. What lasts lives in the contracts and CHANGES.md.
