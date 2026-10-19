# 010 — upgrade — Design

## Approach

Text-only change to `spectrace-start`; no `trace.py` change. The upgrade procedure lives in
one new reference file, `references/upgrade.md`, that `SKILL.md` points at from Phase 0 and
Phase 3, so the check and the write rules exist once (DRY, A4) and `SKILL.md` stays under its
200-line budget (A5). Every comparison uses a command whose output is exact, not a reading
by eye: the old `.spectrace/trace.py` can't be trusted to know about newer files, so the
bundled files in the skill's `assets/` are always the reference.

- D1@1 (implements R1, R8, R9): `references/upgrade.md` defines the check as four probes, each with its command: (a) `python3 .spectrace/trace.py --version` against `python3 assets/trace.py --version` (`python` on Windows), outdated when the repo's number is lower; (b) `git diff --no-index --stat .spectrace/format.md assets/format.md`, outdated when not empty; (c) the text between `<!-- spectrace:protocol -->` and `<!-- /spectrace:protocol -->` in `AGENTS.md` compared with `assets/agents-protocol.md` the same way, outdated when it differs or the markers are missing; (d) each `## ` heading of the `AGENTS.md` template in `references/templates.md` that the repo's `AGENTS.md` lacks, skipping "Testing" when `project-type` is not `software`. No probe outdated → nothing is said and the caller continues.
- D2@1 (implements R1, R8): `SKILL.md` Phase 0 gains a step before "the project exists": when `planning/product.md` has real content and `.spectrace/` exists, run the check in `references/upgrade.md`; continue to Phase 6/7 after it, or straight away when nothing is outdated.
- D3@1 (implements R9): `SKILL.md` Phase 0 routes a direct request ("update spectrace in this project", "actualiza spectrace") to the check alone, and ends after its report without starting Phase 6.
- D4@1 (implements R2, R3): Before writing, `upgrade.md` prints one summary — trace `old → new`, the `format.md` diff stat, the protocol diff (`git diff --no-index` of the two texts) and the missing section names — then asks per item (trace + format as one item, protocol, each section) yes / skip. A skipped item is not written and is listed in the report.
- D5@2 (implements R4): Accepted trace and format items copy `assets/trace.py` and `assets/format.md` over `.spectrace/`, and replace the package as one unit: `assets/spectrace/` is copied to `.spectrace/spectrace.new/`, the old folder deleted, and the new one renamed into place. The protocol item replaces only the text between the markers (appends the block with markers when they are absent), the same rule as Phase 3 step 4; the skill then confirms with `git diff AGENTS.md` that no line outside the block changed.
- D6@1 (implements R5): An accepted missing section is inserted at its template position (after the previous template heading present in the file, else before the protocol block) with the template text. When the section needs interview answers, the skill asks only the question-bank dimensions that feed it and follows the phase that fills it — for "Testing", Phase 4's rule: each `toolchain` command run once, `none` for a missing mode, `TBD` when unanswered — and records them in `.spectrace/interview.md`.
- D7@2 (implements R6, R7): The upgrade writes only `.spectrace/trace.py`, `.spectrace/spectrace/`, `.spectrace/format.md`, `.spectrace/interview.md` and `AGENTS.md`. It runs `trace check` before writing and again after; when the first passed and the second fails, it prints the output and says the upgrade caused it, without reverting silently or editing `planning/`.
- D8@1 (implements R10): `README.md` "Install" says that updating is two steps: `pnpm dlx skills update`, then run `spectrace-start` (or ask "update spectrace in this project") inside each project.
- D9@1 (implements R11): `tests/test_skills.py` passes after the edits; `spectrace-start/SKILL.md` stays at most 200 lines.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Procedure in the skill, no `trace.py upgrade` command | No code, no `VERSION` bump; an old installed trace isn't needed to upgrade itself | The agent runs the probes, not a program | Each probe is one exact command (`--version`, `git diff --no-index`); D5 checks the result with `git diff` |
| Bundled `assets/` as the reference | Same source Phase 3 copies from; nothing new to keep in sync | Needs the skill's folder path | Paths are relative to the skill root, as Phase 3 already does |
| Format compared by content, trace by `VERSION` | Matches R1; a local edit to `format.md` shows up | A trace with the same `VERSION` but edited code isn't detected | Out of scope: `VERSION` is the trace's contract; hand edits to it are already against A3 |
| One yes/skip per item | User keeps any local tweak they want (R3) | More prompts | Trace + format grouped as one item; nothing asked when nothing is outdated (R8) |
| Missing-section check by heading only | Simple, never touches existing text (R5) | Rules added later inside an existing section (e.g. 008's default agent rules) aren't offered | Shown as a known limit in `upgrade.md`; a later spec can add per-section diffs |

Grounding: `git diff --no-index <a> <b>` compares two paths outside the index and exits 1
when they differ (git-scm.com/docs/git-diff); git is already required by Phase 3.

## Deliverables

- `skills/spectrace-start/references/upgrade.md` (new)
- `skills/spectrace-start/SKILL.md`
- `README.md`

## Sequencing

`upgrade.md` first (it defines the check and writes), then the `SKILL.md` hooks that call it,
then the README, then the test run.
