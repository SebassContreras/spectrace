# 005 — distribution — Requirements

## What's being built

Everything needed to install spectrace and keep it healthy: one install command,
CI and the README.

## Who it serves

Users installing the skills; the maintainer.

## Requirements

- R1@2: Installs with one command for any agent, through the `skills` CLI, into the folder each agent reads; no plugin, installer script or release archive to maintain.
- R2@1: CI runs the `trace.py` tests and `trace check` on this repo's own `planning/` on every push.
- ~~R3@1: A release is cut manually from a workflow that bumps the manifests' version and tags it.~~ retired 2026-10-06
- R4@2: The README explains the idea, installation and the three skills, and fits on about one screen before the details; it shows CI, license and Python badges and states its limits.
- R5@1: CI runs the tests on the oldest supported Python (3.9) and a current one, on Linux and Windows.
- R6@1: The GitHub repository is public, with a description and topics that make it findable.

## Out of scope

- Publishing: creating the GitHub repository and the first push happen only on the maintainer's explicit go-ahead.

## Dependencies

002, 003, 004.

## Owner split

Agent prepares everything; the maintainer creates the repository.
