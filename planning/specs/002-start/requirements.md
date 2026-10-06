# 002 — start — Requirements

## What's being built

The `spectrace-start` skill: the guided interview that turns a natural-language idea into a
project's `product.md`, `architecture.md`, `roadmap.md` and each spec's
`requirements.md`, and installs the trace into the target repo. Ported from
specloop's `start` (interview contract, question bank, handoff) and `advance`
(Phase 0.5, drafting requirements), without anything loop-related.

## Who it serves

Anyone starting a project or a new spec in a repo, in English or Spanish.

## Requirements

- R1@1: The interview asks one question at a time, writes after every answer to a resumable ledger (`.spectrace/interview.md`), records skips with a reason, and never invents an answer.
- R2@1: It produces `planning/product.md`, `planning/architecture.md` with A items, `planning/roadmap.md`, and one `requirements.md` per spec with R items, every R item observably checkable.
- R3@1: Requirements can be answered live or drafted from the interview, with every line not given by the user marked as a cited standard or a judgement; each draft is shown in full for yes / changes / defer before it is written.
- R4@1: It copies `trace.py` and `format.md` into `.spectrace/`, and offers to update an older copy.
- R5@1: It writes the execution protocol into `AGENTS.md` between `<!-- spectrace:protocol -->` markers and never creates `CLAUDE.md`.
- R6@1: In a folder without git it initializes a repository after the user confirms.
- R7@1: It ends by running `trace status --write`, so the roadmap's `Status`/`Stage` are right from the first row.

## Out of scope

- Design and tasks (003).
- Worker CLI configuration (there is no loop).

## Dependencies

001 (format and `trace.py`).

## Owner split

All agent.
