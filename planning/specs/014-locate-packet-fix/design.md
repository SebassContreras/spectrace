# 014 — locate-packet-fix — Design

## Approach

Everything here is a view over what 012 and 013 built; the only new stored data is the token
table. Output is plain text or JSON, deterministic and without dates, so it diffs and caches.

- D1@1 (implements R1): The index gains a `tokens` table: the identifiers and string literals of each symbol, its path, and the text of items and tasks, split on camelCase, snake_case and digits, folded to lowercase without accents, with a simple plural strip (Spanish and English). `locate` scores a match by weight — name above path above item and task text above body — adds the `why` tasks and items of the top symbols, prints the tokens that matched and takes `--limit N`.
- D2@1 (implements R2, R6): A packet is assembled from the records, the index and `check`: Decisions (items covered, with revision and `retired` flag), Symbols (exact, from the records), Dependents (inferred ones with confidence and candidate counts, top N), Tests, Incidents (the `check` issues of the task's spec), Severity signals, Not analysed. For a task it reads that task's record. For `--diff` it runs the recorder between `--base` (a git ref; by default the tree of the last closed task) and the working tree or `HEAD`, and takes as decisions the tasks that diff adds under `.spectrace/changes/`. It needs neither `state.json` nor the index file: both are rebuilt in memory.
- D3@1 (implements R2): Severity signals are facts, not a score: a symbol's signature changed (`sig`), a removed symbol still referenced, the number of dependents of a changed symbol, a changed symbol no test references, a `partial` record, files not analysed.
- D4@1 (implements R3): `skills/spectrace-fix/SKILL.md`, at most 200 lines, in phases: preconditions (`.spectrace/` exists, no open task); the symptom in the user's words and `locate`; explain with `why` and `impact`; classify with the user — the code deviates from a decision that holds (a task under it), the decision is wrong or missing (hand over to `spectrace-change`), or the code is outside the trace (say so); write a `kind: test` task first, a regression test that fails before the fix, then the task with `kind: fix` and `covers:` the item; stop, never execute. `format.md` documents `kind: fix`.
- D5@1 (implements R3, R5): `README.md` lists four skills, describes `why`, `impact`, `locate`, `packet` and `index`, gives the CI recipe (checkout with full history, `trace check --strict`, `trace packet --diff --base origin/<base branch>` appended to the job summary), and states the limits of the code map: inferred relations, dynamic Python, unsupported languages, work done outside tasks.
- D6@1 (implements R4): `spectrace-plan` Phase 0 runs `locate` for each requirement when the repo already has code, to name existing files and symbols under "Deliverables"; `spectrace-change` Phase 3 adds `impact --deep` to the manifest; `spectrace-start` gains the question-bank dimension `codebase` (existing code? which languages?) in Phase A and mentions it in Phase 3; `agents-protocol.md` adds `trace locate "<words>"` to its line about finding code.
- D7@1 (implements R5): This repo's `.github/workflows/ci.yml` runs the packet step on pull requests, so the recipe is used here first.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Lexical `locate`, no model | deterministic; no dependency | words in a request must resemble words in the code | accent folding, plural stripping, expansion through `why`; the agent rephrases; measured against `rg` (T006) |
| A packet of facts, not a score | nothing hides inside a number | the reader weighs the signals | fixed order, short sections, "Not analysed" always present |
| A fourth skill for fixes | fixes enter the ledger instead of landing outside any task | more surface | at most 200 lines; hands over to `spectrace-change` rather than duplicating it |

## Deliverables

- `skills/spectrace-fix/SKILL.md` (new)
- `skills/spectrace-start/assets/spectrace/` — `views/locate.py`, `views/packet.py`, `commands.py`, `index.py`
- `skills/spectrace-start/assets/format.md`, `skills/spectrace-start/assets/agents-protocol.md`
- `skills/spectrace-plan/SKILL.md`, `skills/spectrace-change/SKILL.md`,
  `skills/spectrace-start/SKILL.md`, `skills/spectrace-start/references/question-bank.md`
- `README.md`, `.github/workflows/ci.yml`
- `tests/test_locate.py` and `tests/test_packet.py` (new)

## Sequencing

Tokens and `locate`, then the packet, then their tests, then `format.md`, the skill and the docs,
then the CI step, then the final run of the structure tests and the full suite.

## Trade-offs context

Costs of decisions the table above does not cover.

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| D2 `--diff` rebuilds state and index in memory | works on a clean CI checkout | cost on a large diff | only the files of the diff; output capped, "Not analysed" lists the rest |
| D1 strips Spanish and English plurals | requests in the users' two languages match | two fixed languages; some false matches | `--limit`, the matched tokens printed; another language only when measured |
| D7 runs the packet on every pull request | the recipe is used here first | CI time; a shallow clone has no history | `fetch-depth: 0`; the step only writes the summary, it never fails the job |
