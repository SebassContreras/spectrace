# spectrace

**Specs you can change your mind about.**

[![CI](https://github.com/SebassContreras/spectrace/actions/workflows/ci.yml/badge.svg)](https://github.com/SebassContreras/spectrace/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](skills/spectrace-start/assets/trace.py)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2.svg)](https://agentskills.io)
[![Dependencies: none](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#install)

spectrace turns a plain-language description of a project into specs — requirements,
design, tasks — where every decision has an ID and a revision, and every task records
exactly what it changed. When you change your mind, it lists every task, file, line and
test that implemented the old decision and turns them into cleanup tasks, so nothing
from the old approach is left behind. Any coding agent can execute the tasks; there is
no orchestrator to run.

> **Status:** early. The trace is tested on Linux and Windows (Python 3.9 and 3.13);
> the full flow with a fresh agent is not yet verified end to end
> ([spec 006](planning/specs/006-e2e-verification/requirements.md)).

## Install

From your project's folder:

```sh
pnpm dlx skills add SebassContreras/spectrace
```

The [`skills` CLI](https://github.com/vercel-labs/skills) copies the three skills into
the folder your agent reads — `.claude/skills/` for Claude Code, `.agents/skills/` for
OpenCode, Codex, Cursor, GitHub Copilot and most others. Add `-g` to install for every
project, `--skill '*' -y` to skip the prompts; `pnpm dlx skills update` updates them.

Running spectrace needs **git** and **Python 3.9+** in the project. Nothing else.

## How it works

```
 you describe the idea          any agent executes            you change your mind
          │                             │                              │
          ▼                             ▼                              ▼
 spectrace-start ──► spectrace-plan ──► trace start / done ──► spectrace-change
 interview → R items  design → D items   exact diff per task      revise / retire →
 roadmap, A items     tasks + covers:    (no commit needed)       manifest → cleanup tasks
```

| Skill | What it does |
|---|---|
| `spectrace-start` | Interviews you one question at a time (any project type, English or Spanish) and writes `planning/`: product, architecture (A items), roadmap, and each spec's requirements (R items). Installs `.spectrace/trace.py` and the task protocol in `AGENTS.md`. |
| `spectrace-plan` | Closes a spec's design — D items, each naming the R items it implements — and breaks it into single-action, verifiable tasks, each declaring what it `covers:`. |
| `spectrace-change` | Revises, rewords, retires or reinstates decisions, records why, and turns everything that implemented the old one into cleanup tasks: redo by default, refactor only with a written reason. |

## Executing tasks

Tell your agent to execute the specs. The protocol `spectrace-start` writes into
`AGENTS.md` has it run:

```sh
python3 .spectrace/trace.py status          # what's next
python3 .spectrace/trace.py start 002/T004  # snapshot before editing
python3 .spectrace/trace.py done 002/T004   # record exactly what changed
python3 .spectrace/trace.py check           # must pass before finishing
```

`start` and `done` snapshot the working tree without committing or touching the
staging area, so each task's diff is exact even when several tasks share one commit or
none. The diff is kept in `.spectrace/changes/` and summarized on the task. The roadmap's
`Status` and `Stage` columns are computed from the files, never typed.

## Changing direction

```
- ~~D1@1 (implements R1): Sessions live in localStorage.~~ retired 2026-10-12 → D3
- D3@1 (implements R1): Sessions live in an httpOnly cookie.
```

```
$ python3 .spectrace/trace.py impact 001/D1
- 001/T001 [agent] [done] Session store
    src/store.ts → src/session/store.ts: 14/14 added lines still present
```

The spec can't read as done until that work is removed or redone. `trace check`
reports, and the spec stays open, while any of these hold:

| State | Meaning |
|---|---|
| **suspect** | A finished task covers an older revision of an item, or a retired one. |
| **changed** | An item's text changed under finished work without a revision bump (`trace review` accepts a wording-only edit). |
| **mentions a deleted file** | A file a task deleted is still named somewhere outside history. |
| **uncovered** | A requirement no design item or task covers; a design item no task covers. |
| **orphan** | A reference to an item or task that doesn't exist. |

To go back to a retired approach, `trace restore NNN/TNNN` undoes the task that removed
it, inside a new task, so the restored code is traced too.

The whole format is defined once, in
[`skills/spectrace-start/assets/format.md`](skills/spectrace-start/assets/format.md).

## Limits

- **Meaning in prose.** A sentence that describes an old decision without naming a file
  is found by `spectrace-change`'s term sweep — an agent's judgement — not by a check.
- **Agent discipline.** Edits made outside a task are reported (`check`, and `start`
  refuses until they're adopted or ignored), not prevented.
- **Work outside the repo** — a CMS, an email, a dashboard setting — leaves no diff to
  trace; record it as a `[human]` task.
- **One open task at a time.** Parallel agents in one working tree would mix their diffs.

## Development

```sh
python3 -m unittest discover -s tests
python3 skills/spectrace-start/assets/trace.py check
```

This repository is planned and built with spectrace itself: see
[`planning/`](planning/roadmap.md) and [`AGENTS.md`](AGENTS.md).

## License

[MIT](LICENSE)
