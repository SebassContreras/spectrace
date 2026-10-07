#!/usr/bin/env python3
"""spectrace trace: status, per-task change capture, and the spec trace check.

Implements .spectrace/format.md. Python 3.9+, standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date

VERSION = "1"
EXCLUDE = (":(exclude)planning", ":(exclude).spectrace")
PATCH_LIMIT = 200_000
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
IDENT = {"GIT_AUTHOR_NAME": "spectrace", "GIT_AUTHOR_EMAIL": "spectrace@localhost",
         "GIT_COMMITTER_NAME": "spectrace", "GIT_COMMITTER_EMAIL": "spectrace@localhost"}

ITEM_RE = re.compile(r"^\s*-\s+(?P<kind>[RDA])(?P<num>\d+)@(?P<rev>\d+)"
                     r"(?:\s*\((?P<rel>[^)]*)\))?:\s*\S")
RETIRED_RE = re.compile(r"^\s*-\s+~~(?P<kind>[RDA])(?P<num>\d+)@(?P<rev>\d+)"
                        r"(?:\s*\((?P<rel>[^)]*)\))?:.*~~\s*retired\s+\d{4}-\d{2}-\d{2}")
ITEMISH_RE = re.compile(r"^\s*-\s+(~~)?[RDA]\d+@")
TASK_RE = re.compile(r"^- \[(?P<box>[ x])\] T(?P<num>\d{3}) \[(?P<owner>agent|human)\] "
                     r"\[status:(?P<status>todo|in_progress|blocked|done)\] (?P<text>\S.*?)\s*$")
TASKISH_RE = re.compile(r"^- \[[ xX]\] ")
FIELD_RE = re.compile(r"^\s+(?P<key>covers|kind|retires|changes):\s*(?P<val>.*?)\s*$")
REF_RE = re.compile(r"^(?:(?P<spec>\d{3})/)?(?P<kind>[RDA])(?P<num>\d+)(?:@(?P<rev>\d+))?$")
TASKREF_RE = re.compile(r"^(?:(?P<spec>\d{3})/)?T(?P<num>\d+)$")
SEVERITY = {"error": 0, "pending": 1, "warning": 2}


class TraceError(Exception):
    pass


# ---------- files ----------

def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().splitlines(keepends=True)


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(lines))


def eol(line):
    return line[len(line.rstrip("\r\n")):] or "\n"


def unfenced(lines):
    """Yield (index, line) outside ``` fences, so examples in docs are never parsed."""
    fenced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line.rstrip("\r\n")


# ---------- model ----------

class Item:
    def __init__(self, kind, num, rev, retired, implements, where, spec, text):
        self.kind, self.num, self.rev = kind, num, rev
        self.retired, self.implements, self.where = retired, implements, where
        self.spec, self.text = spec, " ".join(text.split())

    @property
    def key(self):
        return f"{self.kind}{self.num}"

    @property
    def ref(self):
        return (f"{self.spec}/" if self.spec else "") + f"{self.key}@{self.rev}"

    @property
    def fingerprint(self):
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()[:16]


class Task:
    def __init__(self, spec, num, owner, status, box, text, line):
        self.spec, self.num, self.owner, self.status = spec, num, owner, status
        self.box, self.text, self.line = box, text, line
        self.covers, self.retires, self.kind, self.changes = [], [], None, None

    @property
    def ref(self):
        return f"{self.spec}/T{self.num:03d}"


class Spec:
    def __init__(self, sid, name, row):
        self.id, self.name, self.row = sid, name, row
        self.dir = f"planning/specs/{sid}-{name}"
        self.items, self.tasks, self.deps, self.cells = {}, [], [], {}
        self.priority = self.status = self.stage = None


class Repo:
    def __init__(self, root):
        self.root = root
        self.issues = []  # (severity, where, message, spec id or None)
        self.global_items, self.specs = {}, {}
        self.columns, self.rows = {}, []
        try:
            with open(self.path(".spectrace/fingerprints.json"), encoding="utf-8") as f:
                self.fingerprints = json.load(f)
        except (OSError, ValueError):
            self.fingerprints = {}
        self.saved_fingerprints = dict(self.fingerprints)
        self.load()
        self.trace()
        self.compute()

    def issue(self, severity, where, message, spec=None):
        self.issues.append((severity, where, message, spec))

    def path(self, rel):
        return os.path.join(self.root, *rel.split("/"))

    # --- parsing ---

    def load(self):
        if os.path.exists(self.path("planning/architecture.md")):
            self.parse_items("planning/architecture.md", "A", self.global_items)
        self.parse_roadmap()
        specs_dir = self.path("planning/specs")
        folders = sorted(os.listdir(specs_dir)) if os.path.isdir(specs_dir) else []
        known = {f"{s.id}-{s.name}" for s in self.specs.values()}
        for folder in folders:
            if re.match(r"^\d{3}-", folder) and folder not in known:
                self.issue("error", f"planning/specs/{folder}", "folder has no roadmap row")
        for spec in self.specs.values():
            if not os.path.isdir(self.path(spec.dir)):
                self.issue("error", "planning/roadmap.md", f"{spec.id}: no folder {spec.dir}", spec.id)
                continue
            for name, kind in (("requirements.md", "R"), ("design.md", "D")):
                rel = f"{spec.dir}/{name}"
                if os.path.exists(self.path(rel)):
                    self.parse_items(rel, kind, spec.items, spec.id)
            if os.path.exists(self.path(f"{spec.dir}/tasks.md")):
                self.parse_tasks(f"{spec.dir}/tasks.md", spec)

    def parse_items(self, rel, kind, into, sid=None):
        for i, line in unfenced(read_lines(self.path(rel))):
            where = f"{rel}:{i + 1}"
            m = RETIRED_RE.match(line) or ITEM_RE.match(line)
            if not m:
                if ITEMISH_RE.match(line):
                    self.issue("error", where, "malformed item line", sid)
                continue
            if m.group("kind") != kind:
                self.issue("error", where, f"{m.group('kind')} item does not belong in {rel.rsplit('/', 1)[-1]}", sid)
                continue
            rel_text = (m.group("rel") or "").strip()
            implements = re.findall(r"\bR(\d+)\b", rel_text) if rel_text.startswith("implements") else []
            item = Item(kind, int(m.group("num")), int(m.group("rev")), m.re is RETIRED_RE,
                        [f"R{int(n)}" for n in implements], where, sid, line)
            if item.key in into:
                self.issue("error", where, f"duplicate ID {item.key}", sid)
            into[item.key] = item

    def parse_roadmap(self):
        rel = "planning/roadmap.md"
        if not os.path.exists(self.path(rel)):
            self.issue("error", rel, "missing")
            return
        for i, line in unfenced(read_lines(self.path(rel))):
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not self.columns:
                if "ID" in cells and "Spec" in cells:
                    self.columns = {c: n for n, c in enumerate(cells)}
                    missing = {"ID", "Spec", "Status", "Depends on", "Stage", "Priority"} - set(cells)
                    if missing:
                        self.issue("error", rel, f"missing columns: {', '.join(sorted(missing))}")
                continue
            if set("".join(cells)) <= set("-: "):
                continue

            def get(col):
                n = self.columns.get(col)
                return cells[n] if n is not None and n < len(cells) else ""
            sid = get("ID")
            if not re.fullmatch(r"\d{3}", sid):
                self.issue("error", f"{rel}:{i + 1}", f"bad spec ID {sid!r}")
                continue
            spec = Spec(sid, get("Spec"), i)
            deps = get("Depends on")
            spec.deps = [] if deps in ("", "—", "-") else [d.strip() for d in deps.split(",")]
            prio = get("Priority")
            spec.priority = int(prio) if prio.isdigit() else None
            spec.cells = {"Status": get("Status"), "Stage": get("Stage")}
            self.specs[sid] = spec
            self.rows.append(sid)
        for spec in self.specs.values():
            for dep in spec.deps:
                if dep not in self.specs:
                    self.issue("error", rel, f"{spec.id} depends on unknown spec {dep}", spec.id)

    def parse_tasks(self, rel, spec):
        task = None
        for i, line in unfenced(read_lines(self.path(rel))):
            where = f"{rel}:{i + 1}"
            if m := TASK_RE.match(line):
                task = Task(spec.id, int(m.group("num")), m.group("owner"), m.group("status"),
                            m.group("box"), m.group("text"), i)
                if any(t.num == task.num for t in spec.tasks):
                    self.issue("error", where, f"duplicate task T{task.num:03d}", spec.id)
                if (task.box == "x") != (task.status == "done"):
                    self.issue("error", where, "checkbox and status disagree", spec.id)
                spec.tasks.append(task)
                continue
            if TASKISH_RE.match(line):
                self.issue("error", where, "malformed task line", spec.id)
                task = None
                continue
            if not line.strip():
                continue
            if not line[0].isspace():
                task = None
                continue
            f = FIELD_RE.match(line)
            if task and f:
                key, val = f.group("key"), f.group("val")
                values = [v.strip() for v in val.split(",") if v.strip()]
                if key == "covers":
                    task.covers += values
                elif key == "retires":
                    task.retires += values
                elif key == "kind":
                    task.kind = val
                else:
                    task.changes = val
        for t in spec.tasks:
            if not t.covers:
                self.issue("error", f"{rel}:{t.line + 1}", f"{t.ref} has no covers:", spec.id)

    # --- resolution ---

    def resolve(self, raw, spec_id):
        m = REF_RE.match(raw)
        if not m or not m.group("rev"):
            return None, None
        key = f"{m.group('kind')}{int(m.group('num'))}"
        if m.group("kind") == "A":
            return self.global_items.get(key), int(m.group("rev"))
        spec = self.specs.get(m.group("spec") or spec_id)
        return (spec.items.get(key) if spec else None), int(m.group("rev"))

    def find_task(self, raw, spec_id=None):
        m = TASKREF_RE.match(raw.strip())
        spec = self.specs.get(m.group("spec") or spec_id) if m else None
        if not spec:
            return None
        return next((t for t in spec.tasks if t.num == int(m.group("num"))), None)

    # --- trace states ---

    def trace(self):
        retired_by_done = set()
        for spec in self.specs.values():
            for t in spec.tasks:
                for raw in t.retires:
                    target = self.find_task(raw, spec.id)
                    if not target:
                        self.issue("error", t.ref, f"retires unknown task {raw}", spec.id)
                    elif t.status == "done":
                        retired_by_done.add(target.ref)
                    elif target.status == "done":
                        self.issue("pending", t.ref, f"cleanup of {target.ref} not done yet", spec.id)
        for spec in self.specs.values():
            for item in spec.items.values():
                for r in item.implements:
                    target = spec.items.get(r)
                    if not target:
                        self.issue("error", item.where, f"{item.key} implements unknown {r}", spec.id)
                    elif target.retired and not item.retired:
                        self.issue("pending", item.where, f"{spec.id}/{item.key} implements retired {r}", spec.id)
            for t in spec.tasks:
                for raw in t.covers:
                    item, rev = self.resolve(raw, spec.id)
                    if item is None:
                        self.issue("error", t.ref, f"covers unknown item {raw}", spec.id)
                        continue
                    if not (item.retired or item.rev != rev) or t.ref in retired_by_done:
                        continue
                    why = "retired" if item.retired else f"now @{item.rev}"
                    if t.status == "done":
                        self.issue("pending", t.ref, f"suspect: covers {raw}, {why}", spec.id)
                    else:
                        self.issue("pending", t.ref, f"covers outdated {raw} ({why})", spec.id)
                if t.status == "done" and t.owner == "agent" and t.changes is None:
                    self.issue("warning", t.ref, "done without changes: (finished outside trace)", spec.id)
            self.uncovered(spec)
        self.deleted_mentions()
        self.changed_text()

    def items(self):
        yield from (i for i in self.global_items.values() if not i.retired)
        for spec in self.specs.values():
            yield from (i for i in spec.items.values() if not i.retired)

    def built_on(self):
        """{item ref: spec ids} for items a finished task covers at their current revision."""
        out = {}
        for spec in self.specs.values():
            for t in (t for t in spec.tasks if t.status == "done"):
                for raw in t.covers:
                    item, rev = self.resolve(raw, spec.id)
                    if item and not item.retired and rev == item.rev:
                        out.setdefault(item.ref, set()).add(spec.id)
        return out

    def changed_text(self):
        """An item's meaning must not change under finished work without a revision bump."""
        for item_ref, specs in self.built_on().items():
            item = next(i for i in self.items() if i.ref == item_ref)
            seen = self.fingerprints.get(item_ref)
            if seen and seen != item.fingerprint:
                for sid in sorted(specs):
                    self.issue("pending", item.where, f"text of {item_ref} changed under finished work: bump its "
                               f"revision (spectrace-change), or `review {item_ref.split('@')[0]}` if wording only", sid)

    def record_fingerprints(self):
        built = self.built_on()
        fresh = {i.ref: i.fingerprint for i in self.items()}
        kept = {k: v for k, v in self.fingerprints.items() if k in built}
        merged = {**fresh, **kept}
        if merged != self.saved_fingerprints:
            os.makedirs(self.path(".spectrace"), exist_ok=True)
            with open(self.path(".spectrace/fingerprints.json"), "w", encoding="utf-8", newline="\n") as f:
                json.dump(dict(sorted(merged.items())), f, indent=1)
                f.write("\n")

    def deleted_mentions(self):
        """A file a task deleted must not still be named anywhere outside history."""
        patches, renames = load_patches(self.root)
        deleted = {b["old"]: ref for ref, blocks in patches.items() for b in blocks
                   if b["status"] == "deleted" and b["old"] not in renames
                   and not os.path.exists(self.path(b["old"]))}
        if not deleted:
            return
        listed = git(self.root, "ls-files", "-z", "-co", "--exclude-standard").split("\0")
        for rel in filter(None, listed):
            history = rel.startswith(".spectrace/") or (
                rel.startswith("planning/") and rel.rsplit("/", 1)[-1] in ("tasks.md", "changes.md"))
            full = self.path(rel)
            if history or not os.path.isfile(full) or os.path.getsize(full) > 1_000_000:
                continue
            with open(full, "rb") as f:
                data = f.read()
            if b"\0" in data[:1024]:
                continue
            for n, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
                if RETIRED_RE.match(line):
                    continue
                for path, ref in deleted.items():
                    if path in line:
                        self.issue("pending", f"{rel}:{n}", f"mentions {path}, deleted by {ref}", ref[:3])

    def covered_now(self, item):
        for spec in self.specs.values():
            for t in spec.tasks:
                for raw in t.covers:
                    found, rev = self.resolve(raw, spec.id)
                    if found is item and rev == item.rev:
                        return True
        return False

    def uncovered(self, spec):
        active = [i for i in spec.items.values() if not i.retired]
        ds = [i for i in active if i.kind == "D"]
        if ds:
            for r in (i for i in active if i.kind == "R"):
                if not any(r.key in d.implements for d in ds) and not self.covered_now(r):
                    self.issue("pending", r.where, f"uncovered: {spec.id}/{r.key} has no design item or task", spec.id)
        if spec.tasks:
            for d in ds:
                if not self.covered_now(d):
                    self.issue("pending", d.where, f"uncovered: {spec.id}/{d.key} has no task", spec.id)

    # --- computed roadmap columns ---

    def compute(self):
        for spec in self.specs.values():
            active = [i for i in spec.items.values() if not i.retired]
            agent = [t for t in spec.tasks if t.owner == "agent"]
            pending = any(sev == "pending" and sid == spec.id for sev, _, _, sid in self.issues)
            if not any(i.kind == "R" for i in active):
                stage = "requirements"
            elif not any(i.kind == "D" for i in active):
                stage = "design"
            elif not spec.tasks:
                stage = "tasks"
            else:
                stage = "build"
            if any(t.status == "blocked" for t in agent):
                status = "blocked"
            elif stage == "build" and all(t.status == "done" for t in agent) and not pending:
                status = "done"
            elif any(t.status in ("in_progress", "done") for t in spec.tasks):
                status = "in_progress"
            else:
                status = "todo"
            spec.status, spec.stage = status, ("—" if status == "done" else stage)
        for spec in self.specs.values():
            for col, value in (("Status", spec.status), ("Stage", spec.stage)):
                if spec.cells.get(col) != value:
                    self.issue("error", "planning/roadmap.md",
                               f"{spec.id} {col} is {spec.cells.get(col) or 'empty'!r}, files say {value!r}"
                               " (run: status --write)", spec.id)

    def next_task(self):
        def order(s):
            return (s.priority if s.priority is not None else 10**9, s.id)
        for spec in sorted(self.specs.values(), key=order):
            if spec.status == "done" or any(self.specs[d].status != "done" for d in spec.deps if d in self.specs):
                continue
            for t in spec.tasks:
                if t.owner == "agent" and t.status == "todo":
                    return t
        return None

    def write_roadmap(self):
        rel = self.path("planning/roadmap.md")
        lines = read_lines(rel)
        for spec in self.specs.values():
            line = lines[spec.row]
            body = line.rstrip("\r\n")
            lead = body[:len(body) - len(body.lstrip())]
            parts = body.strip().split("|")  # ['', cell, ..., '']
            for col, value in (("Status", spec.status), ("Stage", spec.stage)):
                n = self.columns[col] + 1
                cell = f" {value} "
                parts[n] = cell + " " * max(0, len(parts[n]) - len(cell))
            lines[spec.row] = lead + "|".join(parts) + eol(line)
        write_lines(rel, lines)
        self.record_fingerprints()


# ---------- git ----------

def git(root, *args, env=None, raw=False):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=root,
                       capture_output=True, env=dict(os.environ, **(env or {})))
    if p.returncode != 0:
        raise TraceError(f"git {' '.join(args)}: {p.stderr.decode(errors='replace').strip()}")
    return p.stdout.decode("utf-8", errors="replace").strip("" if raw else None)


def snapshot(root):
    """Tree of the whole working tree (honoring .gitignore), without touching the real index."""
    index = os.path.join(root, git(root, "rev-parse", "--git-path", "index"))
    tmp = os.path.join(root, git(root, "rev-parse", "--git-path", "spectrace-index"))
    if os.path.exists(index):
        shutil.copyfile(index, tmp)
    elif os.path.exists(tmp):
        os.remove(tmp)
    try:
        env = {"GIT_INDEX_FILE": tmp}
        git(root, "add", "-A", env=env)
        return git(root, "write-tree", env=env)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def keep(root, name, tree):
    commit = git(root, "commit-tree", tree, "-m", f"spectrace {name}", env=IDENT)
    git(root, "update-ref", f"refs/spectrace/{name}", commit)


def kept(root, name):
    try:
        return git(root, "rev-parse", "--verify", "--quiet", f"refs/spectrace/{name}^{{tree}}")
    except TraceError:
        return None


def drop(root, name):
    if kept(root, name):
        git(root, "update-ref", "-d", f"refs/spectrace/{name}")


def reference_tree(root):
    """The tree when the last task closed; else HEAD; else empty."""
    if last := kept(root, "last"):
        return last
    try:
        return git(root, "rev-parse", "--verify", "--quiet", "HEAD^{tree}")
    except TraceError:
        return EMPTY_TREE


def diff(root, a, b, *flags):
    return git(root, "diff", "--no-color", "--no-ext-diff", "-M", *flags, a, b, "--", ".", *EXCLUDE, raw=True)


def numstat(root, a, b):
    out, parts = [], diff(root, a, b, "--numstat", "-z").split("\0")
    while parts:
        head = parts.pop(0)
        if not head.strip():
            continue
        add, rem, path = head.lstrip().split("\t", 2)
        if not path:  # rename: old and new paths follow
            path = f"{parts.pop(0)} → {parts.pop(0)}"
        out.append(f"{path} (binary)" if add == "-" else f"{path} (+{add} -{rem})")
    return out


# ---------- state ----------

def state_path(root):
    return os.path.join(root, ".spectrace", "state.json")


def load_state(root):
    try:
        with open(state_path(root), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(root, state):
    os.makedirs(os.path.dirname(state_path(root)), exist_ok=True)
    # Patches must stay byte-exact across clones, or `restore` breaks on CRLF checkouts.
    for name, text in ((".gitignore", "state.json\n"), (".gitattributes", "changes/*.patch -text\n")):
        if not os.path.exists(os.path.join(root, ".spectrace", name)):
            with open(os.path.join(root, ".spectrace", name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    if state:
        with open(state_path(root), "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    elif os.path.exists(state_path(root)):
        os.remove(state_path(root))


# ---------- task edits ----------

def edit_task(repo, task, status=None, changes=None, note=None):
    rel = repo.path(f"{repo.specs[task.spec].dir}/tasks.md")
    lines = read_lines(rel)
    i = task.line
    end_of_line = eol(lines[i])
    if status:
        box = "x" if status == "done" else " "
        lines[i] = f"- [{box}] T{task.num:03d} [{task.owner}] [status:{status}] {task.text}{end_of_line}"
    end = i + 1
    while end < len(lines) and lines[end].strip() and lines[end][0].isspace():
        end += 1
    block = lines[i + 1:end]
    if changes is not None:
        block = [l for l in block if not re.match(r"^\s+changes:", l)]
        fields = [n for n, l in enumerate(block) if FIELD_RE.match(l.rstrip("\r\n"))]
        block.insert((fields[-1] + 1) if fields else 0, f"      changes: {changes}{end_of_line}")
    if note:
        block.append(f"      └─ {note}{end_of_line}")
    lines[i + 1:end] = block
    write_lines(rel, lines)


# ---------- commands ----------

def need_task(repo, raw):
    task = repo.find_task(raw)
    if not task:
        raise TraceError(f"no task {raw} (use NNN/TNNN, e.g. 001/T005)")
    return task


def cmd_status(repo, args):
    if args.write:
        repo.write_roadmap()
        repo = Repo(repo.root)
    state = load_state(repo.root)
    nxt = repo.next_task()
    if args.json:
        print(json.dumps({
            "specs": [{"id": s.id, "spec": s.name, "status": s.status, "stage": s.stage}
                      for s in (repo.specs[i] for i in repo.rows)],
            "open": state.get("open"), "next": nxt.ref if nxt else None}, indent=2))
        return 0
    print(f"{'ID':<5}{'Spec':<28}{'Status':<13}Stage")
    for sid in repo.rows:
        s = repo.specs[sid]
        print(f"{s.id:<5}{s.name:<28}{s.status:<13}{s.stage}")
    print(f"\nopen: {state.get('open') or '—'}")
    print(f"next: {nxt.ref + '  ' + nxt.text if nxt else '—'}")
    errors = sum(1 for i in repo.issues if i[0] == "error")
    if errors:
        print(f"\n{errors} error(s) — run: check")
    return 0


def cmd_start(repo, args):
    root = repo.root
    task = need_task(repo, args.task)
    state = load_state(root)
    if state.get("open"):
        raise TraceError(f"{state['open']} is still open — finish it (done/block/abort) first")
    if task.status == "done" or (args.adopt and args.ignore):
        raise TraceError(f"{task.ref} is already done" if task.status == "done" else "use --adopt or --ignore, not both")
    current = snapshot(root)
    reference = reference_tree(root)
    stray = numstat(root, reference, current)
    if stray and not (args.adopt or args.ignore):
        print("Files changed outside any task since the last one closed:")
        print("\n".join(f"  {s}" for s in stray))
        print(f"\nRe-run with --adopt (count them as part of {task.ref}) or --ignore (leave them out).")
        return 2
    keep(root, "base", reference if args.adopt else current)
    save_state(root, {"open": task.ref, "started": date.today().isoformat()})
    edit_task(repo, task, status="in_progress")
    Repo(root).write_roadmap()
    print(f"started {task.ref}: {task.text}")
    return 0


def close_open(repo, raw):
    task = need_task(repo, raw)
    current = load_state(repo.root).get("open")
    if current != task.ref:
        raise TraceError(f"{task.ref} is not the open task (open: {current or 'none'})")
    return task


def cmd_restore(repo, args):
    """Undo a finished task's recorded changes; the open task records the result."""
    task = need_task(repo, args.task)
    current = load_state(repo.root).get("open")
    if not current:
        raise TraceError("open a task first (trace start NNN/TNNN) so the restored code is recorded")
    patch = os.path.join(repo.root, ".spectrace", "changes", f"{task.spec}-T{task.num:03d}.patch")
    if not os.path.exists(patch):
        raise TraceError(f"{task.ref} has no recorded patch")
    with open(patch, encoding="utf-8") as f:
        if f.readline().startswith("# patch over size limit"):
            raise TraceError(f"{task.ref}'s patch was too large to record in full; redo it by hand")
    try:
        git(repo.root, "apply", "-R", "--check", patch)
    except TraceError as e:
        raise TraceError(f"{task.ref}'s changes no longer apply cleanly; redo them instead.\n{e}")
    git(repo.root, "apply", "-R", patch)
    print(f"restored: undid {task.ref}'s changes inside {current}")
    return 0


def cmd_done(repo, args):
    root = repo.root
    task = close_open(repo, args.task)
    base, current = kept(root, "base"), snapshot(root)
    files = numstat(root, base, current)
    patch_abs = os.path.join(root, ".spectrace", "changes", f"{task.spec}-T{task.num:03d}.patch")
    if files:
        patch = diff(root, base, current, "--binary")
        if len(patch.encode()) > PATCH_LIMIT:
            patch = "# patch over size limit — file summary only\n" + "\n".join(files) + "\n"
        os.makedirs(os.path.dirname(patch_abs), exist_ok=True)
        with open(patch_abs, "w", encoding="utf-8", newline="\n") as f:
            f.write(patch)
    elif os.path.exists(patch_abs):
        os.remove(patch_abs)
    edit_task(repo, task, status="done", changes=", ".join(files) or "none")
    keep(root, "last", current)
    drop(root, "base")
    save_state(root, {})
    Repo(root).write_roadmap()
    print(f"done {task.ref}: {len(files)} file(s)")
    for f in files:
        print(f"  {f}")
    return 0


def cmd_abort(repo, args):
    task = close_open(repo, args.task)
    drop(repo.root, "base")
    save_state(repo.root, {})
    edit_task(repo, task, status="todo")
    Repo(repo.root).write_roadmap()
    print(f"aborted {task.ref}; files on disk are untouched")
    return 0


def cmd_block(repo, args):
    task = need_task(repo, args.task)
    if load_state(repo.root).get("open") == task.ref:
        drop(repo.root, "base")
        save_state(repo.root, {})
    edit_task(repo, task, status="blocked", note=f"blocked: {args.reason}")
    Repo(repo.root).write_roadmap()
    print(f"blocked {task.ref}")
    return 0


def cmd_check(repo, args):
    root = repo.root
    if not load_state(root).get("open"):
        stray = numstat(root, reference_tree(root), snapshot(root))
        if stray:
            names = ", ".join(s.split(" (")[0] for s in stray[:5]) + (" …" if len(stray) > 5 else "")
            repo.issue("warning", "working tree", f"{len(stray)} file(s) changed outside any task: {names}")
    issues = sorted(repo.issues, key=lambda x: SEVERITY[x[0]])
    for sev, where, msg, _ in issues:
        print(f"{sev.upper():<8} {where}  {msg}")
    counts = {k: sum(1 for i in issues if i[0] == k) for k in SEVERITY}
    print(f"\n{counts['error']} error(s), {counts['pending']} pending, {counts['warning']} warning(s)")
    failed = any(i[0] == "error" for i in issues) or (args.strict and any(i[0] == "pending" for i in issues))
    return 1 if failed else 0


def parse_patch(text):
    """Per-file blocks of a git patch: old/new path, status, added and removed lines."""
    blocks, b = [], None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            b = {"old": None, "new": None, "status": "modified", "added": [], "removed": [], "hunk": False}
            blocks.append(b)
        elif b is None:
            continue
        elif b["hunk"] and line and line[0] in "+-":
            if len(line[1:].strip()) >= 4:
                b["added" if line[0] == "+" else "removed"].append(line[1:].strip())
        elif line.startswith("@@"):
            b["hunk"] = True
        elif line.startswith(("rename from ", "rename to ")):
            b["status"] = "renamed"
            b["old" if line.startswith("rename from") else "new"] = line.split(" ", 2)[2]
        elif line.startswith("new file mode"):
            b["status"] = "new"
        elif line.startswith("deleted file mode"):
            b["status"] = "deleted"
        elif line.startswith("--- a/"):
            b["old"] = line[6:]
        elif line.startswith("+++ b/"):
            b["new"] = line[6:]
    return blocks


def load_patches(root):
    """{task ref: blocks} for every recorded patch, and the rename map they imply."""
    folder = os.path.join(root, ".spectrace", "changes")
    patches, renames = {}, {}
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        m = re.fullmatch(r"(\d{3})-T(\d{3})\.patch", name)
        if not m:
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            blocks = parse_patch(f.read())
        patches[f"{m.group(1)}/T{m.group(2)}"] = blocks
        for b in blocks:
            if b["status"] == "renamed":
                renames[b["old"]] = b["new"]
        # A move recorded as delete + add: same file name, mostly the same lines.
        for gone in (b for b in blocks if b["status"] == "deleted" and b["removed"]):
            for new in (b for b in blocks if b["status"] == "new"):
                same = len(set(gone["removed"]) & set(new["added"]))
                if gone["old"].rsplit("/", 1)[-1] == new["new"].rsplit("/", 1)[-1] and same >= 0.8 * len(set(gone["removed"])):
                    renames[gone["old"]] = new["new"]
    return patches, renames


def follow(root, path, renames):
    seen = set()
    while not os.path.exists(os.path.join(root, *path.split("/"))) and path in renames and path not in seen:
        seen.add(path)
        path = renames[path]
    return path


def file_presence(root, blocks, renames):
    out = []
    for b in blocks:
        if b["status"] == "deleted" or not b["new"] or not b["added"]:
            continue
        now_path = follow(root, b["new"], renames)
        label = b["new"] if now_path == b["new"] else f"{b['new']} → {now_path}"
        target, now = os.path.join(root, *now_path.split("/")), set()
        if os.path.exists(target):
            with open(target, encoding="utf-8", errors="replace") as f:
                now = {l.strip() for l in f}
        out.append({"path": label, "present": sum(1 for a in b["added"] if a in now),
                    "added": len(b["added"]), "deleted": not os.path.exists(target)})
    return out


def find_item(repo, raw):
    m = REF_RE.match(raw)
    if not m or (m.group("kind") != "A" and not m.group("spec")):
        raise TraceError("use NNN/R2, NNN/D3 or A4 (revision optional)")
    spec = repo.specs.get(m.group("spec"))
    home = repo.global_items if m.group("kind") == "A" else (spec.items if spec else {})
    item = home.get(f"{m.group('kind')}{int(m.group('num'))}")
    if not item:
        raise TraceError(f"no item {raw}")
    return item


def cmd_review(repo, args):
    item = find_item(repo, args.ref)
    repo.fingerprints[item.ref] = item.fingerprint
    repo.record_fingerprints()
    print(f"reviewed {item.ref}: current text accepted as a wording-only edit")
    return 0


def cmd_impact(repo, args):
    item = find_item(repo, args.ref)
    targets = [item]
    if item.kind == "R":
        targets += [d for d in repo.specs[item.spec].items.values() if d.kind == "D" and item.key in d.implements]
    rows = []
    patches, renames = load_patches(repo.root)
    for s in repo.specs.values():
        for t in s.tasks:
            if not any(repo.resolve(raw, s.id)[0] in targets for raw in t.covers):
                continue
            retired_by = [o.ref for s2 in repo.specs.values() for o in s2.tasks
                          if any(repo.find_task(r, s2.id) is t for r in o.retires)]
            rows.append({"task": t.ref, "owner": t.owner, "status": t.status, "kind": t.kind or "",
                         "covers": t.covers, "text": t.text, "changes": t.changes, "retired_by": retired_by,
                         "files": file_presence(repo.root, patches.get(t.ref, []), renames)})

    def label(i):
        return i.ref + (" (retired)" if i.retired else "")
    print(f"# Impact of {label(item)}\n")
    if len(targets) > 1:
        print("Design items implementing it: " + ", ".join(label(i) for i in targets[1:]) + "\n")
    if not rows:
        print("No task covers it.")
    for r in rows:
        tag = f" [{r['kind']}]" if r["kind"] else ""
        print(f"- {r['task']} [{r['owner']}] [{r['status']}]{tag} {r['text']}")
        print(f"    covers: {', '.join(r['covers'])}")
        if r["retired_by"]:
            print(f"    retired by: {', '.join(r['retired_by'])}")
        for f in r["files"]:
            where = "file deleted" if f["deleted"] else f"{f['present']}/{f['added']} added lines still present"
            print(f"    {f['path']}: {where}")
        if not r["files"] and r["status"] == "done":
            print(f"    no patch recorded ({r['changes'] or 'finished outside trace'}) — search the code by hand")
    return 0


# name: (handler, help, arguments) — "--x" is a switch, anything else positional.
COMMANDS = {
    "status": (cmd_status, "spec status, stage and next task (--write: into roadmap.md)", ("--write", "--json")),
    "start": (cmd_start, "open a task and snapshot the working tree", ("task", "--adopt", "--ignore")),
    "done": (cmd_done, "close the open task and record its changes", ("task",)),
    "abort": (cmd_abort, "close the open task without recording it", ("task",)),
    "block": (cmd_block, "mark a task blocked with a reason", ("task", "reason")),
    "check": (cmd_check, "verify the trace; exit 1 on errors (--strict: also on pending)", ("--strict",)),
    "impact": (cmd_impact, "what implemented an item: tasks, files, lines still present", ("ref",)),
    "review": (cmd_review, "accept an item's current text as a wording-only edit", ("ref",)),
    "restore": (cmd_restore, "undo a finished task's recorded changes, inside the open task", ("task",)),
}


def parser():
    p = argparse.ArgumentParser(prog="trace", description=f"spectrace trace (format v{VERSION})")
    p.add_argument("-C", dest="cwd", default=".", help="run as if started in this directory")
    p.add_argument("--version", action="version", version=f"spectrace trace {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, (_, text, arguments) in COMMANDS.items():
        s = sub.add_parser(name, help=text)
        for a in arguments:
            s.add_argument(a, action="store_true") if a.startswith("--") else s.add_argument(a)
    return p


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = parser().parse_args(argv)
    try:
        root = os.path.normpath(git(os.path.abspath(args.cwd), "rev-parse", "--show-toplevel"))
        if not os.path.isdir(os.path.join(root, "planning")):
            raise TraceError(f"no planning/ folder in {root} — run the spectrace-start skill first")
        return COMMANDS[args.cmd][0](Repo(root), args)
    except TraceError as e:
        print(f"trace: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
