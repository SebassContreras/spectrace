"""Markdown adapter: headings outside fences as `Section > Subsection`, `(frontmatter)`, `(preamble)`."""
import re

from . import ADAPTERS, Span

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def symbols(text):
    lines = text.splitlines()
    spans, first = [], 1
    if lines and lines[0].strip() == "---":
        close = next((n for n in range(1, len(lines)) if lines[n].strip() in ("---", "...")), None)
        if close is not None:
            spans.append(Span("(frontmatter)", "frontmatter", 1, close + 1, None))
            first = close + 2
    heads, fenced = [], False
    for n in range(first, len(lines) + 1):
        line = lines[n - 1]
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and (m := HEADING_RE.match(line)):
            heads.append((n, len(m.group(1)), m.group(2)))
    end_of_preamble = heads[0][0] - 1 if heads else len(lines)
    if any(lines[n - 1].strip() for n in range(first, end_of_preamble + 1)):
        spans.append(Span("(preamble)", "preamble", first, end_of_preamble, None))
    path, seen = [], {}  # (level, title) of the open sections; repeated names get (2), (3)
    for i, (n, level, title) in enumerate(heads):
        path = [p for p in path if p[0] < level] + [(level, title)]
        end = next((m - 1 for m, lv, _ in heads[i + 1:] if lv <= level), len(lines))
        name = " > ".join(t for _, t in path)
        seen[name] = seen.get(name, 0) + 1
        spans.append(Span(name if seen[name] == 1 else f"{name} ({seen[name]})", "section", n, end, None))
    return spans


for ext in ("md", "markdown"):
    ADAPTERS[ext] = ("markdown", symbols)
