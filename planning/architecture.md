# Architecture

Project-wide decisions. Item grammar: `.spectrace/format.md` (in this repo:
`skills/spectrace-start/assets/format.md`).

## Container

- A1@2: Three skills — `spectrace-start`, `spectrace-plan`, `spectrace-change` (prefixed: installed without a plugin namespace, a bare `plan` would collide with other skills). No orchestrator: any agent executes tasks by following the protocol `spectrace-start` writes into `AGENTS.md`.
- A2@1: One script, `trace.py` — Python 3.9+, standard library only, git via subprocess. It is the only executable installed in a target repo, copied into `.spectrace/`.
- A7@1: Skills target the open Agent Skills format and are written in English; the interview runs in the user's language.
- A8@1: `AGENTS.md` is the only instructions file a target repo gets; no `CLAUDE.md`.

## Conventions

- A3@1: Derived state is written only by `trace.py` — roadmap `Status`/`Stage`, task `in_progress`/`done`/`blocked`, `changes:` — and verified by `trace check`.
- A4@1: `format.md` is the single definition of the format. Skills cite it and never restate it; a test parses its examples.
- A5@3: Size budget — each `SKILL.md` body at most 200 lines, `trace.py` at most 900; enforced by `tests/test_skills.py`.
- A6@1: Changing direction: delete and redo by default; refactor in place only with a written justification in the spec's `changes.md`. A test covering a retired requirement is deleted, not adapted.
- A9@1: Conventional Commits; a commit for a task carries a `Spec: NNN/TNNN` trailer when there is one. Commits are optional for the trace.

