"""`trace locate "<text>"`: rank decisions, tasks, files and symbols that match a free-text request."""
from .. import TraceError, index
from ..tokens import tokens
from .why import anchored_hits, exact_hits

# How much a matched word weighs, by where it matched: a name says more than a body.
WEIGHTS = {"name": 4, "path": 3, "text": 2, "body": 1}
EXPAND = 3  # top symbols whose tasks and decisions are added through `why`


def score(found):
    return sum(WEIGHTS[where] * len(words) for where, words in found.items())


def candidates(repo, words):
    """[(score, kind, label, {where: words})] for every symbol, file, item and task that matches."""
    out, query = [], set(words)
    db = index.refresh(repo.root)
    try:
        body = {}
        marks = ",".join("?" * len(query))
        for path, symbol, token in db.execute(f"SELECT path, symbol, token FROM tokens WHERE token IN ({marks})",
                                              sorted(query)):
            body.setdefault((path, symbol), set()).add(token)
        paths = [r[0] for r in db.execute("SELECT path FROM files")]
    finally:
        db.close()
    for (path, symbol), hit in body.items():
        name = query & set(tokens(symbol))
        found = {"name": name, "path": query & set(tokens(path)), "body": hit - name}
        out.append((score(found), "symbol", f"{path}::{symbol}", found))
    for path in paths:
        if hit := query & set(tokens(path)):
            out.append((score({"path": hit}), "file", path, {"path": hit}))
    for item in repo.items():
        if hit := query & set(tokens(item.text)):
            out.append((score({"text": hit}), "item", f"{item.ref} {item.text[:80]}", {"text": hit}))
    for spec in repo.specs.values():
        for t in spec.tasks:
            if hit := query & set(tokens(t.text)):
                out.append((score({"text": hit}), "task", f"{t.ref} [{t.status}] {t.text[:80]}", {"text": hit}))
    return sorted(out, key=lambda c: (-c[0], c[1], c[2]))


def cmd_locate(repo, args):
    words = tokens(args.text)
    if not words:
        raise TraceError("give some words to look for, e.g. trace locate \"session expiry\"")
    limit = int(args.limit or 10)
    ranked = candidates(repo, words)[:limit]
    print(f"# Locate \"{args.text}\" — words: {', '.join(dict.fromkeys(words))}\n")
    if not ranked:
        print("Nothing matched: rephrase with words the code or the specs would use.")
        return 0
    recs = repo.records
    for n, (points, kind, label, found) in enumerate(ranked, 1):
        why = ", ".join(f"{where}({' '.join(sorted(ws))})" for where, ws in found.items() if ws)
        print(f"{n}. [{kind}] {label}  — score {points}, matched {why}")
        if kind == "symbol" and n <= EXPAND:
            path, symbol = label.split("::", 1)
            for ref, _ in (exact_hits(recs, path, symbol) + anchored_hits(repo.root, recs, path, symbol))[:3]:
                task = repo.find_task(ref)
                if task:
                    print(f"     why: {ref} → {', '.join(repo.covers_label(task))}")
    return 0
