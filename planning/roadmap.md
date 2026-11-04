# Roadmap

Specs in execution order. Status is `todo`, `in progress` or `done` and stays in step with the spec's checkboxes. Only the next spec is written in full.

> Specs 001–034 belong to the previous four-skill design and are retired; see [CHANGES.md](../CHANGES.md).

| ID  | Spec | Status | Depends on |
|-----|------|--------|------------|
| 035 | single-skill | in progress | — |
| 036 | audit-alignment | done | 035 |

## Ideas

Anything worth doing later, including small fixes not done right away.

- **Stop-time verify gate:** when a spec task flips to `[x]` and code changed, run the command declared in `TESTING.md` and block the stop if it fails. Left out of 035 because a suite at every turn end is slow.
- **Glossary contract:** an optional ninth file for canonical terms, if a project's vocabulary keeps drifting.
- **Narrow Antigravity's PostToolUse matcher** from `*` to the real file-edit tool names once `--record` has captured them.
