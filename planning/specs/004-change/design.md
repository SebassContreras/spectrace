# 004 — change — Design

## Approach

- D1@1 (implements R1, R6): Refuse while `.spectrace/state.json` has an open task. Map the user's description to concrete R, D and A items and propose, per item, revise (next revision, new text), retire (struck through, dated, `→` replacement) or add (next free number); write nothing before the user confirms.
- D2@1 (implements R2): Record the change in the format's History shape — the spec's `changes.md` for R and D items, `planning/changes.md` for A items — creating the file if missing.
- D3@1 (implements R3): Run `trace impact` on every revised or retired item and present the result as the retirement manifest, including D items that implement a revised R.
- D4@1 (implements R4): Classify each finished task in the manifest with the user — still valid (re-point `covers:` to the new revision, add a dated "reviewed" note), redo (default: a task that `retires:` it plus tasks for the new items), or refactor in place (only with a one-sentence justification recorded in `changes.md`). A test covering a retired R gets a task that deletes it. A not-yet-started task covering a changed item is re-pointed or removed outright. New tasks follow the `spectrace-plan` skill's task rules.
- D6@1 (implements R7): After the manifest, sweep: search terms are the paths deleted or renamed, the names the old items introduce and their key nouns; every hit outside history is listed with the manifest and becomes an edit — a task when it is outside `planning/`, a direct edit of spec context inside it.
- D7@1 (implements R8): Reinstate path: retire the current item (→ the new one), add the old statement back as the next item number, and for each task that removed the old work add a task covering the new item that runs `trace restore` on it; a patch that no longer applies becomes a redo task instead.
- D8@1 (implements R9): Wording path: when the user confirms the meaning is unchanged, edit the text, run `trace review <ref>`, and record it in `changes.md` as a wording fix — no revision bump, no manifest.
- D5@1 (implements R5): End with `trace status --write` and `trace check`: no errors; the remaining pending items are exactly the suspect tasks whose cleanup tasks are still to do.

## Deliverables

- `skills/spectrace-change/SKILL.md`
