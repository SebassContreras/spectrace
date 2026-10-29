# Documentation & Content Design Guidelines

This document governs editorial style, Markdown formatting, visual conventions, and content hierarchy for `spectrace`. As a framework built on pure Markdown and Agent Skills, its design focuses on document clarity, scannable information architecture, and rigorous schema compliance.

---

## 📝 Document Hierarchy & Structure

### 1. Spec & Document Layout
- **Single H1 (`#`):** Exactly one H1 per file, strictly matching the spec ID/name (e.g., `# 030 — separation-of-concerns...`) or document title.
- **Sectioning (H2 `##` & H3 `###`):** Use standardized sections:
  - For specs: `## Goal`, `## Requirements`, `## Design`, `## Tasks`, `## Changes`.
  - For governance docs: `## Overview`, `## Principles`, `## Invariants`.
- **Task Formatting:** Strictly follow `- [ ] NNN/TNNN [agent|human] <action> — covers <R/D>`. Completed tasks use `- [x]`.

### 2. Skill Frontmatter Specification
Every skill in `skills/` must follow the Agent Skills standard:
- Valid YAML frontmatter enclosed in `---`.
- Required fields: `name` (matching directory name in kebab-case) and `description` (under 1024 characters, clear trigger phrases).
- Single H1 matching `name` followed by clear step-by-step procedures (`## Step 1`, `## Step 2`).

---

## 🎨 Visual Formatting & Alert Callouts

### 1. Alert Callouts
Use standard GitHub markdown alerts sparingly to emphasize critical information:
- `> [!NOTE]`: Contextual background or non-critical hints.
- `> [!TIP]`: Workflow efficiencies and shortcuts.
- `> [!IMPORTANT]`: Essential prerequisites or constraints.
- `> [!WARNING]`: Breaking changes or deprecated behaviors.
- `> [!CAUTION]`: Destructive actions.

### 2. Diagrammatic Conventions (Mermaid)
- Prefer `flowchart TD` or `flowchart LR` for workflows and architectures.
- Keep diagrams readable: maximum 10–12 nodes per diagram.
- Always quote node labels containing special characters (e.g., `id["Node (detail)"]`).

---

## 🗣️ Tone, Voice & Language

### 1. Voice & Tone
- **Imperative & Action-Oriented:** For instructions and task definitions, write in clear imperative form ("Create template", "Update skill", "Verify output").
- **Concise & Direct:** Omit pleasantries, conversational filler, and speculative statements.
- **Traceable:** Every decision, requirement, or change must link to its rationale.

### 2. Language Standard
- All framework code, skill definitions, templates, and specs in `spectrace` are written in **English**.
