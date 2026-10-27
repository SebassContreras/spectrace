# 027 — required-trailer

## Goal
Every code commit is traced or marked untraced on purpose: a commit without a `Spec:`
trailer is refused, not warned about, and a CI check catches commits that skipped the
hooks. Check: in lienzo, two agent commits on 2026-10-27 (`17ba32e`, `9292fd4`) went
in without a trailer after a warning; with this spec both would have been refused.

## Requirements
- R1: `commit-msg` refuses a commit with changes outside `planning/` and the spectrace
  install and no `Spec:` trailer; `Spec: none` still lets an untraced change through on
  purpose. A merge commit is not judged: its changes were judged on their own commits.
- R2: A CI check refuses a pushed range or pull request holding such a commit, so
  `--no-verify` or a clone without `core.hooksPath` doesn't get one through unseen.
- R3: The install path list still lives once, in `commit-msg`.

## Design
- D1 (R1): The no-trailer branch of `commit-msg` exits 1 instead of 0; a commit with
  `MERGE_HEAD` present is accepted untouched. Replaces the warning in 022/D1.
  Trade-off: `git revert` and other generated messages now need `Spec:` added by hand;
  the refusal message says how.
- D2 (R2, R3): `check-trailers <base> <head>`, POSIX sh next to the hooks, walks the
  non-merge commits of `base..head` (only `head` when `base` is empty or all zeros)
  and applies the same rule to each commit's own diff. It reads `install_re` from
  `.githooks/commit-msg` instead of repeating it. Trade-off: a pushed branch is only
  checked from the commit it was at before; history before the install is never judged.
- D3 (R2): `assets/ci/spectrace.yml`, a GitHub Actions workflow that runs
  `check-trailers` on push and pull request; `spectrace-plan` installs it to
  `.github/workflows/` when the remote is GitHub. That path joins `install_re`.

## Tasks
- [x] 027/T001 [agent] `commit-msg` refuses code commits without a trailer, merges exempt; tests — covers D1, R1; replaces 022/D1 warning
- [x] 027/T002 [agent] `check-trailers` and the CI workflow asset; tests — covers D2, D3, R2, R3
- [x] 027/T003 [agent] `spectrace-plan` installs `check-trailers` and the workflow; installed in this repo — covers D3
- [x] 027/T004 [agent] Docs: README (closing tasks, limits), agents block and its copy, `product.md` — covers D1, D2, D3
- [ ] 027/T005 [agent] Verify: suite passes; the 026 hooks fail the new tests — covers R1, R2
