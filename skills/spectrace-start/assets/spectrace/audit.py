"""Consistency audit: alignment between architecture, scope, interview and specs."""
import os, re
from typing import List, Tuple, Optional

# Issue tuple: (severity, where, message, spec)
AuditIssue = Tuple[str, str, str, Optional[str]]


def _read_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def check_architecture_alignment(repo) -> List[AuditIssue]:
    """Verify every active A item in architecture.md has an operative entry or reference in AGENTS.md."""
    arch_path = repo.path("planning/architecture.md")
    agents_path = repo.path("AGENTS.md")
    if not os.path.exists(arch_path) or not os.path.exists(agents_path):
        return []

    agents_content = _read_file(agents_path)
    issues: List[AuditIssue] = []

    arch_lines = _read_file(arch_path).splitlines()
    for idx, line in enumerate(arch_lines, start=1):
        m = re.match(r"^-\s+(A\d+)@\d+:\s*(.*)", line.strip())
        if not m:
            continue
        a_id, text = m.group(1), m.group(2)
        pattern = rf"\b{a_id}\b"
        if not re.search(pattern, agents_content):
            issues.append((
                "warning",
                f"planning/architecture.md:{idx}",
                f"{a_id} has no operative entry or reference in AGENTS.md",
                None,
            ))
    return issues


def check_scope_alignment(repo) -> List[AuditIssue]:
    """Flag specs or tasks with terms declared out-of-scope in planning/product.md."""
    prod_path = repo.path("planning/product.md")
    if not os.path.exists(prod_path):
        return []

    prod_text = _read_file(prod_path)
    lines = prod_text.splitlines()

    in_out_of_scope = False
    prohibited_terms = []
    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip().lower()
            in_out_of_scope = heading in ("not for now", "out of scope")
            continue
        if in_out_of_scope and line.strip().startswith("- "):
            bullet = line.strip()[2:].strip()
            term = re.split(r"[:;—]", bullet)[0].strip()
            clean_term = re.sub(r"^(no\s+|per-)", "", term, flags=re.IGNORECASE).strip()
            if len(clean_term) >= 4:
                prohibited_terms.append(clean_term.lower())

    if not prohibited_terms:
        return []

    issues: List[AuditIssue] = []

    for sid, spec in repo.specs.items():
        spec_dir = spec.dir
        req_path = repo.path(f"{spec_dir}/requirements.md")
        if os.path.exists(req_path):
            req_lines = _read_file(req_path).splitlines()
            in_req_out_of_scope = False
            for idx, rline in enumerate(req_lines, start=1):
                if rline.startswith("## "):
                    in_req_out_of_scope = "out of scope" in rline.lower()
                    continue
                if in_req_out_of_scope:
                    continue
                lower_line = rline.lower()
                for term in prohibited_terms:
                    if re.search(rf"\b{re.escape(term)}\b", lower_line):
                        issues.append((
                            "warning",
                            f"{spec_dir}/requirements.md:{idx}",
                            f"mentions concept declared out-of-scope in product.md: '{term}'",
                            sid,
                        ))
                        break

        for task in spec.tasks:
            lower_text = task.text.lower()
            for term in prohibited_terms:
                if re.search(rf"\b{re.escape(term)}\b", lower_text):
                    issues.append((
                        "warning",
                        f"{spec_dir}/tasks.md:{task.line}",
                        f"task {task.ref} introduces concept declared out-of-scope in product.md: '{term}'",
                        sid,
                    ))
                    break

    return issues


def check_interview_alignment(repo) -> List[AuditIssue]:
    """Verify no active spec is built with unresolved blocking dimensions in interview.md."""
    interview_path = repo.path(".spectrace/interview.md")
    if not os.path.exists(interview_path):
        return []

    lines = _read_file(interview_path).splitlines()
    open_dimensions = []
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("|") and not line.strip().startswith("|-"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                dim, status = cols[0], cols[1].lower()
                if status == "open" and dim not in ("dimension", "---"):
                    open_dimensions.append((dim, idx))

    if not open_dimensions:
        return []

    issues: List[AuditIssue] = []
    for sid, spec in repo.specs.items():
        if spec.status in ("in_progress", "todo") and spec.tasks:
            for dim, lnum in open_dimensions:
                if dim.startswith(f"{sid}.") or dim.startswith(f"{int(sid):03d}."):
                    issues.append((
                        "warning",
                        f".spectrace/interview.md:{lnum}",
                        f"open interview dimension '{dim}' unresolved while spec {sid} is active",
                        sid,
                    ))
                elif not re.match(r"^\d{3}\.", dim):
                    if dim in spec.name.lower() or dim in spec.dir.lower():
                        issues.append((
                            "warning",
                            f".spectrace/interview.md:{lnum}",
                            f"global open interview dimension '{dim}' conflicts with active spec {sid}",
                            sid,
                        ))
    return issues


def run_audit(repo) -> List[AuditIssue]:
    """Execute all consistency audit checks and return list of issues."""
    issues: List[AuditIssue] = []
    issues.extend(check_architecture_alignment(repo))
    issues.extend(check_scope_alignment(repo))
    issues.extend(check_interview_alignment(repo))
    return issues
