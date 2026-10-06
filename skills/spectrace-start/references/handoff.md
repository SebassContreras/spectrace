# Writing `planning/handoff.md`

Read this at any stopping point where the user said yes to a handoff. A handoff is a
point-in-time note for whoever resumes — a later session or a person. It is **not a
source of truth**: `planning/roadmap.md` and `trace status` own order and status, each
spec's `tasks.md` owns the work, `.spectrace/interview.md` owns the interview. Point at
them, don't copy them.

## Before writing

1. Overwrite the file, don't append — history lives in `git log -- planning/handoff.md`.
2. Run `trace status` and read the ledger first. Write only what you saw there or the
   user said; leave gaps as "unknown", never guess.
3. Get the session id (below), once, before the first line is written.

## Session id

One line right under the title, so a resume is one command.

- **Claude Code**: read `$CLAUDE_CODE_SESSION_ID` with the shell tool (`echo
  "$CLAUDE_CODE_SESSION_ID"`; PowerShell: `$env:CLAUDE_CODE_SESSION_ID`). Write
  `Session: <id> — resume with \`claude --resume <id>\` from this repo's root.`
- **Any other harness**: only if it exposes a session id you can read from its own
  environment or documentation. Otherwise omit the line.
- Empty or unset → omit the line. Never invent, shorten or reuse an id.

The handoff must still be enough to resume without the session id.

## Shape

Sections in this order; drop one only when it would be empty.

```
# Handoff — YYYY-MM-DD

Session: <id> — resume with `claude --resume <id>`      ← omit if unavailable

One paragraph: point-in-time note, not a source of truth; what owns each thing.
Branch and working-tree state; the open task, if any (`trace status`).

## Done this session
What changed and why, one bullet each, with the spec or file it lives in.

## Next
Ordered. Each item: what, and why it's next (priority, dependency, blocker).
Name the exact step to resume: the `spectrace-start` skill (the ledger picks up at the first
`open` dimension), the `spectrace-plan` skill for spec NNN, or `trace status` → next task.

## Open / skipped
Every ledger `open` or `skipped` dimension and every deferred spec, with the reason.

## Traps
Things that already cost time or will: non-obvious ordering, files `trace` owns, a
decision the user already made that shouldn't be re-litigated.

## Not verified — don't claim otherwise
What was written but never run.
```

## Rules

- Terse, structural, no filler (`planning/styles.md` rules apply if present).
- Dates are absolute (`2026-10-06`), never "today".
- Reference code as `path:line` or a task ID (`002/T005`), not by pasting it.
- Never record an answer the user didn't give; quote or omit.
- If only per-spec requirements remain, say so and name both paths — draft mode or
  one question at a time — and which the user chose, if they did.
