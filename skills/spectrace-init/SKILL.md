---
name: spectrace-init
description: >-
  Initializes Spectrace in a new or unmanaged repository, or upgrades a repository using
  an older version of Spectrace to the current 7-contract progressive disclosure model
  (PRODUCT.md, ARCHITECTURE.md, ENGINEERING.md, DESIGN.md, TESTING.md, CHANGES.md, AGENTS.md,
  and planning/).
  Use when: "init spectrace", "initialize spectrace", "setup spectrace", "upgrade spectrace",
  "migrate to spectrace", "update spectrace in this repo", "add spectrace to this project".
---

# spectrace-init

Run **inside the target repository**. This skill configures or updates the repository to follow Spectrace's two-tier architecture: durable governance contracts at the root and execution specs in `planning/`.

---

## 🧭 Repository Blueprint & Contract Roles

When Spectrace is installed or updated, the repository maintains 7 single-responsibility root files:

| Document | Responsibility | When Upgrading / Migrating |
|:---|:---|:---|
| **`PRODUCT.md`** | Vision, target audience, problems solved, and **explicit non-goals**. | Keep existing vision; populate from README if missing. |
| **`ARCHITECTURE.md`** | System topology, directory map, layer boundaries, and Mermaid diagrams. | Purify: remove code quality / engineering rules and keep topology. |
| **`ENGINEERING.md`** | Core principles (KISS/YAGNI, SRP, DRY, DIP/ACL, casing conventions). | Extract from old `ARCHITECTURE.md` or `DESIGN.md`, or scaffold from template. |
| **`DESIGN.md`** | UI/UX visual tokens OR documentation/editorial guidelines (**Context-Aware**). | Split out non-design rules; align with target repo type. |
| **`TESTING.md`** | Invariant testing, input partitioning, table tests, and test hygiene. | Extract test guidelines if mixed in other docs; initialize from template. |
| **`CHANGES.md`** | Historical append-only ledger of pivots, replacements, and deprecations. | Preserve existing history; record this migration as an entry. |
| **`AGENTS.md`** | Operational manual for AI agents (< 150 lines) with pointers to root contracts. | Refresh to the latest concise standard; preserve project build/test commands. |
| **`planning/`** | `planning/roadmap.md` and `planning/specs/` slices. | Preserve all existing specs; clean up retired specs if needed. |
| **`.agentignore`** | Prevents context bloat for AI coding assistants. | Add or update with standard ignores (build outputs, lockfiles, node_modules). |

---

## Step 1 — Detect Target State

Inspect the current repository to classify it into one of two paths:

1. **Path A: Greenfield or Unmanaged Repository**
   - The repository has no `planning/` directory and lacks Spectrace root contracts (`AGENTS.md`, `PRODUCT.md`, etc.).
   - *Action:* Proceed to [Step 2 (Greenfield Setup)](#step-2--greenfield-setup).

2. **Path B: Legacy Spectrace Repository (Upgrade/Migration)**
   - The repository already has `AGENTS.md` or `planning/`, but uses an older format (e.g. missing `ENGINEERING.md`, outdated `DESIGN.md` containing engineering rules, retired git hooks/trailers, or pre-028 architecture).
   - *Action:* Proceed to [Step 3 (Upgrade / Migration)](#step-3--upgrade--migration).

---

## Step 2 — Greenfield Setup

For new repositories or existing codebases adopting Spectrace for the first time:

1. **Analyze Repository Context & Stack:**
   - Detect project type:
     - **UI / Web / Mobile:** Contains React, Vue, Svelte, Next.js, HTML/CSS, Tailwind, Flutter, etc.
     - **Documentation / Governance:** Contains mostly Markdown, docs site (Docusaurus, VitePress, Astro), or governance protocols.
     - **CLI / Backend / Library:** Contains Go, Rust, Python CLI, API endpoints, backend services, or SDK libraries without a frontend UI.
2. **Scaffold 7 Root Decision Contracts:**
   - **`AGENTS.md`:** Adapt from `skills/spectrace-plan/assets/agents-block.md`. Add exact project verification commands (build, test, lint, format) for the detected stack. Keep under 150 lines.
   - **`PRODUCT.md`:** Adapt from `skills/spectrace-plan/assets/product-template.md`. Summarize project vision, target personas, and explicit non-goals based on existing README or conversation.
   - **`ARCHITECTURE.md`:** Adapt from `skills/spectrace-plan/assets/architecture-template.md`. Document current directory map, component communications, and Mermaid topology diagram.
   - **`ENGINEERING.md`:** Adapt from `skills/spectrace-plan/assets/engineering-template.md`. Document KISS/YAGNI, SRP, DRY, DIP/ACL, and stack casing standards.
   - **`DESIGN.md` (Context-Aware Selection):**
     - For UI apps: use `assets/design-template.md` (tokens, colors, typography, states, accessibility).
     - For Docs/Governance: use `assets/design-docs-template.md` (editorial standards, frontmatter, callouts).
     - For Backend/CLI: define CLI argument shapes, stdout/stderr formatting, or API error payloads. **Never inject CSS tokens into non-UI repositories.**
   - **`TESTING.md`:** Adapt from `skills/spectrace-plan/assets/testing-template.md`. Document contract invariants, input partitioning, and table test patterns.
   - **`CHANGES.md`:** Adapt from `skills/spectrace-plan/assets/changes-template.md`. Initialize with empty ledger table.
   - **`.agentignore`:** Adapt from `skills/spectrace-plan/assets/agentignore-template`.
   - **`planning/roadmap.md`:** Create roadmap skeleton with `# Roadmap` table (`ID`, `Spec`, `Status`, `Depends on`) and `## Ideas`.
3. **Present Summary:** Show created contracts and confirm next steps with user.

---

## Step 3 — Upgrade / Migration

For repositories already using an older version of Spectrace:

1. **Audit Obsolete Mechanics:**
   - **Git Hooks / Scripts:** Check for `.spectrace/hooks`, `.husky`, or `.git/hooks` enforcing commit trailers or spec linting. Remove or deprecate them; Spectrace uses zero hooks and zero runtime.
   - **Commit Trailers:** Inform the user that strict commit trailer hooks are retired in favor of standard Conventional Commits.
   - **Monolithic or Displaced Rules:**
     - Check if `ARCHITECTURE.md` or `DESIGN.md` contains engineering rules (KISS, SRP, DRY, DIP, casing).
     - Check if `TESTING.md`, `PRODUCT.md`, `ENGINEERING.md`, or `CHANGES.md` are missing.
2. **Non-Destructive Extraction & Refactoring:**
   - **Create `ENGINEERING.md`:** If missing, extract existing craftsmanship and code rules from `ARCHITECTURE.md` or `DESIGN.md` into a new `ENGINEERING.md`. Fill any gaps using `skills/spectrace-plan/assets/engineering-template.md`.
   - **Purify `ARCHITECTURE.md`:** Keep only system topology, layer boundaries, directory map, and component communication. Remove redundant engineering guidelines.
   - **Refactor `DESIGN.md`:** Ensure `DESIGN.md` contains only design/UI or editorial guidelines. Remove engineering or testing principles.
   - **Ensure `TESTING.md` exists:** If testing rules were scattered in `AGENTS.md` or `ARCHITECTURE.md`, extract them into `TESTING.md`.
   - **Ensure `PRODUCT.md` exists:** If vision and non-goals were in `README.md` or `AGENTS.md`, isolate them into `PRODUCT.md`.
   - **Update `AGENTS.md`:** Replace verbose or legacy instructions with the lean pointers format from `assets/agents-block.md`, retaining custom build/test commands.
   - **Update `.agentignore`:** Ensure modern AI tool ignores are present.
3. **Record in `CHANGES.md`:**
   - Append an entry to `CHANGES.md` documenting the migration:
     ```markdown
     | YYYY-MM-DD | Governance | Migrated repository to Spectrace 7-contract suite (extracted ENGINEERING.md, TESTING.md, updated AGENTS.md, retired legacy hooks) | Standardize progressive disclosure |
     ```
4. **Audit `planning/roadmap.md` and active specs:**
   - Ensure the roadmap table has columns `| ID | Spec | Status | Depends on |`.
   - Verify existing specs don't have broken links or conflicting task syntax.

---

## Step 4 — Verification & Report

1. Verify all 7 root documents exist and adhere to single responsibility:
   - `PRODUCT.md` (Product scope & non-goals)
   - `ARCHITECTURE.md` (Topology & structural map)
   - `ENGINEERING.md` (Code quality & principles)
   - `DESIGN.md` (Context-aware UI or editorial design)
   - `TESTING.md` (Verification invariants & input partitioning)
   - `CHANGES.md` (Historical log)
   - `AGENTS.md` (Lean operational manual < 150 lines)
2. Verify `planning/roadmap.md` is intact and `.agentignore` exists.
3. Report the outcome to the user with a list of updated or created files.
