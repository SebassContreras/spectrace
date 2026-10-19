"""Command line: the argument parser and main()."""
import argparse, os, sys

from . import VERSION, TraceError
from .commands import COMMANDS
from .gitio import git
from .model import Repo


def parser():
    p = argparse.ArgumentParser(prog="trace", description=f"spectrace trace (format v{VERSION})")
    p.add_argument("-C", dest="cwd", default=".", help="run as if started in this directory")
    p.add_argument("--version", action="version", version=f"spectrace trace {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, (_, text, arguments) in COMMANDS.items():
        s = sub.add_parser(name, help=text)
        for a in arguments:
            if a.endswith("="):  # "--x=" takes a value
                s.add_argument(a[:-1])
            elif a.endswith("?"):  # "x?" is an optional positional
                s.add_argument(a[:-1], nargs="?")
            elif a.startswith("--"):
                s.add_argument(a, action="store_true")
            else:
                s.add_argument(a)
    return p


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = parser().parse_args(argv)
    try:
        root = os.path.normpath(git(os.path.abspath(args.cwd), "rev-parse", "--show-toplevel"))
        if not os.path.isdir(os.path.join(root, "planning")):
            raise TraceError(f"no planning/ folder in {root} — run the spectrace-start skill first")
        return COMMANDS[args.cmd][0](Repo(root), args)
    except TraceError as e:
        print(f"trace: {e}", file=sys.stderr)
        return 1
