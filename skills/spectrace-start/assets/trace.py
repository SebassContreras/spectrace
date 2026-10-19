#!/usr/bin/env python3
"""spectrace trace: status, per-task change capture, and the spec trace check.

Implements .spectrace/format.md. Python 3.9+, standard library only. The code lives in
the `spectrace/` package next to this file; this launcher keeps the command and the
names `tests/test_trace.py` imports.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectrace.cli import main  # noqa: E402,F401
from spectrace.model import ITEM_RE, RETIRED_RE, TASK_RE, FIELD_RE, BLOCKED_RE  # noqa: E402,F401

if __name__ == "__main__":
    sys.exit(main())
