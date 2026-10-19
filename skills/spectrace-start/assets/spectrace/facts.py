"""Per-file Python facts for the index: definitions, imports, and the names each symbol uses."""
import ast
import builtins
from collections import Counter

from .symbols import language, symbols as spans_of
from .tokens import tokens

BUILTINS = set(dir(builtins))


def local_names(fn):
    """Parameters and names a function binds itself: never references to other code."""
    a = fn.args
    out = {x.arg for x in a.posonlyargs + a.args + a.kwonlyargs}
    out |= {x.arg for x in (a.vararg, a.kwarg) if x}
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            out.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node is not fn:
            out.add(node.name)
        elif isinstance(node, ast.arg):
            out.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            out.add(node.name)
    return out


class Refs(ast.NodeVisitor):
    """(symbol, kind, name, base, line) for every name a symbol uses; kind is name, attr or base."""

    def __init__(self):
        self.out, self.scope, self.locals = [], [], [set()]

    def where(self):
        return ".".join(self.scope) or "(module)"

    def visit_ClassDef(self, node):
        for b in node.bases:
            if isinstance(b, ast.Name):
                self.out.append((".".join(self.scope + [node.name]), "base", b.id, None, b.lineno))
            elif isinstance(b, ast.Attribute):
                base = b.value.id if isinstance(b.value, ast.Name) else None
                self.out.append((".".join(self.scope + [node.name]), "base", b.attr, base, b.lineno))
        for d in node.decorator_list + node.keywords:
            self.visit(d)
        self.scope.append(node.name)
        for stmt in node.body:
            self.visit(stmt)
        self.scope.pop()

    def visit_FunctionDef(self, node):
        for d in node.decorator_list + node.args.defaults + node.args.kw_defaults:
            if d is not None:
                self.visit(d)
        nested = len(self.locals) > 1  # a function inside a function is part of it, not a symbol
        if not nested:
            self.scope.append(node.name)
        self.locals.append(self.locals[-1] | local_names(node))
        for stmt in node.body:
            self.visit(stmt)
        self.locals.pop()
        if not nested:
            self.scope.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.locals[-1] | BUILTINS and not node.id.startswith("__"):
            self.out.append((self.where(), "name", node.id, None, node.lineno))

    def visit_Attribute(self, node):
        base = node.value.id if isinstance(node.value, ast.Name) else None
        self.out.append((self.where(), "attr", node.attr, base, node.lineno))
        self.generic_visit(node)


def imports(tree):
    """(bound name, module, imported name or None, line) for each import in the file."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                bound = a.asname or a.name.split(".")[0]
                out.append((bound, a.name if a.asname else a.name.split(".")[0], None, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            module = "." * node.level + (node.module or "")
            out += [(a.asname or a.name, module, a.name, node.lineno) for a in node.names if a.name != "*"]
    return out


def symbol_tokens(spans, text):
    """(symbol, token, count) for the words of each symbol's own lines: names, strings, comments."""
    lines, out = text.splitlines(), []
    for s in spans:
        counts = Counter(tokens("\n".join(lines[s.start - 1:s.end])) + tokens(s.name))
        out += [(s.name, t, n) for t, n in sorted(counts.items())]
    return out


def extract(path, text):
    """(symbols, imports, refs, tokens, status) of one file. Only Python is read for relations."""
    if not path.endswith(".py"):
        if language(path) == "file":
            return [], [], [], [], "no adapter"
        spans = spans_of(path, text)
        return [(s.name, s.kind, s.start, s.end) for s in spans], [], [], symbol_tokens(spans, text), "symbols only"
    try:
        tree = ast.parse(text)
        spans = [s for s in spans_of(path, text) if s.kind != "import"]
    except (SyntaxError, ValueError) as e:
        return [], [], [], [], f"does not parse: {type(e).__name__}"
    walker = Refs()
    walker.visit(tree)
    defs = [(s.name, s.kind, s.start, s.end) for s in spans]
    return defs, imports(tree), walker.out, symbol_tokens(spans, text), "ok"
