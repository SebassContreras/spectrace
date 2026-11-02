# 034 — project-overlay-and-safe-upgrade

## Goal

A repository can customize how spectrace works for it (for example where specs live, names, statuses, language) and still take every spectrace update without losing those customizations, with no project-specific case written into spectrace. Customizations live in one file that updates never overwrite; the skills obey it; the upgrade shows what it would change before changing it.

## Requirements

- R1: Project preferences live in a single file, `.spectrace/overlay.md`, that no spectrace update (skills install, `bin/spectrace-init.mjs` scaffold or upgrade) creates content in after its first empty scaffold, overwrites or deletes.
- R2: Every spectrace skill reads the overlay first when it exists and gives its rules precedence over the skill's own text; when it does not exist, behavior is identical to today.
- R3: `bin/spectrace-init.mjs --upgrade` changes nothing on disk unless `--apply` is passed; without it, it prints the planned changes (file, action) and exits 0.
- R4: When the upgrade must change a root contract the repository already edited, it keeps the repository's edits: only-upstream-changed applies, only-repository-changed is kept, both-changed on different lines merges, both-changed on the same lines stops with the conflict shown and nothing written for that file.
- R5: After `--apply`, the upgrade runs the checks listed in the overlay and reports each failed check; it never rolls back or edits on its own because of one.
- R6: The format of the overlay and the precedence rule are documented once, in `ARCHITECTURE.md`, and every other place only links to it.

## Design

- D1 (R1, R6): `.spectrace/overlay.md` is free Markdown with two optional sections: `## Rules` (one `###` heading per rule, written as an instruction to the agent) and `## Checks` (one line per rule: ``- <rule heading>: `<shell command>` ``, exit 0 means the rule still holds). The directory name keeps spectrace's footprint to one visible place. `--init` creates the file with the two headings and a comment, only when absent.
- D2 (R2): Each `SKILL.md` gets one fixed first step: "If `.spectrace/overlay.md` exists, read it; where a rule there and a step below disagree on the same matter, the overlay rule wins and you say so." No skill names any specific preference, so no project case enters spectrace.
- D3 (R3): `bin/spectrace-init.mjs` already has a `--dry-run` flag and `safeWrite`. Invert the default for `--upgrade`: dry-run unless `--apply`. The plan prints one line per file: `create`, `append`, `merge`, `conflict`, `unchanged`. `--dry-run` stays accepted as a synonym of the default; initialization of a repo that has no spectrace contracts (greenfield) is unchanged.
- D4 (R4): The CLI only owns root contracts, so only they are merged. The base of a contract is the template it was last scaffolded from, recorded in `.spectrace/base/<file>` the first time spectrace writes it (for a repository that predates this spec, the base is absent and the file is treated as "both may have changed": append-only, as `reconcilePrinciples()` already does). With a base, merge with `git merge-file -p` when `git` is on the path; without `git`, fall back to append-only and print a notice. (assumed: `git` is present wherever agents run; the fallback covers when it is not.)
- D5 (R5): After `--apply`, run each command of `## Checks` with a timeout and print `ok` or `FAIL: <rule heading>`; exit code 1 when any fails. Commands come from the repository's own file, so the CLI executes nothing the repository did not already hold.
- D6 (R2): Skills themselves are installed and overwritten by the external skills installer (`skills-lock.json`), not by this CLI; spectrace cannot merge them. The overlay is therefore the only protection for skill behavior; editing a `SKILL.md` by hand stays unsupported and `spectrace-review` reports a skill whose hash differs from the lock while no overlay rule explains it.

### Trade-offs & Mitigations (ENG-6)

- Choice: an overlay file vs. marked protected zones inside each `SKILL.md` vs. editing the skills and merging.
  - Pros: one file, one place to look, no change to how skills are installed; works for any preference of any project.
  - Cons: the agent must obey the precedence rule; a rule the skill text contradicts relies on judgement.
  - Mitigation: `## Checks` verifies the outcome instead of trusting obedience; skills with an unexplained hash difference are flagged by review.
- Choice: dry-run by default vs. apply by default.
  - Pros: no surprise writes in repositories with customizations.
  - Cons: one extra flag per upgrade.
  - Mitigation: the plan output ends with the exact `--apply` command.
- Choice: `git merge-file` vs. a hand-written merge.
  - Pros: standard, well-tested, no code to maintain (ENG-1, ENG-4: one interface, no abstraction for a single use).
  - Cons: depends on `git`.
  - Mitigation: append-only fallback already exists.

## Tasks

- [ ] 034/T001 [agent] Document the overlay format and precedence rule in `ARCHITECTURE.md` and record the decision in `CHANGES.md` — covers R1, R6, D1
- [ ] 034/T002 [agent] Add the fixed first step to the four `SKILL.md` files and a note in `spectrace-init` about the overlay — covers R2, D2
- [ ] 034/T003 [agent] Scaffold an empty `.spectrace/overlay.md` in init (only when absent) and never touch it in upgrade — covers R1, D1
- [ ] 034/T004 [agent] Make `--upgrade` dry-run by default with `--apply`, and print the per-file plan — covers R3, D3
- [ ] 034/T005 [agent] Record `.spectrace/base/<file>` when a contract is scaffolded and merge with `git merge-file` on upgrade, append-only fallback without `git` — covers R4, D4
- [ ] 034/T006 [agent] Run the overlay `## Checks` after `--apply` and report failures — covers R5, D5
- [ ] 034/T007 [agent] Add the skill-hash-without-overlay finding to `spectrace-review` — covers R2, D6
- [ ] 034/T008 Verify: assert 7 partitions — (a) no overlay: upgrade output and results match today's; (b) overlay present: the file is byte-identical after `--apply`, and init on a repo that has one leaves it alone; (c) upgrade without `--apply` leaves the tree byte-identical and lists the plan; (d) merge: only upstream changed, only repository changed, both changed different lines, both changed the same lines (file untouched, conflict printed); (e) contract with no recorded base falls back to append-only and is idempotent on a second run; (f) no `git` on the path falls back with a notice; (g) checks: one passing and one failing check give `ok` and `FAIL` and exit 1 — covers R1–R6
- [ ] 034/T009 [human] Try the upgrade on one real customized repository and confirm no customization was lost — covers R1–R5

## Changes

None yet.

## Original request

"escribe una spec para abordar estos casos en spectrace" — after: "aunque spectrace es mío no quiero poner esta casuística, dame otras soluciones que sean aptas a cualquier usuario y a cualquier proyecto para mantener spectrace actualizado pero con sus modificaciones o preferencias", and: "no directo a spectrace para que tenga en cuenta los overlay".
