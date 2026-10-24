"""The trace commands: one handler per command, and the table the parser is built from."""
import json, os
from datetime import date

from . import TraceError, records
from .gitio import git, snapshot, keep, kept, drop, reference_tree, diff, numstat
from .model import SEVERITY, Repo, find_item
from .state import load_state, save_state, edit_task
from .leftover import cmd_keep
from .mentions import removed_mentions, removed_terms
from .audit import run_audit
from .views.impact import cmd_impact
from .views.index_view import cmd_index, graph
from .views.locate import cmd_locate
from .views.packet import cmd_packet
from .views.why import cmd_why

PATCH_LIMIT = 200_000


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
    print(f"\nopen: {state.get('open') or '—'}\nnext: {nxt.ref + '  ' + nxt.text if nxt else '—'}")
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
        touched = records.changed_symbols(records.record(root, reference, current))
        print("Files changed outside any task since the last one closed:\n" + "\n".join(f"  {s}" for s in stray) +
              ("\nSymbols: " + ", ".join(touched) if touched else "") +
              f"\n\nRe-run with --adopt (count them as part of {task.ref}) or --ignore (leave them out).")
        return 2
    keep(root, "base", reference if args.adopt else current)
    save_state(root, {"open": task.ref, "started": date.today().isoformat()})
    edit_task(repo, task, status="in_progress")
    Repo(root).write_roadmap()
    print(f"started {task.ref}: {task.text}")
    for raw in task.covers:
        if item := repo.resolve(raw, task.spec)[0]:
            print(f"  {raw}: {item.text}")
    return 0


def close_open(repo, raw):
    task = need_task(repo, raw)
    current = load_state(repo.root).get("open")
    if current != task.ref:
        raise TraceError(f"{task.ref} is not the open task (open: {current or 'none'})")
    return task


def cmd_restore(repo, args):
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
    touch = records.record(root, base, current) if files else None
    records.write(root, task.ref, touch)
    edit_task(repo, task, status="done", changes=", ".join(files) or "none")
    keep(root, "last", current)
    drop(root, "base")
    save_state(root, {})
    fresh_repo = Repo(root)
    fresh_repo.write_roadmap()
    print(f"done {task.ref}: {len(files)} file(s)")
    for f in files:
        print(f"  {f}")
    if touch:
        (added, total_added), (removed, total_removed) = records.accounted(touch)
        print(f"accounted {added}/{total_added} added, {removed}/{total_removed} removed lines"
              + (" (partial record)" if touch["partial"] else ""))
    if nxt := fresh_repo.next_task():
        print(f"next: {nxt.ref}  {nxt.text} -> run: trace start {nxt.ref}")
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
    if args.reason.startswith("conflicts "):
        ref, sep, why = args.reason[len("conflicts "):].partition(":")
        if not sep or not why.strip():
            raise TraceError('a conflict reads "conflicts <ref>: <why>", e.g. "conflicts 011/D2: needs two stores"')
        find_item(repo, ref.strip())
    if load_state(repo.root).get("open") == task.ref:
        drop(repo.root, "base")
        save_state(repo.root, {})
    edit_task(repo, task, status="blocked", note=f"blocked: {args.reason}")
    Repo(repo.root).write_roadmap()
    print(f"blocked {task.ref}")
    return 0


def cmd_check(repo, args):
    root = repo.root
    if getattr(args, "audit", False):
        for sev, where, msg, sp in run_audit(repo):
            repo.issue(sev, where, msg, sp)
    if removed_terms(repo.records):  # only then is the index worth refreshing
        g, db = graph(repo)
        db.close()
        defined = {n for names in g.defs.values() for n in names}
        for rel, n, term, (path, name, ref) in removed_mentions(root, repo.records, defined):
            repo.issue("warning", f"{rel}:{n}", f"mentions {term}, which {ref} removed from {path}", ref[:3])
    if not load_state(root).get("open"):
        reference, current = reference_tree(root), snapshot(root)
        stray = numstat(root, reference, current)
        if stray:
            names = ", ".join(s.split(" (")[0] for s in stray[:5]) + (" …" if len(stray) > 5 else "")
            touched = records.changed_symbols(records.record(root, reference, current), limit=5)
            repo.issue("warning", "working tree", f"{len(stray)} file(s) changed outside any task: {names}"
                       + (f"; symbols: {', '.join(touched)}" if touched else ""))
    issues = sorted(repo.issues, key=lambda x: SEVERITY[x[0]])
    for sev, where, msg, _ in issues:
        print(f"{sev.upper():<8} {where}  {msg}")
    counts = {k: sum(1 for i in issues if i[0] == k) for k in SEVERITY}
    print(f"\n{counts['error']} error(s), {counts['pending']} pending, {counts['warning']} warning(s)")
    failed = any(i[0] == "error" for i in issues) or (args.strict and any(i[0] == "pending" for i in issues))
    return 1 if failed else 0



def cmd_audit(repo, args):
    issues = sorted(run_audit(repo), key=lambda x: SEVERITY[x[0]])
    if getattr(args, "json", False):
        items = []
        for sev, where, msg, sp in issues:
            f, _, l = where.partition(":")
            items.append({"severity": sev, "where": where, "file": f, "line": int(l) if l.isdigit() else None,
                          "message": msg, "spec": sp})
        print(json.dumps({"audit": items}, indent=2))
    else:
        for sev, where, msg, _ in issues:
            print(f"{sev.upper():<8} {where}  {msg}")
        counts = {k: sum(1 for i in issues if i[0] == k) for k in SEVERITY}
        print(f"\n{counts['error']} error(s), {counts['pending']} pending, {counts['warning']} warning(s)")
    failed = any(i[0] == "error" for i in issues) or (getattr(args, "strict", False) and any(i[0] in ("pending", "warning") for i in issues))
    return 1 if failed else 0


def cmd_review(repo, args):
    item = find_item(repo, args.ref)
    repo.fingerprints[item.ref] = item.fingerprint
    repo.record_fingerprints()
    print(f"reviewed {item.ref}: current text accepted as a wording-only edit")
    return 0


# name: (handler, help, arguments) — "--x" is a switch, "--x=" takes a value, "x?" is optional, else positional.
COMMANDS = {
    "status": (cmd_status, "spec status, stage and next task (--write: into roadmap.md)", ("--write", "--json")),
    "start": (cmd_start, "open a task and snapshot the working tree", ("task", "--adopt", "--ignore")),
    "done": (cmd_done, "close the open task and record its changes", ("task",)),
    "abort": (cmd_abort, "close the open task without recording it", ("task",)),
    "block": (cmd_block, "mark a task blocked with a reason", ("task", "reason")),
    "check": (cmd_check, "verify the trace; exit 1 on errors (--strict: also on pending, --audit: include audit)", ("--strict", "--audit")),
    "audit": (cmd_audit, "consistency audit across architecture, product and interview (--strict, --json)", ("--strict", "--json")),
    "impact": (cmd_impact, "what implemented an item, or what depends on code (path[::symbol])",
               ("ref", "--direction=", "--depth=", "--deep")),
    "review": (cmd_review, "accept an item's current text as a wording-only edit", ("ref",)),
    "restore": (cmd_restore, "undo a finished task's recorded changes, inside the open task", ("task",)),
    "keep": (cmd_keep, "accept a retired task's symbol that stays, with a written reason", ("address", "reason")),
    "index": (cmd_index, "build the code index (--status: what it holds, --rebuild, --dump: JSON)",
              ("--status", "--rebuild", "--dump")),
    "locate": (cmd_locate, "rank the decisions, tasks, files and symbols matching some words", ("text", "--limit=")),
    "packet": (cmd_packet, "a review packet for a task (--diff [--base ref]: for a diff), Markdown or --json",
               ("task?", "--json", "--diff", "--base=")),
    "why": (cmd_why, "the tasks and decisions behind a piece of code: path or path::symbol", ("address",)),
}
