# Roadmap

Specs in execution order. `Status` (`todo`, `in progress`, `done`) is maintained directly by agents and humans as specs progress.

> Historical note: Specs 001–027 (including hook and trailer enforcement machinery) have been retired; see [CHANGES.md](../CHANGES.md).

| ID  | Spec | Status | Depends on |
|-----|------|--------|------------|
| 028 | streamlined-foundation | done | — |
| 029 | scaffold-assets-and-surface-audit | done | 028 |
| 030 | separation-of-concerns-and-context-aware-design | done | 029 |
| 031 | extract-engineering-principles | done | 030 |
| 032 | spectrace-init-and-upgrade | done | 031 |
| 033 | research-principle | done | 031 |
| 034 | project-overlay-and-safe-upgrade | todo | 032 |
| 035 | single-skill | in progress | 032 |

## Ideas

Anything worth doing later, including small fixes not done right away. Ideas can be added freely without debate; they are converted into specs (or fixed directly, if trivial) when prioritized.

- **Stop-time verify gate:** when a spec task flips to `[x]` and code changed, run the command declared in `TESTING.md` and block the stop if it fails. Left out of 035 because a suite at every turn end is slow.
- **Glossary contract:** an optional ninth file for canonical terms, if a project's vocabulary keeps drifting.
