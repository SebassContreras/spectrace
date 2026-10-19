"""Mentions of symbols a task removed that are no longer defined anywhere: warnings, never gates."""
import re

from .model import text_lines

KINDS = ("class", "function", "method", "variable", "attribute")
MIN_BARE = 6  # a bare name shorter than this is too common to search for
CAP = 3  # hits reported per name


def removed_terms(records):
    """{search term: (path, name, task ref)} for removed symbols; a nested name is searched qualified."""
    out = {}
    for ref, rec in sorted(records.items()):
        for path, f in rec["files"].items():
            for s in f["symbols"]:
                if s["change"] == "removed" and s["kind"] in KINDS and ("." in s["name"] or len(s["name"]) >= MIN_BARE):
                    out[s["name"]] = (path, s["name"], ref)
    return out


def removed_mentions(root, records, defined):
    """[(path, line, term, (removed path, name, task ref))] — at most CAP per term."""
    terms = {t: v for t, v in removed_terms(records).items() if t not in defined}
    if not terms:
        return []
    pattern = re.compile(r"(?<!\w)(" + "|".join(map(re.escape, sorted(terms, key=len, reverse=True))) + r")(?!\w)")
    hits, seen = [], {}
    for rel, n, line in text_lines(root):
        for m in pattern.finditer(line):
            term = m.group(1)
            if seen.get(term, 0) < CAP:
                seen[term] = seen.get(term, 0) + 1
                hits.append((rel, n, term, terms[term]))
    return hits
