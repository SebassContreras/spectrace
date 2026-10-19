#!/usr/bin/env bash
# say.sh <harness> <log name> <conversation id|new> <text...>: one driver turn in the throwaway repo.
SP="$(cd "$(dirname "$0")" && pwd)"
h="$1"; name="$2"; conv="$3"; shift 3
E="$TEMP/spectrace-e2e/$([ "$h" = claude ] && echo claude-code || echo agy)"
export PYTHONIOENCODING=utf-8
printf '%s\n' "$*" > "$SP/p-$h.txt"
if [ "$conv" = new ]; then python "$SP/turn.py" "$h" "$E" "$name" "$SP/p-$h.txt"
else python "$SP/turn.py" "$h" "$E" "$name" "$SP/p-$h.txt" "$conv"; fi
