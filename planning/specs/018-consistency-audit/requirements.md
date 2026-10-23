# 018 — consistency-audit — Requirements

## What's being built

A consistency audit command (`trace audit` or automated check module) that verifies alignment between the project's guiding documents (`planning/product.md`, `.spectrace/interview.md`, `planning/architecture.md`, `planning/styles.md`), execution instructions (`AGENTS.md`, `skills/*/SKILL.md`), and the code and tasks produced. It alerts on:
1. Architectural decisions ($A$ items) in `architecture.md` missing operative reflection in `AGENTS.md` or violated in skills/code.
2. Scope creep: specs or tasks that introduce concepts declared out of scope ("Not for now" / "Out of scope") in `product.md`.
3. Unaddressed interview dimensions: dimensions marked `open` or critical constraints in `interview.md` ignored in `requirements.md`.
4. Style and rule divergence between `styles.md` / `AGENTS.md` and the artifacts or code.

## Who it serves

Engineering leads and autonomous agents running Spectrace, providing an objective gate to prevent drift between project intent, architecture, agent guidelines, and implementation.

## Requirements

- R1@1: Add an audit module to `spectrace/` (callable via `trace audit` and integrated optionally into `trace check --audit`) that reads guiding documents and reports divergences.
- R2@1: Check Architecture Alignment: verify that every active $A$ item in `planning/architecture.md` has a corresponding operative entry or reference in `AGENTS.md` ("Stack & conventions" or "Rules for agents").
- R3@1: Check Scope Alignment: parse "Current MVP scope" and "Not for now" / "Out of scope" in `planning/product.md`, flagging specs or tasks whose titles or descriptions contain prohibited keywords or out-of-scope concepts.
- R4@1: Check Interview Ledger Alignment: if `.spectrace/interview.md` exists, verify that no spec is planned or built with unresolved blocking dimensions that directly conflict with the spec's domain.
- R5@1: Output clear, structured diagnostic warnings and errors with file and line references, formatted consistently with `trace check`.

## Out of scope

- Natural Language processing via external cloud LLMs (must run locally with standard library Python).
- Automatically modifying or overwriting guiding documents without human approval.

## Dependencies

- 008 (architecture-defaults)
- 011 (modular-core)
- 017 (rigorous-engineering-policy)

## Owner split

- `agent`: Implement audit logic, test suite, and CLI command integration.
- `human`: Review the divergence rules and tolerance thresholds.
