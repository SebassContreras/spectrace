# Operations

> Owns: exact, repeatable procedures and environment facts to set up, run, build, release and recover the project · Not here: why (CHANGES.md), standards (ENGINEERING.md), structure (ARCHITECTURE.md)

## Setup

Node 20 or later. There is no install step: the project has no dependencies.

## Run

- Tests: `node --test "tests/*.test.mjs"`
- Guard on this repository: `node skills/spectrace/assets/guard/guard.mjs --all`
- Try the scaffold: copy the assets into a temporary repository following `SKILL.md`, "Init" step 2, then run that repository's guard.

## Build and release

There is no build. A project installs the skill with `pnpm dlx skills add SebassContreras/spectrace` and picks up a new version by running that again and then the skill's update mode. A release is a merge to `main`.

## Environment

No variables. The hooks read their payload from stdin and need `git` on the PATH for the branch, status and commit-range checks.

## Recover

- A hook blocked something it should not have: run `node skills/spectrace/assets/guard/guard.mjs --all`, read the rule id in the message and open an issue with the command. To unblock right now, remove the hook entry from `.claude/settings.json`; CI still enforces.
- Guard tests fail after a rule change: the failing row names the case, and a mutation check shows which rule it guards.
