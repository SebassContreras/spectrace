# 015 — e2e-graph — Design

## Approach

Reuse spec 006's scenario, driver and report; add only what the code map needs. The `tdo`
project already has the flows the code map must survive — a decision retired, replaced and
reinstated — and its code is written by agents, not by us.

- D1@1 (implements R1, R2, R3): `e2e/scenario.md` "Verification" gains three sections. Records: for each task, `NNN-TNNN.touch.json` against the driver's snapshots — the per-file totals equal `git diff --numstat` between them, and the symbols equal those a `git diff -U0` between them touches in the project's Python files. Why: the tasks `trace why tdo/store.py::<function>` lists after step 3, after step 4 and after step 5, compared with the tasks each step ran. Leftover: `check --strict` exits 1 after the change conversation, exits 0 after the last cleanup task, and its output then has no `leftover` line.
- D2@1 (implements R4): A new "Step 7 — Find and fix". The driver makes the title-length check in `tdo/store.py` off by one (the comparison `>` becomes `>=`, in whatever form the harness wrote it), logs the diff and does not commit. Prompt, in a new conversation: "Use the spectrace-fix skill. `tdo add` rejects a title of exactly 120 characters; it should accept it." Answers: the stray change → ignore; the classification → the code deviates from the title-length requirement, fix under it; the task list → approve. Then, in a new conversation: "Execute the next spectrace task. Don't commit." Checks: the transcript shows `trace locate` and `trace why`; a `kind: test` task precedes the new task, which has `kind: fix` and `covers:` the title-length item at its current revision; its record lists the function that holds the check as modified; `trace check --strict` exits 0; `trace why` on that function lists the fix task first.
- D3@1 (implements R5): `e2e/report.md` gains a "Code map" table with the result of each check per harness, plus the gaps and repeats, following the conventions the report already uses.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Reuse the `tdo` scenario | real agent-written code; retire and restore already scripted | Python only | other languages arrive with their adapters and their own gates |
| Inject the bug by hand in step 7 | a known, minimal defect; no commit needed | the driver edits code the harness wrote | the step says so, the diff is logged, and the stray change is answered with `--ignore` |

## Deliverables

- `e2e/scenario.md`
- `e2e/report.md`

## Sequencing

The scenario text first, then the Claude Code run, then the second harness, then the summary
table. A defect a run exposes becomes a new task that fixes it, and the failing step is repeated,
as in spec 006.
