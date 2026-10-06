"""Tests for skills/spectrace-start/assets/trace.py. Run: python -m unittest discover -s tests"""
import contextlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get("SPECTRACE_ASSETS") or os.path.join(HERE, "..", "skills", "spectrace-start", "assets")
spec = importlib.util.spec_from_file_location("spectrace_trace", os.path.join(ASSETS, "trace.py"))
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)

GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")

ROADMAP = """# Roadmap

| ID  | Spec | Status | Depends on | Stage | Priority |
|-----|------|--------|------------|-------|----------|
| 001 | auth |        | —          |       | 1        |
"""
REQUIREMENTS = """# 001 — auth — Requirements

- R1@1: A user signs in with email.
- R2@1: A session expires after 24 hours.
"""
DESIGN = """# 001 — auth — Design

- D1@1 (implements R1): Sessions live in localStorage.
- D2@1 (implements R2): Expiry is checked on every request.
"""
TASKS = """# 001 — auth — Tasks

- [ ] T001 [agent] [status:todo] Session store
      covers: D1@1
- [ ] T002 [agent] [status:todo] Expiry check
      covers: D2@1
- [ ] T003 [agent] [status:todo] Expiry test
      covers: R2@1
      kind: test
"""


def run(cwd, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = trace.main(["-C", cwd, *args])
    return code, out.getvalue()


def sh(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, env=GIT_ENV,
                          check=True).stdout.decode()


class TraceTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="spectrace-test-")
        self.write("planning/roadmap.md", ROADMAP)
        self.write("planning/architecture.md", "# Architecture\n\n- A1@1: Python 3.9+.\n")
        self.write("planning/specs/001-auth/requirements.md", REQUIREMENTS)
        self.write("planning/specs/001-auth/design.md", DESIGN)
        self.write("planning/specs/001-auth/tasks.md", TASKS)
        self.write("src/app.txt", "line one of the app\n")
        sh(self.root, "init", "-q")
        sh(self.root, "add", "-A")
        sh(self.root, "commit", "-qm", "init")
        self.assertEqual(run(self.root, "status", "--write")[0], 0)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel, text):
        path = os.path.join(self.root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, *rel.split("/")), encoding="utf-8") as f:
            return f.read()

    def replace(self, rel, old, new):
        text = self.read(rel)
        self.assertIn(old, text)
        self.write(rel, text.replace(old, new))

    def task(self, ref, edits):
        self.assertEqual(run(self.root, "start", ref)[0], 0)
        for rel, text in edits.items():
            self.write(rel, text)
        self.assertEqual(run(self.root, "done", ref)[0], 0)

    def check(self, *flags):
        code, out = run(self.root, "check", *flags)
        return code, out

    def status(self):
        import json
        return json.loads(run(self.root, "status", "--json")[1])

    # --- capture ---

    def test_tasks_without_commits_get_disjoint_patches(self):
        head = sh(self.root, "rev-parse", "HEAD")
        self.task("001/T001", {"src/app.txt": "line one of the app\nsession store added\n",
                               "src/store.txt": "store module body\n"})
        self.task("001/T002", {"src/expiry.txt": "expiry check body\n",
                               "src/app.txt": "line one of the app\nsession store added\nexpiry wired in\n"})
        p1 = self.read(".spectrace/changes/001-T001.patch")
        p2 = self.read(".spectrace/changes/001-T002.patch")
        self.assertIn("src/store.txt", p1)
        self.assertNotIn("src/expiry.txt", p1)
        self.assertIn("src/expiry.txt", p2)
        self.assertNotIn("src/store.txt", p2)
        self.assertIn("+expiry wired in", p2)
        self.assertNotIn("+session store added", p2)
        self.assertEqual(sh(self.root, "rev-parse", "HEAD"), head, "no commit is made")
        self.assertEqual(sh(self.root, "diff", "--cached", "--name-only"), "", "staging area untouched")
        tasks = self.read("planning/specs/001-auth/tasks.md")
        self.assertIn("- [x] T001 [agent] [status:done] Session store", tasks)
        self.assertIn("changes: src/app.txt (+1 -0), src/store.txt (+1 -0)", tasks)

    def test_planning_and_spectrace_are_never_task_changes(self):
        self.assertEqual(run(self.root, "start", "001/T001")[0], 0)
        self.write("planning/product.md", "# Product\n")
        self.write("src/store.txt", "store module body\n")
        run(self.root, "done", "001/T001")
        self.assertNotIn("planning/", self.read(".spectrace/changes/001-T001.patch"))

    def test_one_open_task_at_a_time(self):
        self.assertEqual(run(self.root, "start", "001/T001")[0], 0)
        self.assertEqual(self.read(".spectrace/.gitattributes"), "changes/*.patch -text\n",
                         "patches must survive CRLF checkouts for restore")
        self.assertEqual(run(self.root, "start", "001/T002")[0], 1)

    def test_changes_outside_a_task_are_refused_then_adopted(self):
        self.write("src/stray.txt", "edited with no task open\n")
        code, out = self.check()
        self.assertIn("changed outside any task", out)
        self.assertEqual(run(self.root, "start", "001/T001")[0], 2)
        self.assertEqual(run(self.root, "start", "001/T001", "--adopt")[0], 0)
        run(self.root, "done", "001/T001")
        self.assertIn("src/stray.txt", self.read(".spectrace/changes/001-T001.patch"))

    def test_abort_returns_task_to_todo(self):
        run(self.root, "start", "001/T001")
        self.assertEqual(run(self.root, "abort", "001/T001")[0], 0)
        self.assertIn("[status:todo] Session store", self.read("planning/specs/001-auth/tasks.md"))
        self.assertIsNone(self.status()["open"])

    # --- roadmap ---

    def test_status_and_stage_are_computed(self):
        s = self.status()["specs"][0]
        self.assertEqual((s["status"], s["stage"]), ("todo", "build"))
        self.task("001/T001", {"src/a.txt": "aaaa\n"})
        self.task("001/T002", {"src/b.txt": "bbbb\n"})
        self.task("001/T003", {"src/c.txt": "cccc\n"})
        s = self.status()["specs"][0]
        self.assertEqual((s["status"], s["stage"]), ("done", "—"))
        self.assertIn("| 001 | auth | done ", self.read("planning/roadmap.md"))
        self.assertEqual(self.check("--strict")[0], 0)

    def test_hand_edited_roadmap_fails_check(self):
        self.replace("planning/roadmap.md", "| todo ", "| done ")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("files say 'todo'", out)
        run(self.root, "status", "--write")
        self.assertEqual(self.check()[0], 0)

    def test_stage_follows_the_files(self):
        self.write("planning/specs/001-auth/tasks.md", "# Tasks\n")
        self.write("planning/specs/001-auth/design.md", "# Design\n")
        run(self.root, "status", "--write")
        self.assertEqual(self.status()["specs"][0]["stage"], "design")

    def test_human_tasks_do_not_hold_a_spec_open_and_blocked_rolls_up(self):
        self.write("planning/specs/001-auth/tasks.md", TASKS +
                   "- [ ] T004 [human] [status:todo] Create provider account\n      covers: R1@1\n")
        run(self.root, "status", "--write")
        for ref, f in (("001/T001", "a"), ("001/T002", "b")):
            self.task(ref, {f"src/{f}.txt": f * 4 + "\n"})
        run(self.root, "block", "001/T003", "needs a fixture")
        self.assertEqual(self.status()["specs"][0]["status"], "blocked")
        self.assertIn("└─ blocked: needs a fixture", self.read("planning/specs/001-auth/tasks.md"))
        self.task("001/T003", {"src/c.txt": "cccc\n"})
        self.assertEqual(self.status()["specs"][0]["status"], "done")

    # --- trace ---

    def test_revision_bump_makes_done_task_suspect(self):
        self.task("001/T001", {"src/a.txt": "aaaa\n"})
        self.replace("planning/specs/001-auth/design.md", "- D1@1 (implements R1): Sessions live in localStorage.",
                     "- D1@2 (implements R1): Sessions live in an httpOnly cookie.")
        run(self.root, "status", "--write")
        code, out = self.check()
        self.assertEqual(code, 0, "pending does not fail plain check")
        self.assertIn("suspect: covers D1@1, now @2", out)
        self.assertEqual(self.check("--strict")[0], 1)
        self.replace("planning/specs/001-auth/tasks.md", "covers: D1@1", "covers: D1@2")
        self.assertNotIn("suspect", self.check()[1])

    def test_a_suspect_task_alone_keeps_the_spec_open(self):
        for ref, f in (("001/T001", "a"), ("001/T002", "b"), ("001/T003", "c")):
            self.task(ref, {f"src/{f}.txt": f * 4 + "\n"})
        self.assertEqual(self.status()["specs"][0]["status"], "done")
        # R2 stays implemented by D2, so the only pending item is T003 going suspect.
        self.replace("planning/specs/001-auth/requirements.md", "- R2@1: A session expires after 24 hours.",
                     "- R2@2: A session expires after 8 hours.")
        run(self.root, "status", "--write")
        self.assertEqual(self.status()["specs"][0]["status"], "in_progress")
        self.assertEqual(self.check("--strict")[0], 1)

    def test_retire_impact_and_cleanup(self):
        self.task("001/T001", {"src/store.txt": "localStorage.setItem(session)\n"})
        self.replace("planning/specs/001-auth/design.md",
                     "- D1@1 (implements R1): Sessions live in localStorage.",
                     "- ~~D1@1 (implements R1): Sessions live in localStorage.~~ retired 2026-10-12 → D3\n"
                     "- D3@1 (implements R1): Sessions live in an httpOnly cookie.")
        code, out = run(self.root, "impact", "001/D1")
        self.assertEqual(code, 0)
        self.assertIn("001/T001", out)
        self.assertIn("src/store.txt: 1/1 added lines still present", out)
        self.assertIn("suspect: covers D1@1, retired", self.check()[1])
        self.write("planning/specs/001-auth/tasks.md", self.read("planning/specs/001-auth/tasks.md") +
                   "- [ ] T004 [agent] [status:todo] Remove localStorage sessions\n"
                   "      covers: D3@1\n      retires: T001\n")
        run(self.root, "status", "--write")
        self.assertEqual(run(self.root, "start", "001/T004")[0], 0)
        os.remove(os.path.join(self.root, "src", "store.txt"))
        run(self.root, "done", "001/T004")
        out = self.check()[1]
        self.assertNotIn("suspect", out)
        self.assertIn("file deleted", run(self.root, "impact", "001/D1")[1])

    def test_impact_follows_a_recorded_rename(self):
        body = "".join(f"session store line {n}\n" for n in range(10))
        self.task("001/T001", {"src/store.txt": body})
        self.assertEqual(run(self.root, "start", "001/T002")[0], 0)
        os.makedirs(os.path.join(self.root, "lib"))
        os.replace(os.path.join(self.root, "src", "store.txt"), os.path.join(self.root, "lib", "store.txt"))
        run(self.root, "done", "001/T002")
        self.assertIn("src/store.txt → lib/store.txt", self.read("planning/specs/001-auth/tasks.md"))
        out = run(self.root, "impact", "001/D1")[1]
        self.assertIn("src/store.txt → lib/store.txt: 10/10 added lines still present", out)

    def test_impact_infers_a_rename_recorded_as_delete_and_add(self):
        body = "".join(f"session store line {n}\n" for n in range(10))
        self.task("001/T001", {"src/store.txt": body})
        removed = "".join(f"-{l}\n" for l in body.splitlines())
        added = "".join(f"+{l}\n" for l in body.splitlines())
        self.write(".spectrace/changes/001-T002.patch",
                   "diff --git a/src/store.txt b/src/store.txt\ndeleted file mode 100644\n--- a/src/store.txt\n+++ /dev/null\n"
                   f"@@ -1,10 +0,0 @@\n{removed}"
                   "diff --git a/lib/store.txt b/lib/store.txt\nnew file mode 100644\n--- /dev/null\n+++ b/lib/store.txt\n"
                   f"@@ -0,0 +1,10 @@\n{added}")
        os.makedirs(os.path.join(self.root, "lib"))
        os.replace(os.path.join(self.root, "src", "store.txt"), os.path.join(self.root, "lib", "store.txt"))
        out = run(self.root, "impact", "001/D1")[1]
        self.assertIn("src/store.txt → lib/store.txt: 10/10 added lines still present", out)
        self.assertNotIn("mentions src/store.txt", self.check()[1], "a move is not a deletion")

    def test_mention_of_a_deleted_file_keeps_its_spec_open(self):
        for ref, f in (("001/T001", "a"), ("001/T002", "b"), ("001/T003", "c")):
            self.task(ref, {f"src/{f}.txt": f * 4 + "\n"})
        self.write("docs/guide.md", "Run src/a.txt to start.\n")
        self.write("planning/specs/001-auth/tasks.md", self.read("planning/specs/001-auth/tasks.md") +
                   "- [ ] T004 [agent] [status:todo] Remove src/a.txt\n      covers: D1@1\n")
        run(self.root, "status", "--write")
        self.assertEqual(run(self.root, "start", "001/T004", "--adopt")[0], 0)
        os.remove(os.path.join(self.root, "src", "a.txt"))
        run(self.root, "done", "001/T004")
        out = self.check("--strict")[1]
        self.assertIn("docs/guide.md:1  mentions src/a.txt, deleted by 001/T004", out)
        self.assertNotIn("tasks.md", out, "history files are never flagged")
        self.assertEqual(self.status()["specs"][0]["status"], "in_progress")
        self.write("docs/guide.md", "Run the app to start.\n")
        run(self.root, "status", "--write")
        self.assertEqual(self.status()["specs"][0]["status"], "done")

    def test_r_impact_includes_design_items_that_implement_it(self):
        self.task("001/T002", {"src/expiry.txt": "check expiry on request\n"})
        out = run(self.root, "impact", "001/R2")[1]
        self.assertIn("001/D2@1", out)
        self.assertIn("001/T002", out)
        self.assertIn("001/T003", out)

    def test_uncovered_and_orphans(self):
        self.write("planning/specs/001-auth/design.md", DESIGN + "- D3@1 (implements R9): Nothing covers this.\n")
        self.replace("planning/specs/001-auth/tasks.md", "covers: D2@1", "covers: D7@1")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("D3 implements unknown R9", out)
        self.assertIn("covers unknown item D7@1", out)
        self.assertIn("uncovered: 001/D3 has no task", out)

    def test_malformed_lines_are_errors(self):
        self.write("planning/specs/001-auth/tasks.md", TASKS + "- [ ] T4 agent todo Bad line\n")
        self.write("planning/specs/001-auth/requirements.md", REQUIREMENTS + "- R3@: no revision\n")
        out = self.check()[1]
        self.assertIn("malformed task line", out)
        self.assertIn("malformed item line", out)

    def test_text_change_under_finished_work_needs_a_bump_or_review(self):
        design = "planning/specs/001-auth/design.md"
        # Not built on yet: editing is free, the fingerprint is re-baselined.
        self.replace(design, "Expiry is checked on every request.", "Expiry is checked per request.")
        run(self.root, "status", "--write")
        self.assertNotIn("changed under finished work", self.check()[1])
        for ref, f in (("001/T001", "a"), ("001/T002", "b"), ("001/T003", "c")):
            self.task(ref, {f"src/{f}.txt": f * 4 + "\n"})
        self.assertEqual(self.status()["specs"][0]["status"], "done")
        # Built on: a silent edit is reported and keeps the spec open.
        self.replace(design, "Sessions live in localStorage.", "Sessions live in a cookie.")
        run(self.root, "status", "--write")
        self.assertIn("text of 001/D1@1 changed under finished work", self.check()[1])
        self.assertEqual(self.status()["specs"][0]["status"], "in_progress")
        # Wording only: review accepts it.
        self.assertEqual(run(self.root, "review", "001/D1")[0], 0)
        run(self.root, "status", "--write")
        self.assertNotIn("changed under finished work", self.check()[1])
        self.assertEqual(self.status()["specs"][0]["status"], "done")
        # Meaning: a bump makes the task suspect instead.
        self.replace(design, "- D1@1 (implements R1): Sessions live in a cookie.",
                     "- D1@2 (implements R1): Sessions live in a signed token.")
        out = self.check()[1]
        self.assertIn("suspect: covers D1@1, now @2", out)
        self.assertNotIn("changed under finished work", out)

    def test_restore_brings_back_what_a_task_removed(self):
        self.task("001/T001", {"src/store.txt": "localStorage.setItem(session)\n"})
        self.write("planning/specs/001-auth/tasks.md", self.read("planning/specs/001-auth/tasks.md") +
                   "- [ ] T004 [agent] [status:todo] Remove the store\n      covers: D1@1\n      retires: T001\n"
                   "- [ ] T005 [agent] [status:todo] Bring the store back\n      covers: D1@1\n")
        run(self.root, "status", "--write")
        self.assertEqual(run(self.root, "start", "001/T004")[0], 0)
        os.remove(os.path.join(self.root, "src", "store.txt"))
        run(self.root, "done", "001/T004")
        self.assertEqual(run(self.root, "restore", "001/T004")[0], 1, "needs an open task")
        self.assertEqual(run(self.root, "start", "001/T005")[0], 0)
        self.assertEqual(run(self.root, "restore", "001/T004")[0], 0)
        self.assertEqual(self.read("src/store.txt"), "localStorage.setItem(session)\n")
        run(self.root, "done", "001/T005")
        self.assertIn("+localStorage.setItem(session)", self.read(".spectrace/changes/001-T005.patch"))
        self.assertEqual(run(self.root, "start", "001/T002")[0], 0)
        self.assertEqual(run(self.root, "restore", "001/T004")[0], 1, "no longer applies: the file is back")

    def test_examples_in_fences_are_ignored(self):
        self.write("planning/specs/001-auth/requirements.md",
                   REQUIREMENTS + "\n```\n- R9@1: an example, not a requirement\n```\n")
        self.assertNotIn("R9", self.check()[1])


class FormatDocTest(unittest.TestCase):
    """format.md's examples must be exactly what trace.py parses."""

    def test_examples_parse(self):
        with open(os.path.join(ASSETS, "format.md"), encoding="utf-8") as f:
            blocks = re.findall(r"```\n(.*?)```", f.read(), re.S)
        items = next(b for b in blocks if "R2@1:" in b)
        for line in items.strip().splitlines():
            self.assertTrue(trace.RETIRED_RE.match(line) or trace.ITEM_RE.match(line), line)
        tasks = next(b for b in blocks if "[status:" in b)
        for line in tasks.rstrip().splitlines():
            if line.startswith("- ["):
                self.assertTrue(trace.TASK_RE.match(line), line)
            elif "└─" not in line:
                self.assertTrue(trace.FIELD_RE.match(line), line)


if __name__ == "__main__":
    unittest.main()
