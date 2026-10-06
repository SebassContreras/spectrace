<!-- spectrace:protocol -->
## Working on tasks

Specs live in `planning/`; how they are written is in `.spectrace/format.md`. Run the
trace with `python3` (`python` on Windows).

1. `python3 .spectrace/trace.py status` — pick the `next` task, or the one you were asked for. Skip `[human]` tasks; tell the user they are theirs.
2. `python3 .spectrace/trace.py start NNN/TNNN` — before editing anything. If it lists files changed outside any task, ask the user whether to `--adopt` or `--ignore` them.
3. Read the spec's `requirements.md` and `design.md`; do only that task, following `planning/architecture.md`.
4. Verify it against the task text and the R items it covers.
5. `python3 .spectrace/trace.py done NNN/TNNN` — records exactly what changed. Stuck? `block NNN/TNNN "reason"`.
6. Before saying you're finished: `python3 .spectrace/trace.py check` must exit 0.

Never edit by hand: a task's status or `changes:` line, the roadmap's `Status`/`Stage`
(the trace owns them), or the meaning of an R, D or A item (the `spectrace-change` skill does it,
so the history and the trace stay right). One commit per task is welcome but optional;
if you commit, add a `Spec: NNN/TNNN` trailer.
<!-- /spectrace:protocol -->
