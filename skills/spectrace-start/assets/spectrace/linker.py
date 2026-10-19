"""Links the cached facts into relations between symbols, each with a confidence.

`exact`: bound by an import, defined in the same module, or `self.x` through the class and
its bases with one answer. `inferred`: an attribute name matched across the repo, with
its number of candidates. A name that resolves to nothing in the repo is dropped and
counted in the resolution rate; names bound to modules outside the repo are external.
"""
from collections import namedtuple

from .symbols import matches

EXTERNAL = ("external", None)
Edge = namedtuple("Edge", "src_path src_symbol dst_path dst_symbol confidence candidates line kind")


def module_names(path, paths):
    """Dotted names a Python file is importable as: from the repo root, `src/`, and its package root."""
    parts = path[:-3].split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    top = len(parts) - 1  # parts[:top] is the file's folder; climb while it is a package
    while top > 0 and "/".join(parts[:top]) + "/__init__.py" in paths:
        top -= 1
    names = {".".join(parts), ".".join(parts[top:])}
    if parts[0] == "src":
        names.add(".".join(parts[1:]))
    return {n for n in names if n}


def hits(name, symbol):
    """Does code named `name` fall under the queried `symbol` (None: the whole file)?"""
    return symbol is None or (name is not None and matches(name, symbol))


class Graph:
    def __init__(self, db):
        self.files = {r[0]: {"lang": r[1], "test": bool(r[2]), "status": r[3]}
                      for r in db.execute("SELECT path, lang, test, status FROM files")}
        self.defs = {}
        for path, name, kind in db.execute("SELECT path, name, kind FROM symbols"):
            self.defs.setdefault(path, {})[name] = kind
        py = {p for p, f in self.files.items() if p.endswith(".py")}
        self.modules = {n: p for p in sorted(py) for n in module_names(p, py)}
        self.by_last = {}
        for path, names in self.defs.items():
            for name in names:
                self.by_last.setdefault(name.rsplit(".", 1)[-1], []).append((path, name))
        self.bindings = {}
        for path, bound, module, name, _ in db.execute("SELECT * FROM imports"):
            self.bindings.setdefault(path, {})[bound] = self.resolve_import(path, module, name)
        refs = list(db.execute("SELECT path, symbol, kind, name, base, line FROM refs"))
        self.bases = {(p, s): n for p, s, k, n, b, _ in refs if k == "base"}
        self.resolved, self.dropped, best = {}, {}, {}
        for ref in refs:
            for e in self.link(*ref):
                key = e[:4]
                if key not in best or (best[key].confidence, best[key].line) > (e.confidence, e.line):
                    best[key] = e
        self.edges = sorted(best.values(), key=lambda e: (e.src_path, e.src_symbol, e.dst_path, e.dst_symbol or ""))

    # --- resolution ---

    def module_file(self, from_path, module):
        if not module.startswith("."):
            return self.modules.get(module)
        level = len(module) - len(module.lstrip("."))
        base = from_path.split("/")[:-1]
        base = base[:len(base) - (level - 1)] if level > 1 else base
        rest = [p for p in module.lstrip(".").split(".") if p]
        stem = "/".join(base + rest)
        return next((p for p in (f"{stem}.py", f"{stem}/__init__.py") if p in self.files), None)

    def resolve_import(self, path, module, name):
        """(path, symbol or None) the import binds, or None for a module outside the repo."""
        if name is None:
            target = self.module_file(path, module)
            return (target, None) if target else None
        sub = self.module_file(path, module + name if module.endswith(".") else f"{module}.{name}")
        if sub:
            return sub, None
        target = self.module_file(path, module)
        if not target:
            return None
        return target, (name if name in self.defs.get(target, {}) else None)

    def class_member(self, path, cls, member, seen=()):
        """(path, Class.member) through the class and its bases; EXTERNAL when a base is outside the repo."""
        if f"{cls}.{member}" in self.defs.get(path, {}):
            return path, f"{cls}.{member}"
        base = self.bases.get((path, cls))
        if base is None or (path, cls) in seen:
            return None
        binds = self.bindings.get(path, {})
        if base in binds and binds[base] is None:
            return EXTERNAL
        target = binds.get(base) or ((path, base) if base in self.defs.get(path, {}) else None)
        if target and target[1]:
            return self.class_member(target[0], target[1], member, seen + ((path, cls),))
        return None

    def link(self, path, symbol, kind, name, base, line):
        lang = self.files.get(path, {}).get("lang", "python")
        edge_kind = "subclass" if kind == "base" else "uses"

        def exact(dst):
            self.resolved[lang] = self.resolved.get(lang, 0) + 1
            return [Edge(path, symbol, dst[0], dst[1], "exact", 1, line, edge_kind)]

        def drop():
            self.dropped[lang] = self.dropped.get(lang, 0) + 1
            return []
        binds = self.bindings.get(path, {})
        if base is None and kind != "attr":
            if name in binds:
                return exact(binds[name]) if binds[name] else []
            if name in self.defs.get(path, {}):
                return exact((path, name))
            return drop()
        if base in ("self", "cls") and symbol != "(module)":
            cls = symbol.rsplit(".", 1)[0] if "." in symbol else symbol
            hit = self.class_member(path, cls, name)
            if hit is EXTERNAL:
                return []
            if hit is None and cls in self.defs.get(path, {}):
                hit = (path, cls)  # an instance attribute: it belongs to the class
            return exact(hit) if hit else drop()
        if base is not None and base in binds:
            target = binds[base]
            if target is None:
                return []  # an attribute of something outside the repo
            member = f"{target[1]}.{name}" if target[1] else name
            if member in self.defs.get(target[0], {}):
                return exact((target[0], member))
        candidates = self.by_last.get(name, [])
        if not candidates:
            return []  # most likely a method of a library type: external, not counted
        self.resolved[lang] = self.resolved.get(lang, 0) + 1
        return [Edge(path, symbol, p, n, "inferred", len(candidates), line, edge_kind) for p, n in candidates]

    # --- queries ---

    def mark_tests(self, paths):
        """Also treat these files as tests (recorded by a `kind: test` task)."""
        for p in paths:
            if p in self.files:
                self.files[p]["test"] = True

    def is_test(self, path):
        return self.files.get(path, {}).get("test", False)

    def tests_of(self, path, symbol=None):
        """Test symbols whose resolved references include that code: [(path, symbol, confidence)]."""
        return sorted({(e.src_path, e.src_symbol, e.confidence) for e in self.edges
                       if self.is_test(e.src_path) and e.dst_path == path and hits(e.dst_symbol, symbol)})

    def resolution_rate(self, lang="python"):
        done, lost = self.resolved.get(lang, 0), self.dropped.get(lang, 0)
        return done / (done + lost) if done + lost else None
