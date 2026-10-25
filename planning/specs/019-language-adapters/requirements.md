# 019 — language-adapters — Requirements

## What's being built

Symbol-level tracing for languages other than Python and Markdown. Today `symbols/__init__.py` registers only those two adapters, `facts.py` skips every non-`.py` file, and `linker.py` resolves only Python module paths, so a TypeScript, Rust, Go or Dart file is read as `lang: file`: no spans, no imports, no graph edges. Every symbol-level view (`impact --deep/--direction/--depth`, `why path::symbol`, `packet` dependents, `leftover`/`keep` per symbol) then returns empty or file-level results.

This spec adds one generic adapter for brace-delimited languages, driven by a per-language table (declaration keywords, import syntax, path resolution), instead of one hand-written module per language. Python keeps its `ast` adapter. Unsupported languages are reported as not analysed instead of silently returning empty lists.

## Who it serves

Teams running spectrace on non-Python codebases (first: orki, TypeScript), and the agents that rely on `impact` and `leftover` before deleting or changing a symbol.

## Requirements

- R1@1: A generic adapter returns `Span`s for brace-delimited languages through the existing `symbols(text) -> [Span]` interface, ignoring braces inside strings, comments and template literals.
- R2@1: Adding a language is a table entry (extensions, declaration keywords, import patterns, resolution rules), not a new module. The first entries are TypeScript/JavaScript (`ts`, `tsx`, `js`, `jsx`, `mts`), Rust (`rs`), Go (`go`) and Dart (`dart`).
- R3@1: Recognised declarations per entry cover at least: TS/JS `function`, `class` and its methods, `interface`, `type`, `enum`, `export const` arrow functions; Rust `fn`, `struct`, `enum`, `trait`, `impl` methods; Go `func`, methods with receivers, `type`; Dart `class`, `mixin`, `extension`, top-level and member functions.
- R4@1: `facts.py` dispatches by language and extracts imports and identifier references for every adapter-backed language, not only `.py`.
- R5@1: `linker.py` resolves imports per language: TS relative paths (`./y` → `y.ts`, `y.tsx`, `y/index.ts`, `y.d.ts`) and `tsconfig.json` `baseUrl`/`paths` aliases; Rust `mod`/`use crate::`; Go module paths from `go.mod`; Dart relative and `package:` imports from `pubspec.yaml`.
- R6@1: An edge whose import resolves to an exported symbol is `exact`; an edge matched by bare name is `inferred`. Only `exact` edges keep a spec open, as today.
- R7@1: No Python default is assumed: the `"python"` fallbacks in `linker.py` use the file's real `lang`, and `resolution_rate` is reported per language.
- R8@1: For a file with no adapter, every symbol-level command states `Not analysed: no adapter for .<ext>` instead of returning an empty list that reads as "no dependents".
- R9@1: `trace index --status` lists each indexed language with its file count, symbol count and resolution rate.
- R10@1: Once R1–R6 hold, `leftover` and `keep` work per symbol for adapter-backed languages, with no change to their own logic.
- R11@1: Each adapter behaviour has one test with a small source fixture, and one e2e scenario retires a task over a TypeScript file and gets per-function leftovers from `check`.

## Out of scope

- tree-sitter or any other new dependency (it can later sit behind the same interface, with explicit approval).
- Type-aware resolution (overloads, generics, dynamic dispatch); those edges stay `inferred`.
- Changing the Python `ast` adapter.

## Dependencies

- 011 (modular-core)
- 015 (e2e-graph)

## Owner split

- `agent`: Adapter, language table, facts/linker changes, tests and e2e scenario.
- `human`: Approve the initial language list and accept the precision of the regex/brace approach.
