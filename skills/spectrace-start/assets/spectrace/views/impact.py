"""`trace impact <item>`: what implemented a decision — tasks, files, symbols, and what is still there."""
import os
from collections import Counter

from .. import records
from ..model import find_item
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


def cmd_impact(repo, args):
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
        if not r["files"] and r["status"] == "done":
            print(f"    no patch recorded ({r['changes'] or 'finished outside trace'}) — search the code by hand")
    return 0
