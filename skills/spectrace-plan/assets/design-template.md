# UI/UX Design & Style Guidelines

This document governs visual UI/UX conventions, semantic design tokens, component interaction states, and accessibility standards. AI agents must follow these rules when implementing user interfaces, screens, or frontend components.

---

## 🎨 Visual & UI/UX Standards

### 1. Design Token Strategy
- **Tokens over Raw Values:** Always use semantic design tokens or CSS variables. Never hardcode arbitrary hex codes, pixel margins, or magic numbers.
- **Color Semantics:**
  - `primary`: Core actions, primary buttons, and key interactive focal points.
  - `surface` / `background`: Background tiers for cards, panels, and body.
  - `muted`: Subdued text, secondary borders, and placeholders.
  - `destructive` / `danger`: Destructive actions, error states, and warnings.
  - `accent`: Highlights, badges, and attention indicators.
- **Typography Scale:**
  - Standard scale: `xs` (12px), `sm` (14px), `base` (16px), `lg` (18px), `xl` (20px), `2xl` (24px), `3xl` (30px).
  - Explicit line-heights tied to font size for optimal readability.
- **Spacing Scale:**
  - Adhere strictly to a 4px / 8px incremental scale (`4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`).

### 2. Component Hierarchy & Layout
- **Composition over Inheritance:** Build composite components from tested primitives.
- **Responsive Layout:** Design mobile-first or fluid layout using Flexbox and Grid. Avoid fixed viewport widths.
- **State Feedback:** Every interactive control must declare clear states:
  - `default`
  - `hover`
  - `focus` (visible focus ring for keyboard navigation)
  - `active`
  - `disabled` (reduced opacity, `aria-disabled="true"`, pointer-events none)
  - `loading` (spinner or skeleton placeholder, non-interactive)

### 3. Accessibility (A11y)
- **Contrast:** Maintain WCAG AA compliant contrast ratios (minimum 4.5:1 for normal text, 3:1 for large text) for all elements.
- **Keyboard Navigation:** All interactive elements must be focusable via Tab and operable via Enter/Space.
- **Semantics:** Use standard HTML tags (`<button>`, `<nav>`, `<main>`, `<dialog>`) instead of nested `<div>`s with click handlers.
- **Screen Readers:** Include descriptive `aria-label` when visual labels are omitted (e.g., icon-only buttons).

### 4. Copy, Tone & Microcopy
- **Action-Oriented Labels:** Button labels must be imperative verbs (e.g., "Save changes", "Delete project", "Create account").
- **Clear Error Messages:** State what happened and how to fix it; avoid cryptic status codes or blame.
- **Language & Locale:** Follow the repository's specified primary interface language.
