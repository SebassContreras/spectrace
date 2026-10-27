# 022 — git-hooks

## Goal

The two things agents forgot or skipped in the 021 trial are enforced by git, not by
memory: the roadmap status, and the review after a change of direction. Check: a commit
whose `Spec:` task isn't ticked is refused; the roadmap status changes by itself.

## Requirements

- R1: The roadmap `Status` is never written by hand; it follows the `[agent]`
  checkboxes.
- R2: A commit with a `Spec: NNN/TNNN` trailer is refused unless that task is ticked.
- R3: After a change of direction, nothing that still follows the old way can be closed
  silently.

## Design

- D1 (R1, R2): Two POSIX sh hooks in `skills/spectrace-plan/assets/hooks/`, installed
  to `.githooks/` with `core.hooksPath`: `pre-commit` writes `Status` into the staged
  roadmap; `commit-msg` checks the trailer's task is `[x]` and warns on code commits
  without a trailer. Git and awk only.
- D2 (R3): `spectrace-change` turns the reason for a change into a requirement with a
  test, lists the old approach's assumptions to search for, and ends with a
  `Review:` task that the `pre-commit` hook refuses to close without a `reviewed:`
  note.

## Tasks

- [x] 022/T001 [agent] Write `pre-commit` and `commit-msg` hooks and try them in a scratch repo — covers D1
- [x] 022/T002 [agent] Install hooks from `spectrace-plan`; protocol block drops manual status — covers D1, R1
- [x] 022/T003 [agent] `spectrace-change`: assumptions list, reason → requirement + test, final Review task — covers D2
- [x] 022/T004 [agent] Install the hooks in this repo and document them in the README — covers D1
- [x] 022/T005 [agent] Re-run the scratch trial (plan → execute → change → execute) with hooks on — covers R1, R2, R3
- [x] 022/T006 [agent] `commit-msg` refuses a ticked `[agent]` task with no work outside `planning/`; a `Review:` runs in a fresh agent when possible (`reviewed (self):` otherwise) — covers R2, R3
- [x] 022/T007 [agent] README.md: quick start, hooks in the plan row, trailer placement, note for old-version users — covers D1, D2

## Changes

- 2026-10-26: Trial 2 (`bkm`, 4 specs, 23 commits, 27 tests): Status never typed by an
  agent; no hook refusal needed. The assumptions list found whole-collection loads,
  in-memory ids/filters and a raw-bytes test that no grep for "json" shows, plus an
  `AUTOINCREMENT` trap in the new design. The Review task found a real regression
  (`rm` with a huge id crashed) and added a task for it. Gaps it exposed: a commit that
  only ticked the box, and a review by the code's own author — fixed by T006.
