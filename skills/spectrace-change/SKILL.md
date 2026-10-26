---
name: spectrace-change
description: >-
  Changes a spectrace project at any time — before or after the first version ships —
  without leaving old work behind. Handles a change of direction (replaces the old
  requirement or decision in the spec, finds what it built with git log --grep and
  git grep, and adds cleanup tasks), a bug (regression test task plus fix task), a new
  idea or feature (adds it to the right spec or a new one), and a convention that gets
  in the way (proposes updating it instead of working around it). Use when: "we changed
  our mind about X", "now we want Y instead", "this decision was wrong", "X is broken",
  "add this to the plan", "cambiamos de idea", "ya no queremos X", "hay un bug en",
  "agrega esto", "esta regla estorba".
---

# spectrace-change

Run **inside the target repo**. The format and protocol are in the `<!-- spectrace -->`
block of `AGENTS.md` — read it first. If the repo has no `planning/`, no block or no
`.githooks/`, point to the `spectrace-plan` skill (it installs or repairs them) and
stop.

Changes are normal, not exceptions: never refuse one because a spec is `done` or the
first version shipped. Write nothing before the user confirms what is about to change.

## Step 1 — What kind of change

Ask what changed and why if the user hasn't said, in their words. Then classify, and
say which:

- **New idea or feature** → Step 2.
- **Change of direction** — something already specced or built should be different
  or go away → Step 3.
- **Bug** — the code doesn't do what the spec says → Step 4.
- **A convention in the way** — `AGENTS.md`, `product.md` or a Design line forces a
  worse solution → Step 5.

## Step 2 — New idea or feature

- Fits an open spec (not `done`) and is small → new requirement, design line and tasks
  appended to it.
- Otherwise → a new spec: follow the `spectrace-plan` skill's Steps 2–4 for it alone.
- "Someday" ideas → one line in the roadmap's `## Ideas`. No discussion needed.

## Step 3 — Change of direction

1. **Find the items.** Read the specs that mention it; name each R or D that changes.
2. **Find what the old item built**:
   - `git log --grep "Spec: NNN/" --stat` — the commits of the tasks that covered it
     (match task IDs from the spec's `covers`). `git show <sha>` for detail.
   - `git grep -n` for every name the old approach introduced — files, functions,
     commands, flags, env vars, config keys — and its key nouns, across code, tests,
     docs, `AGENTS.md` and other specs. Untracked files are left alone.
   - **Assumptions.** From the user's reason, list what the old approach assumed —
     not its names, its habits: "loads the whole collection", "ids are max + 1",
     "filters in memory", "the file is text". For each, a `git grep` pattern or the
     files to read.
   - Read the files those commits touched — docs included: a doc written by a task
     shows up in `git log --grep` like code. Code that relies on the old approach
     without naming it (a pattern, an assumption, a test that compares raw output)
     only shows up by reading.
   - Read every doc in `product.md` → `## Docs` for sentences that describe the old
     way without naming it ("four skills", "the agent always…"). `git blame` on a line
     tells which spec wrote it; a commit with `Spec: none` or no trailer means nobody
     traced it.
   Show the list: what is still in the code, what's already gone, and docs that
   describe the old way.
3. **Choose where the work goes.** Small and inside one spec that isn't `done` → tasks
   appended to that spec. Otherwise → a **new spec** named after the change
   (`006-sqlite-storage`), written with the `spectrace-plan` skill's Step 3; done specs
   stay `done` and only get their items struck.
4. **Propose the edit**, current line and new line side by side:
   - Replace: strike the old item and point to the new one: `- ~~D1 (R1): Sessions in
     localStorage.~~ → D3` in the same spec, or `→ 006/D1` when the new item lives in a
     new spec.
   - Drop: strike it with nothing after it: `- ~~R4: Export to PDF.~~ dropped`.
   - Wording only (same meaning): edit in place, no strike.
   For a replaced R, check whether each D serving it still holds. Done tasks that
   covered a struck item stay as they are — they're history.
5. **Propose tasks**, in the order they can run without breaking the build:
   build the new way beside the old code, switch the callers and tests to it, then remove the old code
   (`— replaces D1`, or `— covers D3; replaces D1` when one task does both), then docs
   outside `planning/`. When the switch changes a data format, callers and tests move
   in one task. `planning/` files (product, other specs) are edited directly as part
   of the change, not as tasks.
   - Remove and rebuild by default; rewrite in place only when the user prefers it —
     note why in Changes.
   - A test of a dropped requirement is deleted; a test of a replaced one is rewritten
     for the new item.
   - A not-started task for the old item: delete its line, or re-point its `covers`.
   - A detail the user didn't settle (a path, a message, a format): pick the simplest
     and mark it `(assumed)` in the Design line.
   - **The reason becomes a requirement with a test.** "The JSON file is rewritten on
     every add" → `R2: add and rm write only that row` plus a test task for it, so
     whatever still follows the old way fails a test instead of hiding.
   - **The last task is a review**: `[agent] Review: re-read <the files the old
     commits touched> and the assumptions list; nothing still assumes <old way> —
     covers <the new items>`, which also re-reads the docs in `## Docs`. It closes
     only with a `reviewed:` note naming what was
     read and found (the hook refuses it otherwise); anything found becomes a new task
     before it. Best done by an agent that didn't write the change. The assumptions
     list it checks against lives in the `## Changes` entry (step 6).
   - Tasks run in file order. A task added later goes where it must run, not at the
     end; its number is just the next free one (T009 may sit between T004 and T005).
6. On a yes, write the edits and tasks, and add to each touched spec's `## Changes`:
   `- YYYY-MM-DD: D1 → 006/D1. Why: <the user's reason>. Work: 006.` In the spec that
   holds the work, indent the assumptions list under that line
   (`  - assumed: loads the whole collection — bkm/cli.py`).
   Reopen a spec (`in progress`) only when its own tasks were added. If a spec added
   earlier now depends on the reopened one, check its `Depends on`.

## Step 4 — Bug

1. Get the symptom: what was done, what happened, what was expected. Don't turn it
   into a cause yet.
2. Find the code (`git grep`, the spec's tasks, `git log --grep "Spec: NNN/"`), read it,
   and reproduce the bug if you can without editing files.
3. Decide with the user:
   - The code breaks a requirement that still holds → tasks in that spec (reopen it if
     `done`): `[agent] Regression test: <the symptom as a failing check> — covers R2`
     first, then `[agent] Fix <what> — covers R2`, closed in one commit (the test
     fails until the fix lands). If a Design line caused the bug,
     replace it (Step 3.4) and the fix task ends `— covers D4; replaces D2`.
   - The requirement itself is wrong, or no requirement forbids the behaviour (a
     Design line allows it) → a change of direction (Step 3) or a new requirement
     (Step 2), with the regression test task all the same.
   - The fix belongs in a task not started yet → edit that task instead of adding a
     fix task; the regression test goes right after it.
4. If the bug was noted in the roadmap's `## Ideas`, remove that line.

## Step 5 — A convention in the way

Conventions describe how the project is today; they are not laws.

1. Name the line, what it forces, and the better solution it blocks. `git blame` on
   it tells which spec put it there, if any.
2. Propose the simplest change to it: edit, replace or delete the line.
3. On a yes, edit the file and add a `## Changes` line to the spec that needed it. If
   code already follows the old convention and should change, treat it as Step 3.
   On a no, record the user's call in the spec's Changes and continue the old way.

## Step 6 — Report and stop

Report what changed, what the old approach left in the code, and the new tasks. Any
agent executes them through the protocol in `AGENTS.md`. **Stop** — never execute the
tasks here.

## Style

- Terse. The user's language in the conversation; English in the files.
- Never invent the reason for a change or the expected behaviour — ask.
