# 005 — distribution — Design

## Approach

- ~~D1@1 (implements R1): `.claude-plugin/plugin.json` and `marketplace.json` name the plugin `spectrace` at `0.1.0` with `skills: ./skills/`; `install.sh` and `install.ps1` download the release archive and copy `skills/` into `.agents/skills` (and `.claude/skills` when a `.claude/` folder exists), leaving an existing install alone unless forced. Adapted from specloop's.~~ retired 2026-10-06 → D5
- D2@1 (implements R2): `.github/workflows/ci.yml` runs `python3 -m unittest discover -s tests` and `trace.py check` on every push and pull request.
- ~~D3@1 (implements R3): `.github/workflows/release.yml`, run by hand, computes the next version from the Conventional Commits that touched `skills/` since the last tag (`scripts/next_version.py`, ported from specloop's `next-version.mjs`), commits the manifest bump through the GitHub API so it is signed, tags it, builds a deterministic `spectrace-skills.tar.gz` with a checksum and publishes the release. One workflow instead of specloop's two.~~ retired 2026-10-06
- D5@1 (implements R1): Installation is the `skills` CLI reading `skills/` straight from the repository — `pnpm dlx skills add SebassContreras/spectrace` (`-g` for global, `skills update` to update); the repo ships no plugin manifest, installer script or release archive.
- D4@2 (implements R4): `README.md` — badges (CI, license, Python 3.9+, Agent Skills), the idea in one paragraph, install, the three skills, how tasks are executed and traced, changing direction, limits, development.
- D6@1 (implements R5): `ci.yml` matrix through `actions/setup-python@v7`: Python 3.9 on `ubuntu-24.04` (3.9 has no builds for newer Ubuntu images), Python 3.13 on `ubuntu-latest` and `windows-latest`.
- D7@1 (implements R6): Public repository `SebassContreras/spectrace`, its description and topics set with `gh`.

## Deliverables

- `.github/workflows/ci.yml`
- `README.md`
