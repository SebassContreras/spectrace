---
name: spectrace-change
description: >-
  Handles architectural pivots, bugs, small fixes, new features, and convention updates without
  leaving stale code behind. Updates root context documents (CHANGES.md, PRODUCT.md,
  ARCHITECTURE.md, ENGINEERING.md, DESIGN.md, TESTING.md), strikes obsolete spec decisions
  (~~D1~~ → D2), and adds verifiable cleanup and test tasks to specs in planning/. Small
  corrections that break no requirement skip planning/ entirely: the commit is the record.
  Pure Markdown and Git, zero runtime and zero hooks.
  Use when: "we changed our mind about X", "now we want Y instead", "this decision was wrong",
  "X is broken", "add this to the plan", "pivot architecture", "deprecate X", "fix bug in Y",
  "small fix", "typo in X", "quick correction", "this rule is in the way".
---

# spectrace-change

Run **inside the target repo**. The execution protocol is in `AGENTS.md`. If the repository lacks `AGENTS.md` or `planning/`, run `spectrace-init` or `spectrace-plan` first.

Changes and pivots are expected. Never refuse a change because a spec is marked `done` or software has shipped. Confirm all proposed changes with the user before writing files.

---

## Step 1 — Classify the Change

Ask what changed and why if not specified. Classify into one of four categories:

1. **New idea or feature** → Step 2
2. **Change of direction / Pivot** — an existing requirement, design, or architecture must change → Step 3
3. **Bug or small correction** — code or docs are wrong under the current specs and contracts (broken behavior, typo, stale doc, confusing message) → Step 4
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

## Step 4 — Bug or Small Correction

1. **Analyze Symptom:** Document exact steps, actual outcome, and expected outcome.
2. **Locate Code:** Inspect code with `git grep` and identify which requirement (`R`) or design decision (`D`), if any, is violated.
3. **Pick the smallest route that fits** — never create a spec just to hold a fix:

   | Situation | Route |
   |:---|:---|
   | **Trivial correction** — violates no `R`/`D` and fits in one commit (typo, stale doc, wrong message, small defect) | **4a** — no `planning/` entry |
   | **Bug against a requirement** — breaks an `R` or `D` of an existing spec, fixable without changing it | **4b** — tasks in the owning spec |
   | **The fix requires changing an `R` or `D`** | **Step 3** — change of direction |

### 4a — Trivial Correction

- Do not add a spec, roadmap row, or tracking list. The Conventional Commit (`fix:`, `docs:`) is the record; `git log --grep "^fix"` recovers the history.
- If it changes code behavior, add a regression test in the same commit (per `TESTING.md`).
- If the user asked for the fix, apply it in this turn after confirming it (the only exception to Step 6). If it will not be done now, append one bullet to `## Ideas` in `planning/roadmap.md`.

### 4b — Bug Against a Requirement

1. Add tasks to the spec that owns the violated item — even if it is `done`:
   - Regression test task: `- [ ] NNN/TNNN [agent] Regression test: <failing check> — covers R1`.
   - Fix task: `- [ ] NNN/TNNN [agent] Fix <component>: <resolution> — covers R1`.
2. If the spec was `done`, set its roadmap status back to `in progress` and add a `## Changes` line: `- YYYY-MM-DD: Reopened for bug <summary>. Work: T00N–T00M.` A bug reopens its spec; only changes of direction across specs become a new spec.
3. If a design decision caused the bug, the decision itself must change → go to Step 3.
4. If the bug was listed in `## Ideas`, remove it from the backlog.

---

## Step 5 — Convention in the Way

Rules describe current patterns, not immutable laws.

1. Identify the blocking convention in `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md`.
2. Propose the simplest update to the user (edit, replace, or remove).
3. Upon approval: update the document, record the rationale in `CHANGES.md`, and add necessary refactoring tasks to active specs.

---

## Step 6 — Report and Stop

Summarize what was changed, list newly added tasks in `planning/`, and stop. Any coding agent can execute the tasks following `AGENTS.md`. **Do not execute tasks in this turn** — except a trivial correction (Step 4a) the user asked to fix.
