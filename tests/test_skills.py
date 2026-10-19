"""Structural checks for every skills/*/SKILL.md, and the size budget.

Protects A7 (open Agent Skills format: agentskills.io/specification) and A5 (each
SKILL.md body at most 200 lines, each module of spectrace/ at most 600). Breaks if a
skill gains a non-spec frontmatter key, a name that differs from its folder, an
over-long description or body, a reference to a file that doesn't exist, or a module
outgrows its budget.
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
MODULE_LIMIT = 600
PACKAGE = os.path.join(SKILLS, "spectrace-start", "assets", "spectrace")


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

    def test_every_module_within_budget(self):
        modules = sorted(os.path.relpath(os.path.join(d, n), PACKAGE) for d, _, files in os.walk(PACKAGE)
                         for n in files if n.endswith(".py"))
        self.assertIn("model.py", modules)
        for rel in modules:
            with open(os.path.join(PACKAGE, rel), encoding="utf-8") as f, self.subTest(module=rel):
                self.assertLessEqual(len(f.read().splitlines()), MODULE_LIMIT)

    def test_referenced_files_exist(self):
        for name in self.skills():
            _, body = parse(os.path.join(SKILLS, name, "SKILL.md"))
            for ref in set(REF_RE.findall(body)):
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue(os.path.exists(os.path.join(SKILLS, name, *ref.split("/"))))


class ReadmeTest(unittest.TestCase):
    """Protects 014 R5: the README documents the CI recipe and every skill."""

    def setUp(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            self.readme = f.read()

    def test_the_ci_recipe_names_the_gate_and_the_packet(self):
        self.assertIn("trace.py check --strict", self.readme)
        self.assertIn("trace.py packet --diff --base", self.readme)
        self.assertIn("fetch-depth: 0", self.readme)

    def test_every_skill_is_listed(self):
        listed = set(re.findall(r"^\| `(spectrace-[a-z]+)` \|", self.readme, re.M))
        self.assertEqual(listed, set(SkillStructureTest().skills()))


if __name__ == "__main__":
    unittest.main()
