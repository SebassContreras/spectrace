---
name: spectrace-start
description: >-
  Starts a spectrace project or adds a spec to one. Runs a guided interview in
  natural language (project type, goal, stack and tools, agent rules, styles), then
  writes planning/product.md, planning/architecture.md (decisions as A items),
  planning/roadmap.md and each spec's requirements.md (R items with IDs and
  revisions), installs the trace script in .spectrace/ and the task protocol in
  AGENTS.md. Use for any new app, site, content, operations or research project, or
  a new feature spec, in English or Spanish, even with typos: "I want to build X",
  "start a new spec for Y", "quiero crear una app", "nueva spec para Z". Works in a
  folder without git (initializes it after asking).
---

# spectrace-start

Run **inside the target repo**. Ask **one question at a time** and wait for the reply.
Everything this skill writes is described in `references/templates.md`; the grammar of
items, tasks and the roadmap is in `assets/format.md` (copied to `.spectrace/format.md`).

**Owns only:** `AGENTS.md` (its sections and the protocol block), `planning/product.md`,
`planning/architecture.md`, `planning/styles.md`, `planning/roadmap.md` (rows, never
`Status`/`Stage`), `planning/specs/*/requirements.md` and the stubs beside it,
`planning/handoff.md`, and `.spectrace/` (`trace.py`, `format.md`, `interview.md`). Never
create `CLAUDE.md`, a README, CI config or anything else — those are project
deliverables the roadmap decides.

## Interview contract

Applies to every Q&A phase. `references/question-bank.md` defines the dimensions.

- **Ledger.** `.spectrace/interview.md`, one row per dimension
  (`covered` / `skipped` / `open`), written after every answer, in the user's own words.
  It makes an interrupted interview resumable and a skip distinguishable from an
  oversight.
- **A phase ends** when each of its dimensions is `covered` or `skipped` and the
  closing sweep (question bank, Phase F) comes back with nothing new.
- **Never infer an answer** to close a dimension — leave it `open`, ask again in the
  sweep. `TBD` on disk beats a guess.
- **Follow up** on anything named but unspecified ("the dashboard", "our brand").
- **Unsure user** → the question bank's help-me-decide protocol.
- **Plain chat questions** by default. A selectable-options tool only for a closed
  choice with 2–6 real answers (project type, yes/no) — never with a skip preselected.
- **Stopping.** The user can stop at any point. Before stopping, ask whether to write
  `planning/handoff.md`; if yes, follow `references/handoff.md`.

## Phase 0 — Detect state

1. `.spectrace/interview.md` exists → resumed interview: report what's covered and
   continue from the first `open` dimension. Add any question-bank dimension the ledger
   lacks as `open`.
2. `planning/product.md` has real content → the project exists: go to Phase 6 for a new
   spec (or Phase 7 for a seeded spec without requirements). Offer to revisit Phases
   3–5 only if the user says a decision changed — and then point to the `spectrace-change` skill
   for anything already recorded as an A item.
3. Otherwise → a new project: Phase 1.

Never overwrite a file with real content without explicit confirmation.

## Phase 1 — Ledger only

Create `.spectrace/interview.md` with every Phase A dimension `open`. Write nothing
else yet: the user's first sight of the run is a question, not a wall of files.

## Phase 2 — Type & vision (question bank, Phase A)

The opening request is context, not an answer. Start with `idea-detail` in the user's
language (quote the opening request back and ask them to expand). Record it verbatim,
then structure it — problem, users, main flow, data, integrations — without inventing
choices. Settle `project-type` (for software, the concrete form). Draft `goal` from the
narrative and show it for yes / changes. Then the remaining Phase A dimensions, grounded
in the narrative. Close with the sweep.

## Phase 3 — Scaffold

1. **git.** No repository here → ask, then `git init`. The trace needs git.
2. **Files** (only if missing), from `references/templates.md`: `AGENTS.md`,
   `planning/product.md` (filled from `goal`, `audience`, `mvp`), `planning/architecture.md`
   (headers keyed to `project-type`), `planning/roadmap.md`, `planning/specs/`.
3. **Trace.** Copy `assets/trace.py` and `assets/format.md` (paths relative to this
   skill's folder) into `.spectrace/`. If `.spectrace/trace.py` already exists with a
   lower `VERSION`, show both versions and ask before replacing it.
4. **Protocol.** Write `assets/agents-protocol.md` into `AGENTS.md`, replacing the text
   between `<!-- spectrace:protocol -->` and `<!-- /spectrace:protocol -->` if present,
   appending it otherwise. Touch nothing else in `AGENTS.md`.

## Phase 4 — Technologies, architecture & tools (Phase B)

Ask the block matching `project-type` — no software questions for a marketing project.
Each settled answer becomes an A item in `planning/architecture.md`
(`- A<n>@1: <decision> — why: <reason>`) and its short operative form goes into
`AGENTS.md` → "Stack & conventions". Nothing decided → a bullet under "Still to define",
and a decision spec in Phase 6. Never invent a stack. Close with the sweep.

## Phase 5 — Helper skills, agent rules, styles (Phases C, D)

- Recommend only helper skills relevant to the Phase B answers; install nothing without
  explicit confirmation; what can't be installed becomes a roadmap spec.
- `agent-rules` → `AGENTS.md` → "Rules for agents".
- Styles: detail (hex values, type stacks) into `planning/styles.md`, the operative
  summary into `AGENTS.md` → "Style", each marked hard rule or default. Never invent a
  style value. Close with the sweep.

## Phase 6 — Roadmap

1. Propose the ordered specs needed to reach the goal: setup first (from Phases 3–5,
   including uninstallable helpers and `open` decisions), then features. Use
   type-appropriate examples — software: scaffold, database, test harness; marketing:
   audience research, brand guidelines, channel setup.
2. Ask the `mvp` cut: which are in the first phase.
3. Show the list; confirm add / remove / reorder; ask each item's dependencies
   explicitly; ask whether to record the confirmed order as `Priority`.
4. For each confirmed spec: folder `planning/specs/NNN-name/` (kebab-case,
   `NNN` = highest ID + 1), stub `design.md` and `tasks.md`, and a roadmap row with
   `Status`/`Stage` empty. Then run `python3 .spectrace/trace.py status --write`
   (`python` on Windows) — never type those two cells yourself.
5. Sweep against `done-when`: anything no spec covers is a missing row.

## Phase 7 — Requirements, per spec

Before the first spec, ask once: answer each spec's requirements here, one question at
a time, or have them **drafted** from the interview for approval. "Sigue solo" / "decide
tú" at any point switches to drafting.

**Q&A mode.** Question bank Phase E, one question at a time, writing after each answer.

**Draft mode.** For one spec at a time:
1. Read the ledger, `planning/*.md`, the spec's roadmap row and every sibling spec's
   `requirements.md`, so drafts don't overlap.
2. Derive each section. Where the interview doesn't settle something, use the current
   industry standard, confirmed by a short web search; mark every line the user didn't
   give: `_(standard: <name> — <primary source URL>)_`, `_(judgement, no standard)_`, or
   `_(standard, unverified — no web search)_`. A fact only the user knows (an account,
   a budget, a preference) is asked live — just that one question.
3. Show the **full draft** — not a summary — for **yes**, **changes** (revise, re-show)
   or **defer** (leave it, move on). If the user said to proceed without confirming,
   still print each draft, treat it as yes, and list every marked line in the report.
4. On yes, write it and record the spec's Phase E rows in the ledger as
   `covered (drafted)`.

Either mode: R items are numbered from `R1@1`, each one checkable (templates). After
each spec, run `trace status --write`, then ask whether to continue to the next spec —
never chain silently through all of them.

## Phase 8 — Report

1. Run `python3 .spectrace/trace.py check` and fix any error it reports in files this
   skill wrote.
2. Tell the user what exists, every dimension left `open` or `skipped`, and the next
   step: the `spectrace-plan` skill on the first spec `trace status` shows at stage `design`.
3. Ask whether to write `planning/handoff.md`.

## Style

- Terse and structural; no filler, no marketing language; the user's language for the
  conversation, the project's language (Phase D `tone`) for the files.
- Never fabricate product, architecture, requirements or style content — `TBD` instead.
- One question at a time.
