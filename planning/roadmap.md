# Roadmap

Specs in order. `Status` is written by the pre-commit hook from each spec's
checkboxes. Specs 001–020 (the interview, `trace.py` and the code graph) were
retired by 021; they live in git history.

| ID  | Spec    | Status      | Depends on |
|-----|---------|-------------|------------|
| 021 | realign | done        | —          |
| 022 | git-hooks | done        | 021      |
| 023 | docs-tracing | done   | 022      |
| 024 | specs-folder | done | 023 |
| 025 | task-evidence | done | 024 |
| 026 | hook-tests | done | 025 |
| 027 | required-trailer | done        | 026 |

## Ideas

Anything worth doing later. No debate needed to add one; it becomes a spec when we pick
it.

- Alignment rules: when a task adds a public surface (MCP tool, CLI command, endpoint),
  the plan adds a task to register it where it must appear (`AGENTS.md`, skills, docs).
