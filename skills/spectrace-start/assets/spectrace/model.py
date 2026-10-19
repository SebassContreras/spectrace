"""The planning files as objects: items, tasks, specs and the Repo that traces them."""
import hashlib, json, os, re

from . import TraceError, records
from .leftover import leftovers
from .gitio import git
from .patches import load_patches

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
BLOCKED_RE = re.compile(r"^\s+└─ blocked: (?:conflicts (?P<ref>[^:\s]+)\s*:\s*(?P<why>.*?)\s*$)?")
SEVERITY = {"error": 0, "pending": 1, "warning": 2}


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


def text_lines(root):
    """(path, line number, line) of every text file outside history, retired item lines left out.

    History is `.spectrace/` and the `tasks.md` and `changes.md` files under `planning/`."""
    listed = git(root, "ls-files", "-z", "-co", "--exclude-standard").split("\0")
    for rel in filter(None, listed):
        history = rel.startswith(".spectrace/") or (
            rel.startswith("planning/") and rel.rsplit("/", 1)[-1] in ("tasks.md", "changes.md"))
        full = os.path.join(root, *rel.split("/"))
        if history or not os.path.isfile(full) or os.path.getsize(full) > 1_000_000:
            continue
        with open(full, "rb") as f:
            data = f.read()
        if b"\0" in data[:1024]:
            continue
        for n, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            if not RETIRED_RE.match(line):
                yield rel, n, line


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
        self.conflict = None  # (ref, why) when the last block note reads `conflicts <ref>: <why>`

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
            if task and (b := BLOCKED_RE.match(line)):  # the latest block reason wins
                task.conflict = (b.group("ref"), b.group("why")) if b.group("ref") else None
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

    def retired_by(self, task):
        """Refs of the tasks whose `retires:` names `task`."""
        return [o.ref for s in self.specs.values() for o in s.tasks
                if any(self.find_task(r, s.id) is task for r in o.retires)]

    def covers_label(self, task):
        """A task's covers, each with its spec and a `retired` or `now @N` flag."""
        out = []
        for raw in task.covers:
            item, rev = self.resolve(raw, task.spec)
            flag = "" if item is None else " (retired)" if item.retired else "" if rev == item.rev else f" (now @{item.rev})"
            out.append((raw if raw.startswith("A") or "/" in raw else f"{task.spec}/{raw}") + flag)
        return out

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
                if t.status == "blocked" and t.owner == "agent" and t.conflict:
                    self.issue("pending", t.ref, f"decision conflict: {t.conflict[0]} — {t.conflict[1]}; keep it, edit it "
                               "or retire it (spectrace-change), then resume with start", spec.id)
                if t.status == "done" and t.owner == "agent" and t.changes is None:
                    self.issue("warning", t.ref, "done without changes: (finished outside trace)", spec.id)
            self.uncovered(spec)
        self.deleted_mentions()
        self.records = records.load(self.root)
        self.leftover()
        self.record_totals()
        self.changed_text()
        self.record_guard()

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

    def guarded_refs(self):
        """{item ref: spec ids} whose text is guarded: built-on items, and every active A item."""
        out = self.built_on()
        for item in self.global_items.values():
            if not item.retired:
                out.setdefault(item.ref, set())
        return out

    def changed_text(self):
        """A guarded item's meaning must not change without a revision bump."""
        for item_ref, specs in self.guarded_refs().items():
            item = next(i for i in self.items() if i.ref == item_ref)
            seen = self.fingerprints.get(item_ref)
            if seen and seen != item.fingerprint:
                under = "under finished work" if specs else "without a revision bump"
                for sid in sorted(specs) or [None]:
                    self.issue("pending", item.where, f"text of {item_ref} changed {under}: bump its revision "
                               f"(spectrace-change), or `review {item_ref.split('@')[0]}` if wording only", sid)

    # --- record guard: no decision changes or disappears without a changes.md entry ---

    def all_items(self):
        """{item ID: item} for every item, retired ones included; the ID has no revision."""
        out = {i.key: i for i in self.global_items.values()}
        for spec in self.specs.values():
            out.update({f"{spec.id}/{i.key}": i for i in spec.items.values()})
        return out

    def built_ids(self):
        """IDs of items a finished task covers, at any revision."""
        out = set()
        for spec in self.specs.values():
            for t in (t for t in spec.tasks if t.status == "done"):
                for raw in t.covers:
                    if (m := REF_RE.match(raw)) and m.group("kind") != "A":
                        out.add(f"{m.group('spec') or spec.id}/{m.group('kind')}{int(m.group('num'))}")
        return out

    def has_entry(self, item):
        rel = f"{self.specs[item.spec].dir}/changes.md" if item.spec else "planning/changes.md"
        try:
            text = "".join(read_lines(self.path(rel)))
        except OSError:
            return False
        return re.search(rf"\b{item.key}@{item.rev}\b", text) is not None

    def record_guard(self):
        """Findings on guarded IDs seen before: gone without retiring, or bumped or retired with no entry."""
        self.unrecorded = set()
        current, built = self.all_items(), self.built_ids()
        for iid, (rev, retired) in self.fingerprints.get("_ids", {}).items():
            if not (iid.startswith("A") or iid in built):
                continue
            sid = iid.split("/")[0] if "/" in iid else None
            item = current.get(iid)
            if item is None:
                self.unrecorded.add(iid)
                home = self.specs[sid].dir if sid in self.specs else "planning/architecture.md"
                self.issue("pending", home, f"{iid} disappeared without being retired: put it back struck "
                           "through (spectrace-change)", sid)
            elif (item.rev > rev or (item.retired and not retired)) and not self.has_entry(item):
                self.unrecorded.add(iid)
                what = "retired" if item.retired and not retired else f"bumped from @{rev}"
                self.issue("pending", item.where, f"{item.ref} {what} with no changes.md entry naming "
                           f"{item.key}@{item.rev} (spectrace-change)", sid)

    def record_fingerprints(self):
        guarded = self.guarded_refs()
        fresh = {i.ref: i.fingerprint for i in self.items()}
        kept = {k: v for k, v in self.fingerprints.items() if k in guarded}
        seen = self.fingerprints.get("_ids", {})
        ids = {iid: [i.rev, i.retired] for iid, i in self.all_items().items()}
        ids.update({iid: seen[iid] for iid in self.unrecorded})  # findings keep their baseline
        merged = {**fresh, **kept, "_ids": dict(sorted(ids.items()))}
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
        for rel, n, line in text_lines(self.root):
            for path, ref in deleted.items():
                if path in line:
                    self.issue("pending", f"{rel}:{n}", f"mentions {path}, deleted by {ref}", ref[:3])

    def leftover(self):
        """Code a retired task added must be gone once its cleanup is done, or kept with a reason."""
        for cleanup, ref, where in leftovers(self, self.records):
            self.issue("pending", cleanup.ref, f"leftover: {where}, added by {ref}, is still there unchanged: "
                       f'remove it, or `keep {where} "<reason>"`', cleanup.spec)

    def record_totals(self):
        """A record's symbols and buckets must add up to its file totals (the recorder's fault if not)."""
        for ref, rec in self.records.items():
            if missing := records.unaccounted(rec):
                self.issue("warning", f".spectrace/changes/{ref.replace('/', '-')}.touch.json",
                           f"unaccounted: {missing} line(s) of {ref}'s record are in no symbol or bucket", ref[:3])

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
