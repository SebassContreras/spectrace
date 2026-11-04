# Changes

> Owns: changes of direction: what was replaced, when and why · Not here: release notes or commit history (git), plans (planning/), standing rules (the other contracts)

A decision recorded here is revisable. It explains why we moved; it does not forbid moving again. Entries older than 2026-11-04 use the wording of the previous design, where some say "do not reintroduce"; read those as history.

Entry format: `### YYYY-MM-DD — Title`, then **What changed**, **Why** and **Replaces**. Newest first.

## Ledger

### 2026-11-04 — No hooks: the skill copies files and suggests the rest

- **What changed:**
  - `guard.mjs`, its tests, the Claude and Antigravity hook files, `permissions.deny`, `attribution` and the CI workflow are no longer shipped or installed, here or in the scaffold. `SKILL.md` lists them as optional extras to offer as a question; the skill writes one only when the user says yes. Specs 035 (open task T014 about Antigravity payloads) and its guard requirements are closed with this change.
  - The skill asks for the language of the product's own text, apart from the language the agent speaks. The three `DESIGN.md` variants now carry it (UI: a Language section; interface: the language of messages; content: the language of the piece), and AGENTS rule 3 points there.
- **Why:** the hooks and the guard added more to maintain than they protected, and the author was not convinced by them. Scaffolding should stay a file copy.
- **Replaces:** the 2026-11-04 entries that describe the guard, the hooks and the real-session checks of them; read them as history.

### 2026-11-04 — Checked in real sessions

- **What changed:**
  - Claude Code hooks (Bash and PowerShell tools), `attribution`, `permissions.deny` (Read, `cat`, `Get-Content`), the `skills add` installer, `init` run by an agent and the migration of a copy of a real repository were run for real, in throwaway repositories. Nothing failed; the findings below changed the docs.
  - AGENTS rule 3 has two fills (the project language and the language the user speaks); `planning/specs/` is created with a `.gitkeep`; the migration path says where project rules go, what to do with the old skills and the evidence of old tasks, and to edit in place.
  - This repository's tests no longer branch or loop inside a test body, as its own TESTING.md asks.
- **Why:** the `init` run found the language rule ambiguous and the empty folder untracked. The migration run found the procedure silent about project rules and old skills, and its agent admitted that "one task that covers everything" satisfies the lint without adding coverage, so the procedure now forbids it.
- **Not verified:** Antigravity's hooks, because headless Antigravity needs a permission flag that only the author can run.
- **Sources:** https://code.claude.com/docs/en/permissions.md, https://code.claude.com/docs/en/hooks.md (accessed 2026-11-04).

### 2026-11-04 — Audit: PowerShell, a checked router, a repository that installs what it ships

- **What changed:**
  - The Claude hooks match `Bash|PowerShell`. The guard also reads PowerShell here-strings, checks that every file the `AGENTS.md` router names exists, stops answering "continue" to Antigravity after the same problem was reported twice, and prints its usage instead of waiting on a terminal.
  - This repository installs exactly what it ships (`.agents/`, `.claude/`, `CLAUDE.md`, the workflow), and a test keeps the copies identical. `.gitattributes` forces LF.
  - No fact has two owners any more. The hard rules in `AGENTS.md` are the cross-cutting ones; the test and "done" rules live only in `TESTING.md`; the layer rule left `ENGINEERING.md`; language and naming left `DESIGN.md` and `ENGINEERING.md`.
  - `SKILL.md` gained the migration path from the previous design and how to adapt the contracts to a project that is not software.
- **Why:**
  - On Windows Claude Code routes shell commands through its PowerShell tool, and a hook that matches only `Bash` never fires there, so the commit rules did not apply on the author's machine.
  - The router of this repository pointed at files that did not exist and nothing checked it.
  - Several rules were written in two contracts, against the one-owner rule.
  - Antigravity sends no `stop_hook_active`, so a Stop hook that keeps answering "continue" could loop on a problem the agent cannot fix.
- **Replaces:** the Bash-only matcher, and hard rules 3 and 4 of `AGENTS.md`, now owned by `TESTING.md`.
- **Sources:** https://code.claude.com/docs/en/hooks.md#powershell, https://code.claude.com/docs/en/tools-reference.md#powershell-tool (accessed 2026-11-04).

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
