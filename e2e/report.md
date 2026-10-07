# End-to-end report

Results of running `e2e/scenario.md`. Evidence is the command, its exit code and the
relevant output; driver logs (prompts, harness output, snapshots) stayed outside the
repo.

## Claude Code

Claude Code 2.1.292, default model, print mode (`claude -p --output-format json`,
`--resume <session_id>`, `--dangerously-skip-permissions`). Throwaway repo:
`%TEMP%/spectrace-e2e/claude-code/`. Skills installed with
`pnpm dlx skills add SebassContreras/spectrace -a claude-code -s '*' -y --copy` →
`.claude/skills/spectrace-{start,plan,change}/` and `skills-lock.json`. The harness
also loads the driver machine's user-level instructions (`~/.claude/CLAUDE.md`);
nothing in them touches spectrace.

### R1 — interview, plan, three tasks, exact changes: **pass**

- `spectrace-start`: 38 turns, one conversation. Wrote `AGENTS.md` (protocol block
  included), `planning/{product,architecture,styles,roadmap}.md`, specs
  `001-storage` (R1–R7) and `002-cli` (R1–R4), `.spectrace/`. `trace check` → exit 0
  (one warning: `AGENTS.md` uncommitted, as expected before the driver's commit).
- `spectrace-plan` on 001: 12 turns. D1 (`tdo.json` in the current directory), D2
  (read and rewritten whole with `json`), D3 (`tdo/store.py` API); 8 open questions;
  T001–T010, five of them tests. The design gate asked about each uncovered R (R2, R5,
  R7) one at a time. `trace check` → exit 0.
- Three task conversations, prompt "Execute the next spectrace task. Don't commit.":
  001/T001, T002, T003 in order, one `todo → done` per conversation.

| Task | Driver diff vs. recorded patch | numstat = `changes:` |
|---|---|---|
| 001/T001 | EXACT | `tdo/__init__.py (+0 -0)`, `tdo/__pycache__/__init__.cpython-314.pyc (binary)` |
| 001/T002 | EXACT | `tdo/store.py (+27 -0)` |
| 001/T003 | EXACT | `tdo/__pycache__/store.cpython-314.pyc (binary)`, `tdo/store.py (+16 -0)` |

`git log` after the three tasks: only the two driver commits. `trace check` → exit 0.

Findings:

- **`.pyc` files recorded as task changes.** The target repo has no `.gitignore`, so
  bytecode written while a task verifies itself is part of the tree and of the task's
  recorded change. Exact, but noise — and the patch carries no binary data ("Binary
  files … differ"), so `trace restore` of such a task cannot reapply or reverse it.
  The harness noticed, did not touch `changes:`, and suggested a `.gitignore`.
  `spectrace-start` proposed a `scaffold` spec that would likely have carried one; the
  scenario declined it.
- **Inferred interview answers.** `spectrace-start` closed `project-type` (from the
  opening request, which the question bank says never closes it), `audience`,
  `runtime`, `framework`, `data-model`, `interface`, `identity`, `third-party`, both
  specs' `what`/`serves`/`owner-split` from earlier answers without asking. The
  inferences were right here, but the skill's contract says never infer to close a
  dimension.
- **Gaps** (questions the scenario didn't answer; answered consistently with it):
  how `tdo` is launched; which OS; accessibility; what "rejected" means for the title
  limit; the five storage edge cases; the CLI's exact output; the plan's open
  questions (left open).
- **Scenario fix.** The R1 compare command appended an `echo`, adding a newline the
  recorded patch doesn't have; corrected in `scenario.md`.
- The title-length item is `001/R7` in this run ("Adding a task whose title is longer
  than 80 characters raises an error and stores nothing; a title of exactly 80
  characters is accepted."); step 6 rewords that text.

### R2 — retire a design item: **pass, with a gap in the strict gate**

- Change conversation (4 turns): the skill first proposed *revising* D1/D2 to `@2`
  and *adding* an R8 the user never stated (offered for confirmation, not written).
  Asked to retire instead, it retired D1@1 → D4 and D2@1 → D5, added D4/D5 (SQLite),
  edited the open questions, wrote `changes.md`, and proposed T011 (`retires: T002`),
  T012 (SQLite helper), T013 (rewrite `add`'s body, which the sweep found calling the
  JSON helpers), and deleted not-started T010 (named `tdo.json`) for T014.
- Manifest: `impact 001/D1` and `001/D2` both list only 001/T002, `tdo/store.py: 19/19
  added lines still present` — T002's patch adds 27 lines, 19 non-blank; the JSON
  identifiers (`import json`, `tdo.json`, `json.load`, `json.dump`) all sit on those
  lines. The sweep also found `add`'s `_load()`/`_save()` calls (T003) — correct.
- `check --strict` before cleanup → exit 1 (`suspect: covers D1@1, retired`, same
  for D2@1). After T011 → exit 0. After T012, T013 → exit 0.
- After T013: `git grep --untracked` for `json`, `tdo.json`, `_load`, `_save` → nothing
  outside history; `sqlite3`/`tdo.db` in `tdo/store.py`.

Findings:

- **Strict gate covers only `retires:` tasks.** `check --strict` passed after T011
  while `add` still called the deleted `_load`/`_save` — stale code the change's own
  sweep found and gave to T013, which has no `retires:` and so isn't gated.
- **`trace.py` corrupts a patch whose last hunk ends in blank context lines.** `git()`
  returns `stdout.strip()`, so T011's recorded patch lost its last two context lines
  (`" "`): driver diff ≠ patch, and `git apply --check -R 001-T011.patch` → `corrupt
  patch at line 40`. `trace restore` of a retiring task is exactly what R4 needs.
- **Binary changes are recorded without data.** Patches come from `git diff` without
  `--binary`; a task that touched a `.pyc` (T001, T003, T011, T012 here) cannot be
  reverse-applied.
- **Scenario fix:** `git grep` skips untracked files; with no commits during the run
  every check needs `--untracked` (and `:(exclude)*.pyc`).
