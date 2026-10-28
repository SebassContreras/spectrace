# spectrace

**Spec-driven development for AI coding agents — with durable root contracts and zero runtime friction.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2.svg)](https://agentskills.io)

spectrace transforms any high-level plan or idea into structured, thin-slice specifications in `planning/` while keeping architectural and design contracts directly at the repository root. Any coding agent executes tasks step by step and marks progress with simple Markdown checkboxes.

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

1. **Install the skills** in your repository.
2. **Generate the foundation:** Tell your agent:
   > *"Turn this plan into specs."*
   `spectrace-plan` initializes root contracts (`AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`) and generates `planning/roadmap.md` with ordered specs in `planning/specs/`.
3. **Execute:** Tell any agent:
   > *"Execute the specs."*
   The agent picks the next open task, checks the architecture/design rules, implements the change, verifies it, marks `[x]`, and makes a standard commit.
4. **Pivots & Changes:** When plans change, tell your agent:
   > *"We changed our mind about X, now we want Y instead."*
   `spectrace-change` logs the pivot in `CHANGES.md`, strikes obsolete design items (`~~D1~~ → D2`), and adds safe cleanup tasks.

---

## 🏛️ Two-Tier Architecture

Spectrace separates **governance contracts** at the project root from **action plans** in `planning/`:

```text
├── AGENTS.md               # Quick operational manual & pointers for AI agents (< 150 lines)
├── PRODUCT.md              # Vision, target users, problem statement, and scope boundaries
├── ARCHITECTURE.md         # System overview, tech stack, layers, and Mermaid diagrams
├── DESIGN.md               # Visual UI/UX tokens, accessibility, and code conventions
├── CHANGES.md              # Historical ledger of pivots, replacements, and deprecations
├── README.md               # Human-oriented overview and setup guide
│
├── planning/               # Pure execution plan
│   ├── roadmap.md          # Specs sequence, dependencies, and idea backlog
│   └── specs/              # Atomic specification slices
│       └── NNN-name.md     # Goal, Requirements, Design, and Checkbox Tasks
│
└── skills/                 # Agent Skills
    ├── spectrace-plan/     # Generates specs and foundational contracts
    └── spectrace-change/   # Handles pivots, refactors, and deprecation tasks
```

### Why Root Decision Files?
Modern AI coding agents (Claude Code, Cursor, Copilot, Antigravity, Windsurf) immediately scan the repository root on startup. Placing `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `CHANGES.md` at the root guarantees immediate context discovery without wasting tokens searching nested folders.

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

## 🛠️ The Two Skills

| Skill | Purpose |
|---|---|
| **`spectrace-plan`** | Takes any plan, design, or transcript and generates root decision documents (`AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`), `planning/roadmap.md`, and ordered specs in `planning/specs/`. |
| **`spectrace-change`** | Handles pivots, bugs, and new requirements. Identifies affected code, strikes obsolete spec decisions, updates `CHANGES.md`, and sequences cleanup tasks so old code is cleanly eliminated. |

---

## License

[MIT](LICENSE)
