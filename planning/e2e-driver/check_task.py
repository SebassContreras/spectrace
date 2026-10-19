"""check_task.py <repo> <before tree> <after tree>: R1 (exact patch) and 015 R1 (record) for the task(s) done between.

Finds the tasks whose status went to done between the two trees, then checks each one's patch
against the driver diff and its record's totals against numstat and its own buckets."""
import json, os, re, subprocess, sys

repo, b, a = sys.argv[1:4]
EX = ["--", ".", ":(exclude)planning", ":(exclude).spectrace"]


def git(*args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def done_tasks(tree):
    out = set()
    for path in git("ls-tree", "-r", "--name-only", tree, "planning/specs").split():
        if path.endswith("tasks.md"):
            spec = path.split("/")[2][:3]
            out |= {f"{spec}/T{m}" for m in re.findall(r"^- \[x\] T(\d{3})", git("show", f"{tree}:{path}"), re.M)}
    return out


new = sorted(done_tasks(a) - done_tasks(b))
print("tasks done in this conversation:", new or "none")
driver = git("diff", "--no-color", "--no-ext-diff", "-M", "--binary", b, a, *EX)
numstat = {}
for line in git("diff", "--numstat", "-M", b, a, *EX).splitlines():
    add, rem, path = line.split("\t", 2)
    if add != "-":
        numstat[path.split(" => ")[-1].replace("{", "").replace("}", "")] = [int(add), int(rem)]
for ref in new:
    stem = os.path.join(repo, ".spectrace", "changes", ref.replace("/", "-"))
    patch = open(stem + ".patch", encoding="utf-8", newline="").read() if os.path.exists(stem + ".patch") else ""
    exact = "EXACT" if (patch == driver if len(new) == 1 else None) else ("n/a (several tasks)" if len(new) > 1 else "DIFFERS")
    rec_line = "no record"
    if os.path.exists(stem + ".touch.json"):
        rec = json.load(open(stem + ".touch.json", encoding="utf-8"))
        got = {p: f["lines"] for p, f in rec["files"].items() if f["lines"] is not None}
        adds_up = all(f["lines"] == [sum(s["lines"][i] for s in f["symbols"]) + sum(v[i] for v in f["other"].values())
                                     for i in (0, 1)] for f in rec["files"].values() if f["lines"] is not None)
        totals = "TOTALS OK" if got == numstat or len(new) > 1 else f"TOTALS DIFF {got} != {numstat}"
        syms = {p: [f"{s['name']}:{s['change']}" for s in f["symbols"]] for p, f in rec["files"].items() if f["symbols"]}
        rec_line = f"{totals} {'ADDS UP' if adds_up else 'UNACCOUNTED'} symbols={syms} skipped={rec['skipped']}"
    print(f"{ref}: patch {exact}; record {rec_line}")
