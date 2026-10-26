<!-- spectrace -->
## Planning

Work is planned in `planning/`:

```
planning/product.md      what this is, who it's for, stack, how to run and test, docs
planning/roadmap.md      specs in order, their status, and a free "Ideas" list
planning/NNN-name.md     one file per spec
```

A spec file:

```markdown
# 003 — login

## Goal
What should work when this spec is done, and how we'll know.

## Requirements
- R1: A user signs in with email and password.

## Design
- ~~D1 (R1): Sessions live in localStorage.~~ → D2
- D2 (R1): Sessions live in an httpOnly cookie.

## Tasks
- [x] 003/T001 [agent] Login form — covers R1
- [ ] 003/T002 [agent] Session cookie middleware — covers D2
- [ ] 003/T003 [agent] Remove the localStorage session code — replaces D1
- [ ] 003/T004 [human] Create the mail provider account — covers R1
      blocked: waiting for billing approval

## Changes
- 2026-10-12: D1 → D2. Why: localStorage is readable by any script. Work: T003.
```

- `R`/`D` labels are never reused; a replaced item stays, struck through, with `→`.
- A task ends with `— covers` and the R or D items it implements, comma-separated
  (`covers R2, D3`); a cleanup task ends with `— replaces D1` (or
  `— covers D3; replaces D1`). Items of another spec are written `006/D1`, both
  after `→` and in `covers`/`replaces`.
- `[agent]`: any agent does it. `[human]`: the user does it; agents report and skip it.
- `## Changes` appears with the first change.
- **Docs are deliverables.** `product.md` → `## Docs` lists the docs the project keeps
  and what each describes. A doc changes inside the task whose work it describes, so
  `git blame` on any doc line leads to a commit, its `Spec:` and the decision behind it.
- A task whose text starts with `Review:` is closed only with an indented
  `reviewed: <files read> — found <what>` line under it. Anything it finds becomes a
  new task placed before it.
- Roadmap table: `| ID | Spec | Status | Depends on |`. `Spec` is the name after
  `NNN-`; `Depends on` is `—` or spec IDs separated by commas. `Status` (`todo`,
  `in progress`, `done`) is written by the git hook from the `[agent]` checkboxes —
  never by hand.

## Working on tasks

Git hooks in `.githooks/` keep this honest: they write the roadmap `Status`, refuse a
commit whose `Spec:` task isn't ticked or that ticks an `[agent]` task without any work
outside `planning/`, and refuse a ticked `Review:` task without its `reviewed:` note.
Never bypass them (`--no-verify`); when one refuses, fix what it says.

1. `git pull` and `git status`. If `git config core.hooksPath` isn't `.githooks`, run
   `git config core.hooksPath .githooks`; if `.githooks/` itself is missing, tell the
   user to run the `spectrace-plan` skill, which reinstalls it. Uncommitted changes in
   `planning/`,
   `AGENTS.md`, `.githooks/` or `.gitattributes` (fresh specs, a spectrace install) →
   commit them first as `docs(planning): <what>`. Leave other untracked files
   alone. Open `planning/roadmap.md` and take the first `[ ]` `[agent]` task of the
   first spec not `done` whose dependencies are done (or the task you were asked for).
2. Read the spec. Do only that task, then verify it: run the project's tests, or run
   the thing itself when there are no tests yet.
3. **Close it with one commit**: the change, the task's `[x]`, and a trailer. Stage
   the files you touched by name, never `git add -A`.

   ```
   feat(login): session cookie middleware

   Spec: 003/T002
   ```

   The `Spec:` line goes in the message's last paragraph, together with any other
   trailer (`Co-Authored-By:`…) and no blank line between them — git only reads that
   paragraph as trailers. A change that belongs to no spec on purpose (a typo, a
   chore) carries `Spec: none` instead.

   Two small tasks that only make sense together (a function and its test) may share a
   commit with one `Spec:` line each. A task is closed only when that commit exists —
   never leave a ticked box uncommitted or a commit without its trailer.
4. **A `Review:` task** needs eyes that didn't write the code: hand it to a fresh
   agent (a subagent given only the task text and the spec) when your harness can;
   otherwise do it yourself and write `reviewed (self):`. Read the files, don't skim.
5. Stuck: add `blocked: <reason>` under the task, commit it, tell the user, move on.
6. **A convention or decision in the way** — or two items of a spec that contradict
   each other: these files describe the current state, not laws. Don't work around one
   and don't pick a side silently. Propose the simplest change to the user (the
   `spectrace-change` skill applies it). If the user isn't there to answer, mark the
   task `blocked: conflicts D2: <why>; propose: <change>`, commit, and move on.
7. **A new idea or a bug found mid-task**: add a line to the roadmap's `## Ideas` (or
   a task to the right spec) and keep going. Nothing is out of scope; it's just later.

What a spec built: `git log --grep "Spec: 003/" --stat`.
<!-- /spectrace -->
