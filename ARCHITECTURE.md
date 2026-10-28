# Architecture Blueprint

## System Overview

Spectrace provides a lightweight, spec-driven development methodology tailored for autonomous and semi-autonomous AI coding agents. It transforms unstructured plans and ideas into verifiable thin-slice specifications while maintaining living architectural and design contracts at the repository root.

```mermaid
graph TD
    A[Human / High-Level Plan] -->|spectrace-plan| B[Root Directives & planning/]
    B --> C[Root Decision Layer]
    B --> D[planning/ Execution Layer]
    
    subgraph "Root Decision Layer (Context Contracts)"
        C1[AGENTS.md - Operational manual]
        C2[PRODUCT.md - Scope & vision]
        C3[ARCHITECTURE.md - Structural blueprints]
        C4[DESIGN.md - UI/UX & Code standards]
        C5[CHANGES.md - Pivot & deprecation ledger]
    end

    subgraph "planning/ Execution Layer (Action Plan)"
        D1[roadmap.md - Ordered specs & status]
        D2[specs/NNN-name.md - Thin slices with tasks]
    end

    D2 -->|Agent executes task| E[Codebase Changes]
    E -->|Verify & Test| F[Check task box [x]]
    F -->|All tasks done| G[Update roadmap.md to done]
    
    H[Pivot or New Requirement] -->|spectrace-change| C4
    H -->|spectrace-change| D2
```

---

## Directory Organization

The repository strictly isolates **governance/decision contracts** at the project root from **transient action plans** in `planning/`.

```text
├── AGENTS.md               # Primary agent entrypoint (< 150 lines, pointers & DoD)
├── PRODUCT.md              # Vision, target users, problem statement, and scope boundaries
├── ARCHITECTURE.md         # Structural patterns, boundaries, and system topology
├── DESIGN.md               # Visual system tokens, UI components, and code conventions
├── CHANGES.md              # Historical ledger of pivots, replacements, and deprecations
├── README.md               # Human-oriented overview, installation, and usage
│
├── planning/               # Pure execution and scheduling layer
│   ├── roadmap.md          # Specs sequence, dependencies, statuses, and idea backlog
│   └── specs/              # Atomic specification slices
│       ├── 001-scaffold.md
│       └── 002-feature.md
│
└── skills/                 # Agent Skills (agentskills.io specification)
    ├── spectrace-plan/     # Skill to generate specs, roadmap, and foundational docs
    ├── spectrace-change/   # Skill to manage architectural pivots and refactor cleanup
    └── spectrace-review/   # Skill to audit code against 10 engineering & testing principles
```

---

## Structural Boundaries & Invariants

1. **Root-Level Discovery:**
   - AI tools (Claude Code, Cursor, Copilot, Antigravity) automatically inspect root directory context on startup.
   - Core decisions (`ARCHITECTURE.md`, `DESIGN.md`, `CHANGES.md`) live at the root so agents instantly acquire boundaries without deep directory traversal.

2. **Execution Isolation in `planning/`:**
   - `planning/` contains **only** execution artifacts (`roadmap.md` and `specs/`).
   - Broad architecture discussions must never be siloed inside individual specs; when a spec introduces a durable architectural pattern, it must be documented in `ARCHITECTURE.md`.

3. **Zero Runtime & Zero Hook Dependency:**
   - Development is driven by Markdown checkboxes (`- [ ]` / `- [x]`) and standard Git commits.
   - No platform-dependent shell scripts or Git commit-message hooks are enforced, preventing tool breakage across operating systems.

4. **Skill Standards:**
   - Every skill in `skills/` complies with the Agent Skills specification (`SKILL.md` with YAML frontmatter `name` and `description` under 1024 characters).
