# 012 — change-records — Requirements

## What's being built

At the moment a task finishes, the trace records which symbols it added, changed or
removed, and accounts for every line it added or removed, so that the link from a
decision to code is exact down to the function, class or section and can be followed in
both directions. From that record come `trace why` (from code to decision), symbols in
`trace impact`, a `check` that finds the code of a retired decision that is still there,
and the names of the symbols changed outside any task.

## Who it serves

Developers and agents who need to know what a decision produced, why a piece of code
exists and whether a change of direction left anything behind; and the `spectrace-change`
skill, which today finds old code by hand with `git blame`.

## Requirements

- R1@1: When a task finishes, the symbols it added, changed or removed are recorded exactly, and every line it added or removed, of any length, is attributed to a symbol or to an explicit bucket, without needing the task's patch.
- R2@1: `trace why <path[::symbol]>` names the tasks and decisions behind a piece of code — including code that no longer exists — or says it is outside the trace.
- R3@1: `trace impact` of a decision lists, per task, the symbols it introduced and whether each is unchanged, changed or gone (following renames), and counts the lines of the task still inside each symbol.
- R4@1: When the code of a retired decision is still present, unchanged, after its cleanup tasks are done, `trace check` reports it as pending, and `trace keep` accepts it with a written reason.
- R5@1: Tasks finished before records existed still answer `why` and `impact`, labelled `anchored`.
- R6@1: A file that cannot be read, or a task that is very large, never breaks `done`: the record says what was skipped, why, and whether it is partial.
- R7@1: Python and Markdown are understood by name — functions, classes, methods, variables, class attributes and imports; sections — and any other file is recorded at file level.
- R8@1: The record is verifiable: its symbols and buckets add up to each file's total, and `trace check` reports a record that does not.
- R9@1: Changes made outside any task are reported by symbol when a task starts and by `trace check`.

## Out of scope

- Relations between symbols — callers, imports, tests: spec 013.
- Free-text search and review packets: spec 014.
- Languages other than Python and Markdown by name: any other file stays at file level.
- Rewriting history: tasks finished before this spec keep their patches only and are answered by anchoring (R5).

## Dependencies

011.

## Owner split

All agent.
