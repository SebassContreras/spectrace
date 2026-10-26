# 023 — docs-tracing

## Goal

Docs follow the specs the same way code does: every doc line leads to the spec that
wrote it, a change of direction finds the docs it makes stale, and a change outside
every spec is marked on purpose. Check: `git blame README.md` on a line from this spec
shows a commit with `Spec: 023/…`.

## Requirements

- R1: Each project lists the docs it keeps and what each describes.
- R2: A spec that changes what a listed doc describes gets a task to update it.
- R3: A change of direction finds stale docs, including sentences that don't name the
  old thing.
- R4: A commit outside every spec can say so on purpose, distinct from a forgotten
  trailer.

## Design

- D1 (R1): `product.md` gets `## Docs`: one line per doc, with what it describes;
  `AGENTS.md` is always listed.
- D2 (R2): `spectrace-plan` adds a docs task whenever a spec touches what a listed doc
  describes; the doc changes in that task's commit, so `git blame` reaches the spec.
- D3 (R3): `spectrace-change` reads every listed doc in its sweep, uses `git blame` to
  tell which spec wrote a line, and its `Review:` task re-reads the docs.
- D4 (R4): The trailer `Spec: none` marks a deliberate untraced change; the
  `commit-msg` hook accepts it silently and still warns on a missing trailer.

## Tasks

- [x] 023/T001 [agent] `commit-msg` accepts `Spec: none`; warning suggests it — covers D4
- [x] 023/T002 [agent] Protocol block: docs are deliverables, `Spec: none` — covers D1, D2, D4
- [x] 023/T003 [agent] `spectrace-plan`: `## Docs` in product.md, docs tasks — covers D1, D2
- [x] 023/T004 [agent] `spectrace-change`: read listed docs, `git blame`, Review covers docs — covers D3
- [x] 023/T005 [agent] This repo: `## Docs` in product.md, README section on docs — covers D1
