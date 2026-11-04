# Research: keeping a coding agent in check

> Owns: the findings and proposals of the 2026-11-04 session on agent control, dead code after pivots and where specs live · Not here: accepted decisions (they go to the contracts and CHANGES.md once taken), specs (`planning/roadmap.md`)

Status: **discussion**. Nothing here is implemented or decided yet.

## 1. Starting point

specloop, spectrace and the spec-driven tools tried so far all fail at the same thing: full control over what the agent does in the code.

What works in spectrace:

- The scaffold of rules: PRODUCT, ARCHITECTURE, DESIGN, ENGINEERING, TESTING and OPERATIONS. With them the agent keeps its judgment most of the time. It weighs the pros and cons of a task, heads off errors and writes coherent tests. It does not always get this right.
- Planning with specs, as an idea.

What does not work:

1. **It obeys instead of objecting.** Suppose we decide something counterproductive, such as "do not use the letter m", that hurts the rest of the project. The agent does not push back and argue for using the "m". It builds odd workarounds around the decision.
2. **Changes of direction leave debris.** We add tasks and cases, validate, and find it should have been done differently. Dead, obsolete or spaghetti code is left all over.
3. **Specs in the repo.** With more than one developer they cause merge conflicts, and the files grow fast. It might be better if they lived in GitHub or ClickUp and the agent read them from there.

## 2. Premise

- Full control over an agent is not possible with any tool. The agent is probabilistic, and every extra rule is more text competing for its attention. Compliance drops as sessions grow and after context compaction.
- If the goal is "nothing slips through", every tool fails and more process keeps getting added. That is what happened with specloop, spectrace and the spec-driven frameworks.
- **Reachable goal:** whatever slips through is caught before it reaches `main`, and undoing it is cheap.
- Control lives in the diff, in deterministic checks and in git, not in the instructions.

## 3. Evidence: the failing rules are already written

Both failures are already covered by text in spectrace:

- "If a rule here is wrong, say so and propose the change. Do not work around it." (`skills/spectrace/assets/contracts/AGENTS.md`, hard rule 4, repeated at the end of `playbooks/change.md`)
- "Add a task that removes the old code, tests and docs" (`playbooks/change.md`, change of direction, step 2)

**Conclusion:** the problem is not the wording. Better wording will not fix it.

## 4. What stays

- The contracts and the router in `AGENTS.md`.
- The short hard rules: git, secrets, language.

## 5. Problem 1: it obeys instead of objecting

### Causes

- **The working flow puts the agent in executor mode.** `AGENTS.md` says "Take the first open `[agent]` task… Implement only that task." Hard rule 4 asks it to object, while the flow asks it to do only the task. The flow wins because it is concrete and it applies at the moment of acting.
- **The rule is abstract.** The agent never perceives "do not use m" as a wrong rule. It perceives it as a constraint to satisfy, so rule 4 never fires.
- **Decisions carry no reason.** The spec format asks for a trade-off only "when it is not obvious" (`plan.md`, Design). A decision without a reason can only be obeyed, not argued with.
- **A decision written into a contract is defended.** The agent assumes the user had a reason for an odd decision.

### Mitigation

1. **Make a workaround an observable signal, not a judgment.** Each of these counts as a workaround:
   - a wrapper or shim to dodge something,
   - duplicated code,
   - a special case in a conditional,
   - a try/except that silences errors,
   - disabling a test or a lint rule.

   The rule: if honoring a decision needs any of these, stop and report the conflict before writing code.
2. **Every decision has a "why" and a "revisit if"**, for example "revisit if it forces workarounds". That gives the agent something to argue with.
3. **Separate hard rules from decisions.** Git and secrets rules are not negotiable; product decisions are. Today both are written the same way.
4. **Add a critic with a clean context**: a subagent, `/code-review` or another session. It reads the diff and the decisions and answers "which decision is forcing workarounds?". This works better than asking the implementing agent to object to itself.
5. **Human side:** before recording an odd decision, ask for the strongest argument against it. Once it is written down, it is harder to move.

**Limit:** sycophancy goes down but does not disappear.

## 6. Problem 2: dead code and spaghetti after a change of direction

### Causes

- Agents add code. They rarely delete unless asked.
- The "remove the old code" step fires only when someone declares a change of direction. The real case is **gradual drift**: tasks and cases are added and validated, and only then is the approach found to be wrong. No single step looks like a change of direction, so the step never fires.

### Mitigation

1. **Discard and redo (the most important one).** With agents code is cheap, so a wrong attempt is not evolved further. Explore on a branch. If validation shows the approach was wrong, delete the branch, write down what was learned in three lines and reimplement cleanly from `main`. This is the only measure that attacks spaghetti. No tool detects spaghetti.
2. **Deterministic check.** A dead-code detector (knip, vulture, deptry, ruff F401/F841), plus a Claude Code Stop hook, plus CI. It catches what is left unused. It does not catch code that is still wired in but no longer makes sense; only a review sees that.
3. **Diffs small enough to read.** If a diff is too big to review, control is already lost.
4. **Delete first.** On a change of direction, the first commit removes what no longer applies, and only then does building start.
5. Run `/simplify` after each change of direction.

## 7. Problem 3: where specs live

### 7.1 Split by rate of change

| What | Where |
|---|---|
| Contracts | Repo. They change rarely, are versioned with the code and the agent reads them offline |
| Current decisions, with their reason | Repo, inside the contract they affect |
| Work in progress: roadmap, specs, tasks, blockers | A tracker (GitHub Issues or ClickUp), **only with a team** |
| History | git, pull requests and closed issues |

- With a team, the conflict point is `roadmap.md`, a single file everyone edits.
- `CHANGES.md` grows without end and repeats what git and pull requests already keep.

**Cost of a tracker:**

- The spec and the code no longer change in the same commit.
- The agent needs network access and credentials.
- **ClickUp** has an official hosted MCP server in public beta: `claude mcp add --transport http clickup https://mcp.clickup.com/mcp`, with OAuth. Its daily call allowance is 100 on the free plan, and it can delete tasks, so use it mostly read-only.

### 7.2 Solo developer: specs stay in the repo

The reason to move them out, conflicts between developers, does not apply. The remaining problem, growth, is solved by deleting:

- One file per spec, and only the next one written in full. `plan.md` already says this.
- Delete the spec when it is done. `plan.md` already says this.
- The roadmap shows only open work. Finished work is in `git log`.
- Drop `CHANGES.md`. The reason lives in the contract and the history in git.
- **When a decision changes, rewrite the spec instead of striking items.** `~~D1~~ → D2` is the documentation version of dead code: obsolete text that piles up. git already keeps the previous version.

Advantages: spec and code go in the same commit, it works offline, and the agent reads it with no extra tool.

GitHub Issues makes sense for a solo developer only to see or capture tasks from the web or a phone, to manage several repos, or when another developer is about to join.

### 7.3 GitHub mechanisms for tasks

| spectrace | GitHub |
|---|---|
| Spec | An issue, created from an issue form (`.github/ISSUE_TEMPLATE/spec.yml`) with Goal, Requirements, Design and Tasks |
| Tasks | A `- [ ]` checklist in the issue body. Sub-issues exist but are too much for one developer |
| Phase or release | Milestone |
| Roadmap | A Project (board, table or roadmap view with custom fields), or the list of milestones |
| `blocked:` | A "blocked by" dependency or a label |
| `verified:` / done | `Closes #12` in the commit message. The issue closes when the commit reaches `main`; no pull request needed |

- **CLI:** `gh issue create/list/view/edit/close`. Since gh v2.94 (2026-06-10) the CLI also handles issue types, sub-issues and dependencies. Issue types need an organization.
- **MCP:** there is an official GitHub MCP server. In Claude Code, `gh` is enough.
- **Proposal for spectrace:** init asks one question, `planning: repo | github`. The spec format is the same in both, so moving from one to the other is copy and paste.

## 8. Ceremony scales with risk

The worry was that verification protocols (pull requests, issues, CI as a gate) slow down small tasks and a single developer.

That worry is right. The pull request plus CI gate was meant for teams, and it also clashes with the rule of committing straight to `main`.

**Principle:**

- What is automatic and fast always applies: the contracts, the workaround signals and the local check.
- What costs human time applies only when the risk justifies it: a spec, an issue, a pull request, a reviewer, a disposable branch.

| Measure | Cost per task | When |
|---|---|---|
| Contracts and router | None, they already exist | Always |
| Workaround signals as a stop condition | None until it fires, and then it saves time | Always |
| Local check (lint, dead code, affected tests) | Seconds | Always |
| Short spec | Minutes | Features with several tasks |
| Issue, pull request and CI as a gate | High | Team only |
| Clean-context reviewer, disposable branch | High | Only when a decision or the approach changes |

### Levels

| Level | When | What happens |
|---|---|---|
| **0, small** | It fits in one sentence and touches no recorded decision | No spec, issue or pull request. The agent implements, the local check runs, it commits to `main`. The user reads the diff, which is small |
| **1, feature** | Several tasks or several sessions | Short spec with Goal and Tasks. Solo: in the repo, commit to `main`. Team: issue and pull request |
| **2, decision or direction** | It contradicts or changes a recorded decision, needs a workaround, or changes the approach | Plan with a conflicts section, a disposable branch, delete first, then a clean-context reviewer |

### Rules that keep the levels coherent

- **Escalation to level 2 is triggered by observable signals, not by size.** "Small, skip the protocol" is exactly how gradual drift starts, since every step looked small. A one-line task that forces a workaround around a decision is level 2. A large feature that touches no decision stays at level 1.
- **The agent proposes the level in one line and the user can override it.** If the agent underrates a task, the damage is bounded because the local check always runs.
- **Solo:** no pull request. Commit to `main`, and CI on push is an alarm after the fact, not a gate.
- **The Stop hook runs only fast checks.** If the full test suite is slow, it goes to CI.

**Compared with spectrace today:** every task currently pays manual ceremony: marking `[x]`, writing the `verified:` line and updating the roadmap. The automatic check replaces that. Done well, level 0 is faster than the current flow, not slower.

## 9. Tools surveyed

Most sources are blogs, aggregators or vendor pages. Star counts and vendor claims are unverified.

### Dead-code detectors (highest impact)

| Stack | Tool | Finds |
|---|---|---|
| TS/JS | [knip](https://www.tothenew.com/blog/knip-an-essential-tool-for-code-hygiene/) | Unused files, exports, types and dependencies. `--max-issues 0` fails CI |
| Python | [vulture](https://github.com/jendrikseipp/vulture) | Unused functions, classes and variables, with a confidence level. Ships a pre-commit hook and exits with code 3 on findings |
| Python | deptry | Dependencies in `pyproject.toml` that are no longer imported |
| Python | ruff (F401, F841) | Unused imports and variables |

A documented case: an agent switched charting libraries and left the old dependency installed. The linter caught it; the spec did not ([source](https://stevekinney.com/courses/self-testing-ai-agents/dead-code-detection)). A real example of knip as a required CI job: [linearis#242](https://github.com/linearis-oss/linearis/pull/242).

### Enforcement through Claude Code hooks

- **Stop hook:** when the agent tries to finish, it runs lint, the dead-code detector and tests. If one fails, it returns `decision: block` with the reason, and the agent keeps working. Check `stop_hook_active` to avoid a loop. Docs: code.claude.com/docs/en/hooks. Guides: [codeongrass](https://codeongrass.com/blog/claude-code-hooks-done-means-tests-passed/), [claudefa.st](https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement).
- **PostCompact / SessionStart hook:** re-injects the rules after context compaction.
- [proof-of-done](https://pypi.org/project/proof-of-done/): checks the agent's claims against what actually ran in the transcript.
- Why hooks beat instructions: [dev.to](https://dev.to/kenimo49/almost-every-time-vs-every-time-why-hooks-beat-instructions-for-ai-agents-28bf), [bitbytebit](https://bitbytebit.substack.com/p/agent-hooks-deterministic-guardrails).

### Spec-driven frameworks

- [OpenSpec](https://openspec.dev/docs/getting-started) (Fission AI, MIT). Built for existing codebases. Each change gets a folder with `proposal.md`, `design.md`, `tasks.md` and spec deltas marked **ADDED / MODIFIED / REMOVED**; archiving merges the deltas into the main specs. Install with `pnpm add -g @fission-ai/openspec`, then run `openspec init`. It is the closest to spectrace, and what it adds is an explicit REMOVED.
- **GitHub Spec Kit:** the agent-agnostic default, leaning toward greenfield work.
- **Rejected:** BMAD, which is very heavy with 12+ AI personas, and Kiro, which forces a change of IDE.
- The most common complaint against all of them is manual spec drift, the same problem spectrace has. Comparisons: [Augment](https://www.augmentcode.com/tools/best-spec-driven-development-tools), [aicodingpatterns](https://aicodingpatterns.com/en/patterns/openspec-vs-spec-kit-vs-bmad/), [spec-compare](https://github.com/cameronsjo/spec-compare).

### Review and cleanup

- Built into Claude Code: `/simplify` for reuse and cleanup, and `/code-review` for bugs.
- [obra/superpowers](https://trevorlasn.com/blog/superpowers-claude-code-skills) (plugin, MIT): brainstorm, then plan, then TDD, then a two-stage review that checks spec compliance first and code quality second. It deletes code written before its test.
- Dead-code agents and commands:
  - [devflow](https://github.com/benny9193/devflow): `/dead-code` writes a removal patch.
  - [unused-code-cleaner](https://www.remoteopenclaw.com/agents/claude/davila7/claude-code-templates/unused-code-cleaner)
  - [dead-code-finder](https://www.claudepluginhub.com/commands/samuelj90-dead-code-finder-plugins-dead-code-finder/commands/remove-dead-code)
  - [skills-dead-code](https://github.com/torifo/skills-dead-code)
  - [refactor-clean](https://openskillindex.com/skills/sc30gsw-claude-code-customes-refactor-clean)

### Optional

- [decision-cli](https://github.com/kurdin/decision-cli): ADRs over MCP, with a lifecycle that includes superseded. Register it with `claude mcp add decision -- pnpm dlx @aitool/decision-cli mcp`. Adoption is low. Similar tools: [mcp-server-decisions](https://pypi.org/project/mcp-server-decisions), [AdrMcp](https://nuget.org/packages/adrmcp).
- [Serena](https://github.com/oraios/Serena) (MCP): symbol-level tools such as finding every reference before deleting something.
- [CodeScene CodeHealth MCP](https://codescene.io/docs/developer-tools/mcp/codescene-mcp-server.html): a code health score the agent has to keep. Partly paid.
- Drift detection: no tool targets "obsolete code after a change of direction". The closest are [drift-analyzer](https://pypi.org/project/drift-analyzer/2.5.1/), which looks for architectural erosion in Python, and [Catching AI Drifts](https://khaledea.substack.com/p/catching-ai-drifts-program-analysis).

## 10. Candidate changes to spectrace

| Area | Change |
|---|---|
| Keep | Contracts, router, short hard rules |
| `AGENTS.md` working flow | Replace "take the next task, implement only that task" with: propose the level, then for level 2 a plan with conflicts, implement, local check, clean reviewer |
| Hard rules vs decisions | Separate them. Every decision gets a "why" and a "revisit if" |
| Workarounds | An explicit list of workaround signals as a stop condition |
| `change.md` | Discard and redo as the default when validation fails. On a change of direction, delete first |
| Spec format | Rewrite instead of striking `~~D1~~ → D2` |
| `CHANGES.md` | Remove: the reason lives in the contract, the history in git |
| `roadmap.md` | Open work only |
| Planning location | Init asks `planning: repo \| github` |
| Extras offered by the skill | Add a dead-code check for the stack plus a fast Stop hook |

## 11. Open questions

- With a team, does planning happen in GitHub or ClickUp? This decides the level 1 design for teams.
- Which repo should pilot the dead-code check and the Stop hook: Triarii (Python), a TS project, or spectrace as an extra?
- Does removing `CHANGES.md` lose anything that git and the contracts do not already keep?

## Sources

- ClickUp MCP: [contextbolt](https://contextbolt.com/blog/clickup-mcp/), [developersdigest](https://www.developersdigest.tech/mcp-servers/clickup), [codegen](https://codegen.com/mcp/clickup/)
- GitHub CLI 2.94: [changelog](https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/), [classmethod](https://dev.classmethod.jp/en/articles/github-cli-294-issue-types-sub-issues/)
- Pre-merge verification and spec drift: [Augment](https://www.augmentcode.com/guides/ai-agent-pre-merge-verification)
