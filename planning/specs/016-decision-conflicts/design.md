# 016 — decision-conflicts — Design

## Approach

Decisions stay binding; what changes is how they change. The mechanism reuses what exists: a
task is already `blocked` with a reason, `start` already resumes a blocked task, and
`spectrace-change` already revises and retires. An item no finished task covers is already
free to edit (001 D7: the trace re-baselines it), so a decision can change spec by spec until
something is built on it; after that, a bump and the usual cleanup.

- D1@1 (implements R1): `cmd_block` treats a reason that starts with `conflicts ` as a conflict: what follows must be a reference `find_item` accepts (`A5`, `011/D2`; revision optional) and a `:`, otherwise it raises and writes nothing. Any other reason is unchanged.
- D2@1 (implements R2): `parse_tasks` keeps the last `└─ blocked: conflicts <ref>: <why>` note of a task, and the trace states report one pending per agent task that is `blocked` and has it: `decision conflict: <ref> — <why>; keep it, edit it or retire it (spectrace-change), then resume with start`, on the task's spec. When the task leaves `blocked` the note stays as history and is ignored. A blocked task without the prefix is unchanged.
- D3@1 (implements R3): `spectrace-change` gains "Phase 0b — Start from a conflict", entered when the user names a conflict or `check` lists one. It shows the item's text and the reason and asks: keep, edit or retire, proposing the simplest direct change first ("<ref> forces over-engineering; propose X. Approved?"). Keep writes no decision and adds `└─ conflict kept YYYY-MM-DD: <how the task will fit>` under the task; the agent resumes it with `start`. Edit and retire continue with Phases 1–5, the item preselected and the reason as the entry's `Why`; the blocked task is then re-pointed or replaced like any task that covers a changed item. Phase 5 also allows the conflicts of the changed item among the pending ones.
- D4@1 (implements R4): The `product.md` template in `references/templates.md` has `## What this is`, `## Who uses it`, `## Current MVP scope` and `## Not for now`; `spectrace-start` Phase 3 fills them from `goal`, `audience` and the two questions of the `mvp` dimension (what is in, what is explicitly not), which the question bank already asks. Existing `product.md` files are not touched (010 R6).
- D5@1 (implements R5): `agents-protocol.md` gains one short paragraph, "When a decision is in the way": do not work around it; `block` with `conflicts <ref>: <why>`; propose changing it by the simplest direct route and let the user keep, edit or retire it; and the scope filter — needed for the MVP, in by the simplest route; not needed, postponed without debate. `spectrace-plan` Phase 0 step 4 and its Phase 1 rule on a contradicting A item propose the change instead of designing around it or stopping. `format.md` documents the conflict note, the pending state, and that an item no finished task covers can be edited freely. The 010 upgrade check carries the paragraph to repos that already have the protocol block.
- D6@1 (implements R6): This repo's `AGENTS.md` "Working on tasks" gets the protocol's paragraph and `product.md` "Scope filter" becomes a pointer to it, so the rule lives in one place. The items 002/R4@1, 002/D4@1, 010/R4@1, 010/D5@1 and 010/D7@1 name only `trace.py` and `format.md` as what is copied, replaced or written; a `spectrace-change` session, between tasks because the skill refuses while one is open, revises each to include the `spectrace/` package and re-points the done tasks that covered the old revision as still valid, citing 011/T008, which wrote the package install. It refactors in place for the reason of the 2026-10-19 entry: that text keeps its structure and gains the folder. 007/D2@1 and D3@1 say "in `trace.py`'s `cmd_start`" and "`cmd_done`"; they are reworded to "the `start` handler" and "the `done` handler", then `trace review`.
- D7@1 (implements R7): `fingerprints.json` keeps the hash of every active A item and the ID of every item seen, not only of built ones. The first time an item is seen it is baselined without a finding, so adopting a repo is silent. After that, for an A item or an item a finished task covers, `check` reports as pending: its text changed with the same revision (the existing `changed` rule, no longer needing a covering task for A items); its ID missing without being struck through; its revision above the baseline, or a retirement, with no `changes.md` entry naming the reference (the spec's file, or `planning/changes.md` for A). Who changed it is `git blame` on that entry; no field is added. R and D items of a spec nothing has been built on stay free to edit.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Guard A items from their first baseline, not from a commit | adopting a repo flags nothing; nothing retroactive; works without commits | an edit made before the first baseline is invisible | `spectrace-start` runs `status --write` at setup, so the baseline is the interview's result |
| The author is `git blame`, not a `By:` field | no format change; old `changes.md` files stay valid | needs the entry to be committed to name anyone | the entry is the thing that must exist; commits are the team's habit (A9) |
| A conflict is a `block` with a convention, not a new command or state | version 1 traces stay valid; reuses `block`, `start` and the spec status | an agent must follow the convention | the protocol paragraph, a check that makes it visible, an unknown reference refused |
| Only conflict blocks are pending, not every blocked task | exact; a wait on a person adds no noise | a block without the prefix is not flagged | any blocked agent task already rolls its spec up to `blocked` |
| No automatic workaround detection | simple; no false alarms | a workaround can still be written | A14, the cheap path (blocking costs less than inventing a detour), and the `done` diff the user reviews |
| Prose is context; a rule that must bind becomes an A item | one mechanism; no hashing of noisy files | a rule left in prose is not guarded | the interview and `spectrace-plan` promote settled rules to A items |
| This spec runs after 011, not first | the old test caps `trace.py` at 900 lines and it has 896; A5@4 already chose per-module budgets | the code part waits for the refactor | 011 changes no behavior; the skill part of this spec is small |

## Deliverables

- `spectrace/commands.py` and `spectrace/model.py` (from 011), `tests/test_trace.py`
- `skills/spectrace-start/assets/format.md`, `skills/spectrace-start/assets/agents-protocol.md`
- `skills/spectrace-change/SKILL.md`, `skills/spectrace-plan/SKILL.md`,
  `skills/spectrace-start/SKILL.md`, `skills/spectrace-start/references/templates.md`
- `AGENTS.md`, `planning/product.md` (this repo)

## Sequencing

After 011 and before 012. The trace first (block, then the report, then its test), then
`format.md`, the skills and the protocol, then the template, then this repo's own files, then
the `spectrace-change` session for the earlier items (T010).

## Trade-offs context

Costs of decisions the table above does not cover.

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| D3 adds a phase to `spectrace-change` | a conflict has one entry point | the skill grows toward its 200-line budget | the A5 test guards it; the phase reuses Phases 1–5 |
| D4 leaves existing `product.md` files alone | no overwrite of the user's text | old repos lack the new sections | the upgrade report names them; the user adds them when wanted |
| D6 revises items of 002 and 010 | the old text matches the package install | noise in their history | refactor in place, with the reason written (A6) |
