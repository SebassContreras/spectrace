"""Tests for change records (spectrace/records.py) through the trace commands.

Run: python -m unittest discover -s tests
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("SPECTRACE_ASSETS") or os.path.join(HERE, "..", "skills", "spectrace-start", "assets"))
from spectrace import records  # noqa: E402
from spectrace.cli import main  # noqa: E402

GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
TASKS = "".join(f"- [ ] T00{n} [agent] [status:todo] Step {n}\n      covers: D1@1\n" for n in range(1, 6))
STORE = '''import json


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
'''


class Project:
    """A throwaway git repo with one spec of five tasks covering D1."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="spectrace-records-")
        self.write("planning/roadmap.md", "| ID | Spec | Status | Depends on | Stage | Priority |\n"
                   "|---|---|---|---|---|---|\n| 001 | store | | — | | 1 |\n")
        self.write("planning/specs/001-store/requirements.md", "- R1@1: Data is stored.\n")
        self.write("planning/specs/001-store/design.md", "- D1@1 (implements R1): Data is a JSON file.\n")
        self.write("planning/specs/001-store/tasks.md", TASKS)
        self.write("README.md", "# Demo\n")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True, env=GIT_ENV)
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True, env=GIT_ENV)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=self.root, check=True, env=GIT_ENV)
        self.run("status", "--write")

    def run(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = main(["-C", self.root, *args])
        return code, out.getvalue()

    def write(self, rel, text):
        path = os.path.join(self.root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def task(self, ref, edit):
        assert self.run("start", ref)[0] == 0
        edit()
        code, out = self.run("done", ref)
        assert code == 0, out
        return out, self.record(ref)

    def record(self, ref):
        with open(os.path.join(self.root, ".spectrace", "changes", ref.replace("/", "-") + ".touch.json"),
                  encoding="utf-8") as f:
            return json.load(f)


def symbols_of(rec, path):
    return {s["name"]: s for s in rec["files"][path]["symbols"]}


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.p = Project()
        self.addCleanup(shutil.rmtree, self.p.root, True)

    def test_every_added_and_removed_line_is_accounted_for(self):
        out, rec = self.p.task("001/T001", lambda: self.p.write("store.py", STORE))
        self.assertIn("accounted 11/11 added, 0/0 removed lines", out)
        self.assertEqual(rec["files"]["store.py"]["lines"], [11, 0])
        self.assertEqual(records.unaccounted(rec), 0)
        self.assertEqual(sorted(symbols_of(rec, "store.py")), ["load", "save"])
        self.assertEqual(rec["files"]["store.py"]["other"], {"imports": [1, 0], "module": [4, 0]})

    def test_a_renamed_function_keeps_its_history(self):
        self.p.task("001/T001", lambda: self.p.write("store.py", STORE))
        _, rec = self.p.task("001/T002", lambda: self.p.write("store.py", STORE.replace("def load(", "def read(")))
        read = symbols_of(rec, "store.py")["read"]
        self.assertEqual((read["change"], read["from"], read["lines"]), ("renamed", "load", [1, 1]))

    def test_a_removed_symbol_is_recorded_with_its_lines(self):
        self.p.task("001/T001", lambda: self.p.write("store.py", STORE))
        _, rec = self.p.task("001/T002", lambda: self.p.write("store.py", STORE.split("\n\ndef save")[0] + "\n"))
        save = symbols_of(rec, "store.py")["save"]
        self.assertEqual((save["change"], save["lines"]), ("removed", [0, 3]))
        self.assertEqual(records.unaccounted(rec), 0)

    def test_a_file_that_does_not_parse_is_skipped_at_file_level(self):
        _, rec = self.p.task("001/T001", lambda: self.p.write("broken.py", "def broken(:\n    pass\n"))
        self.assertEqual(rec["skipped"][0]["path"], "broken.py")
        self.assertIn("SyntaxError", rec["skipped"][0]["reason"])
        self.assertEqual(rec["files"]["broken.py"]["other"], {"file": [2, 0]})

    def test_a_binary_file_has_no_line_totals(self):
        def edit():
            with open(os.path.join(self.p.root, "logo.bin"), "wb") as f:
                f.write(bytes(range(256)))
        _, rec = self.p.task("001/T001", edit)
        self.assertIsNone(rec["files"]["logo.bin"]["lines"])

    def test_a_task_over_the_caps_is_recorded_at_file_level_and_partial(self):
        def edit():
            self.p.write("store.py", STORE)
            self.p.write("notes.md", "# Notes\n")
        with mock.patch.object(records, "TASK_LIMIT", 1):
            out, rec = self.p.task("001/T001", edit)
        self.assertIn("(partial record)", out)
        self.assertTrue(rec["partial"])
        self.assertEqual(rec["files"]["store.py"]["symbols"], [])
        self.assertEqual(rec["files"]["store.py"]["other"], {"file": [11, 0]})


class ViewsTest(unittest.TestCase):
    def setUp(self):
        self.p = Project()
        self.addCleanup(shutil.rmtree, self.p.root, True)
        self.p.task("001/T001", lambda: self.p.write("store.py", STORE))

    def test_why_names_the_task_and_decision_behind_live_code(self):
        out = self.p.run("why", "store.py::load")[1]
        self.assertIn("- 001/T001 [done] Step 1\n    load added\n    covers: 001/D1@1", out)

    def test_why_answers_for_code_that_no_longer_exists(self):
        self.p.task("001/T002", lambda: self.p.write("store.py", STORE.split("\n\ndef save")[0] + "\n"))
        out = self.p.run("why", "store.py::save")[1]
        self.assertIn("001/T002 [done] Step 2\n    save removed", out)
        self.assertIn("001/T001 [done] Step 1\n    save added", out)

    def test_why_says_when_code_is_outside_the_trace(self):
        out = self.p.run("why", "README.md")[1]
        self.assertIn("outside the trace: no task recorded README.md", out)

    def test_impact_reports_each_symbol_and_the_lines_still_inside(self):
        self.p.task("001/T002", lambda: self.p.write("store.py", STORE.replace("return json.load(f)", "return {}")))
        out = self.p.run("impact", "001/D1")[1]
        self.assertIn("store.py::load [added] changed: 2/3 added lines still inside", out)
        self.assertIn("store.py::save [added] unchanged", out)

    def test_a_retired_tasks_unchanged_symbol_is_a_leftover_until_kept(self):
        self.p.write("planning/specs/001-store/tasks.md", TASKS +
                     "- [ ] T006 [agent] [status:todo] Drop the store\n      covers: D1@1\n      retires: T001\n")
        self.p.task("001/T006", lambda: self.p.write("store.py", STORE.replace("return json.load(f)", "return {}")))
        code, out = self.p.run("check", "--strict")
        self.assertEqual(code, 1)
        self.assertIn("leftover: store.py::save, added by 001/T001, is still there unchanged", out)
        self.assertNotIn("leftover: store.py::load", out, "rewritten code is not a leftover")
        self.assertEqual(self.p.run("keep", "store.py::save", "the CLI still saves")[0], 0)
        self.assertNotIn("leftover", self.p.run("check")[1])

    def test_a_reinstated_symbol_is_not_a_leftover_if_recorded_by_a_task_after_cleanup(self):
        self.p.write("planning/specs/001-store/tasks.md", TASKS +
                     "- [ ] T006 [agent] [status:todo] Drop the store\n      covers: D1@1\n      retires: T001\n" +
                     "- [ ] T007 [agent] [status:todo] Reinstate the store\n      covers: D1@1\n")
        # Cleanup task drops save():
        self.p.task("001/T006", lambda: self.p.write("store.py", STORE.split("\n\ndef save")[0] + "\n"))
        # Later task brings back save() identical to T001:
        self.p.task("001/T007", lambda: self.p.write("store.py", STORE))
        code, out = self.p.run("check", "--strict")
        self.assertNotIn("leftover: store.py::save", out)


    def test_keep_needs_a_reason(self):
        self.assertEqual(self.p.run("keep", "store.py::save", " ")[0], 1)

    def test_a_task_without_a_record_is_answered_by_anchoring_its_patch(self):
        os.remove(os.path.join(self.p.root, ".spectrace", "changes", "001-T001.touch.json"))
        out = self.p.run("why", "store.py::load")[1]
        self.assertIn("001/T001 [done] Step 1\n    anchored: load", out)

    def test_changes_outside_a_task_are_named_by_symbol(self):
        self.p.write("store.py", STORE + "\n\ndef drop(path):\n    pass\n")
        self.assertIn("symbols: store.py::drop (added)", self.p.run("check")[1])
        code, out = self.p.run("start", "001/T002")
        self.assertEqual(code, 2)
        self.assertIn("Symbols: store.py::drop (added)", out)


if __name__ == "__main__":
    unittest.main()
