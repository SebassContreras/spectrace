"""The trace commands: one handler per command, and the table the parser is built from."""
import json, os
from datetime import date

from . import TraceError
from .gitio import git, snapshot, keep, kept, drop, reference_tree, diff, numstat
from .model import REF_RE, SEVERITY, Repo
from .patches import load_patches, file_presence
from .state import load_state, save_state, edit_task

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
        print("Files changed outside any task since the last one closed:\n" + "\n".join(f"  {s}" for s in stray) +
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
    edit_task(repo, task, status="done", changes=", ".join(files) or "none")
    keep(root, "last", current)
    drop(root, "base")
    save_state(root, {})
    fresh_repo = Repo(root)
    fresh_repo.write_roadmap()
    print(f"done {task.ref}: {len(files)} file(s)")
    for f in files:
        print(f"  {f}")
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
    if not load_state(root).get("open"):
        stray = numstat(root, reference_tree(root), snapshot(root))
        if stray:
            names = ", ".join(s.split(" (")[0] for s in stray[:5]) + (" …" if len(stray) > 5 else "")
            repo.issue("warning", "working tree", f"{len(stray)} file(s) changed outside any task: {names}")
    issues = sorted(repo.issues, key=lambda x: SEVERITY[x[0]])
    for sev, where, msg, _ in issues:
        print(f"{sev.upper():<8} {where}  {msg}")
    counts = {k: sum(1 for i in issues if i[0] == k) for k in SEVERITY}
    print(f"\n{counts['error']} error(s), {counts['pending']} pending, {counts['warning']} warning(s)")
    failed = any(i[0] == "error" for i in issues) or (args.strict and any(i[0] == "pending" for i in issues))
    return 1 if failed else 0



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


def cmd_review(repo, args):
    item = find_item(repo, args.ref)
    repo.fingerprints[item.ref] = item.fingerprint
    repo.record_fingerprints()
    print(f"reviewed {item.ref}: current text accepted as a wording-only edit")
    return 0


def cmd_impact(repo, args):
    item = find_item(repo, args.ref)
    targets = [item]
    if item.kind == "R":
        targets += [d for d in repo.specs[item.spec].items.values() if d.kind == "D" and item.key in d.implements]
    rows = []
    patches, renames = load_patches(repo.root)
    for s in repo.specs.values():
        for t in s.tasks:
            if not any(repo.resolve(raw, s.id)[0] in targets for raw in t.covers):
                continue
            retired_by = [o.ref for s2 in repo.specs.values() for o in s2.tasks
                          if any(repo.find_task(r, s2.id) is t for r in o.retires)]
            rows.append({"task": t.ref, "owner": t.owner, "status": t.status, "kind": t.kind or "",
                         "covers": t.covers, "text": t.text, "changes": t.changes, "retired_by": retired_by,
                         "files": file_presence(repo.root, patches.get(t.ref, []), renames)})

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
        if not r["files"] and r["status"] == "done":
            print(f"    no patch recorded ({r['changes'] or 'finished outside trace'}) — search the code by hand")
    return 0


# name: (handler, help, arguments) — "--x" is a switch, anything else positional.
COMMANDS = {
    "status": (cmd_status, "spec status, stage and next task (--write: into roadmap.md)", ("--write", "--json")),
    "start": (cmd_start, "open a task and snapshot the working tree", ("task", "--adopt", "--ignore")),
    "done": (cmd_done, "close the open task and record its changes", ("task",)),
    "abort": (cmd_abort, "close the open task without recording it", ("task",)),
    "block": (cmd_block, "mark a task blocked with a reason", ("task", "reason")),
    "check": (cmd_check, "verify the trace; exit 1 on errors (--strict: also on pending)", ("--strict",)),
    "impact": (cmd_impact, "what implemented an item: tasks, files, lines still present", ("ref",)),
    "review": (cmd_review, "accept an item's current text as a wording-only edit", ("ref",)),
    "restore": (cmd_restore, "undo a finished task's recorded changes, inside the open task", ("task",)),
}
