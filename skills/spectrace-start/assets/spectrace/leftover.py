"""Code of a retired task that is still there, unchanged, after its cleanup is done; and `trace keep`."""
import json, os

from . import TraceError, records
from .views import address

KEEPS = ".spectrace/keeps.json"


def load_keeps(root):
    try:
        with open(os.path.join(root, *KEEPS.split("/")), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def leftovers(repo, recs):
    """[(cleanup task, retired task ref, address)] for each symbol a retired task added that is unchanged."""
    kept = {k["symbol"] for k in load_keeps(repo.root)}
    # Order of tasks done in the repository across all specs
    order = [t.ref for s in repo.specs.values() for t in s.tasks if t.status == "done"]
    indices = {ref: i for i, ref in enumerate(order)}
    out = []
    for spec in repo.specs.values():
        for cleanup in (t for t in spec.tasks if t.status == "done"):
            cleanup_idx = indices.get(cleanup.ref, -1)
            for raw in cleanup.retires:
                target = repo.find_task(raw, spec.id)
                if target is None or target.ref not in recs:
                    continue
                for path, f in sorted(recs[target.ref]["files"].items()):
                    for s in (s for s in f["symbols"] if s["change"] == "added"):
                        (now_path, now_name), body = records.live(repo.root, recs, target.ref, path, s["name"])
                        where = f"{now_path}::{now_name}"
                        # D6@2: if a task done after cleanup recorded the symbol again, it is not a leftover
                        reinstated = any(
                            indices.get(ref, -1) > cleanup_idx and
                            any(sym["name"] == now_name and sym["change"] in ("added", "modified", "renamed")
                                for sym in recs[ref]["files"].get(now_path, {}).get("symbols", []))
                            for ref in recs
                        )
                        if not reinstated and body is not None and records.body_hash(body) == s["body"] and where not in kept:
                            out.append((cleanup, target.ref, where))
    return out


def cmd_keep(repo, args):
    if not args.reason.strip():
        raise TraceError("keep needs a reason: why this code stays although its decision was retired")
    path, symbol = address(args.address)
    if symbol is None:
        raise TraceError("keep takes a symbol: path::Qualified.name")
    recs = records.load(repo.root)
    task = next((ref for ref in sorted(recs, reverse=True)
                 if any(s["name"] == symbol and s["change"] == "added"
                        for s in recs[ref]["files"].get(path, {}).get("symbols", []))), None)
    if task is None:
        raise TraceError(f"no task recorded adding {path}::{symbol}")
    keeps = [k for k in load_keeps(repo.root) if k["symbol"] != f"{path}::{symbol}"]
    keeps.append({"reason": args.reason.strip(), "symbol": f"{path}::{symbol}", "task": task})
    with open(os.path.join(repo.root, *KEEPS.split("/")), "w", encoding="utf-8", newline="\n") as f:
        json.dump(sorted(keeps, key=lambda k: k["symbol"]), f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"kept {path}::{symbol} (added by {task}): {args.reason.strip()}")
    return 0
