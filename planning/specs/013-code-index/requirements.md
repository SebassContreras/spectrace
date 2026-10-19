# 013 — code-index — Requirements

## What's being built

A disposable index of the code — files, symbols, imports and references — and the questions
it answers: what depends on a piece of code, what a decision's code feeds into, which tests
reference it, and how much of the repo the trace understands. Every relation says how sure it
is, and what could not be analysed is said, never left out in silence.

## Who it serves

Developers and agents who need to know what a change can reach before making it, and the
review of a change, which spec 014 builds on this index.

## Requirements

- R1@1: `trace index` builds a disposable index of files, symbols, imports and references, and refreshes only the files whose content changed.
- R2@1: Every relation carries a confidence — exact or inferred — and, when inferred, its number of candidates; names that cannot be resolved are dropped, never guessed.
- R3@1: `trace impact <path[::symbol]>` lists what depends on that code — callers, importers, subclasses — and the tests that reference it; `--direction out` lists what it depends on.
- R4@1: `trace impact <decision> --deep` adds, for each symbol the decision's tasks introduced, its dependents and tests.
- R5@1: `trace check` warns, and never holds a spec open, about mentions of symbols a task removed.
- R6@1: What could not be analysed — files that do not parse, languages without an adapter — is reported, never left out in silence.
- R7@1: `trace index --status` reports trace coverage — symbols with an exact record, anchored, or outside the trace — and the share of references that were resolved.
- R8@1: The precision and recall of the dependents are measured against this repo's co-change history and reported.

## Out of scope

- Free-text search and review packets: spec 014.
- Languages other than Python: a later spec adds an adapter once it passes a measured gate (A13@1).
- Dynamic features of Python — reflection, `getattr`, registration by string — beyond what name matching finds.

## Dependencies

012.

## Owner split

All agent.
