# Roadmap

Specs in execution order. `Status` (`todo`, `in progress`, `done`) is maintained directly by agents and humans as specs progress.

> Historical note: Specs 001–027 (including hook and trailer enforcement machinery) have been retired; see [CHANGES.md](../CHANGES.md).

| ID  | Spec | Status | Depends on |
|-----|------|--------|------------|
| 028 | streamlined-foundation | done | — |

## Ideas

Anything worth doing later. Ideas can be added freely without debate; they are converted into specs when prioritized.

- **Automated Spec Linting:** A lightweight command or linter to verify that specs follow thin-slice principles without enforcing git commit hooks.
- **Surface Alignment Rules:** When a task adds a public surface (CLI command, tool, API endpoint), the spec automatically includes a task to document it in `ARCHITECTURE.md` or `DESIGN.md`.
