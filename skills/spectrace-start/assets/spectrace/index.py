"""The code index: `.spectrace/index.db`, one disposable `sqlite3` file of per-file facts.

Facts are cached by content hash; files whose size or modification time changed are
re-hashed, and only those whose hash changed are re-extracted. Relations are linked in
memory from the cached facts on every run (`linker.py`), so a changed file can change
what its neighbours resolve to.
"""
import hashlib, os, re

from . import TraceError
from .facts import extract
from .symbols import language
from .gitio import git

DB = ".spectrace/index.db"
SCHEMA = """
CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, hash TEXT, size INTEGER, mtime REAL,
                                  lang TEXT, test INTEGER, status TEXT);
CREATE TABLE IF NOT EXISTS symbols (path TEXT, name TEXT, kind TEXT, start INTEGER, end INTEGER);
CREATE TABLE IF NOT EXISTS imports (path TEXT, bound TEXT, module TEXT, name TEXT, line INTEGER);
CREATE TABLE IF NOT EXISTS refs (path TEXT, symbol TEXT, kind TEXT, name TEXT, base TEXT, line INTEGER);
CREATE TABLE IF NOT EXISTS tokens (path TEXT, symbol TEXT, token TEXT, count INTEGER);
CREATE INDEX IF NOT EXISTS symbols_path ON symbols (path);
CREATE INDEX IF NOT EXISTS imports_path ON imports (path);
CREATE INDEX IF NOT EXISTS refs_path ON refs (path);
CREATE INDEX IF NOT EXISTS tokens_token ON tokens (token);
CREATE INDEX IF NOT EXISTS tokens_path ON tokens (path);
"""
TEST_RE = re.compile(r"(^|/)tests?/|(^|/)test_[^/]*\.py$|_test\.py$")
LIMIT = 1_000_000  # bytes: a larger file is listed, not extracted


FACTS_VERSION = 3  # bump when facts.py extracts differently: the cache is rebuilt


def connect(root, rebuild=False, memory=False):
    try:
        import sqlite3
    except ImportError:
        raise TraceError("this Python has no sqlite3 module: the code index needs it")
    if memory:  # a clean CI checkout: nothing is written to disk
        db = sqlite3.connect(":memory:")
        db.executescript(SCHEMA)
        return db
    path = os.path.join(root, *DB.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if rebuild and os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    if db.execute("PRAGMA user_version").fetchone()[0] != FACTS_VERSION:
        db.close()
        os.remove(path)
        db = sqlite3.connect(path)
        db.execute(f"PRAGMA user_version = {FACTS_VERSION}")
    db.executescript(SCHEMA)
    return db


def is_test(path):
    return bool(TEST_RE.search(path))


def listed(root):
    """Tracked and untracked, not ignored, files of the repo outside history."""
    out = git(root, "ls-files", "-z", "-co", "--exclude-standard").split("\0")
    return sorted(p for p in out if p and not p.startswith((".spectrace/", "planning/")))


def refresh(root, rebuild=False, memory=False):
    """Bring the index up to date with the working tree and return the open connection."""
    db = connect(root, rebuild, memory)
    known = {r[0]: r[1:] for r in db.execute("SELECT path, hash, size, mtime FROM files")}
    present = listed(root)
    for path in set(known) - set(present):
        forget(db, path)
    for path in present:
        full = os.path.join(root, *path.split("/"))
        try:
            st = os.stat(full)
        except OSError:
            continue
        old = known.get(path)
        if old and old[1] == st.st_size and old[2] == st.st_mtime:
            continue
        with open(full, "rb") as f:
            data = f.read()
        digest = hashlib.sha256(data).hexdigest()[:16]
        if old and old[0] == digest:
            db.execute("UPDATE files SET size = ?, mtime = ? WHERE path = ?", (st.st_size, st.st_mtime, path))
            continue
        forget(db, path)
        text = None if st.st_size > LIMIT or b"\0" in data[:1024] else data.decode("utf-8", errors="replace")
        syms, imps, refs, toks, status = extract(path, text) if text is not None else \
            ([], [], [], [], "too large or binary")
        lang = language(path)
        db.execute("INSERT INTO files VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (path, digest, st.st_size, st.st_mtime, lang, int(is_test(path)), status))
        db.executemany("INSERT INTO symbols VALUES (?, ?, ?, ?, ?)", [(path, *s) for s in syms])
        db.executemany("INSERT INTO imports VALUES (?, ?, ?, ?, ?)", [(path, *i) for i in imps])
        db.executemany("INSERT INTO refs VALUES (?, ?, ?, ?, ?, ?)", [(path, *r) for r in refs])
        db.executemany("INSERT INTO tokens VALUES (?, ?, ?, ?)", [(path, *t) for t in toks])
    db.commit()
    return db


def forget(db, path):
    for table in ("files", "symbols", "imports", "refs", "tokens"):
        db.execute(f"DELETE FROM {table} WHERE path = ?", (path,))
