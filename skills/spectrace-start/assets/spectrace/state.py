"""The open-task state file, the files the trace keeps in .spectrace/, and task line edits."""
import json, os, re

from .model import FIELD_RE, read_lines, write_lines, eol


def state_path(root):
    return os.path.join(root, ".spectrace", "state.json")


def load_state(root):
    try:
        with open(state_path(root), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


IGNORES = ("state.json", "__pycache__/", "index.db")


def ensure_ignores(root):
    """Append to .spectrace/.gitignore every generated path it does not list yet."""
    path = os.path.join(root, ".spectrace", ".gitignore")
    text = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
    listed = {line.strip() for line in text.splitlines()}
    missing = [name for name in IGNORES if name not in listed]
    if missing:
        with open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(("\n" if text and not text.endswith("\n") else "") + "".join(f"{n}\n" for n in missing))


def save_state(root, state):
    os.makedirs(os.path.dirname(state_path(root)), exist_ok=True)
    ensure_ignores(root)
    # Patches must stay byte-exact across clones, or `restore` breaks on CRLF checkouts.
    if not os.path.exists(os.path.join(root, ".spectrace", ".gitattributes")):
        with open(os.path.join(root, ".spectrace", ".gitattributes"), "w", encoding="utf-8", newline="\n") as f:
            f.write("changes/*.patch -text\n")
    if state:
        with open(state_path(root), "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    elif os.path.exists(state_path(root)):
        os.remove(state_path(root))


def edit_task(repo, task, status=None, changes=None, note=None):
    rel = repo.path(f"{repo.specs[task.spec].dir}/tasks.md")
    lines = read_lines(rel)
    i = task.line
    end_of_line = eol(lines[i])
    if status:
        box = "x" if status == "done" else " "
        lines[i] = f"- [{box}] T{task.num:03d} [{task.owner}] [status:{status}] {task.text}{end_of_line}"
    end = i + 1
    while end < len(lines) and lines[end].strip() and lines[end][0].isspace():
        end += 1
    block = lines[i + 1:end]
    if changes is not None:
        block = [l for l in block if not re.match(r"^\s+changes:", l)]
        fields = [n for n, l in enumerate(block) if FIELD_RE.match(l.rstrip("\r\n"))]
        block.insert((fields[-1] + 1) if fields else 0, f"      changes: {changes}{end_of_line}")
    if note:
        block.append(f"      └─ {note}{end_of_line}")
    lines[i + 1:end] = block
    write_lines(rel, lines)
