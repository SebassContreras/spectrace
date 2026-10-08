# 007 — agent-loop-and-workflow-optimization — Requirements

## What's being built

Optimizations to the spectrace protocol and trace tooling for agent execution:
1. Clarification and reinforcement of the execution loop when an agent runs multiple tasks or specs consecutively.
2. In `trace start`, direct display of the covered items and their descriptions so the agent doesn't need to read whole files when unnecessary.
3. In `trace done`, direct hint and preview of the next available task (`next: ... -> trace start ...`).
4. Guidance in planning and protocol for browser / slow UI tasks (differentiating automated headless tests vs manual `[human]` reviews).
5. Explicit rule and check that `trace check` is run once at the end of the session, not after every single task.

## Who it serves

Agents and engineers executing specs in target repositories, ensuring tasks are properly started and closed in `done` without jumping across specs or accumulating stray changes.

## Requirements

- R1@1: The protocol in `AGENTS.md` and `skills/spectrace-start/assets/agents-protocol.md` explicitly specifies loop execution behavior: each task must be opened with `trace start` and closed with `trace done` before proceeding to any other task or spec.
- R2@1: `trace start` prints the resolved items (R/D/A) and their text covered by the opened task, reducing mandatory full-file context reads.
- R3@1: `trace done` prints the `next:` task recommendation and start command upon completing a task.
- R4@1: The protocol explicitly states that `trace check` is run once before finishing the overall session, not after every individual task.
- R5@1: Guidelines in `spectrace-plan` and the protocol document how to structure browser and interactive UI verification: separating automated check scripts (`kind: test`, e.g. headless Playwright) from manual user checks (`[human]`).

## Out of scope

- Removing `trace start` or `trace done` (exact git snapshot tracking is essential).
- Changing git staging index handling.

## Dependencies

001, 002, 003, 005.

## Owner split

All agent.
