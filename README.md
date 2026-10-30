# spectrace

**Spec-driven development for AI coding agents — with decoupled root contracts and zero runtime friction.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2.svg)](https://agentskills.io)

spectrace transforms any high-level plan or idea into structured, thin-slice specifications in `planning/` while establishing decoupled architectural, engineering, design, and testing contracts directly at the repository root. Any coding agent executes tasks step by step and marks progress with simple Markdown checkboxes.

When you pivot, discover a bug, or change your mind, spectrace records the rationale in `CHANGES.md` and schedules explicit cleanup tasks so obsolete code is never left behind.

**Pure Markdown and Git. No runtime, no daemons, and no fragile shell hooks.**

---

## 📦 Install

From your project folder:

```sh
pnpm dlx skills add SebassContreras/spectrace
```

The [`skills` CLI](https://github.com/vercel-labs/skills) installs the skills into your agent's skills directory (`.claude/skills/`, `.agents/skills/`, or global with `-g`).

---

## ⚡ Quick Start

1. **Install the skills** in your repository:
   ```sh
   pnpm dlx skills add SebassContreras/spectrace
   ```
2. **Initialize or Upgrade:** Tell your agent:
   > *"Initialize spectrace in this repo"* or *"Upgrade spectrace to the latest version"*
   `spectrace-init` sets up the 7 decoupled contracts (`PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`, `AGENTS.md`) and `planning/`, or migrates legacy spectrace setups without losing historical decisions. Alternatively, run via CLI: `node bin/spectrace-init.mjs .` (or `--upgrade`).
3. **Generate the foundation:** Tell your agent:
   > *"Turn this plan into specs."*
   `spectrace-plan` initializes or builds out specs in `planning/roadmap.md` and `planning/specs/` using **context-aware design**.
4. **Execute:** Tell any agent:
   > *"Execute the specs."*
   The agent picks the next open task, checks the architecture, engineering, and test rules, implements the change, verifies it, marks `[x]`, and makes a standard commit.
5. **Audit & Review:** Tell your agent:
   > *"Review this code against our engineering standards."*
   `spectrace-review` audits the implementation against `ENGINEERING.md` (KISS/YAGNI, SRP, DIP), `TESTING.md` (invariants, table tests), and `ARCHITECTURE.md` (layer boundaries) without altering code.
6. **Pivots & Changes:** When plans change, tell your agent:
   > *"We changed our mind about X, now we want Y instead."*
   `spectrace-change` logs the pivot in `CHANGES.md`, strikes obsolete design items (`~~D1~~ → D2`), and adds safe cleanup tasks.

---

## 🏛️ Two-Tier Architecture & Separation of Concerns

Spectrace isolates **durable governance contracts** at the project root from **transient action plans** in `planning/`, following a progressive disclosure model:

```text
├── AGENTS.md               # Quick operational manual & pointers for AI agents (< 150 lines)
├── PRODUCT.md              # Vision, target users, problem statement, and scope boundaries (non-goals)
├── ARCHITECTURE.md         # System topology, directory map, layer boundaries, and Mermaid diagrams
├── ENGINEERING.md          # Code quality principles: KISS/YAGNI, SRP, DRY, DIP/ACL, casing
├── DESIGN.md               # Context-aware design: UI/UX tokens or content/editorial standards
├── TESTING.md              # Testing standards, contract invariants, input partitioning, and test hygiene
├── CHANGES.md              # Historical ledger of pivots, replacements, and deprecations
├── README.md               # Human-oriented overview and setup guide
│
├── planning/               # Pure execution plan
│   ├── roadmap.md          # Specs sequence, dependencies, and idea backlog
│   └── specs/              # Atomic specification slices
│       └── NNN-name.md     # Goal, Requirements, Design, and Checkbox Tasks
│
└── skills/                 # Agent Skills (agentskills.io compatible)
    ├── spectrace-init/     # Initializes Spectrace in new repos or upgrades legacy repos
    ├── spectrace-plan/     # Generates specs and decoupled foundational contracts
    ├── spectrace-change/   # Handles pivots, refactors, and deprecation tasks
    └── spectrace-review/   # Audits code against engineering, testing, and design standards
```

### Why Decoupled Root Decision Files?
Modern AI coding agents (Claude Code, Cursor, Copilot, Antigravity, Windsurf) immediately scan the repository root on startup. Placing clear, single-responsibility files at the root guarantees immediate context discovery without wasting tokens searching nested folders:
- **`PRODUCT.md`**: Prevents scope creep by declaring explicit boundaries.
- **`ARCHITECTURE.md`**: Tells the agent *where code lives* and *how components wire together*.
- **`ENGINEERING.md`**: Tells the agent *how to write clean, decoupled code* (KISS, SRP, DIP).
- **`DESIGN.md`**: Governs visual tokens for UI apps, or document/editorial conventions for documentation repos (**Context-Aware Design** prevents injecting CSS tokens into non-UI repos).
- **`TESTING.md`**: Enforces invariant testing, input partitioning, and clean AAA table tests.
- **`CHANGES.md`**: Provides historical memory so obsolete patterns are not re-introduced.

---

## 📝 A Spec File

```markdown
# 003 — login

## Goal
A user can sign in and stay signed in across browser reloads.

## Requirements
- R1: A user signs in with email and password.

## Design
- ~~D1 (R1): Sessions live in localStorage.~~ → D2
- D2 (R1): Sessions live in an httpOnly cookie.

## Tasks
- [x] 003/T001 [agent] Login form component — covers R1
- [ ] 003/T002 [agent] Session cookie middleware — covers D2
- [ ] 003/T003 [agent] Remove localStorage session code — replaces D1
- [ ] 003/T004 [human] Provision email provider credentials — covers R1
      blocked: waiting for billing approval

## Changes
- 2026-10-12: D1 → D2. Why: localStorage is vulnerable to script injection. Work: T003.
```

- **`R` (Requirements) & `D` (Design):** Immutable labels. Struck through (`~~D1~~ → D2`) when replaced.
- **Tasks:** `- [ ] NNN/TNNN [agent] ... — covers D2` or `— replaces D1`.
- **`[agent]` vs `[human]`:** Distinguishes autonomous coding tasks from human-only actions (billing, physical actions, private API keys).

---

## 🛠️ The Four Skills

| Skill | Purpose |
|---|---|
| **`spectrace-init`** | Initializes Spectrace in a new repository (with context-aware scaffolding) or safely upgrades a legacy Spectrace repository to the 7-contract progressive disclosure suite without clobbering history. |
| **`spectrace-plan`** | Takes any plan, design, or transcript and generates decoupled root decision documents (`AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`) using context-aware design, plus `planning/roadmap.md` and ordered specs in `planning/specs/`. |
| **`spectrace-change`** | Handles pivots, bugs, and new requirements. Identifies affected code, strikes obsolete spec decisions, updates `CHANGES.md`, and sequences cleanup tasks so old code is cleanly eliminated. |
| **`spectrace-review`** | Audits code against Core Engineering Principles in `ENGINEERING.md`, Testing Standards in `TESTING.md`, Structural Boundaries in `ARCHITECTURE.md`, and Design Compliance in `DESIGN.md`. |

---

## License

[MIT](LICENSE)
