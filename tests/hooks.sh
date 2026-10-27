#!/bin/sh
# Behavior tests for the spectrace git hooks in skills/spectrace-plan/assets/hooks/.
# Each test builds a throwaway repo, makes one commit and checks that it is accepted
# or refused. Run: sh tests/hooks.sh   (HOOKS=<dir> tests another copy of the hooks)
#
# New commits get author dates a minute apart, so the commit-msg hook never takes a
# new commit for an amend of HEAD.

root=$(cd "$(dirname "$0")/.." && pwd)
hooks=${HOOKS:-$root/skills/spectrace-plan/assets/hooks}
spec=planning/specs/001-x.md
clock=1800000000
failed=0

commit() {
  clock=$((clock + 60))
  GIT_AUTHOR_DATE="@$clock +0000" GIT_COMMITTER_DATE="@$clock +0000" \
    git commit -q -m "$1" >/dev/null 2>&1
}
amend() { git commit -q --amend -m "$1" >/dev/null 2>&1; }

new_repo() {
  cd "$(mktemp -d)" || exit 1
  git init -q && git config user.email t@t && git config user.name t
  git config core.autocrlf false
  mkdir -p .githooks planning/specs && cp "$hooks"/* .githooks/
  git config core.hooksPath .githooks
  printf '# Project\n\nConventions.\n\n<!-- spectrace -->\nBlock.\n<!-- /spectrace -->\n' > AGENTS.md
  printf '| ID | Spec | Status | Depends on |\n|---|---|---|---|\n| 001 | x | todo | — |\n' > planning/roadmap.md
  printf '%s\n' '## Tasks' \
    '- [ ] 001/T001 [agent] Code — covers R1' \
    '- [ ] 001/T002 [agent] Verify: build — covers R1' \
    '- [ ] 001/T003 [agent] Review: code — covers R1' > "$spec"
  git add -A && commit init
}
edit() { sed "$1" "$2" > "$2.tmp" && mv "$2.tmp" "$2"; }
tick() { edit "s|^- \[ \] 001/$1 |- [x] 001/$1 |" "$spec"; }
note() { edit "/ 001\/$1 /a\\
      $2" "$spec"; }
trailer() { printf 'work\n\nSpec: %s' "$1"; }

expect_accepted() { if [ "$2" -eq 0 ]; then echo "ok   $1"; else echo "FAIL $1"; failed=1; fi; }
expect_refused() { if [ "$2" -ne 0 ]; then echo "ok   $1"; else echo "FAIL $1"; failed=1; fi; }

task_with_code_is_accepted() {
  new_repo; tick T001; echo x > a.txt; git add -A
  commit "$(trailer 001/T001)"; expect_accepted task_with_code_is_accepted $?
}
task_with_only_planning_is_refused() {
  new_repo; tick T001; git add -A
  commit "$(trailer 001/T001)"; expect_refused task_with_only_planning_is_refused $?
}
trailer_for_unticked_task_is_refused() {
  new_repo; echo x > a.txt; git add -A
  commit "$(trailer 001/T001)"; expect_refused trailer_for_unticked_task_is_refused $?
}
agents_md_conventions_change_is_work() {
  new_repo; tick T001; edit 's/^Conventions\.$/Conventions, updated./' AGENTS.md; git add -A
  commit "$(trailer 001/T001)"; expect_accepted agents_md_conventions_change_is_work $?
}
agents_md_block_only_change_is_not_work() {
  new_repo; tick T001; edit 's/^Block\.$/Block, reinstalled./' AGENTS.md; git add -A
  commit "$(trailer 001/T001)"; expect_refused agents_md_block_only_change_is_not_work $?
}
agents_md_lines_after_unclosed_block_are_work() {
  new_repo; tick T001; edit '/^<!-- \/spectrace -->$/d' AGENTS.md; git add -A; commit "$(trailer none)"
  echo 'Later convention.' >> AGENTS.md; git add -A
  commit "$(trailer 001/T001)"; expect_accepted agents_md_lines_after_unclosed_block_are_work $?
}
verify_without_note_is_refused() {
  new_repo; tick T002; git add -A
  commit "$(trailer 001/T002)"; expect_refused verify_without_note_is_refused $?
}
verify_with_note_needs_no_work() {
  new_repo; tick T002; note T002 'verified: make build — found nothing'; git add -A
  commit "$(trailer 001/T002)"; expect_accepted verify_with_note_needs_no_work $?
}
verify_with_reviewed_note_is_refused() {
  new_repo; tick T002; note T002 'reviewed: a.txt — found nothing'; git add -A
  commit "$(trailer 001/T002)"; expect_refused verify_with_reviewed_note_is_refused $?
}
review_without_note_is_refused() {
  new_repo; tick T003; git add -A
  commit "$(trailer 001/T003)"; expect_refused review_without_note_is_refused $?
}
amend_that_ticks_task_counts_amended_work() {
  new_repo; echo x > a.txt; git add -A; commit "$(trailer none)"
  tick T001; git add -A
  amend "$(trailer 001/T001)"; expect_accepted amend_that_ticks_task_counts_amended_work $?
}
new_commit_for_closed_task_does_not_count_previous_work() {
  new_repo; tick T001; echo x > a.txt; git add -A; commit "$(trailer 001/T001)"
  echo 'More notes.' >> "$spec"; git add -A
  commit "$(trailer 001/T001)"; expect_refused new_commit_for_closed_task_does_not_count_previous_work $?
}
roadmap_status_follows_agent_checkboxes() {
  new_repo; tick T001; echo x > a.txt; git add -A; commit "$(trailer 001/T001)"
  grep -q '^| 001 | x | in progress' planning/roadmap.md
  expect_accepted roadmap_status_follows_agent_checkboxes $?
}
installed_hooks_match_assets() {
  diff -r "$root/skills/spectrace-plan/assets/hooks" "$root/.githooks" >/dev/null
  expect_accepted installed_hooks_match_assets $?
}

task_with_code_is_accepted
task_with_only_planning_is_refused
trailer_for_unticked_task_is_refused
agents_md_conventions_change_is_work
agents_md_block_only_change_is_not_work
agents_md_lines_after_unclosed_block_are_work
verify_without_note_is_refused
verify_with_note_needs_no_work
verify_with_reviewed_note_is_refused
review_without_note_is_refused
amend_that_ticks_task_counts_amended_work
new_commit_for_closed_task_does_not_count_previous_work
roadmap_status_follows_agent_checkboxes
installed_hooks_match_assets
exit $failed
