# 002 — start — Design

## Approach

- D1@1 (implements R1): The interview contract and question bank are ported from specloop's `start`: one question at a time, a resumable ledger (`.spectrace/interview.md`, `| dimension | status | answer |`), recorded skips, the help-me-decide protocol and the closing sweep. Loop-only dimensions (`worker-cli`) are dropped; the per-spec phase asks for R items.
- D2@1 (implements R2): Every file `spectrace-start` writes has its shape in `references/templates.md` — `product.md`, `architecture.md` (headers keyed to project type, decisions as A items), `roadmap.md`, `requirements.md` (context sections plus `## Requirements` with R items).
- D3@1 (implements R3): Draft mode is specloop `advance` Phase 0.5: derived from the ledger and sibling specs; any line the user didn't give is marked `_(standard: <name> — <url>)_` or `_(judgement, no standard)_`; the full draft is shown for yes / changes / defer.
- D4@1 (implements R4): `assets/trace.py` and `assets/format.md` are copied into `.spectrace/`; if a copy exists with a lower `VERSION`, the user is asked before replacing it.
- D5@1 (implements R5): `assets/agents-protocol.md` is written into `AGENTS.md` between the protocol markers, replacing an existing block and leaving everything else untouched; `AGENTS.md` sections: Project, Doc map, Stack & conventions, Style, Rules for agents.
- D6@1 (implements R6): No `.git` → ask, then `git init`.
- D7@1 (implements R7): After any roadmap edit, `trace status --write`; the skill ends with `trace check`.

## Deliverables

- `skills/spectrace-start/SKILL.md`
- `skills/spectrace-start/references/{question-bank,templates,handoff}.md`
- `skills/spectrace-start/assets/agents-protocol.md`
- `tests/test_skills.py` — structural check for every skill
