"""`trace why <path[::symbol]>`: from code to the tasks and decisions behind it."""
from .. import records
from ..patches import load_patches
from . import address, matches


def exact_hits(recs, path, symbol):
    """[(task ref, what it did)] from the records, newest task first, following renames back."""
    hits = []
    for ref in sorted(recs, reverse=True):
        f = recs[ref]["files"].get(path)
        if f is None:
            continue
        if symbol is None:
            hits.append((ref, f["status"]))
        else:
            found = [s for s in f["symbols"] if matches(s["name"], symbol)]
            hits += [(ref, s["name"] + " " + s["change"] + (f" from {s['from']}" if s.get("from") else ""))
                     for s in found]
            symbol = next((s["from"] for s in found if s["name"] == symbol and s.get("from")), symbol)
        path = f.get("from", path)
    return hits


def anchored_hits(root, recs, path, symbol):
    """[(task ref, "anchored")] for tasks without a record whose patch lines land in that code now."""
    patches, renames = load_patches(root)
    hits = []
    for ref in sorted((r for r in patches if r not in recs), reverse=True):
        names = sorted(n for n in records.anchored(root, patches[ref], renames).get(path, ())
                       if symbol is None or matches(n, symbol))
        if names:
            hits.append((ref, "anchored: " + ", ".join(names)))
    return hits


def cmd_why(repo, args):
    path, symbol = address(args.address)
    recs = records.load(repo.root)
    hits = exact_hits(recs, path, symbol) + anchored_hits(repo.root, recs, path, symbol)
    print(f"# Why {args.address}\n")
    if not hits:
        print(f"outside the trace: no task recorded {args.address}")
        return 0
    for ref, what in hits:
        task = repo.find_task(ref)
        if task is None:
            print(f"- {ref} [unknown task] {what}")
            continue
        print(f"- {task.ref} [{task.status}] {task.text}\n    {what}")
        print(f"    covers: {', '.join(repo.covers_label(task))}")
        if retired := repo.retired_by(task):
            print(f"    retired by: {', '.join(retired)}")
    return 0
