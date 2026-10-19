"""`trace impact <item>`: what implemented a decision — tasks, files, symbols, and what is still there."""
import os
from collections import Counter

from .. import TraceError, records
from ..linker import hits
from ..model import REF_RE, find_item
from . import address
from .index_view import graph, not_analysed

LIST_LIMIT = 20
from ..patches import file_presence, load_patches, parse_patch


def task_added_lines(root, ref):
    """{path: Counter of the whole lines the task's patch added}, every length counted."""
    patch = os.path.join(root, ".spectrace", "changes", ref.replace("/", "-") + ".patch")
    if not os.path.exists(patch):
        return {}
    with open(patch, encoding="utf-8") as f:
        blocks = parse_patch(f.read(), min_len=0)
    return {b["new"]: Counter(b["added"]) for b in blocks if b["new"]}


def symbol_lines(root, recs, ref):
    """One line per symbol the task's record names: its change, and where it is now."""
    out, added = [], None
    for path, f in sorted(recs[ref]["files"].items()):
        for s in f["symbols"]:
            where = f"{path}::{s['name']} [{s['change']}]"
            if s["change"] == "removed":
                out.append(where)
                continue
            (now_path, now_name), body = records.live(root, recs, ref, path, s["name"])
            moved = "" if (now_path, now_name) == (path, s["name"]) else f" → {now_path}::{now_name}"
            if body is None:
                out.append(f"{where}{moved} gone")
            elif records.body_hash(body) == s["body"]:
                out.append(f"{where}{moved} unchanged")
            else:
                added = task_added_lines(root, ref) if added is None else added
                mine = added.get(path, Counter()) & Counter(l.strip() for l in body)
                kept = min(sum(mine.values()), s["lines"][0])
                out.append(f"{where}{moved} changed: {kept}/{s['lines'][0]} added lines still inside")
    return out


def anchored_lines(root, blocks, renames):
    return [f"anchored: {path}::{name}" for path, names in sorted(records.anchored(root, blocks, renames).items())
            for name in sorted(names)]


def walk(g, path, symbol, direction, depth):
    """[(depth, edge)] reachable from the code, breadth first; `in` follows dependents, `out` dependencies."""
    frontier, seen, out = {(path, symbol)}, set(), []
    for level in range(1, depth + 1):
        found = set()
        for e in g.edges:
            src, dst = (e.src_path, e.src_symbol), (e.dst_path, e.dst_symbol)
            near, far = (dst, src) if direction == "in" else (src, dst)
            if far in seen or not any(near[0] == p and hits(near[1], s) for p, s in frontier):
                continue
            if far[0] == path and hits(far[1], symbol):
                continue  # inside the code asked about
            out.append((level, e))
            found.add(far)
        seen |= found
        frontier = found
    return out


def deep_lines(g, root, recs, ref):
    """For each symbol the task introduced that still exists: its dependents (depth 2) and tests."""
    out = []
    for path, f in sorted(recs.get(ref, {}).get("files", {}).items()):
        for s in (s for s in f["symbols"] if s["change"] != "removed"):
            (now_path, now_name), body = records.live(root, recs, ref, path, s["name"])
            if body is None:
                continue
            deps = sorted({f"{e.src_path}::{e.src_symbol}" + ("?" if e.confidence == "inferred" else "")
                           for _, e in walk(g, now_path, now_name, "in", 2)})
            tests = sorted({f"{p}::{n}" for p, n, _ in g.tests_of(now_path, now_name)})
            shown = ", ".join(deps[:5]) + (f" +{len(deps) - 5} more" if len(deps) > 5 else "")
            out.append(f"deep: {now_path}::{now_name} — {len(deps)} dependent(s){': ' + shown if deps else ''}; "
                       f"tests: {', '.join(tests[:3]) + (' …' if len(tests) > 3 else '') if tests else 'none found'}")
    return out


def cmd_code_impact(repo, args):
    path, symbol = address(args.ref)
    direction, depth = args.direction or "in", int(args.depth or 2)
    if direction not in ("in", "out"):
        raise TraceError("--direction is in (what depends on it) or out (what it depends on)")
    g, db = graph(repo)
    db.close()
    rows = walk(g, path, symbol, direction, depth)
    label = "Dependents" if direction == "in" else "Dependencies"
    print(f"# Impact of {args.ref} — {label.lower()}, depth {depth}\n")
    for confidence in ("exact", "inferred"):
        group = [(lv, e) for lv, e in rows if e.confidence == confidence]
        if not group:
            continue
        print(f"{label} ({confidence}):")
        for lv, e in group[:LIST_LIMIT]:
            p, s = (e.src_path, e.src_symbol) if direction == "in" else (e.dst_path, e.dst_symbol)
            extra = f", {e.candidates} candidates" if e.confidence == "inferred" else ""
            print(f"- {p}{'::' + s if s else ''} [{e.kind}, depth {lv}{extra}] line {e.line}")
        if len(group) > LIST_LIMIT:
            print(f"+{len(group) - LIST_LIMIT} more")
    if not rows:
        print(f"No {label.lower()} found among the analysed files.")
    if direction == "in":
        tests = g.tests_of(path, symbol)
        print("\nTests that reference it: " + (", ".join(f"{p}::{s} ({c})" for p, s, c in tests) or "none found"))
    skipped = not_analysed(g)
    print("\nNot analysed: " + (", ".join(f"{len(v)} file(s) ({k})" for k, v in skipped.items()) or "nothing"))
    return 0


def cmd_impact(repo, args):
    if not REF_RE.match(args.ref):
        return cmd_code_impact(repo, args)
    item = find_item(repo, args.ref)
    targets = [item]
    if item.kind == "R":
        targets += [d for d in repo.specs[item.spec].items.values() if d.kind == "D" and item.key in d.implements]
    rows = []
    patches, renames = load_patches(repo.root)
    recs = records.load(repo.root)
    for s in repo.specs.values():
        for t in s.tasks:
            if not any(repo.resolve(raw, s.id)[0] in targets for raw in t.covers):
                continue
            rows.append({"task": t.ref, "owner": t.owner, "status": t.status, "kind": t.kind or "",
                         "covers": t.covers, "text": t.text, "changes": t.changes, "retired_by": repo.retired_by(t),
                         "files": file_presence(repo.root, patches.get(t.ref, []), renames),
                         "symbols": symbol_lines(repo.root, recs, t.ref) if t.ref in recs
                         else anchored_lines(repo.root, patches.get(t.ref, []), renames)})

    g = None
    if args.deep:
        g, db = graph(repo)
        db.close()

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
        for line in r["symbols"]:
            print(f"    {line}")
        for line in deep_lines(g, repo.root, recs, r["task"]) if g else []:
            print(f"    {line}")
        if not r["files"] and r["status"] == "done":
            print(f"    no patch recorded ({r['changes'] or 'finished outside trace'}) — search the code by hand")
    return 0
