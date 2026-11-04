# 035 — single-skill

## Goal

One skill, `spectrace`, scaffolds a project: eight single-responsibility root contracts, three repo-owned playbooks, and a `guard` that enforces the deterministic rules in Claude Code, Antigravity and CI. Planning, change handling and review live in the repository, not in the skill. Verify: scaffold a temp repo, run `guard --all` (passes), break a spec, run it again (fails with the rule named).

## Requirements

- R1: `skills/` holds exactly one skill, `spectrace`, with modes `init` and `update` (diff per file, applies only what the user approves). The four old skills, `bin/` and the package `bin` entry are gone.
- R2: Eight root contracts (AGENTS, PRODUCT, ARCHITECTURE, ENGINEERING, DESIGN, TESTING, CHANGES, OPERATIONS), each opening with `> Owns: … · Not here: …`. PRODUCT has no non-goals section.
- R3: `AGENTS.md` is a router of at most 100 lines (hard rules first, then a "before you act, open" table) pointing at `.agents/playbooks/{plan,change,review}.md`.
- R4: `guard` blocks, deterministically: Claude co-author trailers and "Generated with" lines, `--no-verify`, force-push to main, `git add` of `.env`. It lints specs (structure, every R covered by a task and by a `[test]` task, `[x]` needs `verified:`), roadmap coherence, contract headers, and scans a commit range.
- R5: Adapters: `.claude/settings.json` (`attribution` and hooks), `.agents/hooks.json` (Antigravity), `CLAUDE.md` (`@AGENTS.md`) and a CI workflow, all calling the one script.
- R6: Payload shapes of both agents are recorded from real sessions before the adapters are trusted.

## Design

- D1 (R4, R5): `guard.mjs`, zero dependencies, pure functions behind a thin CLI: `--agent claude|antigravity`, `--event PreToolUse|PostToolUse|Stop`, `--all`, `--commits <range>`, `--record`. Claude blocks with exit 2 and stderr; Antigravity with JSON `{"decision":"deny"}` on stdout. Antigravity's payload has no event name, so the event comes from the argument. Source: https://code.claude.com/docs/en/hooks.md, https://antigravity.google/docs/hooks (accessed 2026-11-04).
- D2 (R4): Shell commands are tokenised respecting quotes before any rule runs, so `git commit -m "explain --no-verify"` is not blocked. A hook that fails is not a block (Claude: any exit except 2; Antigravity: undocumented), so CI runs `guard --all` and `--commits`.
- D3 (R4): A spec's `[test]` task tags a task that writes or runs a test. Struck items (`~~D1~~ → D2`) are ignored for coverage; the arrow target must exist. Length over 80 lines is a warning, never an error.
- D4 (R5): `attribution` is written in its compatible object form (`commit` and `pr` empty, `sessionUrl` false) because `false` is rejected by Claude Code before 2.1.281 and the whole file is then skipped. Source: https://code.claude.com/docs/en/settings-reference.md#attribution (accessed 2026-11-04).
- D5 (R3): Playbooks are plain Markdown routed from `AGENTS.md`, not skills or vendor rules, so both agents reach them without invocation. Antigravity loads `AGENTS.md` natively; Claude Code reads it through `CLAUDE.md`. Source: https://code.claude.com/docs/en/memory.md (accessed 2026-11-04).
- D6 (R1, R2): Templates come from what the author's own repos share (browser-nav, job, lienzo), with project specifics stripped.

### Trade-offs

- Repo-owned playbooks may drift from the skill's newest copy; `update` shows the diff. In exchange they work without invoking a skill and the repo can edit them.
- No Stop-time test run in v1: it would run a suite at every turn end. Left in `## Ideas`.

## Tasks

- [x] 035/T001 [agent] `guard.mjs` core: quote-aware tokeniser and the commit, push and `.env` rules — covers R4, D1, D2
      verified: guard.mjs: quote-aware parseShell plus commit, push and .env rules; mutation check (rule disabled) fails 8 tests
- [x] 035/T002 [agent][test] Table-driven tests for those rules, including quoted-text false positives — covers R4, D2
      verified: tests/guard.test.mjs: 29 command rows incl. quoted flag text and heredocs with unbalanced parens; all pass
- [x] 035/T003 [agent] Spec lint and roadmap coherence — covers R4, D3
      verified: lintSpec, parseSpec, checkRoadmap implemented; guard passes spec 035 itself
- [x] 035/T004 [agent][test] Table-driven tests: missing section, uncovered R, no `[test]` task, `[x]` without `verified:`, struck item, done with open tasks — covers R4, D3
      verified: 17 spec rows and 11 roadmap rows pass; removing the verified: check fails 7 tests, removing per-R test coverage fails 2
- [x] 035/T005 [agent] Contract headers, `AGENTS.md` length, `--commits` range scan and `--all` — covers R4
      verified: checkContract, checkContracts, checkCommitMessages, checkAll; range scan tested against a real temp git repo
- [x] 035/T006 [agent][test] Tests for headers, length thresholds and range scan — covers R4
      verified: 7 contract rows (header, 100/101/200/201 line boundaries) plus 4 repo rows and 2 range rows pass
- [x] 035/T007 [agent] Claude and Antigravity payload translators, output formats and `--record` — covers R4, R6, D1
      verified: contextOf, handleHook, render for claude (exit 2) and antigravity (JSON, provisional), plus --record
- [x] 035/T008 [agent][test] Tests of both translators against payloads copied from the docs — covers R4, R6
      verified: 11 adapter rows with payload shapes taken from the hook docs; Stop with stop_hook_active allows; 95/95 pass
- [x] 035/T009 [agent] Templates: eight contracts, `AGENTS.md` router and three playbooks, distilled from the author's repos — covers R2, R3, D5, D6
      verified: 14 template files written from the principles and rules shared by browser-nav, job and lienzo; principle 4 now carries the 2+ vendors condition
- [x] 035/T010 [agent][test] Contract suite over the templates: headers, no non-goals, one owner per command, router targets exist, 100-line cap — covers R2, R3
      verified: tests/templates.test.mjs: 40 rows (headers, owner uniqueness, section ownership, router targets, spec example lints clean); 3 mutations (non-goals, broken router, example without [test]) each fail the suite
- [x] 035/T011 [agent] `SKILL.md` (init and update) and the adapter templates (`settings.json`, `hooks.json`, `CLAUDE.md`, CI workflow) — covers R1, R5, D4
      verified: SKILL.md (82 lines) plus claude-settings.json, antigravity-hooks.json, CLAUDE.md and guard.yml; ${CLAUDE_PROJECT_DIR} in args confirmed in the hooks docs (exec form substitutes each args element)
- [x] 035/T012 [agent][test] Scaffold into a temp repo and assert `guard --all` passes, then fails after a deliberate break; adapter JSON is valid — covers R1, R5
      verified: tests/skill.test.mjs: scaffold of all three kinds passes guard --all, breaks as expected; hooks run with the exact args from claude-settings.json give real exit code 2; 186/186 pass; 3 mutations fail 1, 1 and 4 tests
- [ ] 035/T013 [agent] Delete the four old skills, `bin/`, `package.json` bin and specs 021–034; shrink README, PRODUCT, ARCHITECTURE; record the pivot in `CHANGES.md` — covers R1
- [ ] 035/T015 [agent] Bring this repository to the new layout: its own eight contracts, `.claude/settings.json`, `.agents/hooks.json` and a CI workflow calling the guard from `skills/spectrace/assets/guard/` — covers R2, R5
- [ ] 035/T016 [agent][test] A test runs `guard --all` on this repository and requires exit 0 — covers R2, R5
- [ ] 035/T014 [human] Run `guard --record` inside real Claude Code and Antigravity sessions and confirm the payload fields and block behaviour — covers R6

## Changes

None yet.
