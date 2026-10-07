# End-to-end scenario

The fixed script for spec 006: every run, on every harness, plays exactly this. The
driver is the agent running spec 006; it plays the user. The harness under test only
ever sees the prompts and answers below, the target repo's `AGENTS.md` and the
installed skills.

## The throwaway project

`tdo`: a to-do list command-line tool in Python, standard library only. Two specs —
`storage` (a small module that keeps the tasks) and `cli` (the commands). Only
`storage` is planned and built; `cli` exists so the roadmap has two specs.

The decision the run retires and later reinstates is `storage`'s design item
**"tasks are stored in a JSON file, `tdo.json`, in the current directory"**. Its
identifiers, used by the `git grep` checks: `tdo.json`, `import json`, `json.load`,
`json.dump`.

## Driving a harness

| | Claude Code | agy |
|---|---|---|
| First turn | `claude -p "<prompt>" --dangerously-skip-permissions --output-format json` | `agy -p "<prompt>" --dangerously-skip-permissions` |
| Next turn | same, plus `--resume <session_id>` | same, plus `--conversation <id>` |

- Run from the throwaway repo's root. The conversation ID comes from the first turn's
  output; how agy exposes it is verified at the start of its run (006/T007), not
  guessed.
- One conversation per step below; a new step starts a new conversation.
- The driver answers each question with the row of the matching table. A question no
  row answers is answered consistently with the scenario and logged as a **gap** in
  `e2e/report.md`. A question the scenario has already answered is answered again the
  same way and logged as a **repeat**.
- The driver never edits files the harness owns, except where a step says so.

## Step 0 — Set up (driver)

1. Create `%TEMP%/spectrace-e2e/<harness>/` (fresh: delete it first if it exists) and
   `git init` it.
2. Install the skills from the published repository, project scope, for the harness
   under test: `pnpm dlx skills add SebassContreras/spectrace` with the agent and
   non-interactive flags that `skills add --help` lists (verified at run time).
3. Commit: `chore: install spectrace skills`.

## Step 1 — Interview

Prompt:

> Use the spectrace-start skill. I want to build a small to-do list command-line tool in Python.

| Dimension | Answer |
|---|---|
| git | Already a git repo. |
| `idea-detail` | A personal to-do list I use from the terminal. I add a task with a title, list my tasks with their ids, and mark one done by id. Tasks are kept in the folder I run it in, so each project has its own list. No accounts, no network. |
| `project-type` | Software — a CLI. |
| `goal` | Yes (accept the drafted goal if it says: a terminal to-do list for one person, kept per folder). Otherwise: "A terminal to-do list for one person, kept per folder." |
| `audience` | Me, a developer working in the terminal. |
| `mvp` | Add, list and complete tasks. Not in it: editing, deleting, due dates, priorities, colors. |
| `done-when` | I can add, list and complete tasks from the terminal and the list survives between runs. |
| `constraints-hard` | Python 3.9+, standard library only. |
| `stakeholders` | Nobody else. |
| `automatability` | An agent can do all of it. |
| `runtime` | Python 3.9+. |
| `framework` | None — standard library only, `argparse` for the CLI. No third-party packages. |
| `toolchain` | No package manager. Tests: `python -m unittest discover -s tests`. No formatter or linter. |
| `datastore` | Decided in the storage spec's design. |
| `data-model` | One entity, a task: integer id, title, done flag. |
| `interface` | CLI: `tdo add "<title>"`, `tdo list`, `tdo done <id>`. |
| `identity` | None, single user. |
| `hosting` | Runs locally; no distribution. |
| `ci` | The unit tests pass. |
| `env-secrets` | None. |
| `verification` | Unit tests with `unittest`. |
| `third-party` | None. |
| `observability` | None — it's a local tool. |
| `helper-skills` | None. |
| `agent-rules` | None. |
| `visual-surface` | No. |
| `tone` | Plain English. |
| `code-conventions` | PEP 8, type hints on public functions. |
| `anti-preferences` | None. |
| `preference-strength` | Hard rules. |
| Roadmap | Two specs, in this order: `storage` (the module that keeps the tasks) and `cli` (the three commands). Both in the MVP. `cli` depends on `storage`. Yes, record the order as Priority. |
| Requirements mode | Here, one question at a time. |
| Continue to the next spec? | Yes. |
| `handoff.md` | No. |
| Any sweep ("anything else?", "what haven't we covered?") | Nothing else. |

Requirements, spec `storage`:

| Dimension | Answer |
|---|---|
| `what` | A module that adds, lists and completes tasks and keeps them between runs. |
| `serves` | The `cli` spec. |
| `requirements` | (1) Adding a task stores its title and returns a new id, one higher than the highest so far; the first is 1. (2) Listing returns every task in id order with its id, title and whether it's done. (3) Completing a task by id marks it done; an unknown id raises an error. (4) Tasks persist between runs in the current directory. (5) A title longer than 80 characters is rejected. |
| `out-of-scope` | Editing and deleting tasks. |
| `dependencies` | None. |
| `owner-split` | An agent does it all. |

Requirements, spec `cli`:

| Dimension | Answer |
|---|---|
| `what` | The `tdo` command with `add`, `list` and `done`. |
| `serves` | Me, in the terminal. |
| `requirements` | (1) `tdo add "<title>"` prints the new id. (2) `tdo list` prints one line per task: id, `[x]` or `[ ]`, title. (3) `tdo done <id>` marks it done. (4) Any error prints a message to stderr and exits with status 1. |
| `out-of-scope` | Shell completion, colors. |
| `dependencies` | `storage`. |
| `owner-split` | An agent does it all. |

## Step 2 — Plan `storage`

Prompt:

> Use the spectrace-plan skill on spec 001.

| Question | Answer |
|---|---|
| Q&A or draft | Here, one question at a time. |
| Approach | Tasks are stored in a JSON file, `tdo.json`, in the current directory, read and rewritten whole on every change with the `json` module. The module is `tdo/store.py` with three functions: `add(title) -> int`, `list_tasks() -> list`, `complete(task_id) -> None`. |
| Deliverables | `tdo/__init__.py`, `tdo/store.py`, `tests/test_store.py`. |
| Sequencing | None. |
| Decisions settled | None beyond what's recorded. |
| Open questions | None. |
| An R not covered | Covered by the approach: the store module implements it. |
| "What haven't we covered?" / "Anything no task covers?" | Nothing. |
| The task list | Approve as proposed. |

Then the driver commits: `chore: scaffold and plan`. **No commit from here to the end
of the run.**

## Step 3 — Execute three tasks

Three times, each a new conversation:

> Execute the next spectrace task. Don't commit.

## Step 4 — Retire the JSON decision

Prompt:

> Use the spectrace-change skill. We're moving storage from the JSON file to SQLite: the standard library's `sqlite3`, file `tdo.db` in the current directory. Why: two terminals writing at once corrupt the JSON file.

| Question | Answer |
|---|---|
| The proposed edits | Yes, if the JSON design item is retired → a new item for SQLite, and nothing else changes meaning. Otherwise explain that and ask for that edit. |
| Do the R items still hold? | Yes, all of them. |
| Each finished task in the manifest | The default (redo) for code; delete-and-rewrite for tests of the storage code that read the JSON file directly; still valid for anything the change doesn't touch. |
| Stale mentions found by the sweep | Fix them as proposed. |
| The task list | Approve as proposed. |

Then, each a new conversation, until `trace check --strict` exits 0:

> Execute the next spectrace task. Don't commit.

## Step 5 — Reinstate the JSON decision

Prompt:

> Use the spectrace-change skill. Go back to the JSON file storage we had before SQLite. Why: I want to read and hand-edit my list, and that matters more than two terminals writing at once.

| Question | Answer |
|---|---|
| The proposed edits | Yes, if the SQLite item is retired and the JSON statement comes back as a new item. |
| Do the R items still hold? | Yes, all of them. |
| Tasks | Restore through `trace restore` where it applies; redo (remove) the SQLite code. Approve as proposed. |

Then, each a new conversation, until `trace check --strict` exits 0:

> Execute the next spectrace task. Don't commit.

If spec 001 still has tasks left, keep going until `trace status` shows it `done`, so
every R item in it is built on before step 6.

## Step 6 — Wording edit, then meaning edit

1. The driver rewords `storage`'s title-length item by hand, keeping its ID and
   revision: "A title longer than 80 characters is rejected." → "Titles over 80
   characters are rejected."
2. Prompt, new conversation:

   > Use the spectrace-change skill. I reworded the title-length requirement of spec 001 by hand; the meaning is the same.

   Answer "yes" to confirming the meaning is unchanged.
3. Prompt, new conversation:

   > Use the spectrace-change skill. Titles may now be up to 120 characters, not 80 (spec 001). Why: 80 cuts off real task titles.

   | Question | Answer |
   |---|---|
   | The proposed edits | Yes, if the item's revision goes up. |
   | Each finished task | Redo the length check; the tests that check it are rewritten. Approve as proposed. |

4. Each a new conversation, until `trace check --strict` exits 0:

   > Execute the next spectrace task. Don't commit.

## Verification

Run by the driver, in Git Bash, from the throwaway repo's root. `trace` is
`python .spectrace/trace.py`. Every command, its exit code and the relevant output go
into `e2e/report.md`.

### Snapshots (D5)

A snapshot is the tree of the whole working tree, `.gitignore` honored, taken without
touching the real index. The driver takes one right before and right after every
harness conversation, so it sees everything the harness did — including edits made
outside `trace start`/`done`:

```bash
snap() {  # prints a tree id; $1 names it in snaps.txt
  idx="$(git rev-parse --absolute-git-dir)/e2e-index"
  rm -f "$idx"
  GIT_INDEX_FILE="$idx" git add -A && t=$(GIT_INDEX_FILE="$idx" git write-tree)
  rm -f "$idx"
  echo "$1 $t" >> "$TMPDIR/snaps-<harness>.txt"; echo "$t"
}
```

The index starts empty, so the tree holds every file, tracked or not. `snaps.txt`
lives outside the throwaway repo.

### Exact changes (R1)

For each task conversation, with `$B`/`$A` its before/after snapshots and `NNN-TNNN`
the task the harness reports having run:

```bash
diff <(git diff --no-color --no-ext-diff -M "$B" "$A" -- . ':(exclude)planning' ':(exclude).spectrace') \
     .spectrace/changes/NNN-TNNN.patch && echo EXACT
git diff --numstat -M "$B" "$A" -- . ':(exclude)planning' ':(exclude).spectrace'
```

Pass: `EXACT` for every task (a task with no file changes has no patch and
`changes: none`, and the diff is empty), the numstat matches the task's `changes:`
line, and exactly one task went from `todo` to `done` in that conversation. Also check
`git log` still shows only the step 0 and step 2 commits.

### Retire (R2)

1. Right after step 3: snapshot `pre-change`, and record `trace impact 001/D<n>` for
   the JSON item.
2. Manifest check: for each task `impact` lists, its files and line counts must match
   that task's recorded patch and what is still in the tree; no file in the tree that
   uses an identifier of the JSON decision may be missing from it:
   `git grep --untracked -n -e 'tdo\.json' -e 'import json' -e 'json\.load' -e 'json\.dump' -- . ':(exclude)planning' ':(exclude).spectrace' ':(exclude)*.pyc' ':(exclude).claude' ':(exclude).agents'`
   (`--untracked`: nothing is committed during the run, so the code is untracked;
   the installed skills are excluded — `trace.py` itself imports `json`.)
3. After the change conversation, before any cleanup task: `trace check --strict` →
   exit 1, with a pending `suspect` for every finished task that covered the JSON item.
4. After each cleanup task: `trace check --strict` and record the exit code. Pass: 1
   until the last cleanup task is done, then 0.
5. Then the `git grep` of step 2 finds nothing outside history, and
   `git grep --untracked -n -e sqlite3 -e 'tdo\.db' -- . ':(exclude)planning' ':(exclude).spectrace' ':(exclude)*.pyc' ':(exclude).claude' ':(exclude).agents'`
   finds the new code.

### Restore (R4)

1. Before the reinstate conversation: snapshot `pre-reinstate`.
2. For each restoring task: its conversation transcript shows `trace restore
   001/TNNN` run after `trace start`, and its `changes:` lists the restored files.
3. After the last task: snapshot `post-reinstate`, then
   `git diff --stat pre-change post-reinstate -- . ':(exclude)planning' ':(exclude).spectrace'`.
   Pass: empty (the code is back exactly as it was), the `git grep` for `sqlite3` and
   `tdo.db` finds nothing outside history, and `trace check --strict` exits 0.

### Wording vs. meaning (R5)

1. After the hand edit: `trace check` reports the title-length item as `changed`
   (pending), and the item's `@N` is unchanged.
2. After the wording conversation: the transcript shows `trace review 001/R<n>`;
   `trace check --strict` exits 0; the revision is still `@N`; `changes.md` has a
   wording-fix entry.
3. After the meaning conversation: the item reads `@N+1`; `trace check --strict` exits
   1 with a `suspect` for each finished task that covered `@N`; `changes.md` records
   `MODIFIED R<n>@N → R<n>@N+1`.
4. After the cleanup tasks: `trace check --strict` exits 0.
