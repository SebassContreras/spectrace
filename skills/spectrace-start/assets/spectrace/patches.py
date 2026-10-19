"""Recorded task patches: parsing, loading and the renames they imply."""
import os, re


HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def parse_patch(text, min_len=4):
    """Per-file blocks of a git patch: old/new path, status, added and removed lines.

    `added`/`removed` hold the stripped text of lines at least `min_len` characters long;
    `added_at`/`removed_at` hold the line number of every added (new side) and removed
    (old side) line, whatever its length."""
    blocks, b, old_n, new_n = [], None, 0, 0
    for line in text.split("\n"):
        if line.startswith("diff --git "):
            # Paths from the header first: a binary or mode-only change has no ---/+++ lines.
            old, _, new = line[len("diff --git a/"):].rpartition(" b/")
            b = {"old": old or None, "new": new or None, "status": "modified", "added": [], "removed": [],
                 "hunk": False, "added_at": [], "removed_at": [], "binary": False}
            blocks.append(b)
        elif b is None:
            continue
        elif b["hunk"] and line and line[0] in "+- ":
            if line[0] == " ":
                old_n, new_n = old_n + 1, new_n + 1
                continue
            side = "added" if line[0] == "+" else "removed"
            b[side + "_at"].append(new_n if side == "added" else old_n)
            new_n, old_n = (new_n + 1, old_n) if side == "added" else (new_n, old_n + 1)
            if len(line[1:].strip()) >= min_len:
                b[side].append(line[1:].strip())
        elif m := HUNK_RE.match(line):
            b["hunk"], old_n, new_n = True, int(m.group(1)), int(m.group(2))
        elif line.startswith(("rename from ", "rename to ")):
            b["status"] = "renamed"
            b["old" if line.startswith("rename from") else "new"] = line.split(" ", 2)[2]
        elif line.startswith("new file mode"):
            b["status"], b["old"] = "new", None
        elif line.startswith("deleted file mode"):
            b["status"], b["new"] = "deleted", None
        elif line.startswith(("Binary files ", "GIT binary patch")):
            b["binary"] = True
        elif line.startswith("--- a/"):
            b["old"] = line[6:]
        elif line.startswith("+++ b/"):
            b["new"] = line[6:]
    return blocks


def load_patches(root):
    """{task ref: blocks} for every recorded patch, and the rename map they imply."""
    folder = os.path.join(root, ".spectrace", "changes")
    patches, renames = {}, {}
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        m = re.fullmatch(r"(\d{3})-T(\d{3})\.patch", name)
        if not m:
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            blocks = parse_patch(f.read())
        patches[f"{m.group(1)}/T{m.group(2)}"] = blocks
        for b in blocks:
            if b["status"] == "renamed":
                renames[b["old"]] = b["new"]
        # A move recorded as delete + add: same file name, mostly the same lines.
        for gone in (b for b in blocks if b["status"] == "deleted" and b["removed"]):
            for new in (b for b in blocks if b["status"] == "new"):
                same = len(set(gone["removed"]) & set(new["added"]))
                if gone["old"].rsplit("/", 1)[-1] == new["new"].rsplit("/", 1)[-1] and same >= 0.8 * len(set(gone["removed"])):
                    renames[gone["old"]] = new["new"]
    return patches, renames


def follow(root, path, renames):
    seen = set()
    while not os.path.exists(os.path.join(root, *path.split("/"))) and path in renames and path not in seen:
        seen.add(path)
        path = renames[path]
    return path


def file_presence(root, blocks, renames):
    out = []
    for b in blocks:
        if b["status"] == "deleted" or not b["new"] or not b["added"]:
            continue
        now_path = follow(root, b["new"], renames)
        label = b["new"] if now_path == b["new"] else f"{b['new']} → {now_path}"
        target, now = os.path.join(root, *now_path.split("/")), set()
        if os.path.exists(target):
            with open(target, encoding="utf-8", errors="replace") as f:
                now = {l.strip() for l in f}
        out.append({"path": label, "present": sum(1 for a in b["added"] if a in now),
                    "added": len(b["added"]), "deleted": not os.path.exists(target)})
    return out
