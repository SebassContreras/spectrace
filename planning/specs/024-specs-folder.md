# 024 — specs-folder

## Goal
Spec files live in `planning/specs/NNN-name.md`, so `product.md` and `roadmap.md` stay
easy to find as finished specs pile up. Check: the hooks find specs there and the
skills, block and README name that path.

## Requirements
- R1: Every spec file is `planning/specs/NNN-name.md`; `planning/` keeps only product,
  roadmap and the project's own notes.
- R2: A project with spec files directly in `planning/` gets them moved by
  `spectrace-plan`.

## Design
- D1 (R1): The hooks list `planning/specs/[0-9][0-9][0-9]-*.md`; the block, the skill and
  the README name that path.
- D2 (R2): `spectrace-plan` step 1 `git mv`s stray `planning/NNN-*.md` into
  `planning/specs/`.

## Tasks
- [x] 024/T001 [agent] Hooks read specs from `planning/specs/` (assets and this repo) — covers D1
- [x] 024/T002 [agent] Block, `spectrace-plan` and README name `planning/specs/NNN-name.md` — covers D1
- [x] 024/T003 [agent] `spectrace-plan` moves spec files found directly in `planning/` — covers D2
- [x] 024/T004 [agent] Move 021–023 into `planning/specs/` — covers R1
