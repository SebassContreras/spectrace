<!-- spectrace:protocol -->
## Working on tasks

Specs live in `planning/`; how they are written is in `.spectrace/format.md`. Run the
trace with `python3` (`python` on Windows).

When executing tasks (even across multiple specs), loop steps 1–5 for each task:
1. Synchronize with origin (`git pull` and `git status`) before checking status or answering what's next. Then `python3 .spectrace/trace.py status` — pick the `next` task, or the one you were asked for. Skip `[human]` tasks; tell the user they are theirs.
2. `python3 .spectrace/trace.py start NNN/TNNN` — before editing anything. If it lists files changed outside any task, ask the user whether to `--adopt` or `--ignore` them. Never edit files without an open task.
3. Read the spec's `requirements.md` and `design.md` (or the items printed by `start`); do only that task, following `planning/architecture.md`. To find code, `python3 .spectrace/trace.py locate "<words>"`; before editing code you did not write, `python3 .spectrace/trace.py why <path[::symbol]>` shows the decisions behind it.
4. Verify it against the task text and the R items it covers. Run the narrowest test command from `AGENTS.md` "Testing" for the files the task changed; run the full suite only if the task touched a shared module (config, core, public interfaces), or at session end.
5. `python3 .spectrace/trace.py done NNN/TNNN` — records exactly what changed. Stuck? `block NNN/TNNN "reason"`. Always close the open task before moving to the next task or next spec.
6. Before saying you're finished with the session: `python3 .spectrace/trace.py check` must exit 0 (run once at the end of the session, not after every individual task).

**When a decision is in the way**, do not work around it. Run
`block NNN/TNNN "conflicts <ref>: <why>"` (for example `conflicts 002/D3: needs two stores`),
propose the simplest direct change to that item, and let the user keep, edit or retire it
(the `spectrace-change` skill). Scope filter: what the MVP needs goes in, by the simplest
route; what it does not need is postponed without debate.

Never edit by hand: a task's status or `changes:` line, the roadmap's `Status`/`Stage`
(the trace owns them), or the meaning of an R, D or A item (the `spectrace-change` skill does it,
so the history and the trace stay right). One commit per task is welcome but optional;
if you commit, add a `Spec: NNN/TNNN` trailer.
<!-- /spectrace:protocol -->
