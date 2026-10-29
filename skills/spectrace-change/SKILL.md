---
name: spectrace-change
description: >-
  Handles architectural pivots, bugs, new features, and convention updates without
  leaving stale code behind. Updates root context documents (CHANGES.md, PRODUCT.md,
  ARCHITECTURE.md, ENGINEERING.md, DESIGN.md, TESTING.md), strikes obsolete spec decisions
  (~~D1~~ → D2), and adds verifiable cleanup and test tasks to specs in planning/. Pure Markdown
  and Git, zero runtime and zero hooks.
  Use when: "we changed our mind about X", "now we want Y instead", "this decision was wrong",
  "X is broken", "add this to the plan", "pivot architecture", "deprecate X", "fix bug in Y",
  "this rule is in the way".
---

# spectrace-change

Run **inside the target repo**. The execution protocol is in `AGENTS.md`. If the repository lacks `AGENTS.md` or `planning/`, run `spectrace-plan` first.

Changes and pivots are expected. Never refuse a change because a spec is marked `done` or software has shipped. Confirm all proposed changes with the user before writing files.

---

## Step 1 — Classify the Change

Ask what changed and why if not specified. Classify into one of four categories:

1. **New idea or feature** → Step 2
2. **Change of direction / Pivot** — an existing requirement, design, or architecture must change → Step 3
3. **Bug** — code does not conform to current specs or requirements → Step 4
4. **Convention in the way** — a rule in `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md` impedes the best solution → Step 5

---

## Step 2 — New Idea or Feature

- If it fits naturally into an active spec (`todo` or `in progress`) and is small: append new requirements, design decisions, and tasks to that spec.
- If it spans multiple areas or belongs to a completed spec: create a new spec slice in `planning/specs/` and add it to `planning/roadmap.md`.
- If it is for future consideration: append one bullet to `## Ideas` in `planning/roadmap.md`.

---

## Step 3 — Change of Direction / Pivot

1. **Identify Affected Decisions:** Read `ARCHITECTURE.md`, `ENGINEERING.md`, `TESTING.md`, and the relevant specs. Identify which requirements (`R`) or design decisions (`D`) must change.
2. **Trace Existing Impact:**
   - Run `git grep -n` for affected identifiers (functions, classes, endpoints, configuration keys, file paths).
   - Identify underlying assumptions (e.g., "loads entire file in memory", "uses synchronous HTTP").
   - Review docs: verify whether `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md` describe the obsolete approach.
3. **Record in Root Decision Ledger:**
   - Add an entry to `CHANGES.md` documenting: date, scope, what changed, why, and replaced items.
   - If the pivot alters product scope, architecture, engineering standards, test conventions, or design guidelines, update `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md`.
4. **Update the Spec:**
   - Strike through obsolete items: `- ~~D1 (R1): In-memory store~~ → D2` (or `→ 005/D1` if in a new spec).
   - If an entire requirement is abandoned: `- ~~R3: PDF export~~ dropped`.
5. **Add Verifiable Cleanup Tasks:**
   - Sequence tasks safely: build new logic alongside old, migrate callers/tests, remove old code (`— replaces D1`), then update docs.
   - Convert the reason for the change into an explicit test requirement.
   - End with a `Verify:` or `Review:` task confirming no references to the old pattern remain.

---

## Step 4 — Bug

1. **Analyze Symptom:** Document exact steps, actual outcome, and expected outcome.
2. **Locate Code:** Inspect code with `git grep` and identify which requirement is violated.
3. **Add Regression Test & Fix:**
   - Add a regression test task: `- [ ] NNN/TNNN [agent] Regression test: <failing check> — covers R1`.
   - Add a fix task: `- [ ] NNN/TNNN [agent] Fix <component>: <resolution> — covers R1`.
   - If a design decision caused the bug, replace the decision item and note `— replaces D1`.
4. If the bug was listed in `## Ideas`, remove it from the backlog.

---

## Step 5 — Convention in the Way

Rules describe current patterns, not immutable laws.

1. Identify the blocking convention in `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md`.
2. Propose the simplest update to the user (edit, replace, or remove).
3. Upon approval: update the document, record the rationale in `CHANGES.md`, and add necessary refactoring tasks to active specs.

---

## Step 6 — Report and Stop

Summarize what was changed, list newly added tasks in `planning/`, and stop. Any coding agent can execute the tasks following `AGENTS.md`. **Do not execute tasks in this turn.**
