---
description: Review code changes for quality, bugs, and project compliance. Use before committing or as part of /next-work.
argument-hint: '[subject]'
---

You are now in **reviewer mode**.Review code changes using specialized analysis. Outputs findings organized by severity.

## Step 1: Determine Subject

Look at the end of this file for "ARGUMENTS GIVEN:" to see if a subject was provided.

**If subject provided as argument**:

- Use that subject to find `todos/{subject-slug}/` folder

**If NO subject provided**:

1. Read `todos/roadmap.md`
2. Find the first item marked as in-progress (`- [>]`) and which has no `todos/{subject-slug}/review-findings.md` yet.
3. If no in-progress item, don't do anything and inform the user.

Next you will compare what was done in the worktree branch against the requirements and implementation plan.

## Step 2: Identify Changes

```bash
git status
git diff --name-only HEAD
```

## Step 3: Load Project Context

You already read the `~/.agents/docs/coding-directives.md`. Also read `~/.agents/docs/testing-directives.md`.
Now read project specifics:


- `README.md`, `docs/*` - Project patterns and conventions
- Existing code in same modules - New code should match existing style

## Step 4: Determine Applicable Reviews

Based on changes, select which aspects to run:

| Aspect | When to Run | Focus |
| ------ | ----------- | ----- |
| **code** | Always | Quality, bugs, project compliance |
| **tests** | Test files changed | Coverage, behavioral testing |
| **errors** | Error handling code | Silent failures, catch blocks |
| **types** | Types added/modified | Type design, invariants |
| **comments** | Comments/docs added | Accuracy, maintainability |
| **simplify** | After other reviews pass | Clarity, reduce complexity |

## Step 5: Run Reviews

For each applicable aspect, analyze the changes:

### code (General Quality)

- Follows existing patterns in codebase
- No unnecessary abstractions
- Functions are focused and small
- No code duplication
- Types explicit (no `Any`/`any`)
- Null/undefined handled properly
- Error cases handled, not swallowed

### tests (Test Quality)

- Tests behavior, not implementation
- One assertion per test
- Edge cases covered
- Mocks only at boundaries
- No testing of private methods

### errors (Error Handling)

- No empty catch blocks
- Errors logged with context
- No swallowed exceptions
- Fail-fast where appropriate
- Recovery logic explicit

### types (Type Design)

- Types express invariants
- No `any` or `Any`
- Illegal states unrepresentable
- Validation at boundaries

### comments (Documentation)

- Comments match code behavior
- No stale/misleading comments
- Complex logic explained
- API contracts documented

### simplify (Complexity Reduction)

- Can logic be simplified?
- Are abstractions necessary?
- Can functions be smaller?
- Is code self-documenting?

## Step 6: Aggregate Findings

Organize all findings by severity:

```markdown
# Code Review Findings

## Critical Issues (must fix)
- [aspect] `file:line` - Description
  - Suggested fix: ...

## Important Issues (should fix)
- [aspect] `file:line` - Description
  - Suggested fix: ...

## Suggestions (nice to have)
- [aspect] `file:line` - Minor improvement
  - Reason: ...

## Strengths
- Positive observations about the code

## Verdict
[ ] APPROVE - Ready to commit/merge
[ ] REQUEST CHANGES - Fix critical/important issues first
[ ] NEEDS DISCUSSION - Architectural concerns to resolve
```

## Step 7: Output

- Write to `todos/{subject-slug}/review-findings.md`
- Brief summary to the user and mention file location.

## IMPORTANT

- Run before committing, not after
- Fix critical issues before moving on
- Re-run after applying fixes

---
ARGUMENTS GIVEN: $ARGUMENTS