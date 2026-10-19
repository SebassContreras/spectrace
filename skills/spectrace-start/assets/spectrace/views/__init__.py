"""Read-only views over the records: one module per command."""
from .. import TraceError
from ..symbols import matches  # noqa: F401  (re-exported for the views)


def address(raw):
    """(path, symbol or None) from `path` or `path::Qualified.name`."""
    path, _, symbol = raw.partition("::")
    path = path.replace("\\", "/").strip()
    path = path[2:] if path.startswith("./") else path
    if not path:
        raise TraceError("use a code address: path or path::Qualified.name")
    return path, symbol.strip() or None
