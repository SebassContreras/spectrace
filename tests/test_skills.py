"""Structural checks for every skills/*/SKILL.md, and the size budget.

Protects A7 (open Agent Skills format: agentskills.io/specification) and A5 (each
SKILL.md body at most 200 lines, trace.py at most 900). Breaks if a skill gains a
non-spec frontmatter key, a name that differs from its folder, an over-long
description or body, a reference to a file that doesn't exist, or trace.py outgrows
its budget.
"""
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(ROOT, "skills")
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"`((?:references|assets|scripts)/[\w./-]+)`")
BODY_LIMIT = 200
TRACE_LIMIT = 900
TRACE = os.path.join(SKILLS, "spectrace-start", "assets", "trace.py")


def parse(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise AssertionError(f"{path}: no frontmatter")
    front, body = m.group(1), m.group(2)
    fields, key = {}, None
    for line in front.splitlines():
        top = re.match(r"^([\w-]+):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2)
            fields[key] = "" if value in (">", ">-", "|", "|-") else value.strip("'\"")
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, body


class SkillStructureTest(unittest.TestCase):
    def skills(self):
        names = sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))
        self.assertTrue(names, "no skills found")
        return names

    def test_frontmatter_follows_the_agent_skills_spec(self):
        for name in self.skills():
            fields, _ = parse(os.path.join(SKILLS, name, "SKILL.md"))
            with self.subTest(skill=name):
                self.assertLessEqual(set(fields), ALLOWED_KEYS)
                self.assertEqual(fields.get("name"), name, "name must equal the folder name")
                self.assertRegex(fields["name"], NAME_RE)
                self.assertLessEqual(len(fields["name"]), 64)
                self.assertTrue(fields.get("description"))
                self.assertLessEqual(len(fields["description"]), 1024)

    def test_body_within_budget(self):
        for name in self.skills():
            _, body = parse(os.path.join(SKILLS, name, "SKILL.md"))
            with self.subTest(skill=name):
                self.assertLessEqual(len(body.splitlines()), BODY_LIMIT)

    def test_trace_within_budget(self):
        with open(TRACE, encoding="utf-8") as f:
            self.assertLessEqual(len(f.read().splitlines()), TRACE_LIMIT)

    def test_referenced_files_exist(self):
        for name in self.skills():
            _, body = parse(os.path.join(SKILLS, name, "SKILL.md"))
            for ref in set(REF_RE.findall(body)):
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue(os.path.exists(os.path.join(SKILLS, name, *ref.split("/"))))


if __name__ == "__main__":
    unittest.main()
