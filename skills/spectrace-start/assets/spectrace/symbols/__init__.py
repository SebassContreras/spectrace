"""Language adapters: one interface, `symbols(text) -> list of Span`, chosen by file extension.

A span is a named range of 1-based, inclusive lines. Nested spans are allowed; a line
belongs to the innermost span that contains it. Kind `import` is not a symbol: its lines
go to the `imports` bucket. A file with no adapter has no spans: every line is `file`.
"""
from collections import namedtuple

Span = namedtuple("Span", "name kind start end sig")

ADAPTERS = {}  # extension: (language, symbols function)


def matches(name, symbol):
    """A symbol answers for itself and for what it contains (`Store` for `Store.save`)."""
    return name == symbol or name.startswith(symbol + ".") or name.startswith(symbol + " > ")


def extension(path):
    name = path.rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


def language(path):
    return ADAPTERS.get(extension(path), ("file", None))[0]


def symbols(path, text):
    """Spans of `text` read as the language of `path`; [] for a file-level file.

    Raises SyntaxError when the adapter cannot parse the text."""
    adapter = ADAPTERS.get(extension(path))
    return adapter[1](text) if adapter else []


from . import markdown, python  # noqa: E402,F401  (they register their extensions)
