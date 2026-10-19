"""snap.py <repo> <name>: tree id of the whole working tree (.gitignore honored), real index untouched.

Appends `<name> <tree>` to snaps-<repo folder>.txt beside this script and prints the tree."""
import os, subprocess, sys

repo, name = sys.argv[1:3]
git_dir = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=repo, capture_output=True,
                         text=True, check=True).stdout.strip()
env = dict(os.environ, GIT_INDEX_FILE=os.path.join(git_dir, "e2e-index"))
if os.path.exists(env["GIT_INDEX_FILE"]):
    os.remove(env["GIT_INDEX_FILE"])
subprocess.run(["git", "add", "-A"], cwd=repo, env=env, check=True, capture_output=True)
tree = subprocess.run(["git", "write-tree"], cwd=repo, env=env, capture_output=True, text=True, check=True).stdout.strip()
os.remove(env["GIT_INDEX_FILE"])
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"snaps-{os.path.basename(repo)}.txt"), "a") as f:
    f.write(f"{name} {tree}\n")
print(tree)
