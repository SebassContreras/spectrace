"""Driver: send one turn to a harness in the throwaway repo; print its reply and conversation id.

usage: python turn.py <harness: claude|agy> <repo> <log name> <prompt file> [conversation id]
"""
import io, json, os, shutil, subprocess, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

harness, repo, name, prompt_file = sys.argv[1:5]
conv = sys.argv[5] if len(sys.argv) > 5 else None
prompt = open(prompt_file, encoding="utf-8").read().strip()
logdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2e-logs", harness)
os.makedirs(logdir, exist_ok=True)
if harness == "claude":
    cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--output-format", "json"]
    cmd += ["--resume", conv] if conv else []
else:
    cmd = ["agy", "-p", prompt, "--dangerously-skip-permissions"] + (["--conversation", conv] if conv else [])
t0 = time.time()
p = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace",
                   shell=False) if not cmd.__setitem__(0, shutil.which(cmd[0]) or cmd[0]) else None
with open(os.path.join(logdir, f"{name}.log"), "a", encoding="utf-8") as f:
    f.write(f"\n===== PROMPT ({conv or 'new'})\n{prompt}\n===== EXIT {p.returncode} {time.time() - t0:.0f}s\n"
            f"{p.stdout}\n----- STDERR\n{p.stderr}\n")
if harness == "claude":
    try:
        out = json.loads(p.stdout)
        print("SESSION", out.get("session_id"))
        print(out.get("result", ""))
    except ValueError:
        print("RAW", p.stdout[-3000:], p.stderr[-2000:])
else:
    print(p.stdout[-6000:], p.stderr[-2000:])
