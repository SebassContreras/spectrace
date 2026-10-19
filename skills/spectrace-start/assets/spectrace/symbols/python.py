"""Python adapter (`ast`): functions, classes, methods, module variables, class attributes, imports."""
import ast

from . import ADAPTERS, Span


def signature(node):
    if isinstance(node, ast.ClassDef):
        return "(" + ", ".join(ast.unparse(b) for b in node.bases) + ")"
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"({ast.unparse(node.args)}){returns}"


def assigned(node):
    """Names bound by an assignment statement, in order."""
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    out = []
    for t in targets:
        out += [n.id for n in ast.walk(t) if isinstance(n, ast.Name)]
    return out


def walk(body, prefix, in_class):
    spans = []
    for node in body:
        start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            spans.append(Span(prefix + node.name, "method" if in_class else "function",
                              start, node.end_lineno, signature(node)))
        elif isinstance(node, ast.ClassDef):
            spans.append(Span(prefix + node.name, "class", start, node.end_lineno, signature(node)))
            spans += walk(node.body, f"{prefix}{node.name}.", True)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            kind = "attribute" if in_class else "variable"
            spans += [Span(prefix + n, kind, start, node.end_lineno, None) for n in assigned(node)]
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            spans.append(Span("(imports)", "import", start, node.end_lineno, None))
    return spans


def merged(spans):
    """One span per name: a property and its setter, or a name assigned twice, are one symbol."""
    by_name = {}
    for s in spans:
        if s.kind == "import" or s.name not in by_name:
            by_name[s.name if s.kind != "import" else (s.name, s.start)] = s
        else:
            old = by_name[s.name]
            by_name[s.name] = old._replace(start=min(old.start, s.start), end=max(old.end, s.end), sig=s.sig)
    return list(by_name.values())


def symbols(text):
    return merged(walk(ast.parse(text).body, "", False))


ADAPTERS["py"] = ("python", symbols)
