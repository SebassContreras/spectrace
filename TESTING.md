# Testing

> Owns: what "done" means, what to test, how a test is written and the command that verifies · Not here: code style (ENGINEERING.md), run, build or deploy procedures (OPERATIONS.md)

## Verify

- Narrowest, one test file: `node --test tests/templates.test.mjs`
- Full suite: `node --test "tests/*.test.mjs"`
- Types and lint, if the stack has them: none; there are no dependencies and no build

## What counts as done

A task is done when its check passes and you ran it. A bug fix ships with a test that fails before the fix and passes after. Never weaken, skip or delete a test to make a change pass.

## What to test

- Behavior, not implementation. One test per real behavior or failure mode; no test that cannot fail.
- Partition the inputs: nominal, boundaries (min, max, ±1), empty and malformed, and several invalid fields at once.
- A rule shared by several writers gets one contract suite that runs against all of them.
- Fix a bug by finding its equivalence class, not by asserting the one payload that was reported.
- Assert lifecycles and invariants: uniqueness, idempotency, round-trips.

## How a test reads

- Arrange, act, assert. The name states the behavior and the condition.
- Use the framework's table or parameterized form for input matrices, with a readable label per row.
- No `if`, ternary or loop inside a test body.
- Never mock the unit under test. Mock only the network, third-party APIs, disk and non-deterministic clocks.

## This project

- Node's built-in `node:test`, no dependency. Tests are table-driven rows over the shipped assets.
- After adding or changing a rule, break it on purpose and confirm a test fails (a mutation check); a suite that stays green under a broken rule is not testing it.
