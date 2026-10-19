#!/usr/bin/env bash
# exec_task.sh <harness> <label>: one "Execute the next spectrace task" conversation, snapshotted and checked.
SP="$(cd "$(dirname "$0")" && pwd)"
h="$1"; label="$2"
E="$TEMP/spectrace-e2e/$([ "$h" = claude ] && echo claude-code || echo agy)"
B=$(python "$SP/snap.py" "$E" "$label-before")
bash "$SP/say.sh" "$h" "$label" new "Execute the next spectrace task. Don't commit." | tail -n +2 | tail -12
A=$(python "$SP/snap.py" "$E" "$label-after")
python "$SP/check_task.py" "$E" "$B" "$A"
(cd "$E" && python .spectrace/trace.py check --strict >/dev/null; echo "check --strict exit=$?"; git log --oneline | wc -l)
