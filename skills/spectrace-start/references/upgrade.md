# Upgrading an existing install

Read this from Phase 0 when the project already has `.spectrace/`. It brings what
spectrace copied into the repo up to the skill's bundled files. Paths under `assets/`
and `references/` are relative to this skill's folder; the bundled files are always the
reference, never the repo's own `.spectrace/trace.py`. Use `python3` (`python` on Windows).

## Check

Run the four probes. Each is one command with an exact result — never compare by eye.

| Probe | Command | Outdated when |
|---|---|---|
| (a) trace | `python3 .spectrace/trace.py --version` and `python3 assets/trace.py --version` | the repo's number is lower |
| (b) format | `git diff --no-index --stat .spectrace/format.md assets/format.md` | the output is not empty |
| (c) protocol | `python3 -c "import re,sys;t=open('AGENTS.md',encoding='utf-8').read();m=re.search(r'<!-- spectrace:protocol -->.*?<!-- /spectrace:protocol -->\n?',t,re.S);open(sys.argv[1],'w',encoding='utf-8').write(m.group(0) if m else '')" .spectrace/protocol.tmp`, then `git diff --no-index --stat .spectrace/protocol.tmp assets/agents-protocol.md`; delete `.spectrace/protocol.tmp` after | the output is not empty, or the markers are missing (empty file) |
| (d) sections | list the `## ` headings inside the `AGENTS.md` block of `references/templates.md` and the `## ` headings of the repo's `AGENTS.md` | a template heading is absent from the repo |

For (d), skip "Testing" unless `project-type` is `software` (from
`.spectrace/interview.md`, else the `Type:` line at the top of `AGENTS.md`). The
protocol block is probe (c)'s job, not a section.

A missing `.spectrace/trace.py`, `.spectrace/spectrace/` or `.spectrace/format.md` counts as outdated.

No probe outdated → say nothing and return to the caller.

## Summary and confirmation

Before writing anything, print one summary of every outdated probe:

- trace: `<repo VERSION> → <bundled VERSION>`, and the `format.md` diff stat from (b);
- protocol: the full `git diff --no-index` of the two texts from (c);
- sections: the names of the missing headings from (d).

Then ask, one item at a time, **yes** or **skip**: trace + format as one item, the
protocol, and each missing section. A skipped item is not written and is listed as
skipped in the report.

## Writes

- **Trace + format.** Copy `assets/trace.py` and `assets/format.md` over
  `.spectrace/trace.py` and `.spectrace/format.md`, and replace the package as one unit:
  copy `assets/spectrace/` (without `__pycache__`) to `.spectrace/spectrace.new/`, delete
  `.spectrace/spectrace/`, then rename `spectrace.new` to `spectrace`, so a module a later
  version dropped does not linger and a failed copy leaves the old package intact.
- **Protocol.** Write `assets/agents-protocol.md` into `AGENTS.md`, replacing the text
  between `<!-- spectrace:protocol -->` and `<!-- /spectrace:protocol -->` (markers
  included) if present, appending it at the end otherwise. Then run `git diff AGENTS.md`:
  no line outside the block may change; if one did, restore it.
- **Missing section.** Insert it with its template text, after the last template
  heading that precedes it and is present in the file, else right before the protocol
  block. Never touch an existing section. When its template has placeholders, ask only
  the question-bank dimensions that feed it and follow the phase that normally fills
  it — for "Testing", Phase 4: `toolchain` (each of the three test commands run once
  to confirm the toolchain accepts it, `none` for a mode the runner lacks) and
  `verification`; an unanswered command is `TBD`, never a `<cmd>` placeholder. Record
  each answer in `.spectrace/interview.md`.

## Scope and gate

- Writes only `.spectrace/trace.py`, `.spectrace/spectrace/`, `.spectrace/format.md`, `.spectrace/interview.md`
  and `AGENTS.md`. Never `planning/`: no spec, item, task or roadmap row.
- Run `python3 .spectrace/trace.py check` before the first write and again after the
  last. If the first passed and the second fails, print its output and say the upgrade
  caused it. Never revert silently and never edit `planning/` to make it pass.
- Report: what was written, what was skipped, and both `check` results.

Known limit: (d) compares headings only, so a rule added later inside an existing
section is not offered. Compare that section with the template by hand if needed.
