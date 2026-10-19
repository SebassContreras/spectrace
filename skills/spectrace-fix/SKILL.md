---
name: spectrace-fix
description: >-
  Takes a bug report in a spectrace project to a traced fix. Finds the code from the
  symptom with `trace locate`, explains it with `trace why` and `trace impact`, decides
  with the user whether the code deviates from a decision that holds (a fix under that
  decision), the decision itself is wrong or missing (hand over to spectrace-change), or
  the code is outside the trace — then writes a failing regression test task and a
  `kind: fix` task, and stops. Use when the user reports a bug or a small correction in
  a repo with `.spectrace/`: "X is broken", "this should accept Y", "hay un bug en",
  "no funciona", "arregla esto".
---

# spectrace-fix

Run **inside the target repo**. Grammar: `.spectrace/format.md` — read it first. Run the
trace with `python3` (`python` on Windows): `python3 .spectrace/trace.py <command>`.
Ask **one question at a time**. This skill writes tasks, never code: the fix itself is
executed later, by any agent, through the protocol in `AGENTS.md`.

## Phase 0 — Preconditions

1. **Refuse** if `.spectrace/trace.py` is missing (point to the `spectrace-start` skill).
2. **Refuse** if `trace status` shows an open task: it must be finished (`done`),
   blocked (`block`) or aborted (`abort`) first.
3. Run `trace check` and note existing `error`s; this skill must not add new ones.

## Phase 1 — The symptom

1. Ask for the symptom in the user's words if they have not given it: what they did,
   what happened, what they expected. Do not paraphrase it into a cause.
2. Run `trace locate "<the symptom's key words>"` (the default `--limit` is 10). If
   nothing relevant ranks, rephrase with the words the code or the specs would use —
   names of commands, fields, messages — and run it again, at most three times.
3. Show the top matches with the words each one matched, and say which you will open.

## Phase 2 — Explain

For the code that looks responsible:

1. `trace why <path::symbol>` — the tasks and decisions behind it (`anchored` answers
   come from old patches: say so).
2. `trace impact <path::symbol>` — what depends on it and the tests that reference it;
   read "Not analysed" before trusting an empty list.
3. Read the decisions `why` named (their R and D text, and A items they rely on) and the
   code itself. Reproduce the symptom if you can do it without editing files (run the
   command, a test, a one-off script outside the repo).

## Phase 3 — Classify, with the user

Propose exactly one of these, with the evidence, and ask for a yes:

- **Deviation** — the code does not do what a decision that holds says. The fix goes
  under that decision: name it (`NNN/R2@1`, `NNN/D3@1`).
- **Decision wrong or missing** — the code does what the decision says, and the
  decision is what the user now disputes, or no decision covers the behaviour. Stop
  here and hand over to the `spectrace-change` skill with the symptom as the reason; do
  not write tasks in this skill.
- **Outside the trace** — `why` says the code is outside the trace. Say so, propose the
  spec it belongs to (or a new one through `spectrace-plan`), and let the user choose.
  If they choose an existing spec, continue as a deviation under its closest item.

When in doubt between a deviation and a wrong decision, ask: "Should the code follow
`<item text>`, or should that text change?"

## Phase 4 — Write the tasks

In the `tasks.md` of the spec that owns the item, numbered after its last task, show
both tasks and ask for a yes before writing:

```
- [ ] T012 [agent] [status:todo] Regression test: <the symptom as a failing check>
      covers: R2@1
      kind: test
- [ ] T013 [agent] [status:todo] Fix <what changes>, so that <the symptom> no longer happens
      covers: R2@1
      kind: fix
```

- The test task comes first: a test that **fails before the fix** and passes after,
  at the lowest level that shows the behaviour (`AGENTS.md` → "Testing").
- The fix task covers the item at its **current** revision, one action, verifiable.
- Never weaken or rewrite an existing test to fit the fix; if one contradicts the
  report, that is a decision question — back to Phase 3.
- Then run `trace status --write` and `trace check`: no new `error`.

## Phase 5 — Report and stop

Report the symptom, the classification, the decision, and the two tasks. Say that any
agent executes them with the protocol in `AGENTS.md` (`trace start` → work → `trace
done`), the test task first. **Stop.** Never execute the tasks here.

## Style

- Terse; the user's language in conversation, the project's in files.
- Never invent the cause or the expected behaviour — ask.
- Never edit `Status`/`Stage`, a task's status or a `changes:` line — the trace owns them.
