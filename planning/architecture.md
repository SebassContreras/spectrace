# Architecture

Project-wide decisions. Item grammar: `.spectrace/format.md` (in this repo:
`skills/spectrace-start/assets/format.md`).

## Container

- A1@3: Four skills — `spectrace-start`, `spectrace-plan`, `spectrace-change`, `spectrace-fix` (prefixed: installed without a plugin namespace, a bare `plan` would collide with other skills; `spectrace-fix` arrives with spec 014). No orchestrator: any agent executes tasks by following the protocol `spectrace-start` writes into `AGENTS.md`.
- A2@2: One entry point, `trace.py`, and its package `spectrace/` — Python 3.9+, standard library only, git via subprocess. They are the only executables installed in a target repo, copied together into `.spectrace/` and updated as one unit — why: the code map needs more than one file, and one unit avoids version skew (010 compares by `VERSION`).
- A7@1: Skills target the open Agent Skills format and are written in English; the interview runs in the user's language.
- A8@1: `AGENTS.md` is the only instructions file a target repo gets; no `CLAUDE.md`.
- A12@1: The index is one `sqlite3` file (standard library), git-ignored and refreshed from file hashes — why: atomic writes and indexed queries without reloading a JSON file on every call.
- A13@1: Languages are read through adapters behind one interface: Python (`ast`) and Markdown (headings) in the core, any other file at file level. Another language enters only with a measured exactness gate, and optional dependencies are never required — why: precision before coverage; the core must run with git and Python alone.

## Conventions

- A3@1: Derived state is written only by `trace.py` — roadmap `Status`/`Stage`, task `in_progress`/`done`/`blocked`, `changes:` — and verified by `trace check`.
- A4@1: `format.md` is the single definition of the format. Skills cite it and never restate it; a test parses its examples.
- A5@4: Size budget — each `SKILL.md` body at most 200 lines, each module of `spectrace/` at most 600; enforced by `tests/test_skills.py` — why: one 900-line cap on `trace.py` no longer fits, and the limit exists to keep every file readable.
- A6@1: Changing direction: delete and redo by default; refactor in place only with a written justification in the spec's `changes.md`. A test covering a retired requirement is deleted, not adapted.
- A9@1: Conventional Commits; a commit for a task carries a `Spec: NNN/TNNN` trailer when there is one. Commits are optional for the trace.
- A10@1: The ledger records what each task changed down to symbols, at `done`; code relations live in a disposable index derived from the code and the ledger — why: a task's post-image is gone once the next one closes, and mapping hunks by line number to today's code hit the right symbol 35% of the time.
- A11@1: Every conclusion about code carries a confidence — exact (recorded or parsed) or inferred (heuristic, with its number of candidates). Only exact findings may hold a spec open; inferred ones warn and never claim "no impact" — why: static call-graph analysis of Python misses about 30% of the edges even in the best tools, and a heuristic must not gate.

- A14@1: A decision that gets in the way is never worked around: the task is blocked with the conflict, and the user keeps the decision, edits it or retires it — why: a workaround is accidental complexity, and it turns the old decision into a statement the code no longer follows.
- A15@1: Only what the MVP needs is built, by the simplest route; the rest is postponed without debate — why: guessing a distant future costs more than changing a decision when it stops fitting.
