# Operations

> Owns: exact, repeatable procedures and environment facts to set up, run, build, release and recover the project · Not here: why (CHANGES.md), standards (ENGINEERING.md), structure (ARCHITECTURE.md)

## Setup

Node 20 or later. There is no install step: the project has no dependencies.

## Run

- Tests: `node --test "tests/*.test.mjs"`
- Try the scaffold: copy the assets into a temporary repository following `skills/spectrace/SKILL.md`, "Init" step 2.

## Build and release

There is no build. A project installs the skill with `pnpm dlx skills add SebassContreras/spectrace` and picks up a new version by running that again and then the skill's update mode. A release is a merge to `main`.

This repository installs what it ships. After changing a file under `skills/spectrace/assets/`, copy it to where this repository uses it; `tests/repo.test.mjs` names any copy that is out of date:

```sh
cp skills/spectrace/assets/playbooks/*.md .agents/playbooks/
cp skills/spectrace/assets/CLAUDE.md CLAUDE.md
```

## Environment

No variables.

## Recover

- A test names a shipped file and its installed copy that differ: run the `cp` lines above.
