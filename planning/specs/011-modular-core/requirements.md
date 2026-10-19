# 011 — modular-core — Requirements

## What's being built

The trace's code reorganized from one 896-line script into a small package next to a
launcher, with no change in what the trace does. It gives the code map (specs 012–014)
room to grow: each module has a size budget, the package installs and upgrades as one
unit, and `.spectrace/.gitignore` always lists what the trace generates.

## Who it serves

Everyone who runs `trace.py` today — nothing changes for them — and specs 012–015, which
add modules to the package.

## Requirements

- R1@1: Every `trace.py` command prints the same output and exits with the same status as before the split, for the same inputs.
- R2@1: `spectrace-start` copies `trace.py` and the `spectrace/` package into a target repo together, and an upgrade replaces both as one unit.
- R3@1: Every module of the package stays within its size budget, and a test fails when one does not.
- R4@1: `.spectrace/.gitignore` lists everything the trace generates, also in a repo where that file already existed.

## Out of scope

- New commands, output or formats (specs 012 onward).
- Changing `VERSION`: the contract is the same here.

## Dependencies

005, 010.

## Owner split

All agent.
