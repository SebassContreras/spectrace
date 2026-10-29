---
name: spectrace-plan
description: >-
  Turns a plan that already exists into small ordered specs in planning/ (roadmap.md,
  specs/NNN-name.md with goal, requirements, design, tasks) and establishes decoupled root-level
  decision documents (AGENTS.md, PRODUCT.md, ARCHITECTURE.md, ENGINEERING.md, DESIGN.md, TESTING.md,
  CHANGES.md) with context-aware design scaffolding. Pure Markdown and Git, zero runtime and zero hooks.
  Use when: "turn this plan into specs", "plan this project", "add a spec for X", "new feature: Y",
  "create specs from plan", "generate roadmap", "new spec for Z".
---

# spectrace-plan

Run **inside the target repo**. The execution protocol is defined in `assets/agents-block.md` and installed into the repository's `AGENTS.md`.

---

## 📚 Repository Governance & File Responsibilities

Spectrace enforces a strict Separation of Concerns across root-level documents based on modern industry standards and progressive disclosure:

| Document | Responsibility | Standard Contents | Context-Aware Scoping |
|:---|:---|:---|:---|
| **`PRODUCT.md`** | **Business & Scope** (*The Why & What*) | Vision, target personas, problems solved, functional capabilities, and **explicit non-goals** (preventing scope creep). | Universal across all repositories. |
| **`ARCHITECTURE.md`** | **System Topology** (*The Spatial Blueprint*) | Directory map, component communication, layer boundaries, dependency direction, infrastructure, and Mermaid diagrams. | Universal across all repositories. |
| **`ENGINEERING.md`** | **Craftsmanship & Code Standards** (*How We Write Code*) | KISS/YAGNI (no over-engineering), SRP (single responsibility), DRY by composition, Anti-Corruption Layer / DIP, naming casing, and trade-off documentation. | Universal across all repositories. |
| **`DESIGN.md`** | **Interaction & Visual / Content Design** | UI tokens, component hierarchy, accessibility, copy and tone. | **Context-Aware:**<br>• *UI/Frontend:* Visual tokens, colors, spacing, component states, WCAG AA.<br>• *Docs/Governance:* Editorial guidelines, frontmatter schema, callouts, Mermaid styling, language policy.<br>• *API/CLI:* Payload shapes, CLI flags, error schemas. **Never inject CSS tokens into non-UI repos.** |
| **`TESTING.md`** | **Verification & Test Quality** (*The How to Assert*) | Invariants, contract suites, systematic input partitioning (boundaries, malformed inputs), AAA structure, parameterized/table-driven tests, boundary mocking. | Universal across all repositories. |
| **`CHANGES.md`** | **Historical Ledger** (*The Memory*) | Append-only log of architectural pivots, replaced decisions (`D1 → D2`), and deprecations. | Universal across all repositories. |
| **`AGENTS.md`** | **Operational Manual** (*The Hands*) | Operational commands (build, test, lint), workflow steps, task lifecycle, and pointers to root docs. Kept lean (< 150 lines). | Universal across all repositories. |

---

## Step 1 — Find the plan

1. The plan is in the conversation, or in a file named by the user. If neither, ask for it in one sentence — do not interview. A rough plan is enough.
2. Inspect what already exists: `AGENTS.md`, `PRODUCT.md`, `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, `TESTING.md`, `CHANGES.md`, `planning/roadmap.md`, `planning/specs/`, and existing codebase layout. An existing `planning/` means you are **adding** specs.
3. Ask **one round** of questions strictly about blockers (stack choices left open, credentials). Everything else: choose the simplest standard pattern and record it in the spec's Design.

---

## Step 2 — Cut it into specs

- Each spec is a **thin slice** ending in verifiable running software: a page that renders, a command that answers, an endpoint that responds. Prefer multiple small specs over one monolithic spec.
- The first spec establishes a running scaffold and one end-to-end user path.
- Order specs by dependency and note dependencies in the roadmap's `Depends on`.
- Any idea not needed immediately goes to `## Ideas` in `planning/roadmap.md`.

---

## Step 3 — Write each spec

Write `planning/specs/NNN-name.md`, where `NNN` is the highest existing spec ID + 1 (starting at 001) and `name` is kebab-case. All content in English:

- **Goal** — what works when complete and how to verify it, in 2–3 lines.
- **Requirements** — `R1:`, `R2:`… checkable outcomes.
- **Design** — `D1 (R1):`… decisions serving each requirement. Mark assumptions as `(assumed)`.
- **Tasks** — `- [ ] NNN/T001 [agent] <action> — covers D1`, referencing the R or D items it implements.
  - Granular, verifiable actions.
  - `[human]` for tasks requiring external accounts, credentials, or physical actions; `[agent]` for code and tests.
  - Tests: one test task per checkable requirement.
  - Checks without file changes are written as `Verify: <check>`.
  - Documentation updates: when a public API, command, or architectural boundary changes, include a task to update `ARCHITECTURE.md`, `ENGINEERING.md`, `DESIGN.md`, or `TESTING.md`.

---

## Step 4 — Confirm, then write

1. Present the roadmap rows and per-spec goals/tasks to the user. Ask for confirmation before writing files. If there is no git repo, run `git init` upon confirmation.
2. **First-time setup (when root decision files or `planning/` are absent):**
   - **`AGENTS.md`**: Create or update with the contents of `assets/agents-block.md`. Keep it lean (< 150 lines) with operational instructions and pointers.
   - **`PRODUCT.md`**: Initialize from `assets/product-template.md`. Outline product vision, target audience, core problems solved, and scope boundaries.
   - **`ARCHITECTURE.md`**: Initialize from `assets/architecture-template.md`. Outline system overview, stack, layer boundaries, directory map, and initial Mermaid topology diagram.
   - **`ENGINEERING.md`**: Initialize from `assets/engineering-template.md`. Define Core Engineering Principles (KISS, SRP, DRY, DIP/ACL, stack casing).
   - **`DESIGN.md` (Context-Aware Selection):**
     - **UI / Frontend Repos:** Initialize from `assets/design-template.md`. Define visual tokens, typography, component states, and accessibility rules.
     - **Documentation / Governance Repos:** Initialize from `assets/design-docs-template.md`. Define document hierarchy, frontmatter metadata, callouts, Mermaid diagrams, tone, and bilingual conventions.
     - **CLI / Backend / Library Repos:** Define contract schemas and CLI argument conventions. **Never inject CSS tokens into non-UI repositories.**
   - **`TESTING.md`**: Initialize from `assets/testing-template.md`. Define testing invariants, input partitioning, table-driven test conventions, and mocking boundaries.
   - **`CHANGES.md`**: Initialize from `assets/changes-template.md` with the change protocol and empty log table.
   - **`.agentignore`**: Copy `assets/agentignore-template` to `.agentignore` to prevent context pollution in AI coding tools.
   - **`planning/roadmap.md`**: Create `# Roadmap` table with columns `| ID | Spec | Status | Depends on |` and `## Ideas`.
3. Add each spec file into `planning/specs/NNN-name.md` and add its corresponding row in `planning/roadmap.md` with status `todo`.
4. Delete the initial plan file if requested by the user.

---

## Step 5 — Report and stop

Summarize what was created, highlight any `[human]` tasks, and report the next step: "Tell any agent to execute the specs." **Stop** — do not start executing tasks within the planning phase.
