"""git via subprocess: the only way the trace talks to git."""
import os, shutil, subprocess

from . import TraceError

EXCLUDE = (":(exclude)planning", ":(exclude).spectrace")
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
IDENT = {"GIT_AUTHOR_NAME": "spectrace", "GIT_AUTHOR_EMAIL": "spectrace@localhost",
         "GIT_COMMITTER_NAME": "spectrace", "GIT_COMMITTER_EMAIL": "spectrace@localhost"}


def git(root, *args, env=None, raw=False):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=root,
                       capture_output=True, env=dict(os.environ, **(env or {})))
    if p.returncode != 0:
        raise TraceError(f"git {' '.join(args)}: {p.stderr.decode(errors='replace').strip()}")
    return p.stdout.decode("utf-8", errors="replace").strip("" if raw else None)


def snapshot(root):
    """Tree of the whole working tree (honoring .gitignore), without touching the real index."""
    index = os.path.join(root, git(root, "rev-parse", "--git-path", "index"))
    tmp = os.path.join(root, git(root, "rev-parse", "--git-path", "spectrace-index"))
    if os.path.exists(index):
        shutil.copyfile(index, tmp)
    elif os.path.exists(tmp):
        os.remove(tmp)
    try:
        env = {"GIT_INDEX_FILE": tmp}
        git(root, "add", "-A", env=env)
        return git(root, "write-tree", env=env)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def keep(root, name, tree):
    commit = git(root, "commit-tree", tree, "-m", f"spectrace {name}", env=IDENT)
    git(root, "update-ref", f"refs/spectrace/{name}", commit)


def kept(root, name):
    try:
        return git(root, "rev-parse", "--verify", "--quiet", f"refs/spectrace/{name}^{{tree}}")
    except TraceError:
        return None


def drop(root, name):
    if kept(root, name):
        git(root, "update-ref", "-d", f"refs/spectrace/{name}")


def reference_tree(root):
    """The tree when the last task closed; else HEAD; else empty."""
    if last := kept(root, "last"):
        return last
    try:
        return git(root, "rev-parse", "--verify", "--quiet", "HEAD^{tree}")
    except TraceError:
        return EMPTY_TREE


def diff(root, a, b, *flags):
    return git(root, "diff", "--no-color", "--no-ext-diff", "-M", *flags, a, b, "--", ".", *EXCLUDE, raw=True)


def numstat(root, a, b):
    out, parts = [], diff(root, a, b, "--numstat", "-z").split("\0")
    while parts:
        head = parts.pop(0)
        if not head.strip():
            continue
        add, rem, path = head.lstrip().split("\t", 2)
        if not path:  # rename: old and new paths follow
            path = f"{parts.pop(0)} → {parts.pop(0)}"
        out.append(f"{path} (binary)" if add == "-" else f"{path} (+{add} -{rem})")
    return out
