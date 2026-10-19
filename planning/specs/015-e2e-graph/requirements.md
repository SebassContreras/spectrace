# 015 — e2e-graph — Requirements

## What's being built

The end-to-end scenario of spec 006 extended to the code map: the records, `why` and the
cleanup check are verified on the throwaway project, and a new step takes a bug report
through `spectrace-fix`. It proves, on code written by real agents and under real harnesses,
that the code map and the rest of the trace work together.

## Who it serves

The decision that the code map is ready to share.

## Requirements

- R1@1: After the scenario's execute and retire steps, every task's record matches the snapshots the driver took, and its totals add up.
- R2@1: `trace why` on the storage functions lists the tasks and decisions behind them, before and after the retire and reinstate steps.
- R3@1: During the retire step `trace check --strict` fails until the cleanup tasks are done, and then reports no `leftover` for the retired decision's symbols.
- R4@1: A bug report taken through `spectrace-fix` ends in a traced task under the decision it violates, found with `locate` and `why`.
- R5@1: The extended run is repeated under Claude Code and at least one other harness, and `e2e/report.md` records the result of every check and any gap.

## Out of scope

- Automated end-to-end tests in CI.
- Languages other than Python.

## Dependencies

014.

## Owner split

Agent runs it; the maintainer chooses the second harness.
