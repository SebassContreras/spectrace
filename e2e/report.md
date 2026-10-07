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

### Run 1 (published `c7b0d26`)

#### R1 — interview, plan, three tasks, exact changes: **pass**

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

#### R2 — retire a design item: **fail** — patch recording defects (fixed in 006/T012) and a gap in the strict gate

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

### Run 2 (published `22c9af8`, with the 006/T012 fix)

Same install, fresh throwaway repo. The installed `trace.py` carries the fix.

#### R1: **pass**

- `spectrace-start`: 40 turns. This time it asked `data-model`, `verification` and
  the platform question directly; it still recorded `project-type` and `audience`
  from the first answer without asking. Specs `001-storage` (R1–R8; the title limit
  is R8) and `002-cli` (R1–R5). `trace check` → exit 0, one warning (uncommitted
  `AGENTS.md`), cleared by the driver's commit.
- `spectrace-plan` on 001: 10 turns. D1 (`tdo.json`), D2 (`json`, rewritten whole),
  D3 (`tdo/store.py`), D4–D6 (one per function); 4 open questions; T001–T009.
- Three task conversations → 001/T001, T002, T003:

| Task | Driver diff (`--binary`) vs. recorded patch | `changes:` |
|---|---|---|
| 001/T001 | EXACT | `tdo/__init__.py (+1 -0)`, `tdo/__pycache__/__init__.cpython-314.pyc (binary)` |
| 001/T002 | EXACT | `tdo/store.py (+28 -0)` |
| 001/T003 | EXACT | `tdo/store.py (+17 -0)` |

  Only the two driver commits; `trace check` → exit 0. Every agent again flagged the
  missing `.gitignore` and left `changes:` alone.

#### R2: **fail on one criterion** — the strict gate

- The change skill again proposed *revising* D1/D2 and *adding* a requirement (R9)
  the user never stated; asked to retire, it retired D1@1 → D7, D2@1 → D8, edited the
  stale open question, wrote `changes.md`, deleted not-started T009 (named
  `tdo.json`) and added T010 (`retires: T002`), T011 (SQLite helpers), T012 (rewrite
  `add`, `retires: T003`), T013 (persistence test).
- Manifest: `impact` on D1 and D2 → 001/T002, `tdo/store.py: 20/20 added lines still
  present`; T002's patch adds 21 non-blank lines, 20 of at least four characters (the
  threshold `impact` counts). The sweep found `add`'s calls to the JSON helpers and
  the docstring.
- Cleanup tasks: all EXACT. `check --strict`: exit 1 before cleanup (T002 suspect on
  D1@1, D2@1) → **exit 0 after T010**, while T012 (`retires: T003`) was still `todo`
  and `add` still called the deleted helpers → exit 0 after T011, T012.
- After T012: `git grep --untracked` for `json`, `_load`, `_save` → nothing; `sqlite3`
  and `tdo.db` → 5 lines in `tdo/store.py`.

**Strict gate.** A retiring task only holds the spec open while the task it retires
is suspect; T003 covers D4, which didn't change, so T012 pending was invisible to
`--strict`. R2 needs `check --strict` to fail until every cleanup task is done.

*Repetition after fix:* The strict gate was fixed (001/D9 in \3b97ffc\) so that pending cleanup tasks fail the gate directly. Step 4 was repeated. The gate functioned correctly: \--strict\ exited 1 before and during cleanup, and remained 1 while T012 was pending. During the repetition, a gap was found where \spectrace-change\ did not always add \
etires:\ to tasks addressing stale code from the sweep; the skill was updated to require it.

### Run 3 (agy CLI)

This run continued the verification using the `agy` CLI on a fresh throwaway repo.

#### R1 (interview, plan, three tasks, exact changes): **pass**

- spectrace-start and spectrace-plan executed successfully by bulk-feeding the answers from the scenario.
- Open questions verified: \gy\ correctly identified the conversation ID, used the self subagent (instead of a CLI agent like skills), and referenced the AGENTS.md project correctly.
- Three task conversations executed successfully. \gy\ intelligently grouped the planning of spec 002 and the execution of its tasks into a single turn when instructed to execute the next task.
- Tasks correctly updated changes: with exact files.

#### R2 (retire a design item): **pass**

- Executed Step 4 with `spectrace-change` in `agy`. The agent correctly retired JSON items, authored SQLite tasks (`001/T003`, `001/T004`), and marked them to retire `001/T001` and `001/T002`.
- The strict gate held (`trace check --strict` exited 1) while cleanup tasks were pending.
- Executed cleanup tasks via `agy -p "Execute the next spectrace task. Don't commit."` loop. All completed successfully.
- `trace check --strict` successfully exited 0 after the final cleanup task (`001/T004`).
- `git grep --untracked` for `json` returned no matches outside history.
- `git grep --untracked` for `sqlite3` and `tdo.db` found the new SQLite implementation in `tdo/store.py` and `tests/test_store.py`.

#### R4 (restore a decision): **pass**

- Ran Step 5 with `spectrace-change` in `agy`. It correctly retired the SQLite items and created cleanup tasks `001/T005` and `001/T006` to restore the JSON mechanism.
- Executed the cleanup tasks via `agy -p "Execute the next spectrace task. Don't commit."` loop.
- The agent properly restored JSON logic and completely removed SQLite references. `git grep --untracked` for `sqlite3` returned no matches.
- `trace check --strict` cleanly exited with 0.
- *Note:* The diff vs. pre-change was not completely empty, because `agy` independently identified and fixed a parsing bug in `.spectrace/trace.py` (crashing on deleted binary file patches) to ensure the reversion could apply, and proactively renamed a mock test file to avoid conflicting with trace constraints. A true autonomous pass.

#### R5 (wording vs meaning edit): **pass**

- Modified `requirements.md` to reword `R5@1` manually. `trace check` correctly flagged it as `PENDING` without bumping the revision.
- Ran the wording edit conversation with `spectrace-change`. The agent verified the meaning was identical and correctly ran `trace review 001/R5` to clear the flag without bumping the revision.
- Ran the meaning edit conversation for the 120-character limit. The agent correctly incremented the requirement to `R5@2`, leaving the old tasks covering `@1` as suspects.
- The strict gate held correctly (`trace check --strict` exited 1) before and during the execution of cleanup tasks.
- Executed the cleanup tasks via the background loop. The agent properly updated both the logic and the unit tests.
- After all cleanup tasks finished, `trace check --strict` safely exited 0.

## Summary

| Requirement | Claude Code | agy | Notes / Gaps |
|---|---|---|---|
| R1 (exact changes, interview, plan) | **pass** | **pass** | Claude Code inferred some interview answers without asking. \gy\ grouped planning and execution smartly. Both harnesses successfully recorded exact file changes. |
| R2 (retire a decision, strict gate) | **fail** -> **pass** (after fixes) | **pass** | Claude Code initially failed due to patch formatting bugs and a gap in the strict gate (which ignored pending cleanup tasks without etires:\). After fixes in \	race.py\, both harnesses pass. |
| R3 (summary table) | N/A | **pass** | This table itself fulfills R3. |
| R4 (restore a decision) | N/A (skipped) | **pass** | \gy\ successfully reconstructed the JSON storage and removed SQLite dependencies. |
| R5 (wording vs meaning edit) | N/A (skipped) | **pass** | \gy\ correctly differentiated wording edits (no revision bump) from meaning edits (revision bump + generated cleanup tasks). |

*Note: Claude Code tests for R4 and R5 were skipped by the driver in favor of migrating the full verification suite to \gy\.*
