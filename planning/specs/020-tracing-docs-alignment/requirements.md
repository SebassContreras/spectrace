# 020 — tracing-docs-alignment — Requirements

## What's being built

Documentation for spectrace's tracing tools that matches what the code does. The symbol graph (`index.py`, `linker.py` `Graph`, `views/impact.py`, `views/packet.py`, `leftover.py`) exists but no doc names it or explains it. The skills each mention a different subset (`spectrace-change` uses `impact --deep`, `spectrace-fix` uses `why`/`impact`, `spectrace-plan` only `locate`), and `AGENTS.md` asks only for `locate` and `why`, never `impact --direction` or `--depth`. All docs are in English and use one vocabulary.

## Who it serves

Agents and engineers who use spectrace and need to know which tracing tool answers which question, what each one relies on, and when its result can be trusted.

## Requirements

- R1@1: `AGENTS.md` and `README.md` have a "Tracing tools" section listing every tracing command from `cli.py` (`locate`, `why`, `impact` with `--direction`/`--depth`/`--deep`, `packet`, `index --status`, `leftover`, `keep`, `restore`, `suspect`, `uncovered`): what it answers, what it reads (git diff, `planning/`, or the symbol graph), whether it needs a language adapter, and when to use it.
- R2@1: A "Symbol graph" section explains nodes (files, symbols), edges (`uses`, `subclass`), confidence (`exact`, `inferred`), traversal direction (`in` = dependents, `out` = dependencies) and depth.
- R3@1: A "Language support" table states what works for any file, for adapter-backed languages, and for Python, and is kept in sync with the adapters registered by 019.
- R4@1: The protocol requires `trace impact <path::symbol> --direction in` before deleting a symbol or changing its signature, and requires reading `Not analysed` before trusting an empty result.
- R5@1: `spectrace-plan`, `spectrace-fix` and `spectrace-change` use the same terms as R1–R2 and point to the "Tracing tools" section instead of re-explaining commands.
- R6@1: All spectrace docs, skills and command output are in English; terms in other languages (e.g. "grafo") are not used.
- R7@1: `trace audit` flags a tracing command or flag defined in `cli.py` that is missing from the "Tracing tools" section, and a documented one that no longer exists.

## Out of scope

- New tracing commands or flags.
- Translating docs into other languages.

## Dependencies

- 018 (consistency-audit)
- 019 (language-adapters), for the "Language support" table only

## Owner split

- `agent`: Write the sections, update the three skills, add the audit check.
- `human`: Review wording and the edit-before-delete rule.
