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

## Step 4: Parallel Skill-Based Review

Use the skills below to cover each review aspect. When you can run tasks in parallel, do so: run
each aspect in parallel and explicitly load the matching skill for that aspect. After all aspects
finish, aggregate the findings into a single review.

### Aspect → Skill → Task mapping

| Aspect | When to use | Skill trigger | Task to perform |
|--------|-------------|---------------|-----------------|
| code | Always | `next-code-reviewer` | Review code against project guidelines; find bugs, regressions, and pattern violations. |
| tests | Test files changed | `next-test-analyzer` | Evaluate test coverage, edge cases, and test quality; note missing or weak tests. |
| errors | Error handling changed | `next-silent-failure-hunter` | Detect silent failures, swallowed errors, bad fallbacks, missing logs. |
| types | Types added/modified | `next-type-design-analyzer` | Validate type design, invariants, and unsafe or leaky abstractions. |
| comments | Comments/docs added | `next-comment-analyzer` | Check comment accuracy, staleness, and misleading documentation. |
| simplify | After other reviews pass | `next-code-simplifier` | Identify unnecessary complexity; propose simplifications without behavior changes. |

When parallel execution is not available, load all listed skills yourself and complete the review
with those skills active.

---

## Step 5: Aggregate Findings

Combine findings from the skill-based review with your own observations. Write to `todos/{slug}/review-findings.md`:

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

## Step 6: Manage state

Update `todos/{slug}/state.json` by setting "review" to "approved" or "changes_requested"

---

## Step 7: Commit

Commit all changes in the cwd (worktree).

--- 

## Step 8: Output

Report summary and verdict to the caller

---

## Important

- You ONLY review and report
- Master/orchestrator decides next action
- Re-run review after fixes are applied
