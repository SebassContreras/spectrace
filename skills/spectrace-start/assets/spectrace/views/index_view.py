"""`trace index [--status] [--rebuild] [--dump]`: build the code index and say what it holds."""
import json

from .. import index
from ..linker import Graph
from ..patches import follow, load_patches


def graph(repo, rebuild=False, memory=False):
    """The linked graph over a freshly refreshed index: what every index-reading command uses.

    A file is a test by path or name, or because a `kind: test` task recorded it."""
    db = index.refresh(repo.root, rebuild, memory)
    g = Graph(db)
    recs = repo.records
    g.mark_tests(p for s in repo.specs.values() for t in s.tasks if t.kind == "test" and t.ref in recs
                 for p in recs[t.ref]["files"])
    return g, db


def not_analysed(g):
    """{reason: [paths]} for files whose relations were not read."""
    out = {}
    for path, f in sorted(g.files.items()):
        if f["status"] != "ok":
            out.setdefault(f["status"], []).append(path)
    return out


def coverage(repo, g):
    """Symbols by how the trace knows their file: an exact record, an anchored patch, or neither."""
    patches, renames = load_patches(repo.root)
    exact = {p for rec in repo.records.values() for p in rec["files"]}
    anchored = {follow(repo.root, b["new"], renames) for blocks in patches.values() for b in blocks if b["new"]}
    out = {"exact": 0, "anchored": 0, "outside the trace": 0}
    for path, names in g.defs.items():
        key = "exact" if path in exact else "anchored" if path in anchored else "outside the trace"
        out[key] += len(names)
    return out


def cmd_index(repo, args):
    g, db = graph(repo, args.rebuild)
    try:
        if args.dump:
            tables = {t: [list(r) for r in db.execute(f"SELECT * FROM {t} ORDER BY 1, 2")]
                      for t in ("files", "symbols", "imports", "refs")}
            print(json.dumps(tables, indent=1, ensure_ascii=False))
            return 0
        symbols = db.execute("SELECT count(*) FROM symbols").fetchone()[0]
        print(f"indexed {len(g.files)} file(s), {symbols} symbol(s), {len(g.edges)} relation(s)")
        if args.status:
            counts = coverage(repo, g)
            total = sum(counts.values()) or 1
            print("trace coverage: " + ", ".join(f"{counts[k]} {k} ({100 * counts[k] // total}%)"
                                                 for k in ("exact", "anchored", "outside the trace")))
            for lang in sorted(set(g.resolved) | set(g.dropped)):
                rate = g.resolution_rate(lang)
                print(f"resolution rate ({lang}): {100 * rate:.1f}% of {g.resolved.get(lang, 0) + g.dropped.get(lang, 0)} "
                      "references to repo code (external ones not counted)")
            for reason, paths in not_analysed(g).items():
                shown = ", ".join(paths[:5]) + (f" +{len(paths) - 5} more" if len(paths) > 5 else "")
                print(f"not analysed ({reason}): {len(paths)} — {shown}")
    finally:
        db.close()
    return 0
