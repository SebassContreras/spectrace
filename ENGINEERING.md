# Engineering

> Owns: how code is written here, the principles and the stack conventions · Not here: commands (OPERATIONS.md), what to test and how (TESTING.md), the layer map (ARCHITECTURE.md)

## Principles

1. **KISS / YAGNI.** Build for today's need. Add an interface, adapter or abstraction only with 2+ concrete uses, 2+ implementations or a real test seam. Simple beats clever.
2. **One responsibility.** A file, module or function does one thing. If it does two unrelated things, split it.
3. **Compose, don't inherit.** Share logic through small functions and injected dependencies, not class hierarchies. A rule applied in two places lives in one function both call.
4. **Isolate vendors.** Business logic does not call a third-party SDK or API directly: it calls a project-owned interface that one adapter implements, so the vendor is swappable. Exception: a stable, single-use helper (a date or string library) may be called directly; say so in a comment.
5. **When in doubt.** Small interface, pure function, injected dependency.
6. **Follow the stack.** Use the language and framework's idiomatic conventions and match the existing code before adding a new style. Casing: `kebab-case` files, `PascalCase` types, `camelCase` functions and variables, `UPPER_SNAKE_CASE` constants.
7. **Write down trade-offs.** A significant choice records its pros, cons and mitigation where the decision lives: the spec's Design, a code comment or CHANGES.md.
8. **Confirm with a source.** Before committing to an approach that rests on a fact outside the repo (an API's behavior, a version, a platform rule), look it up, prefer the official specification or docs, and cite `Source: <url> (accessed YYYY-MM-DD)`. Skip it for what a contract already says or what running it settles.
9. **Docs travel with behavior.** A change of behavior updates the contract or doc that describes it in the same task.

## This project

- JavaScript ES modules on Node 20 or later, no dependencies and no build step.
- The skill ships Markdown only. Any script a project adds later is Node, so Windows behaves like Linux.
- A rule enters a template after a failure observed in a real project, not by adding principles up front.
