# 010 — upgrade — Requirements

## What's being built

A way to bring a repo already scaffolded by spectrace up to the current version of the
skills. `pnpm dlx skills update` refreshes the skills themselves, but not what they
copied into the repo: `.spectrace/trace.py`, `.spectrace/format.md`, the protocol block
in `AGENTS.md` and the `AGENTS.md` sections added by later specs (for example "Testing"
from 009). Today these refresh only in `spectrace-start` Phase 3, and Phase 0 skips that
phase for an existing project.

## Who it serves

Developers who use spectrace in a project that is already under way and want the latest
protocol, trace and policies without starting over or editing files by hand.

## Requirements

- R1@1: `spectrace-start` Phase 0, on an existing project, checks for an outdated install
  before going on: a `.spectrace/trace.py` `VERSION` lower than the bundled one, a
  `.spectrace/format.md` that differs from the bundled one, a protocol block in
  `AGENTS.md` that differs from `assets/agents-protocol.md`, or a section from the
  `AGENTS.md` template in `references/templates.md` that is missing.
- R2@1: When anything is outdated, the skill shows the user a summary before writing
  anything: old and new trace version, the protocol diff and the missing sections.
- R3@1: The upgrade writes only after explicit confirmation, and the user can accept or
  skip each item separately.
- R4@2: The upgrade replaces `.spectrace/trace.py`, the `.spectrace/spectrace/` package and
  `.spectrace/format.md` with the bundled files and replaces only the text between `<!-- spectrace:protocol -->` and
  `<!-- /spectrace:protocol -->`; everything else in `AGENTS.md` stays byte-identical.
- R5@1: A missing template section is added to `AGENTS.md` without touching existing
  sections. When the section needs the user's answers (for example the test commands and
  `verification` for "Testing"), the skill asks only those question-bank questions and
  follows the same rules as the phase that normally fills it.
- R6@1: The upgrade never edits `planning/`: no spec, item, task or roadmap row changes.
- R7@1: After the upgrade, `python3 .spectrace/trace.py check` passes on the repo when it
  passed before; if it fails, the skill reports the failure and does not hide it.
- R8@1: When nothing is outdated, Phase 0 continues as today without mentioning the
  upgrade.
- R9@1: The user can ask for the upgrade directly (for example "update spectrace in this
  project"), and the check runs without starting a new spec.
- R10@1: `README.md` explains that updating is two steps: `pnpm dlx skills update`, then
  running `spectrace-start` in the project to apply the upgrade.
- R11@1: All skills still pass `tests/test_skills.py` (bodies at most 200 lines, valid
  frontmatter).

## Out of scope

- Migrating `planning/` files to a newer format.
- Rewriting code or tests in the target repo to fit new policies.
- Updating the skills themselves (that is the `skills` CLI's job).
- Downgrades.

## Dependencies

002, 005, 009.

## Owner split

All agent.
