# spectrace

Interview → traceable specs → any agent executes them → a change of direction
lists exactly what to remove or redo. See `planning/product.md`.

## Doc map

- `planning/product.md` — what this is, who it's for, out of scope.
- `planning/architecture.md` — project-wide decisions (A items). Read before proposing structure.
- `planning/roadmap.md` — specs, order, status. `python skills/spectrace-start/assets/trace.py status` is the live view.
- `planning/specs/NNN-name/` — `requirements.md` (R), `design.md` (D), `tasks.md`, `changes.md`.
- `skills/spectrace-start/assets/format.md` — the format. Single source; cite it, never restate it.

## Rules for agents

- Every `SKILL.md` follows the Agent Skills spec (agentskills.io/specification): frontmatter `name` (equal to its folder name) and `description` (what it does and when to use it, at most 1024 characters) only; paths relative to the skill root; body at most 200 lines (A5).
- Never change an R, D or A item's meaning by hand: bump or retire it and record it in the spec's `changes.md` (the `spectrace-change` skill).
- Never edit `Status`/`Stage` in the roadmap, a task's status, or a `changes:` line — `trace.py` owns them (A3).
- Never guess a CLI flag or file format — verify it before writing it into a skill.
- No GitHub repository, remote or push until the maintainer asks.

<!-- spectrace:protocol -->
## Working on tasks

In this repo the script is `skills/spectrace-start/assets/trace.py` (target repos get it at
`.spectrace/trace.py`). Use `python` on Windows, `python3` elsewhere.

When executing tasks (even across multiple specs), loop steps 1–5 for each task:
1. `python skills/spectrace-start/assets/trace.py status` — pick the `next` task, or the one you were asked for.
2. `python skills/spectrace-start/assets/trace.py start NNN/TNNN` — before editing anything. Never edit files without an open task.
3. Read the spec's `requirements.md` and `design.md` (or the items printed by `start`); do only that task.
4. Verify it against the task text and the R items it covers.
5. `python skills/spectrace-start/assets/trace.py done NNN/TNNN` — records exactly what changed. Stuck? `block NNN/TNNN "reason"`. Always close the open task before moving to the next task or next spec.
6. Before saying you're finished with the session: `python skills/spectrace-start/assets/trace.py check` must exit 0 (run once at the end of the session, not after every individual task).
<!-- /spectrace:protocol -->
