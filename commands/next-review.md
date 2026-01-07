---
argument-hint: '[slug]'
description: Worker command - review code against requirements, output findings with verdict
---

# Review

Read `~/.agents/commands/prime-reviewer.md` first if you haven't already.

Slug given: "$ARGUMENTS"

---

## Step 1: Determine Slug

**If slug provided**: Use that slug to find `todos/{slug}/` folder

**If NO slug provided**:
1. Read `todos/roadmap.md`
2. Find first item marked `[>]` without `todos/{slug}/review-findings.md`
3. If none found, inform the user and stop

---

## Step 2: Load Context

Read these files to understand what was built:

1. `todos/{slug}/requirements.md` - WHAT should have been built
2. `todos/{slug}/implementation-plan.md` - HOW it was supposed to be built
3. `~/.agents/docs/development/coding-directives.md` - Coding standards
4. `~/.agents/docs/development/testing-directives.md` - Testing standards
5. `README.md`, `AGENTS.md`, `docs/*` - Project patterns

---

## Step 3: Identify Changes

```bash
git status
git log --oneline HEAD..main
git log --oneline main..HEAD
git diff $(git merge-base HEAD main)..HEAD --name-only
git diff $(git merge-base HEAD main)..HEAD
```

**Why merge-base?** If main has new commits your branch hasn't merged, `git diff main..HEAD` treats those as regressions. Merge-base limits diff to branch changes only.

---

## Step 4: Dispatch Sub-Agents

Based on changed files, dispatch relevant sub-agents in parallel:

| Changed | Sub-agent to dispatch |
|---------|----------------------|
| Any code | `next-code-reviewer` |
| Test files | `next-test-analyzer` |
| Error handling | `next-silent-failure-hunter` |
| Type definitions | `next-type-design-analyzer` |
| Comments/docs | `next-comment-analyzer` |

Wait for all sub-agents to complete. Collect their findings.

---

## Step 5: Aggregate Findings

Combine sub-agent findings with your own observations. Write to `todos/{slug}/review-findings.md`:

```markdown
# Code Review: {slug}

**Reviewed**: {date}
**Reviewer**: {agent}

## Requirements Coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| {req} | ✅/⚠️/❌ | |

## Critical Issues (must fix)

- [{aspect}] `file:line` - Description
  - Suggested fix: ...

## Important Issues (should fix)

- [{aspect}] `file:line` - Description
  - Suggested fix: ...

## Suggestions (nice to have)

- [{aspect}] `file:line` - Minor improvement

## Strengths

- Positive observations

---

## Verdict

**[ ] APPROVE** - Ready to merge
**[ ] REQUEST CHANGES** - Fix critical/important issues first

{Mark one with [x]}

### If REQUEST CHANGES:

Priority fixes:
1. {issue}
2. {issue}
```

---

## Step 6: Output

- Write findings to `todos/{slug}/review-findings.md`
- Report summary and verdict to the caller

---

## Important

- You ONLY review and report
- Master/orchestrator decides next action
- Re-run review after fixes are applied
