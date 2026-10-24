# 018 — consistency-audit — Design

## Approach

A dedicated audit engine in `spectrace/audit.py` that verifies coherence across Spectrace's guiding documents (`planning/product.md`, `planning/architecture.md`, `planning/styles.md`, `.spectrace/interview.md`), agent operational instructions (`AGENTS.md`, `skills/*/SKILL.md`), and the active specs and tasks.

The audit operates on the in-memory `Repo` model (preserving SRP and DRY without duplicating document parsing) and exposes standalone execution via `trace audit` as well as integrated execution via `trace check --audit`. All findings are reported through standard `repo.issue()` diagnostic tuples (`(severity, where, message, spec)`), maintaining consistency with `trace check` output formatting and exit code conventions.

The design adheres to the 10 Engineering Principles:
1. **KISS / YAGNI**: No heavyweight NLP or external parsers. Relies strictly on standard library Python (`re`, `pathlib`, string searching), simple exact heuristics, and pure rule checkers.
2. **SRP / Separation of Concerns**: Audit rules live in `spectrace/audit.py`, cleanly separated from CLI command handlers (`commands.py`), data loading (`model.py`), and Git operations (`gitio.py`).
3. **DRY via Composition**: Individual check rules are written as small, composable audit functions that receive parsed documents or repo structures and yield findings.
4. **Service Layer & Anti-Corruption**: File system reading and document parsing pass through cleanly defined repo accessors and standard data structures (`AuditFinding`, `DocumentSpan`).
5. **Small Interfaces & Pure Functions**: Rule evaluation functions are pure: `check_architecture_alignment(active_a_items, agents_md_text) -> list[AuditFinding]`.
6. **Behavior-driven Testing**: Tests assert observable diagnostic reporting on concrete sample documents (missing A-items, out-of-scope keywords, conflicting open interview dimensions).
7. **Testing Hygiene**: Given-When-Then test cases, isolated filesystem/mock setups, clear behavior-stating test names.
8. **Follow Stack Standards**: Standard library only (A2), Python 3.9+ idioms, PEP 8 styling, under the 600-line module budget (A5).
9. **Web Research Verification**: Validated static consistency auditing patterns and CLI flag conventions.
10. **Documented Trade-offs with Mitigations**: Full trade-off matrix detailing pros, cons, and concrete mitigations.

---

## Decisions

- D1@1 (implements R1): Add `spectrace/audit.py` containing the `run_audit(repo)` driver and individual inspection checks. Register `trace audit` in `COMMANDS` (`commands.py` and `cli.py`), accepting flags `--json` (machine-readable report) and `--strict` (exit 1 on warnings). Add `--audit` flag to `trace check` to include consistency audit findings within standard trace verification.
- D2@1 (implements R2): Implement `check_architecture_alignment(repo)` in `spectrace/audit.py`. For every active, non-retired $A$ item in `planning/architecture.md` (e.g. `A1`, `A2`, ... `A17`), verify that either its identifier (`A<id>`) or an operative rule referencing its substance appears in `AGENTS.md` (specifically under "Stack & conventions", "Rules for agents", or "Doc map"). Emit `warning` with exact line references in `planning/architecture.md` for any unreferenced or unrepresented architectural rule.
- D3@1 (implements R3): Implement `check_scope_alignment(repo)` in `spectrace/audit.py`. Parse the `## Not for now` and `## Out of scope` sections of `planning/product.md` to extract prohibited scope terms (e.g., "orchestration", "parallel dispatch", "dashboards", "per-harness adapters", "mutation testing"). Scan all spec titles, requirement summaries, and task descriptions in `planning/specs/` against these prohibited terms (excluding `requirements.md` "Out of scope" declarations). Emit `warning` on hits, indicating the offending spec/task, matched keyword, and source declaration in `product.md`.
- D4@1 (implements R4): Implement `check_interview_alignment(repo)` in `spectrace/audit.py`. If `.spectrace/interview.md` exists, parse the ledger table (`| dimension | status | answer |`). Identify dimensions marked `open`. Compare open dimensions against planned or in-progress specs (specs with status `todo` or `in_progress` having tasks created). If an open dimension directly impacts a spec's domain (e.g. open `runtime` or `datastore` when specs implement storage or language bindings), emit `warning` or `pending` with file reference and dimension name.
- D5@1 (implements R5): Standardize all audit findings as `(severity, where, message, spec)` tuples compatible with `repo.issue()`. Output format matches `trace check`: `<SEVERITY> <file:line> <message>`. When `--json` is specified, serialize the findings with keys `severity`, `where`, `file`, `line`, `message`, and `spec`.

---

## Deliverables

- `skills/spectrace-start/assets/spectrace/audit.py`: Audit rule engine and check implementations.
- `skills/spectrace-start/assets/spectrace/commands.py`: Command handler `cmd_audit` and updated `cmd_check` with `--audit` option.
- `skills/spectrace-start/assets/spectrace/cli.py`: CLI parser registration for `audit` and `check --audit`.
- `tests/test_audit.py`: Comprehensive behavior-driven test suite verifying all 4 check dimensions and CLI modes.
- `skills/spectrace-start/assets/format.md`: Document `trace audit` and `trace check --audit` in command reference.

---

## Sequencing

1. Implement core audit checks and pure functions in `spectrace/audit.py`.
2. Connect `cmd_audit` and `cmd_check --audit` in `spectrace/commands.py` and `spectrace/cli.py`.
3. Author behavior-driven tests in `tests/test_audit.py` covering architecture alignment, scope creep detection, interview ledger verification, and CLI output.
4. Document the command in `skills/spectrace-start/assets/format.md` and verify A5 module size budgets.

---

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Rule-based heuristic keyword and identifier matching instead of LLM semantics | Fast, deterministic, runs in <10ms, standard library only (A2, R-out-of-scope) | Can miss complex paraphrasing or trigger on benign mentions | Checkers filter out "Out of scope" sections of specs and support explicit exemption comments; keep audit findings as warnings by default |
| Distinct `spectrace/audit.py` module rather than inlining into `model.py` or `commands.py` | Strict SRP (Principle 2); keeps `model.py` (548 lines) and `commands.py` (220 lines) well under the 600-line budget (A5) | Introduces an additional module in `spectrace/` | All trace commands already import from internal modules; cohesive separation of audit concerns |
| Optional integration into `trace check --audit` while keeping `trace audit` standalone | Developers and CI can run audit on demand without slowing or breaking existing routine `trace check` runs | Two ways to invoke audit checks | `trace audit` is dedicated and supports `--json`; `trace check --audit` provides a single unified pre-flight gate |
| Warn on unreflected $A$ items rather than hard error | Allows incremental drafting of architectural guidelines without halting active task execution | May allow unoperative rules to linger if warnings are ignored | Supported `--strict` flag promotes warnings to exit code 1 for CI gates and release checks |
