"""Change records: which symbols a task added, changed or removed, and where every line went.

The record is computed between two trees (the task's base and the working tree when it
closes), from `git diff -U0 -M` and the symbols of each file's pre- and post-image, so it
needs neither the task's patch nor its size limit.
"""
import hashlib, json, os, re

from . import symbols as adapters
from .gitio import diff, git
from .patches import follow, parse_patch

FILE_LIMIT = 1_000_000  # bytes: a larger file is recorded at file level, and the record is partial
TASK_LIMIT = 400  # changed files: a larger task is recorded at file level, and the record is partial


def body_hash(lines):
    return hashlib.sha256("\n".join(l.rstrip("\r") for l in lines).encode("utf-8")).hexdigest()[:16]


def innermost(spans, count):
    """For each line 1..count, the index of the smallest span holding it, or None."""
    owner = [None] * (count + 2)
    for i in sorted(range(len(spans)), key=lambda i: spans[i].end - spans[i].start, reverse=True):
        for n in range(max(1, spans[i].start), min(count, spans[i].end) + 1):
            owner[n] = i
    return owner


def show(root, tree, path):
    return git(root, "show", f"{tree}:{path}", raw=True)


class Side:
    """One image of a file: its lines, spans, and which span owns each line."""

    def __init__(self, path, text, file_level):
        self.lines = text.splitlines() if text is not None else []
        self.spans = [] if file_level or text is None else adapters.symbols(path, text)
        self.owner = innermost(self.spans, len(self.lines))
        self.by_name = {s.name: s for s in self.spans if s.kind != "import"}

    def hash(self, span):
        return body_hash(self.lines[span.start - 1:span.end])

    def tail_hash(self, span):
        return body_hash(self.lines[span.start:span.end])


def file_record(root, a, b, block, file_level, skipped):
    old_path, new_path = block["old"], block["new"]
    path = new_path or old_path
    lang = "file" if file_level else adapters.language(path)
    rec = {"status": block["status"], "lang": lang,
           "lines": [len(block["added_at"]), len(block["removed_at"])], "symbols": [], "other": {}}
    if block["status"] == "renamed":
        rec["from"] = old_path
    try:
        pre = Side(old_path, None if block["status"] == "new" else show(root, a, old_path), lang == "file")
        post = Side(new_path, None if block["status"] == "deleted" else show(root, b, new_path), lang == "file")
    except (SyntaxError, ValueError) as e:  # ValueError: a null byte in Python source
        skipped.append({"path": path, "reason": f"{type(e).__name__}: {e}".splitlines()[0][:200]})
        pre, post, rec["lang"] = Side(old_path, None, True), Side(new_path, None, True), "file"
    counts, other = {}, {}

    def attribute(side, numbers, column):
        for n in numbers:
            i = side.owner[n] if n < len(side.owner) else None
            span = side.spans[i] if i is not None else None
            if span is None or span.kind == "import":
                bucket = "imports" if span else ("file" if rec["lang"] == "file" else "module")
                other.setdefault(bucket, [0, 0])[column] += 1
            else:
                counts.setdefault(span.name, [0, 0])[column] += 1
    attribute(post, block["added_at"], 0)
    attribute(pre, block["removed_at"], 1)
    added = [n for n in post.by_name if n not in pre.by_name]
    removed = [n for n in pre.by_name if n not in post.by_name]
    renamed = {}
    for new in added:
        s = post.by_name[new]
        match = next((old for old in removed if s.end > s.start and old not in renamed.values()
                      and pre.by_name[old].kind == s.kind
                      and pre.tail_hash(pre.by_name[old]) == post.tail_hash(s)), None)
        if match:
            renamed[new] = match
    for name in sorted(set(post.by_name) | set(pre.by_name)):
        if name in renamed.values():
            continue
        live = name in post.by_name
        span = post.by_name[name] if live else pre.by_name[name]
        if name in renamed:
            change = "renamed"
        elif name in added:
            change = "added"
        elif name in removed:
            change = "removed"
        elif name in counts:
            change = "modified"
        else:
            continue
        lines = counts.get(name, [0, 0])
        if name in renamed:
            gone = counts.get(renamed[name], [0, 0])
            lines = [lines[0] + gone[0], lines[1] + gone[1]]
        entry = {"name": name, "kind": span.kind, "change": change, "lines": lines,
                 "body": (post if live else pre).hash(span)}
        if span.sig is not None:
            entry["sig"] = span.sig
        old = pre.by_name.get(renamed.get(name, name)) if live else None
        if old is not None and change in ("modified", "renamed") and old.sig != span.sig:
            entry["sig_from"] = old.sig
        if name in renamed:
            entry["from"] = renamed[name]
        rec["symbols"].append(entry)
    rec["other"] = {k: v for k, v in sorted(other.items())}
    return rec


def record(root, a, b):
    """The change record between trees `a` and `b`. Never raises: what fails is said in the record."""
    try:
        blocks = [x for x in parse_patch(diff(root, a, b, "-U0"), min_len=0) if x["old"] or x["new"]]
    except Exception as e:  # noqa: BLE001 — `done` must close the task whatever the recorder hits
        return {"files": {}, "partial": True, "skipped": [{"path": "*", "reason": str(e)[:200]}]}
    out = {"files": {}, "partial": len(blocks) > TASK_LIMIT, "skipped": []}
    for block in blocks:
        path = block["new"] or block["old"]
        if block["binary"]:
            out["files"][path] = {"status": block["status"], "lang": "file", "lines": None,
                                  "symbols": [], "other": {}}
            continue
        try:
            big = any(size(root, t, p) > FILE_LIMIT for t, p in ((a, block["old"]), (b, block["new"])) if p)
            out["partial"] = out["partial"] or big
            out["files"][path] = file_record(root, a, b, block, out["partial"], out["skipped"])
        except Exception as e:  # noqa: BLE001
            out["partial"] = True
            out["skipped"].append({"path": path, "reason": f"{type(e).__name__}: {e}".splitlines()[0][:200]})
    return out


def size(root, tree, path):
    return int(git(root, "cat-file", "-s", f"{tree}:{path}"))


def accounted(rec):
    """((attributed, total) added, (attributed, total) removed) over the text files of a record."""
    out = [[0, 0], [0, 0]]
    for f in rec.get("files", {}).values():
        if f.get("lines") is None:
            continue
        for column in (0, 1):
            out[column][0] += sum(s["lines"][column] for s in f["symbols"]) + sum(v[column] for v in f["other"].values())
            out[column][1] += f["lines"][column]
    return tuple(map(tuple, out))


def unaccounted(rec):
    """Lines of the record whose symbols and buckets do not add up to the file totals."""
    missing = 0
    for f in rec.get("files", {}).values():
        if f.get("lines") is None:
            continue
        for column in (0, 1):
            total = sum(s["lines"][column] for s in f["symbols"]) + sum(v[column] for v in f["other"].values())
            missing += abs(f["lines"][column] - total)
    return missing


def write(root, ref, rec):
    """Write the record of task `ref`, or remove it when `rec` is None."""
    path = os.path.join(root, ".spectrace", "changes", ref.replace("/", "-") + ".touch.json")
    if rec is None:
        if os.path.exists(path):
            os.remove(path)
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def changed_symbols(rec, limit=8):
    """`path::name (change)` for the symbols a record names, at most `limit`, then `+N more`."""
    names = [f"{p}::{s['name']} ({s['change']})" for p, f in sorted(rec["files"].items()) for s in f["symbols"]]
    return names[:limit] + ([f"+{len(names) - limit} more"] if len(names) > limit else [])


def current(root, path):
    """(lines, {name: span}) of a file in the working tree; None when it is missing or does not parse."""
    full = os.path.join(root, *path.split("/"))
    if not os.path.isfile(full):
        return None
    with open(full, encoding="utf-8", errors="replace", newline="") as f:
        text = f.read()
    try:
        spans = adapters.symbols(path, text)
    except (SyntaxError, ValueError):
        return None
    return text.splitlines(), {s.name: s for s in spans if s.kind != "import"}


def live(root, recs, ref, path, name):
    """Where a symbol a task recorded is now: ((path, name) today, its current lines or None).

    Later records' file and symbol renames are followed, so a renamed symbol reports its new name."""
    for later in sorted(r for r in recs if r > ref):
        files = recs[later]["files"]
        moved = next((p for p, f in files.items() if f.get("from") == path), None)
        path = moved or path
        name = next((s["name"] for s in files.get(path, {}).get("symbols", []) if s.get("from") == name), name)
    now = current(root, path)
    if now is None or name not in now[1]:
        return (path, name), None
    span = now[1][name]
    return (path, name), now[0][span.start - 1:span.end]


def anchored(root, blocks, renames):
    """{current path: symbol names} for a task without a record, from its patch (labelled `anchored`).

    Each added line is matched by text to the current file; a line found exactly once
    gives the symbol holding it there. Ambiguous or missing lines stay unmapped."""
    out = {}
    for b in blocks:
        if b["status"] == "deleted" or not b["new"] or not b["added"]:
            continue
        path = follow(root, b["new"], renames)
        now = current(root, path)
        if now is None:
            continue
        lines, spans = now
        owner = innermost(list(spans.values()), len(lines))
        names = list(spans)
        where = {}
        for n, line in enumerate(lines, 1):
            where.setdefault(line.strip(), []).append(n)
        found = {names[owner[where[a][0]]] for a in b["added"]
                 if len(where.get(a, [])) == 1 and owner[where[a][0]] is not None}
        if found:
            out.setdefault(path, set()).update(found)
    return out


def load(root):
    """{task ref: record} for every record in .spectrace/changes/."""
    folder, out = os.path.join(root, ".spectrace", "changes"), {}
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if m := re.fullmatch(r"(\d{3})-T(\d{3})\.touch\.json", name):
            try:
                with open(os.path.join(folder, name), encoding="utf-8") as f:
                    out[f"{m.group(1)}/T{m.group(2)}"] = json.load(f)
            except (OSError, ValueError):
                continue
    return out
