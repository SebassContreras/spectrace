# 001 — format-and-trace — Requirements

## What's being built

The format every spec, decision and task is written in, and the script that reads
it: computes status, records what each task changed, and checks the trace.

## Who it serves

Every other spec and skill (they write the format; `trace.py` enforces it), and any
agent executing tasks in a target repo.

## Requirements

- R1@1: Specs, decisions and tasks follow one written format, with IDs and revisions, that a script parses exactly.
- R2@1: Each task's exact changes are recorded when it finishes — without a commit and without touching the staging area — even when several tasks finish between commits.
- R3@2: When a decision is revised or retired, every finished task that implemented it is flagged, with the files and lines it added and whether they are still in the code — following files that were moved or renamed since.
- R4@1: The roadmap's `Status` and `Stage` follow from the spec files, and a hand edit that disagrees is reported.
- R5@1: Runs anywhere with git and Python 3.9+; nothing to install.
- R6@1: When a task deletes a file, any remaining mention of that file's path elsewhere in the repo (outside history) is reported, and the deleting task's spec cannot read as done until the mention is gone.
- R7@1: When the text of an item that finished work was built on changes without a revision bump, it is reported until the revision is bumped or the edit is confirmed as wording only.
- R8@1: What a finished task did can be undone in the working tree from its recorded patch, inside a task, so a retired approach can be reinstated.

## Out of scope

- The skills that write specs (002–004).
- Code-level tags; LLM-based drift detection.

## Dependencies

None.

## Owner split

All agent.
