# 009 — testing-policy — Design

## Approach

Text-only change to three skills' reference files; no new code, no `trace.py` change. The
policy is written once, in the `AGENTS.md` "Testing" template, and the other files point at
it instead of repeating it (DRY, A4).

- D1@1 (implements R1): The `toolchain` row of `question-bank.md` asks for the test commands as three separate answers — one file or module, affected only, full suite — and keeps the "record only what the toolchain accepts" rule. A toolchain with no affected-only mode records that command as "none".
- D2@1 (implements R6): The `verification` row of `question-bank.md` states that unit tests are the default and asks whether e2e or smoke tests are wanted at all; "no" is a valid answer.
- D3@1 (implements R2, R7, R8): `templates.md` gives `AGENTS.md` a `## Testing` section, marked as hard rules, holding the command map (`narrowest`, `affected`, `full`), the run rule, the creation rule, the no-logic/no-vendor rule and the three-times-R tripwire.
- D4@1 (implements R3): `agents-protocol.md` step 4 runs the narrowest command for the files the task changed, and the full suite only for a shared module (config, core, public interfaces) or at session end; it refers to `AGENTS.md` "Testing" for the commands.
- D5@1 (implements R4, R5): `spectrace-plan/SKILL.md` Phase 3 replaces the "every checkable R gets a test" bullet with: at most one `kind: test` task per checkable R, at the lowest level that proves it (unit with a fake adapter before integration); e2e, smoke and browser-driven tasks only when `verification` asks for them, and only then "prefer headless scripts" applies.
- D6@1 (implements R9): `tests/test_skills.py` is run after the edits; `spectrace-plan` and `spectrace-start` stay under 200 lines.
- D7@1 (implements R10): `spectrace-start/SKILL.md` Phase 4 copies the verified `toolchain` test commands and the `verification` answer into `AGENTS.md` "Testing" for `software` projects; `templates.md` marks "Testing" as software-only and keeps its commands `TBD` until Phase 4 fills them.

## Trade-offs

| Decision | Pros | Cons | Mitigation |
|---|---|---|---|
| Policy lives in `AGENTS.md`, not in `trace.py` | No code or format change; any agent reads it | Not enforced, an agent can ignore it | R8 tripwire is reviewable in each task's report; `trace.py` stays out of scope |
| Three commands recorded at setup | Agent never guesses a flag (AGENTS.md rule) | Extra question; some toolchains lack "affected only" | Record "none" and fall back to the narrowest command |
| One test task per R, no numeric cap | Proportional, simple (KISS) | A weak R may be under-tested | Tripwire at 3× R items asks for a justification instead of forbidding |
| E2E only on request | Avoids hundreds of slow tests | A project may need one and not know | `verification` asks explicitly, so the omission is a choice |

Grounding (verified on the web): many small unit tests and very few end-to-end tests —
Vocke, "The Practical Test Pyramid" (martinfowler.com/articles/practical-test-pyramid.html);
affected-only runs — Jest `--findRelatedTests <files>` (jestjs.io CLI docs) and
`nx affected -t test` (nx.dev/ci/features/affected). Both tools document running the
full suite in CI, which matches the "full suite at session end" rule.

## Deliverables

- `skills/spectrace-start/references/question-bank.md`
- `skills/spectrace-start/references/templates.md`
- `skills/spectrace-start/assets/agents-protocol.md`
- `skills/spectrace-plan/SKILL.md`

## Sequencing

Question bank first (it defines the answers), then the template that records them, then the
protocol and plan skill that consume them, then the verification run.
