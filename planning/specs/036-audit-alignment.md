# 036 — audit-alignment

## Goal

Everything the first audit of the single-skill layout found is fixed and guarded by a test: the guard covers the PowerShell tool Windows uses, the router is checked, no fact has two owners and this repository installs exactly what it ships. Verify: `node --test "tests/*.test.mjs"` and `node .agents/guard/guard.mjs --all` both pass.

## Requirements

- R1: The Claude adapter and the guard cover both shell tools, `Bash` and `PowerShell`, including PowerShell here-strings.
- R2: The guard reports a router row that names a file that does not exist.
- R3: Antigravity's Stop answer "continue" is bounded, and running the guard on a terminal prints its usage instead of waiting.
- R4: Each fact lives in one contract template, and a test states which.
- R5: This repository's installed copies (guard, playbooks, hook files, `CLAUDE.md`) are identical to the shipped assets, and `.gitattributes` keeps LF.
- R6: `SKILL.md` covers moving a repository from the previous design and adapting the contracts to a project that is not software.

## Design

- D1 (R1): On Windows Claude Code routes shell commands through the PowerShell tool, and a hook that matches only `Bash` never fires there, so the adapter matches `Bash|PowerShell` and the guard treats both as a shell. Source: https://code.claude.com/docs/en/hooks.md and https://code.claude.com/docs/en/tools-reference.md#powershell-tool (accessed 2026-11-04).
- D2 (R3): Antigravity sends no `stop_hook_active`, so a counter per conversation in the temp directory lets the same errors be answered with "continue" twice, then a warning. Without a conversation id the workspace path is the key.
- D3 (R4): `AGENTS.md` keeps the cross-cutting hard rules; "done" and test rules live in `TESTING.md`, layer rules in `ARCHITECTURE.md`, casing in `ENGINEERING.md`, language in `AGENTS.md`.
- D4 (R5): A test compares each installed copy with its asset, so the first thing that drifts is named.

## Tasks

- [x] 036/T001 [agent] Match `Bash|PowerShell`, read PowerShell here-strings and treat the PowerShell tool as a shell — covers R1, D1
      verified: Claude adapter matcher is Bash|PowerShell; contextOf treats the PowerShell tool as a shell; parseShell reads @'…'@ here-strings
- [x] 036/T002 [agent][test] Rows for the PowerShell tool and here-strings, and the hook run end to end through it — covers R1, D1
      verified: rows for the PowerShell tool and for here-strings with an apostrophe before the trailer, and the hook run end to end with tool_name PowerShell gives exit 2; matcher mutated back to Bash fails 2 tests, PowerShell not treated as a shell fails 3
- [x] 036/T003 [agent] Add the `router-target` check — covers R2
      verified: checkContract takes the repository root and reports router-target; this repository's own router, which named three playbooks that did not exist, was caught the first time it ran
- [x] 036/T004 [agent][test] Rows for `routerTargets` and for a repository with a missing and an existing target — covers R2
      verified: routerTargets rows (header and separator ignored, CRLF, a column that is not a Markdown file) and repository rows with a missing and an existing target; pointing this repository's router at a missing playbook fails 1 test
- [x] 036/T005 [agent] Bound Antigravity's Stop answer; print usage on `--help` and on a terminal — covers R3, D2
      verified: limitRepeats keeps a counter per conversation (the workspace when there is no id), --help prints usage, and a terminal with nothing to read prints usage and exits 2
- [x] 036/T006 [agent][test] Stop rows: first, second and third report, reset after a fix, separate conversations; usage rows — covers R3, D2
      verified: rows for the first, second and third report, reset after a fix, separate conversations and separate workspaces, and the usage rows; an earlier failure showed shared state in the temp directory, so the tests now isolate the state directory
- [x] 036/T007 [agent] Remove the duplicated rules from the templates and this repository's contracts — covers R4, D3
      verified: AGENTS.md hard rules reduced to the four cross-cutting ones; the layer sentence left ENGINEERING; language and naming left DESIGN and ENGINEERING; the fill hints and this repository's contracts updated
- [x] 036/T008 [agent][test] A one-owner table over the templates — covers R4, D3
      verified: tests/templates.test.mjs has a one-owner table over ten statements; re-adding "skip or delete a test" to the AGENTS template fails 1 test
- [x] 036/T009 [agent] Install the shipped copies in this repository and add `.gitattributes` — covers R5, D4
      verified: .agents/guard, .agents/playbooks, .agents/hooks.json, .claude/settings.json, CLAUDE.md and the workflow are installed from the assets; .gitattributes sets eol=lf; guard --all gives 0 errors and 0 warnings
- [x] 036/T010 [agent][test] Identity tests between each installed copy and its asset — covers R5, D4
      verified: tests/repo.test.mjs compares seven installed copies with their assets and checks the workflow runs the installed guard
- [x] 036/T011 [agent] Add the migration path and the non-software adaptation to `SKILL.md`; align README, PRODUCT, ARCHITECTURE, OPERATIONS, DESIGN, `.gitignore` — covers R6
      verified: SKILL.md has the migration path and the non-software note; README, PRODUCT, ARCHITECTURE, OPERATIONS, DESIGN and .gitignore are aligned; CHANGES.md has the audit entry
- [x] 036/T012 [agent][test] `SKILL.md` names what a migration touches — covers R6
      verified: tests/skill.test.mjs has rows over the migration section; the suite passes

## Changes

None yet.
