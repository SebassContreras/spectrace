# Changes

> Owns: changes of direction: what was replaced, when and why · Not here: release notes or commit history (git), plans (planning/), standing rules (the other contracts)

A decision recorded here is revisable. It explains why we moved; it does not forbid moving again. Entries older than 2026-11-04 use the wording of the previous design, where some say "do not reintroduce"; read those as history.

Entry format: `### YYYY-MM-DD — Title`, then **What changed**, **Why** and **Replaces**. Newest first.

## Ledger

### 2026-11-04 — One skill; the repository owns the workflow

- **What changed:**
  - The four skills (init, plan, change, review) and `bin/spectrace-init.mjs` became one skill, `spectrace`, that only scaffolds. Planning, change handling and review are three playbooks the scaffold installs under `.agents/playbooks/`.
  - OPERATIONS.md is the eighth contract, every contract opens with `> Owns: … · Not here: …`, and non-goals left PRODUCT.md.
  - `guard.mjs` enforces the deterministic rules from Claude Code hooks, Antigravity hooks and CI. Claude attribution is switched off through the `attribution` setting.
  - Specs 001–034 were retired, including the unbuilt overlay of 034.
  - `.agentignore` was dropped: neither Claude Code nor Antigravity reads it, per their docs. Secrets are protected by `permissions.deny` in the Claude adapter, with `!` carve-outs so `.env.example` stays readable.
- **Why:**
  - An audit of this repository and of seven repositories that use it showed the contracts were useful and customised, while the specs and the four skills were overhead. The CLI had defects and no tests: a UI design template as the default, the `AGENTS.md` block never installed where a file already existed, and a migration entry that could not be written.
  - Skills are not reliably invoked, while a router in `AGENTS.md` is always read. Text rules are advisory, so rules that must always hold need hooks and CI.
- **Replaces:** the four `spectrace-*` skills, the CLI, specs 021–034, and the "do not reintroduce" wording in favour of revisable decisions.
- **Trade-offs:** repository-owned playbooks can drift from the newest copy in the skill, so update mode shows a diff. Hooks protect only Claude Code and Antigravity and a crashing hook does not block, so CI is the backstop.
- **Sources:** https://code.claude.com/docs/en/hooks.md, https://code.claude.com/docs/en/settings-reference.md, https://antigravity.google/docs/hooks (accessed 2026-11-04).

### 2026-10-31 — Principle 7: Validate with Research, Propagated to Every Entry Point

- **Scope:** Engineering standards, starter asset, `spectrace-init`, `spectrace-plan`, `spectrace-review`, `bin/spectrace-init.mjs`, and `ARCHITECTURE.md` invariant 4.
- **What Changed:**
  - Added `### 7. Validate with Research — Only When It Changes the Decision` to `ENGINEERING.md`: research only when the choice is hard to reverse, depends on a fact outside the repository, or breaks a factual tie; fixed source order; citations as `Source: <url> (accessed YYYY-MM-DD)`.
  - Mirrored the section in `skills/spectrace-plan/assets/engineering-template.md`, so every scaffolded repository inherits it.
  - Upgrade and adoption paths now reconcile an existing `ENGINEERING.md` instead of skipping it: `spectrace-init` Step 3, `spectrace-plan` Step 4 and `bin/spectrace-init.mjs` append the principle sections the file lacks, keep repository-specific principles, and never overwrite.
  - `spectrace-review` flags an uncited hard-to-reverse choice and contract drift: a principle the skill lists, missing from `ENGINEERING.md`, with no excusing entry here.
  - Every enumeration now lists the same seven principles: init table and Step 2, plan table and Step 4, the review read-list, `assets/agents-block.md` and this repository's `AGENTS.md`.
- **Why:**
  - Research had no home after the extraction of six principles, so agents either guessed platform facts or browsed ritualistically.
  - A principle that lives only in this repository never reaches repositories that already carry `ENGINEERING.md`. The enumerations had already drifted: four of six lists omitted trade-offs.
- **Rejected Alternative — do not reintroduce:** Mandatory research on every task (invites invented citations and ritual browsing); overwriting `ENGINEERING.md` from the template on upgrade (destroys repository-specific principles); leaving propagation to memory without an invariant (it fails silently, as the trade-offs omission shows).

### 2026-10-31 — Small Fixes Tracked by Git, Not by a Fix List

- **Scope:** Bug and correction routing (`spectrace-change`, `AGENTS.md` block).
- **What Changed:**
  - `spectrace-change` Step 4 now routes by size: a **trivial correction** (breaks no `R`/`D`, one commit) gets no `planning/` entry — the `fix:`/`docs:` commit is the record; a **bug against a requirement** adds regression and fix tasks to the owning spec, reopening it (`done` → `in progress`) when needed; a fix that needs a different `R`/`D` goes through the change-of-direction protocol.
  - Added a `Small Fixes` section to the `AGENTS.md` block and to this repo's `AGENTS.md`.
  - `## Ideas` explicitly accepts small fixes that won't be done right away.
- **Why:**
  - The bug route told agents to add tasks to a spec, but "done specs stay done" (spec 021) left no place for bugs in finished specs, so agents either inflated fixes into new specs or recorded nothing.
  - Corrections that violate no requirement (typos, stale docs) did not fit any category.
- **Rejected Alternative — do not reintroduce:** A `## Fixes` checklist in `planning/roadmap.md` (or a `planning/fixes.md` file, or a `spectrace-fix` skill). It duplicates what `git log` already records, needs manual cleanup, and turns spectrace into an issue tracker, which `PRODUCT.md` lists as a non-goal. Spec 021 already removed `spectrace-fix` and moved tracking to git for the same reason.
- **Replaced Items:** "Done specs stay done" now applies only to changes of direction; bugs reopen their spec.

### 2026-10-28 — Engineering Standards & spectrace-review Skill Integration

- **Scope:** Code quality governance and testing discipline.
- **What Changed:**
  - Codified the 10 Core Engineering & Testing Principles in `DESIGN.md` (KISS/YAGNI, SRP, Anti-Corruption Layer/DIP, Invariant Testing, Input Partitioning, Clean Table-Driven Tests).
  - Created the read-only audit skill `spectrace-review` to evaluate code changes and task completions against these 10 principles without modifying code.
  - Added engineering constraints and anti-abstraction rules directly into `AGENTS.md`.
- **Why:**
  - Autonomous agents frequently introduce premature abstractions (single-use interfaces/factories) or shallow, anecdotal happy-path tests that fail to catch boundary regressions.
  - Providing explicit invariant standards and an auditing tool ensures code cleanliness without manual human micromanagement.

### 2026-10-28 — Foundation Realignment: Pure Markdown & Root Architecture

- **Scope:** Repository foundation & execution mechanics.
- **What Changed:**
  - Removed all POSIX Git hooks (`.githooks/`), trailer verification scripts (`check-trailers`), and CI trailer enforcement workflows.
  - Eliminated the mandatory `Spec: NNN/TNNN` commit trailer requirement in favor of standard Conventional Commits.
  - Relocated core decision contracts to the repository root: `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `CHANGES.md`.
  - Established `PRODUCT.md` at root to cleanly isolate vision, personas, and product scope boundaries from structural architecture, deprecating `planning/product.md`.
  - Focused `planning/` strictly on actionable execution (`roadmap.md` and `specs/NNN-*.md`).
  - Updated skills (`spectrace-plan` and `spectrace-change`) to generate and manage this streamlined structure.
- **Why:**
  - Shell-based Git hooks caused persistent friction and blocking errors across cross-platform environments (notably Windows path/CRLF discrepancies).
  - Enforcing rigid trailers on every micro-commit interrupted natural agent workflows and created friction without improving code quality.
  - Moving architecture and design contracts to the root maximizes immediate discovery for modern AI agents (Cursor, Claude Code, Copilot, Antigravity) via progressive disclosure.
- **Replaced Items:**
  - `~~Specs 021–027~~`: Git hooks, trailer checkers, and CI trailer validations retired.
