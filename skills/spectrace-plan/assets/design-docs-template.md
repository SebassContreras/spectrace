# Documentation & Content Design Guidelines

This document governs the editorial style, document design, Markdown formatting, visual conventions, and content hierarchy for documentation, runbook, and governance repositories. AI agents must follow these rules when creating or updating documentation.

---

## 📝 Document Hierarchy & Frontmatter

### 1. Metadata Schema (Frontmatter)
Every substantive document should include standard frontmatter indicating its lifecycle and ownership:

```yaml
---
status: draft | in-review | validated | deprecated
owner: <role-or-team>
updated: YYYY-MM-DD
---
```

### 2. Structural Hierarchy
- **Single H1 (`#`):** Exactly one title per document matching the filename and primary topic.
- **Sectioning (H2 `##` & H3 `###`):** Use descriptive, scannable section headers. Do not skip levels (e.g., H2 to H4).
- **Executive Summaries:** Begin operational runbooks and architecture docs with a 2–3 line summary stating purpose and audience.

---

## 🎨 Visual Formatting & Conventions

### 1. Callouts & Visual Alerts
Use standard GitHub/GitLab markdown alerts sparingly to emphasize critical information:
- `> [!NOTE]`: Contextual background or non-critical hints.
- `> [!TIP]`: Best practices and workflow shortcuts.
- `> [!IMPORTANT]`: Essential prerequisites or constraints.
- `> [!WARNING]`: Breaking changes, destructive actions, or risky procedures.
- `> [!CAUTION]`: High-risk operations (production data, credentials, irreversible steps).

### 2. Tables & Key-Value Matrices
- Use markdown tables for comparisons, inventories, parameter references, and problem/solution mappings.
- Keep table columns concise and use backticks for paths, flags, and identifiers.

### 3. Diagrammatic Standards (Mermaid)
- Prefer `flowchart TD` or `flowchart LR` for workflows and architectures.
- Keep diagrams readable: maximum 10–12 nodes per diagram. Split complex multi-tier topologies into progressive sub-diagrams.
- Always quote node labels with special characters (e.g., `id["Node (detail)"]`).

---

## 🗣️ Tone, Voice & Language

### 1. Voice & Tone
- **Imperative & Direct:** For runbooks and procedures, write in clear imperative steps ("1. Run `check.sh`", "2. Verify the output").
- **Objective & Factual:** For architecture and business rules, describe observable behavior objectively. Clearly distinguish observed reality from planned decisions (e.g., `CURRENT:` vs `TARGET:`).

### 2. Language & Bilingual Policy
- Keep code symbols, bash commands, file paths, and technical keys in English.
- If the project operates in Spanish or another domain language, keep domain business terminology consistent with the project glossary, maintaining clear separation between English technical terms and domain concepts.
