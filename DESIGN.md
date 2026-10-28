# Design & Style Guidelines

This document governs visual UI/UX conventions, design tokens, and engineering code standards. AI agents must follow these rules when implementing interfaces or writing code.

---

## 🎨 Visual & UI/UX Standards

### 1. Design Token Strategy
- **Tokens over Raw Values:** Always use semantic design tokens or CSS variables. Never hardcode arbitrary hex codes, pixel margins, or magic numbers.
- **Color Semantics:**
  - `primary`: Core actions, primary buttons, and key interactive focal points.
  - `surface` / `background`: Background tiers for cards, panels, and body.
  - `muted`: Subdued text, secondary borders, and placeholders.
  - `destructive` / `danger`: Destructive actions, error states, and warnings.
- **Spacing Scale:** Adhere to a standard 4px / 8px incremental scale (`4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`).

### 2. Component Hierarchy & Layout
- **Composition over Inheritance:** Build composite components from tested primitives.
- **Responsive Layout:** Design mobile-first or fluid layout using Flexbox and Grid. Avoid fixed viewport widths.
- **State Feedback:** Every interactive control must declare clear hover, focus, active, disabled, and loading states.

### 3. Accessibility (A11y)
- **Contrast:** Maintain WCAG AA compliant contrast ratios for all text elements.
- **Keyboard Navigation:** All interactive elements must be focusable with visible focus rings.
- **Semantics:** Use standard HTML tags (`<button>`, `<nav>`, `<main>`, `<dialog>`) instead of nested `<div>`s with click handlers. Include `aria-label` when the visual label is omitted (e.g. icon-only buttons).

---

## 💻 Engineering & Code Conventions

### 1. File & Identifier Naming
- **Directories & Markdown:** `kebab-case` (e.g., `specs/001-user-auth.md`).
- **Source Files & Modules:** `kebab-case` or framework-idiomatic (e.g., `user-profile.ts` or `UserProfile.tsx`).
- **Classes & Types:** `PascalCase` (e.g., `TaskRunner`, `SpecDefinition`).
- **Functions & Variables:** `camelCase` (e.g., `calculateRoadmapStatus`, `activeSpecId`).
- **Constants & Enums:** `UPPER_SNAKE_CASE` or `PascalCase` (e.g., `MAX_RETRY_COUNT`).

### 2. Typing & Quality
- **Strict Mode:** No implicit `any` in TypeScript or untyped signatures in typed languages.
- **Explicit Returns:** Define explicit return types on public module boundaries and exported functions.
- **Pure Functions:** Favor pure, deterministic functions for business calculations and state transformations.

### 3. Error Handling & Defensive Coding
- **Fail Fast & Explicitly:** Do not swallow errors in empty catch blocks. Log actionable diagnostic context.
- **User-Facing Errors:** Provide human-friendly error messages that suggest recovery steps.

### 4. Testing Standards
- **Behavior over Implementation:** Test observable inputs and outputs rather than internal private variables.
- **Atomic Tests:** Each test case should assert a single behavior or requirement.
