# Design

> Owns: how the content reads and is laid out: audience, voice, structure, terminology and format · Not here: how the project is built or run (ARCHITECTURE.md, OPERATIONS.md), code rules (ENGINEERING.md)

## Audience and voice

Developers and coding agents reading a contract in the middle of a task. Imperative and concise, one instruction per line, no filler and no speculation.

## Structure

- Every contract opens with `> Owns: … · Not here: …`.
- Specs use Goal, Requirements, Design (optional), Tasks and Changes.
- Skill and playbook procedures use numbered steps.

## Terminology

- **contract**: a root Markdown file with one responsibility.
- **playbook**: a repository-owned procedure under `.agents/playbooks/`.
- **guard**: the enforcement script, `guard.mjs`.
- **spec**: a thin slice with requirements and tasks.

Do not call these a "rules file", a "workflow" or a "linter".

## Format

GitHub-flavoured Markdown, tables for routers and comparisons, fenced blocks for examples.
