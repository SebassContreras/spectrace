# 006 — e2e-verification — Requirements

## What's being built

A live run of the whole flow on a throwaway project, proving the skills and the
trace work together.

## Who it serves

The decision that spectrace is ready to share.

## Requirements

- R1@1: A throwaway project goes through `spectrace-start` (two specs), `spectrace-plan`, three tasks executed by an agent following only `AGENTS.md` without committing in between, and each task's recorded changes are exact.
- R2@1: A `spectrace-change` run that retires a design item produces a correct manifest, `trace check --strict` fails until the cleanup tasks are done, and afterwards passes with no code from the retired decision left.
- R3@1: The run is repeated under Claude Code and at least one other harness.
- R4@1: Reinstating a retired decision with `trace restore` brings its code back, recorded under the restoring task.
- R5@1: A wording-only edit and a meaning edit of a built-on item are told apart: the first is confirmed with `trace review`, the second bumps the revision and makes its tasks suspect.

## Out of scope

- Automated end-to-end tests in CI.

## Dependencies

005.

## Owner split

Agent runs it; the maintainer chooses the second harness.
