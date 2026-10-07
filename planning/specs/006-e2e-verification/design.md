# 006 — e2e-verification — Design

## Approach

- D1@1 (implements R1, R3): Each run uses a fresh throwaway git repo outside this one (`%TEMP%/spectrace-e2e/<harness>/`), with the skills installed from the published repo by `pnpm dlx skills add SebassContreras/spectrace` — the install users get, not this working tree.
- D2@1 (implements R1, R2, R4, R5): One fixed scenario, written before any run in `e2e/scenario.md`: a small Python stdlib to-do CLI with two specs (`storage`, `cli`); the design item to retire (tasks stored in a JSON file → SQLite) and its later reinstatement; one wording edit and one meaning edit of a built-on item; and the exact prompt given at each step.
- D3@1 (implements R1, R3): This session plays the user. Each interview turn is a print-mode call resumed by conversation ID (`claude -p --resume <id>`, `agy -p --conversation <id>`), answered from the scenario; a question the scenario doesn't answer is answered consistently with it and logged as a gap.
- D4@1 (implements R1): Each task runs in its own fresh print-mode session whose whole prompt is "Execute the next spectrace task. Don't commit." — the target repo's `AGENTS.md` and the installed skills are its only instructions.
- D5@1 (implements R1): Exactness is checked independently of trace: before and after each task session the driver snapshots the tree with `git write-tree` on a temporary index (`GIT_INDEX_FILE`); that diff, minus `planning/` and `.spectrace/`, must equal the task's `.spectrace/changes/NNN-TNNN.patch` and its `changes:` line.
- D6@1 (implements R2): Retire check: `trace impact` before the change must list exactly the files and lines D5's snapshots attribute to the retired item's tasks; `trace check --strict` exits 1 until the cleanup tasks are done and 0 after; `git grep` for the retired decision's identifiers then finds nothing.
- D7@1 (implements R4): Restore check: after the restoring task, the tree outside `planning/` and `.spectrace/` matches the pre-cleanup snapshot, and the restored files appear in the restoring task's `changes:`.
- D8@1 (implements R5): Edit check: the wording edit makes `trace check` report `changed`, `trace review` clears it, and the revision stays; the meaning edit through `spectrace-change` bumps it to `@2` and the tasks covering it show as suspect.
- D9@1 (implements R3): Same scenario, Claude Code first, then agy. Results go to `e2e/report.md`: pass/fail per R item and harness, with the commands and exit codes as evidence, plus every gap and deviation. A defect in a skill or `trace.py` gets fixed here through `spectrace-change` (new tasks in this spec), then the failed step is run again.
- D10@1 (implements R1, R3): Harness sessions run with `--dangerously-skip-permissions` (both CLIs have it), confined to the throwaway dir — a permission prompt in print mode would stall the run.

## Deliverables

- `e2e/scenario.md`
- `e2e/report.md`

## Sequencing

Scenario before any run. Per harness, on the same throwaway repo: R1 → R2 → R4 (restores what R2 retired) → R5.

## Open questions

- Whether agy reads the project's `AGENTS.md`: its changelog only confirms a global `~/.gemini/AGENTS.md` and `.agents/skills/`. Checked at the start of its run. If it doesn't, that goes in the report as a finding, with no workaround.
- How to get agy's conversation ID for `--conversation`, and which agent name the `skills` CLI uses for agy. Both are verified at run time, not guessed.
