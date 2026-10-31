# 033 — research-principle

## Goal

Add "Validate with Research" as principle 7 of `ENGINEERING.md`, scoped so research is required only when a decision is hard to reverse, depends on an external fact, or breaks a factual tie — and carry the principle to the starter template and to all three distribution paths (greenfield scaffold, upgrade/migration, adoption into an initialized repo), so repositories receive it without anyone re-reading this spec.

## Requirements

- R1: `ENGINEERING.md` defines principle 7 with an explicit "when to research" trigger list and a "do not research" list.
- R2: `skills/spectrace-plan/assets/engineering-template.md` ships the same principle, so new repositories inherit it.
- R3: `spectrace-review` treats an uncited hard-to-reverse choice as a finding and leaves a local reversible choice alone.
- R4: `spectrace-plan` describes `ENGINEERING.md` with principle 7 included.
- R5: `CHANGES.md` records the addition, its rationale and the rejected alternative; the 2026-10-28 entry stays intact.
- R6: The citation format is fixed as `Source: <url> (accessed YYYY-MM-DD)` and lives with the decision it supports.
- R7: `spectrace-init` Step 3 reconciles an existing `ENGINEERING.md` against the template: append the missing principle sections, preserve repository-specific principles and wording, delete nothing, and record the reconciliation in `CHANGES.md`.
- R8: `spectrace-plan` Step 4 applies the same reconciliation when `ENGINEERING.md` already exists.
- R9: `spectrace-review` flags contract drift: a core principle the skill lists but the target `ENGINEERING.md` omits, with no excusing `CHANGES.md` entry, is a finding.
- R10: Every place that enumerates the principles lists the full set consistently, so prose never lags the file.
- R11: `bin/spectrace-init.mjs` upgrade mode reconciles an existing `ENGINEERING.md`: append the missing principle sections, preserve the rest, stay idempotent on a second run, and respect `--dry-run`.

## Design

- D1 (R1, R6): New `### 7. Validate with Research — Only When It Changes the Decision` after §6, in the document's bullet voice: three triggers (hard to reverse; external fact; factual tie-break), what not to research, source preference order, citation format, and the review consequence. Proportionality is inherited from §1, so the principle stays a cheap check rather than a ritual.
- D2 (R2): Mirror the section verbatim in `skills/spectrace-plan/assets/engineering-template.md`; the document stays the source of truth and the asset is its distribution copy.
- D3 (R3, R9): In `spectrace-review/SKILL.md`, extend the `ENGINEERING.md` read-list parenthetical, add a research checkbox under the trade-offs item (numbering 1–11 stays stable), and add a contract-drift checkbox under "Surface Alignment & Spec Traceability".
- D4 (R4, R8, R10): In `spectrace-plan/SKILL.md`, extend the file-responsibilities row and the first-time setup bullet, and add the reconciliation sentence to Step 4.
- D5 (R7, R10): In `spectrace-init/SKILL.md`, extend the contract table row and the Step 2 enumeration, and replace "Create `ENGINEERING.md` if missing" in Step 3 with the reconcile rule.
- D6 (R10): In `assets/agents-block.md`, `README.md`, `skills/spectrace-plan/assets/architecture-template.md` and this repository's `AGENTS.md`, complete every enumeration with the full set.
- D7 (R11): In `bin/spectrace-init.mjs`, add `reconcilePrinciples()`: read the template, split on `### ` headings, append the sections whose heading is absent from the target file, keep existing content untouched, report in `updated`, and write nothing under `--dry-run`. Heading match (not full-text match) keeps it idempotent.
- D8 (R5, ARCH-4): Append the dated `CHANGES.md` entry and add the propagation invariant to `ARCHITECTURE.md` §"Structural Boundaries & Invariants" 4, so a future principle cannot ship to one file only.

### Trade-offs & Mitigations (ENG-6)

- Choice: criterion-based research vs. mandatory research vs. no principle.
  - Pros: kills invented citations and ritual browsing, while still blocking guesses about platform facts (SDK behaviour, licence terms, agentskills.io rules).
  - Cons: "hard to reverse" is a judgement call.
  - Mitigation: three concrete triggers, and review flags only claims that could have a source.
- Choice: append-only reconciliation of `ENGINEERING.md` vs. overwriting it with the template.
  - Pros: upgrades reach existing repositories without losing their custom principles.
  - Cons: a repository can end up with a stale copy of a principle it already edited.
  - Mitigation: match by heading and never rewrite an existing section; the drift check reports the omission instead of forcing a rewrite.

## Tasks

- [x] 033/T001 [agent] Add principle 7 to `ENGINEERING.md` — covers R1, R6, D1
- [x] 033/T002 [agent] Mirror principle 7 in `skills/spectrace-plan/assets/engineering-template.md` — covers R2, D2
- [x] 033/T003 [agent] Add the research and contract-drift checks to `spectrace-review` — covers R3, R9, D3
- [x] 033/T004 [agent] Update `spectrace-plan`: table row, Step 4 enumeration and reconciliation — covers R4, R8, R10, D4
- [x] 033/T005 [agent] Update `spectrace-init`: table row, Step 2 enumeration and Step 3 reconciliation — covers R7, R10, D5
- [x] 033/T006 [agent] Complete the principle enumerations in `assets/agents-block.md` — covers R10, D6
- [x] 033/T007 [agent] Add `reconcilePrinciples()` to `bin/spectrace-init.mjs` — covers R11, D7
- [x] 033/T008 [agent] Record the change in `CHANGES.md` and the propagation invariant in `ARCHITECTURE.md` — covers R5, D8
- [x] 033/T009 [agent] Complete the remaining enumerations in `README.md`, `architecture-template.md` and `AGENTS.md` — covers R10, D6
- [x] 033/T010 Verify: assert 5 partitions — (a) greenfield scaffold copies §7 from the asset; (b) upgrade of a repo whose `ENGINEERING.md` has 6 principles appends §7 and keeps a custom principle; (c) a second CLI run is idempotent; (d) every enumeration names all 7 principles and drift is reported when one is absent; (e) the 2026-10-28 entry is intact and the new entry is dated — covers R1–R11
      verified: partitions (a)–(c) executed against `bin/spectrace-init.mjs` in throwaway directories: greenfield created `ENGINEERING.md` with §7 and the roadmap scaffold; an upgrade of a six-principle file appended §7, kept a custom `### 8.` principle and left §1 untouched; a second run produced one §7 and a byte-identical file; `--dry-run` left the file byte-identical. (d) 11 enumerations across `ENGINEERING.md`, both skills, the plan table, `agents-block.md`, `architecture-template.md`, `README.md` and `AGENTS.md` now name research and trade-offs; drift is covered by the new review checkbox. (e) `CHANGES.md` keeps the 2026-10-28 entry and gains a dated 2026-10-31 entry; `roadmap.md` lists 033.
