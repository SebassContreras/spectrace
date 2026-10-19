# 016 — decision-conflicts — Requirements

## What's being built

A way for decisions to change spec by spec without being worked around. When a task cannot
be done without contradicting a decision that holds, the agent stops and says so; the trace
keeps the spec open; the user keeps the decision, edits it or retires it; and the work goes
on from the answer. The rule is carried by the skills and the protocol, so every repo
spectrace sets up gets it, and this repo applies it to itself before the code map is built.

## Who it serves

Developers whose specs change as the code teaches them something, and the agents that
execute the tasks: a decision that stopped fitting must be changed in the open, never
bent around in the code.

## Requirements

- R1@1: When a task cannot be done without contradicting a decision that holds (A, D or R), the agent stops instead of working around it: `trace block NNN/TNNN "conflicts <ref>: <why>"` records the conflict, and a reference that names no item is refused.
- R2@1: A recorded conflict keeps its spec open: `trace check` reports it as pending, naming the task, the item and the three ways out, and `--strict` fails until the task is resumed.
- R3@1: The user settles a conflict by keeping the decision (the task is redone to fit), editing it or retiring it, each through `spectrace-change` starting from the recorded conflict; the agent only proposes, with the simplest direct change.
- R4@1: `planning/product.md` is written with "Current MVP scope" and "Not for now" besides what the project is and who uses it, from the `mvp` interview answers.
- R5@1: The no-workaround rule and the scope filter reach every repo: they are in the protocol block of `AGENTS.md`, and `spectrace-plan` proposes changing a decision that gets in the way instead of designing around it.
- R6@1: This repo applies the rules to itself before spec 012 starts: its `AGENTS.md` and `product.md` carry them, and the earlier items that the package contradicts are settled through `spectrace-change`.

- R7@1: A decision cannot change or disappear without a record: for an A item, or an item a finished task covers, `trace check` reports as pending a text change without a revision bump, a missing item that was not retired, and a revision bump or retirement with no entry in `changes.md`; a repo that already has items is adopted without any of these findings.

## Out of scope

- Detecting a workaround automatically: the trace cannot tell, and says so; the rule and the cheap path are what prevent it.
- Counting conflicts per decision or flagging a decision as obsolete: `trace impact` already lists what covers it.
- Guarding prose that is not an item (`product.md`, the rest of `AGENTS.md`): it is context and changes freely; a rule that must bind becomes an A item.

## Dependencies

011.

## Owner split

Agent, except T010: it settles earlier decisions through `spectrace-change` and needs the user's approval.
