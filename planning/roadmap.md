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

## Ideas

Anything worth doing later. Ideas can be added freely without debate; they are converted into specs when prioritized.

- **Automated Spec Linting:** A lightweight command or linter to verify that specs follow thin-slice principles without enforcing git commit hooks.
