# 034 — project-overlay-and-safe-upgrade

## Goal

A repository can customize how spectrace works for it (for example where specs live, names, statuses, language) and still take every spectrace update without losing those customizations, with no project-specific case written into spectrace. Customizations live in one file that updates never overwrite; the skills obey it; the upgrade shows what it would change before changing it.

## Requirements

- R1: Project preferences live in a single file, `.spectrace/overlay.md`, that `bin/spectrace-init.mjs` (scaffold or upgrade) creates content in only once, as an empty scaffold when the file is absent, and never overwrites or deletes afterwards. (The skills installer writes only skill folders; see D6.)
- R2: Every spectrace skill reads the overlay first when it exists and gives its rules precedence over the skill's own text; when it does not exist, behavior is identical to today.
- R3: In upgrade mode (`--upgrade`, or detected because `AGENTS.md` or `planning/` already exists), `bin/spectrace-init.mjs` changes nothing on disk unless `--apply` is passed; without it, it prints the planned changes (file, action) and exits 0.
- R4: When the upgrade must change a root contract the repository already edited and a recorded base exists for it, it keeps the repository's edits: only-upstream-changed applies, only-repository-changed is kept, both-changed on different lines merges, both-changed on the same lines stops with the conflict shown and nothing written for that file. Without a recorded base, the contract is handled as today (D4).
- R5: After `--apply`, the upgrade runs the checks listed in the overlay and reports each failed check; it never rolls back or edits on its own because of one.
- R6: The format of the overlay and the precedence rule are documented once, in `ARCHITECTURE.md` (and its starter template, so scaffolded repositories carry it); the skills carry only the fixed first step of D2, identical in each, and every other place only links.

## Design

- D1 (R1, R6): `.spectrace/overlay.md` is free Markdown with two optional sections: `## Rules` (one `###` heading per rule, written as an instruction to the agent) and `## Checks` (one line per rule: ``- <rule heading>: `<shell command>` ``, exit 0 means the rule still holds). The directory name keeps spectrace's footprint to one visible place. The scaffold step of `bin/spectrace-init.mjs` creates the file with the two headings and a comment, only when absent.
- D2 (R2, R6): Each `SKILL.md` gets one fixed first step, added as `## Step 0 — Read the project overlay` so existing step numbers and anchors do not change: "If `.spectrace/overlay.md` exists, read it; where a rule there and a step below disagree on the same matter, the overlay rule wins and you say so." The text is identical in all four skills. No skill names any specific preference, so no project case enters spectrace.
- D3 (R3): `bin/spectrace-init.mjs` already has a `--dry-run` flag and `safeWrite`. Invert the default for upgrade mode, however it is reached (explicit `--upgrade` or detected): dry-run unless `--apply`. The plan prints one line per write, including the `CHANGES.md` upgrade entry and `planning/specs/`: `create`, `append`, `merge`, `conflict`, `unchanged`, and ends with the exact `--apply` command. `--dry-run` stays accepted as a synonym of the default; initialization of a repo that has no spectrace contracts (greenfield) is unchanged.
- D4 (R4): The CLI only merges the seven root contracts; `.agentignore` and the overlay are not merged. The base of a contract is the template it was last scaffolded from (for `DESIGN.md`, the template its type selected), recorded in `.spectrace/base/<file>` the first time spectrace writes it and replaced with the new template after a successful `--apply` of that file. A repository that predates this spec has no base; its contracts are handled as today: `reconcileEngineering()` appends the principle sections `ENGINEERING.md` lacks, every other existing contract is preserved untouched. With a base, merge with `git merge-file -p <current> <base> <upstream>` when `git` is on the path (output on stdout, exit code 0 clean, N > 0 conflicts, negative on error; write the result only on 0). Without `git`, behave as with no base and print a notice. (assumed: `git` is present wherever agents run; the fallback covers when it is not.) Source: https://git-scm.com/docs/git-merge-file (accessed 2026-11-02).
- D5 (R5): After `--apply`, run each command of `## Checks` with a timeout and print `ok` or `FAIL: <rule heading>`; exit code 1 when any fails. Commands come from the repository's own file, so the CLI executes nothing the repository did not already hold.
- D6 (R1, R2): Skills themselves are installed and overwritten by the external skills installer, which records them in a project-level `skills-lock.json` with a `computedHash` per skill; spectrace cannot merge them. The overlay is therefore the only protection for skill behavior; editing a `SKILL.md` by hand stays unsupported, and `spectrace-review` reports a warning naming any skill whose hash differs from the lock. The installer is assumed not to touch `.spectrace/`; it manages skill folders and the lock only. Source: https://www.mintlify.com/vercel-labs/skills/advanced/lock-files (accessed 2026-11-02; community mirror of the vercel-labs/skills docs, hash algorithm not stated there).

### Trade-offs & Mitigations (ENG-6)

- Choice: an overlay file vs. marked protected zones inside each `SKILL.md` vs. editing the skills and merging.
  - Pros: one file, one place to look, no change to how skills are installed; works for any preference of any project.
  - Cons: the agent must obey the precedence rule; a rule the skill text contradicts relies on judgement.
  - Mitigation: `## Checks` verifies the outcome instead of trusting obedience; skills with a hash difference are flagged by review.
- Choice: dry-run by default vs. apply by default.
  - Pros: no surprise writes in repositories with customizations.
  - Cons: one extra flag per upgrade.
  - Mitigation: the plan output ends with the exact `--apply` command.
- Choice: `git merge-file` with a stored base vs. a hand-written merge vs. append-only everywhere.
  - Pros: standard, well-tested, no merge code to maintain (ENG-1, ENG-4: one interface, no abstraction for a single use).
  - Cons: depends on `git`; stores a copy of each scaffolded template under `.spectrace/base/`.
  - Mitigation: without `git` or without a base, contracts are handled as today (D4), which loses nothing.
- Choice: running the overlay's `## Checks` from the CLI vs. leaving them to the agent.
  - Pros: the outcome is verified by exit code, not by trust.
  - Cons: the CLI executes shell commands from a file in the repository, platform-dependent on shell syntax; a cloned repository's overlay runs with the user's rights on `--apply`.
  - Mitigation: only after an explicit `--apply`; the plan lists the commands that will run.

## Tasks

- [ ] 034/T001 [agent] Document the overlay format and precedence rule in `ARCHITECTURE.md` (including the directory map) and in `skills/spectrace-plan/assets/architecture-template.md`, and record the decision in `CHANGES.md` — covers R1, R6, D1
- [ ] 034/T002 [agent] Add the fixed `## Step 0 — Read the project overlay` of D2 to the four `SKILL.md` files and a note in `spectrace-init` about the overlay — covers R2, R6, D2
- [ ] 034/T003 [agent] Scaffold an empty `.spectrace/overlay.md` in the scaffold step (only when absent) and never touch it in upgrade — covers R1, D1
- [ ] 034/T004 [agent] Make upgrade mode (explicit or detected) dry-run unless `--apply`, and print the per-file plan with `create`, `append`, `unchanged`, the `CHANGES.md` entry and the final `--apply` command — covers R3, D3
- [ ] 034/T005 [agent] Record `.spectrace/base/<file>` when a contract is scaffolded and replace it after a successful `--apply` of that file — covers R4, D4
- [ ] 034/T006 [agent] Merge a contract that has a base with `git merge-file`, add `merge` and `conflict` to the plan, and fall back to today's handling plus a notice without `git` — covers R4, D3, D4
- [ ] 034/T007 [agent] Run the overlay `## Checks` after `--apply` and report failures — covers R5, D5
- [ ] 034/T008 [agent] Add the skill-hash-differs-from-lock warning to `spectrace-review`; first confirm from the installer's source how `computedHash` is computed, and if it cannot be reproduced with read-only tools, report the skill as "unverifiable against the lock" instead of guessing — covers R2, D6
- [ ] 034/T009 [agent] Verify: one table-driven suite (TEST-H2; the repo has no test runner, so Node's built-in `node:test`, no dependency) over temp copies of fixture repositories, one row per partition — (a) no overlay: upgrade output and results match today's; (b) overlay present: the file is byte-identical after `--apply`, and the scaffold on a repo that has one leaves it alone; (c) upgrade without `--apply`, both with `--upgrade` and detected from an existing `AGENTS.md`, leaves the tree byte-identical, lists the plan and exits 0; (d) merge with a recorded base: only upstream changed, only repository changed, both changed on different lines, both changed on the same lines (file untouched, conflict printed); (e) contract with no recorded base: `ENGINEERING.md` gets only its missing principles, the others stay untouched, and a second run changes nothing; (f) no `git` on the path falls back with a notice; (g) checks: one passing, one failing, one malformed line and an empty `## Checks` give `ok`, `FAIL`, a reported malformed line and no output, exit 1 only when a check fails; (h) the four `SKILL.md` carry the identical Step 0 and `ARCHITECTURE.md` is the only file defining the overlay format (contract suite, TEST-I2); (i) a skill with a hash different from the lock is warned about, one with no lock file is not — covers R1–R6, D1–D6
- [ ] 034/T010 [human] Try the upgrade on one real customized repository and confirm no customization was lost — covers R1–R5

## Changes

None yet.

## Original request

"escribe una spec para abordar estos casos en spectrace" — after: "aunque spectrace es mío no quiero poner esta casuística, dame otras soluciones que sean aptas a cualquier usuario y a cualquier proyecto para mantener spectrace actualizado pero con sus modificaciones o preferencias", and: "no directo a spectrace para que tenga en cuenta los overlay".
