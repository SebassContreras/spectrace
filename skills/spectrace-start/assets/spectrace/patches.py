"""Recorded task patches: parsing, loading and the renames they imply."""
import os, re


def parse_patch(text):
    """Per-file blocks of a git patch: old/new path, status, added and removed lines."""
    blocks, b = [], None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            b = {"old": None, "new": None, "status": "modified", "added": [], "removed": [], "hunk": False}
            blocks.append(b)
        elif b is None:
            continue
        elif b["hunk"] and line and line[0] in "+-":
            if len(line[1:].strip()) >= 4:
                b["added" if line[0] == "+" else "removed"].append(line[1:].strip())
        elif line.startswith("@@"):
            b["hunk"] = True
        elif line.startswith(("rename from ", "rename to ")):
            b["status"] = "renamed"
            b["old" if line.startswith("rename from") else "new"] = line.split(" ", 2)[2]
        elif line.startswith("new file mode"):
            b["status"] = "new"
        elif line.startswith("deleted file mode"):
            b["status"] = "deleted"
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
