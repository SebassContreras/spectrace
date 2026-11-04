# Playbook: change

> Owns: routing a bug, a fix, a new requirement or a change of direction to the right place · Not here: how to write the code (ENGINEERING.md) or the tests (TESTING.md)

## Classify first

| It is… | Do |
|---|---|
| A trivial correction: a typo, a stale doc, a small defect that breaks no R or D | Commit it as `fix:` or `docs:`, with a regression test if behavior changes. No spec. Not now? One line under `## Ideas` in the roadmap. |
| A bug against a requirement | In the spec that owns it, add a `[test]` regression task and a fix task. If that spec was `done`, set its roadmap row back to `in progress`. |
| A new feature | Follow `plan.md`. |
| A decision that needs a different R or D | A change of direction: the steps below. |

## Change of direction

1. Strike the old item and point to the new one: `~~D1~~ → D2`. Never renumber.
2. Add a task that removes the old code, tests and docs (`— replaces D1`).
3. Add an entry to CHANGES.md: what changed, why and what it replaces.
4. List the contract lines the change makes false, show them as a diff and apply them once the user approves.
5. Run `node .agents/guard/guard.mjs --all`.

A recorded decision is revisable. If new evidence says an earlier choice was wrong, propose the change; do not work around it.
