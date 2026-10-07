---
name: spectrace-change
description: >-
  The way to change direction in a spectrace project without leaving anything behind.
  Revises or retires requirements (R), design (D) or project-wide (A) decisions,
  records why in changes.md, uses the trace to list every task, file, line and test
  that implemented the old decision, and turns that list into cleanup tasks (redo by
  default, refactor only with a written reason) so the spec cannot read as done while
  old code remains. Use when the user changed their mind or an approach turned out
  wrong after specs, design or code exist: "change the auth design to JWT", "we no
  longer need X", "that decision was wrong", "revert the approach in spec 003",
  "cambiamos de idea", "ya no queremos X". Also for corrections found after the fact.
---

# spectrace-change

Run **inside the target repo**. Grammar: `.spectrace/format.md` — read it first. Run
the trace with `python3` (`python` on Windows): `python3 .spectrace/trace.py <command>`.
Ask **one question at a time**. This skill edits closed decisions, so nothing is written
before the user confirms what is about to change.

## Phase 0 — Preconditions

1. **Refuse** if `.spectrace/trace.py` is missing (point to the `spectrace-start` skill).
2. **Refuse** if `trace status` shows an open task: tell the user to finish it
   (`done`), `block` it or `abort` it first — changing decisions under a task in
   flight leaves it half on each side.
3. Run `trace check` and note existing `error`s; this skill must not add new ones.

## Phase 1 — What changed

1. Ask what changed and why, in the user's words. If they name a spec, start there;
   otherwise find the affected items by reading `requirements.md`, `design.md` and
   `planning/architecture.md`.
2. Propose the edit for each affected item — show the current line and the new one:
   - **Revise** — the meaning changes: next revision (`D3@1` → `D3@2`), new text.
   - **Reword** — the user confirms the meaning is unchanged: fix the text, keep the
     revision, then run `trace review <ref>` so the trace accepts it. Record it in
     `changes.md` as a wording fix and skip Phases 3–4. When in doubt, it's a revise.
   - **Retire** — it no longer holds: wrap the statement in `~~`, append
     `retired YYYY-MM-DD` and `→ <replacement>` if there is one.
   - **Add** — the next free number in that file, at `@1`.
   - **Reinstate** — "go back to what we had": retire the current item (→ the new
     one) and add the old statement back as the next item number. Phase 4 brings its
     code back.
   For a revised or retired R, also ask whether each D implementing it still holds.
3. Ask for an explicit yes. On anything else, stop without writing.
4. Apply the edits. Never renumber or delete an item line.

## Phase 2 — History

Append one entry, newest last, in the format's History shape — the spec's
`changes.md` for R and D items, `planning/changes.md` for A items (both if both
changed); create the file with a `# … — Changes` title if missing:

```
## YYYY-MM-DD — <short title>
Why: <the user's reason>
- MODIFIED D3@1 → D3@2
- REMOVED R4@1
- ADDED D7@1
- Tasks: <filled in Phase 4>
```

## Phase 3 — Manifest

Run `trace impact NNN/<item>` (or `A<n>`) for every revised or retired item, and show
the combined result as the **retirement manifest**: each task that covered the old
item, its status, whether it is a test, and per file how many of the lines it added
are still in the code (`file deleted` when gone). A finished task with no patch
recorded is listed as "search by hand" — grep for what its text describes and show
what you find before relying on it.

**Sweep — what the trace can't see.** The trace only knows lines added by tasks that
covered the old item. A README sentence, a comment in a file another task wrote, a
spec's context section or an `AGENTS.md` line can still describe the old decision.
Build the search terms — every path the old decision's tasks created, the names it
introduced (commands, flags, files, env vars, functions), and its key nouns ("plugin",
"release") — and grep the whole repo for each. Classify every hit and show the list
with the manifest:

- **History** — `tasks.md`, `changes.md`, `.spectrace/`, a retired item line: keep.
- **Stale, outside `planning/`** — find which task originally wrote that code (e.g., via `git blame` or `git log -S`) and add a task in Phase 4 that `retires:` it (covering the item that replaces it, or the spec's own item for that file). Without `retires:`, the strict gate won't track this cleanup.
- **Stale, inside `planning/`** (a spec's context, deliverables, a non-item line) —
  edit it directly as part of this change, after the user confirms.

Once tasks have deleted files, `trace check` also flags any remaining mention of their
paths; the sweep exists for everything else.

## Phase 4 — Classify and write tasks

For each **finished** task in the manifest, propose one, and let the user decide:

- **Still valid** — the task's work holds under the new revision. Re-point its
  `covers:` to the new revision and add `└─ reviewed YYYY-MM-DD: <why it holds>`.
- **Redo** — *the default.* A new task that removes what it built
  (`retires: TNNN`, covering the replacement item), plus the tasks that build the new
  decision. Deleting and rebuilding beats bending old code into a new shape.
- **Refactor in place** — only if the user gives a one-sentence reason why changing
  the existing code is better than removing it; record that sentence in the
  `changes.md` entry. The task `retires:` the old one and covers the new item.
- A **test** covering a retired R: a task that deletes the test (`retires:` it) —
  never adapt a test to a requirement it no longer guards.

For each **not-started** task covering a changed item: re-point it if it still
applies, otherwise delete its line (nothing was built) and say so in the entry.

**Reinstate.** Find the tasks that removed the old work (`impact` on the old item:
the tasks listed under "retired by"). For each, add a task covering the reinstated
item whose text says to run `trace restore NNN/TNNN` on it inside that task, then
re-verify the result; the restored code is recorded as that task's change. Also
retire what the current item's tasks built (the usual redo). If `restore` reports the
changes no longer apply, that task becomes a redo instead.

New tasks follow the `spectrace-plan` skill's task rules (single-action, verifiable, `covers:`,
owner, `kind: test` for checkable R items). Number them after the spec's last task —
in the spec of the task being retired when the change spans specs. Show the full list
for confirmation, then write it, and complete the entry's `Tasks:` line.

## Phase 5 — Gate, report, stop

1. Run `trace status --write`, then `trace check`. There must be no `error`. The only
   `pending` items left must be suspect tasks whose cleanup tasks are now `todo`, and
   those cleanup tasks themselves ("cleanup … not done yet") — any other pending item
   means the change is incomplete: fix it with the user.
2. Report: what changed, the manifest in short, the new tasks, and that the spec
   stays open until they are done (`trace check --strict` passes then). Any agent
   executes them through the protocol in `AGENTS.md`.
3. **Stop.** Never execute the cleanup tasks here.

## Style

- Terse; the user's language in conversation, the project's in files.
- Never invent the reason for a change — ask.
- Never edit `Status`/`Stage`, a task's status or a `changes:` line — the trace owns them.
