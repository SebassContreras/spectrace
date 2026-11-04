# Engineering

> Owns: how code is written here, the principles and the stack conventions · Not here: commands (OPERATIONS.md), what to test and how (TESTING.md), the layer map (ARCHITECTURE.md)

## Principles

1. **KISS / YAGNI.** Build for today's need. Add an interface, adapter or abstraction only with 2+ concrete uses, 2+ implementations or a real test seam. Simple beats clever.
2. **One responsibility.** A file, module or function does one thing. If it does two unrelated things, split it.
3. **Compose, don't inherit.** Share logic through small functions and injected dependencies, not class hierarchies. A rule applied in two places lives in one function both call.
4. **Isolate vendors when it pays.** Wrap a third-party SDK or external API behind a project-owned interface when there are 2+ vendors or a test needs a seam; otherwise call it directly.
5. **Follow the stack.** Use the language and framework's idiomatic conventions and match the existing code before adding a new style. Casing: `kebab-case` files, `PascalCase` types, `camelCase` functions and variables, `UPPER_SNAKE_CASE` constants.
6. **Write down trade-offs.** A significant choice records its pros, cons and mitigation where the decision lives: the spec's Design, a code comment or CHANGES.md.
7. **Research only when it changes the decision.** Look it up when the choice is hard to reverse, depends on a fact outside the repo, or two options tie on a fact. Prefer the official specification or docs and cite `Source: <url> (accessed YYYY-MM-DD)`. Do not research what a contract already says or what running it settles.
8. **Docs travel with behavior.** A change of behavior updates the contract or doc that describes it in the same task.

## This project

<fill: only what differs from the principles: dependency and licence rules, linter and formatter choices, naming exceptions>
