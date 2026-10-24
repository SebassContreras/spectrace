# File templates

The shapes of the files `spectrace-start` writes. Item, task and roadmap grammar is defined in
`.spectrace/format.md` — not here. Write content only from the ledger; anything not
yet answered stays `TBD`.

## `AGENTS.md`

```markdown
# <project>

<one-line goal> For: <audience>. Type: <project-type>.

## Doc map

- `planning/product.md` — what this is, who it's for, out of scope.
- `planning/architecture.md` — project-wide decisions (A items).
- `planning/styles.md` — style detail (if present).
- `planning/roadmap.md` — specs, order, status.
- `planning/specs/NNN-name/` — requirements (R), design (D), tasks, changes.
- `.spectrace/format.md` — how all of the above is written.

## Stack & conventions

<short operative form of each A item: "Node 22 (A1)">

## Style

<operative summary from Phase D; hard rules marked as such; points to planning/styles.md>

## Rules for agents

<agent-rules answers; default rules below apply unless overridden>
- **KISS / YAGNI — No Over-Engineering**: Proportionality; start simple and direct; abstract only for 2+ uses/vendors or isolation for testing.
- **SRP / Separation of Concerns**: One responsibility per file/module/class; split multi-concern units.
- **DRY via Composition, not Inheritance**: Extract shared logic into injectable helpers/services; avoid deep inheritance.
- **Service Layer + Anti-Corruption / Dependency Inversion**: Wrap external libraries/APIs in adapter interfaces; business logic depends on interfaces, not vendors.
- **Small Interfaces & Pure Functions**: When in doubt, prefer small interfaces, pure functions, and injected testable dependencies.
- **Testing — Behavior, not Coverage**: Test observable behavior and explicit failure modes; regression test before every bug fix; never weaken tests to pass code.
- **Testing Hygiene**: Strict Given-When-Then / Arrange-Act-Assert; clear behavior-stating test names; no conditionals/loops in tests; mock boundary dependencies only.
- **Follow the Stack's Standards**: Idiomatic conventions, official style guides, and codebase consistency.
- **Web Research for Verification**: Ground non-trivial choices, APIs, libraries, and code examples with official documentation and web research.
- **Trade-off Analysis (Pros & Cons) & Mitigations**: Detail pros and cons of technical decisions; explicitly specify and implement concrete solutions/mitigations for drawbacks.
- **Adhere to Architecture Guidelines**: Strictly follow the project-wide conventions recorded in planning/architecture.md.
- **Sync Before Status**: Always synchronize repository status (`git pull` and `git status`) before reporting pending tasks or answering queries like "what's next" / "¿qué sigue?".

## Testing

<software projects only; omit this section for any other project type. Phase 4 of `spectrace-start` fills the commands from the `toolchain` answer — `TBD` until then; a mode the runner lacks is "none">
- narrowest (one file or module): `<cmd>`
- affected only: `<cmd>`
- full suite: `<cmd>`
- verification: <the `verification` answer — unit only, or which e2e/smoke tests>

Hard rules:
- **Run**: a task runs only the narrowest command covering the files it touched. The full suite runs only at session end or when a shared module (config, core, public interfaces) changed.
- **Create**: tests are minimal and proportional to the requirements, at the lowest level that proves each R (unit before integration). e2e and smoke tests only if the `verification` answer asks for them.
- **Skip**: do not test code without logic (wrappers, config, getters) nor a vendor's own behavior.
- **Tripwire**: if a spec's tests exceed three times its R items, stop and justify it in the task's report. It is a tripwire, not a cap.

<protocol block from assets/agents-protocol.md>
```

`AGENTS.md` is the only instructions file. Never create `CLAUDE.md`. If the repo
already has an `AGENTS.md`, add the sections that are missing and the protocol block;
change nothing else without asking.

## `planning/product.md`

```markdown
# Product

## What this is

## Who uses it

## Current MVP scope

## Not for now
```

## `planning/architecture.md`

```markdown
# Architecture

Project-wide decisions. Grammar: `.spectrace/format.md`.

## <type-keyed headers>

## Still to define
```

Headers by `project-type` (only the category picks the set):

| Type | Headers |
|---|---|
| software | `Container`, `Stack`, `Conventions` |
| marketing/content | `Channels`, `Tools`, `Data sources` |
| operations/process | `Systems`, `Cadence`, `Handoffs` |
| research | `Sources`, `Method`, `Output` |
| other / skipped | `Tools`, `Inputs/Outputs` |

Each decision is an A item under the header it belongs to:
`- A3@1: PostgreSQL 16 — why: relational data, team knows it.`
An undecided dimension is a bullet under `Still to define`, never an invented A item.

For `software` projects, the template seeds default architecture conventions under `## Conventions`:

```markdown
## Conventions

- A1@1: SRP / Separation of Concerns: un archivo/clase = una sola responsabilidad. Alta cohesión, bajo acoplamiento. Si un archivo o clase hace dos cosas, se divide — why: previene dependencias enredadas y facilita el testing y mantenimiento.
- A2@1: Service Layer + Anti-Corruption: nunca llamar librerías/APIs de terceros directamente desde la lógica de negocio; crear capa services/ / adapters/ con interfaces propias e inyectarlas (Dependency Inversion) — why: el dominio debe ser desacoplado e intercambiable de proveedores externos.
- A3@1: DRY con composición, no herencia: evitar jerarquías de herencia profundas; extraer lógica compartida en utils/servicios/helpers inyectables. Usar herencia solo para relaciones 'es-un' reales o Template Method — why: favorece flexibilidad, composabilidad y bajo acoplamiento.
- A4@1: Testability por defecto: ante la duda, diseñar interfaces pequeñas, funciones puras y dependencias inyectables — why: garantiza código predecible, verificable y testeable unitariamente sin mocks frágiles.
- A5@1: KISS / YAGNI sin sobre-ingeniería: aplicar proporcionalidad. No crear interfaces, adapters o abstracciones para un solo uso o un futuro hipotético; abstraer solo ante 2+ usos, 2+ vendors o necesidad de testing (Simple > Inteligente) — why: evita complejidad accidental y código muerto.
```

## `planning/roadmap.md`

```markdown
# Roadmap

Index of every spec. `Status` and `Stage` are written only by `trace`. Grammar:
`.spectrace/format.md`.

| ID  | Spec | Status | Depends on | Stage | Priority |
|-----|------|--------|------------|-------|----------|
```

Nothing else goes in this file — no history, no prose ordering.

## `planning/specs/NNN-name/requirements.md`

```markdown
# NNN — name — Requirements

## What's being built

## Who it serves

## Requirements

- R1@1: <one checkable statement>

## Out of scope

## Dependencies

## Owner split
```

Every R item is observably checkable: someone could tell, by looking or running
something, whether it holds. A hard constraint is an R item too. `## Dependencies` is
written even when the answer is "None."

## `planning/specs/NNN-name/design.md` and `tasks.md` (stubs)

```markdown
# NNN — name — Design

TBD — closed by the `spectrace-plan` skill.
```

```markdown
# NNN — name — Tasks

TBD — written by the `spectrace-plan` skill.
```

## `.spectrace/interview.md`

```markdown
# Interview ledger

| dimension | status | answer |
|-----------|--------|--------|
| idea-detail | open | |
```

One row per question-bank dimension, in phase order; per-spec rows prefixed with the
spec ID (`002.requirements`). Write the user's own words in `answer`, not a paraphrase.
