"""`trace packet <task>`: a review packet of facts, deterministic, as Markdown or `--json`."""
import json, re

from .. import TraceError, records
from ..gitio import git, reference_tree, snapshot
from .impact import walk
from .index_view import graph, not_analysed

TOP = 10  # dependents listed per symbol
CHANGE_RE = re.compile(r"changes/(\d{3})-T(\d{3})\.(?:patch|touch\.json)$")


def symbols_of(rec):
    keep = ("from", "sig", "sig_from")
    return [{"path": p, "name": s["name"], "kind": s["kind"], "change": s["change"],
             **{k: s[k] for k in keep if s.get(k) is not None}}
            for p, f in sorted(rec.get("files", {}).items()) for s in f["symbols"]]


def signals(p, ref_counts):
    """Facts a reviewer weighs, never a score: in a fixed order."""
    out = []
    for s in p["symbols"]:
        key = f"{s['path']}::{s['name']}"
        if "sig_from" in s:
            out.append(f"signature changed: {key} {s['sig_from']} → {s['sig']}")
        if s["change"] == "removed" and ref_counts.get(s["name"].rsplit(".", 1)[-1]):
            out.append(f"removed but still referenced: {key} — {ref_counts[s['name'].rsplit('.', 1)[-1]]} "
                       "reference(s) by that name (inferred)")
    for key, rows in sorted(p["dependents"].items()):
        if rows:
            out.append(f"{len(rows)} dependent(s): {key}")
    for key, tests in sorted(p["tests"].items()):
        if not tests:
            out.append(f"no test references: {key}")
    if p["partial"]:
        out.append("partial record: some files were read at file level")
    if p["not_analysed"]:
        out.append(f"{sum(len(v) for v in p['not_analysed'].values())} file(s) not analysed")
    return out


def dependents(g, path, name):
    rows = sorted({(e.src_path, e.src_symbol or "", e.confidence, e.candidates) for _, e in walk(g, path, name, "in", 1)})
    return [{"path": p, "symbol": s, "confidence": c, **({"candidates": n} if c == "inferred" else {})}
            for p, s, c, n in rows]


def assemble(repo, g, db, tasks, rec):
    """The packet for some tasks and the record of their changes."""
    decisions = sorted({label for t in tasks for label in repo.covers_label(t)})
    syms = symbols_of(rec)
    deps, tests = {}, {}
    for s in syms:
        if s["change"] != "removed":
            key = f"{s['path']}::{s['name']}"
            deps[key] = dependents(g, s["path"], s["name"])
            tests[key] = [f"{p}::{n}" for p, n, _ in g.tests_of(s["path"], s["name"])]
    specs = {t.spec for t in tasks}
    incidents = sorted(f"{sev} {where}: {msg}" for sev, where, msg, sid in repo.issues if sid in specs)
    skipped = {k: v for k, v in not_analysed(g).items()}
    if rec.get("skipped"):
        skipped["skipped by the record"] = sorted(s["path"] for s in rec["skipped"])
    p = {"tasks": sorted(t.ref for t in tasks), "decisions": decisions, "symbols": syms,
         "dependents": deps, "tests": tests, "incidents": incidents,
         "partial": bool(rec.get("partial")), "not_analysed": skipped}
    p["signals"] = signals(p, dict(db.execute("SELECT name, count(*) FROM refs GROUP BY name")))
    return p


def render(p):
    out = [f"# Review packet: {', '.join(p['tasks']) or 'no task'}", "", "## Decisions"]
    out += [f"- {d}" for d in p["decisions"]] or ["- none: the change is outside any task"]
    out += ["", "## Symbols"]
    out += [f"- {s['path']}::{s['name']} ({s['kind']}, {s['change']}{', from ' + s['from'] if s.get('from') else ''})"
            for s in p["symbols"]] or ["- none recorded"]
    out += ["", "## Dependents"]
    for key, rows in sorted(p["dependents"].items()):
        if rows:
            shown = ", ".join(f"{r['path']}::{r['symbol']}" + (f" (inferred, {r['candidates']})" if
                              r["confidence"] == "inferred" else "") for r in rows[:TOP])
            out.append(f"- {key}: {shown}" + (f" +{len(rows) - TOP} more" if len(rows) > TOP else ""))
    if not any(p["dependents"].values()):
        out.append("- no dependents found among the analysed files")
    out += ["", "## Tests"]
    out += [f"- {key}: {', '.join(t) if t else 'none found'}" for key, t in sorted(p["tests"].items())] or ["- none"]
    out += ["", "## Incidents"] + ([f"- {i}" for i in p["incidents"]] or ["- none"])
    out += ["", "## Severity signals"] + ([f"- {s}" for s in p["signals"]] or ["- none"])
    out += ["", "## Not analysed"]
    out += [f"- {reason}: {len(paths)} — {', '.join(paths[:5])}" + (f" +{len(paths) - 5} more" if len(paths) > 5 else "")
            for reason, paths in sorted(p["not_analysed"].items())] or ["- nothing"]
    return "\n".join(out) + "\n"


def emit(p, as_json):
    if as_json:
        print(json.dumps(p, indent=1, sort_keys=True, ensure_ascii=False))
    else:
        print(render(p), end="")


def added_tasks(repo, base, current):
    """Tasks whose patch or record the diff adds under .spectrace/changes/."""
    names = git(repo.root, "diff", "--name-only", "--diff-filter=A", base, current, "--", ".spectrace/changes")
    refs = sorted({f"{m.group(1)}/T{m.group(2)}" for m in map(CHANGE_RE.search, names.splitlines()) if m})
    return [t for t in map(repo.find_task, refs) if t]


def diff_packet(repo, args):
    """The packet of a diff: --base (a git ref; default the tree of the last closed task) to the working tree."""
    try:
        base = git(repo.root, "rev-parse", "--verify", "--quiet", f"{args.base}^{{tree}}") if args.base \
            else reference_tree(repo.root)
    except TraceError:
        raise TraceError(f"no git ref {args.base!r}; on CI, check out with full history (fetch-depth: 0)")
    current = snapshot(repo.root)
    g, db = graph(repo, memory=True)
    try:
        return assemble(repo, g, db, added_tasks(repo, base, current), records.record(repo.root, base, current))
    finally:
        db.close()


def cmd_packet(repo, args):
    if args.diff:
        emit(diff_packet(repo, args), args.json)
        return 0
    if not args.task:
        raise TraceError("give a task (NNN/TNNN), or --diff")
    task = repo.find_task(args.task)
    if task is None:
        raise TraceError(f"no task {args.task} (use NNN/TNNN)")
    if task.ref not in repo.records:
        raise TraceError(f"{task.ref} has no change record (finished before records, or not done yet)")
    g, db = graph(repo)
    try:
        emit(assemble(repo, g, db, [task], repo.records[task.ref]), args.json)
    finally:
        db.close()
    return 0
