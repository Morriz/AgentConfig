---
argument-hint: '[slug]'
description: Architect command - analyze codebase and discuss requirements with orchestrator
---

# Prepare

Read `~/.agents/commands/prime-architect.md` first if you haven't already.

**YOUR ROLE**: Analyze, think, and discuss. You do NOT write or modify any files. The orchestrator drives decisions and handles all file operations.

Slug given: "$ARGUMENTS"

---

## If No Slug Provided

Help decide what to work on:

1. Read `todos/roadmap.md`
2. Report current items and your recommendations:
   - What items are pending?
   - What would you prioritize and why?
   - Any items that need clarification?
3. Discuss with orchestrator until they decide

---

## If Slug Provided

### Requirements Analysis

Check if `todos/{slug}/requirements.md` exists.
Check if `todos/{slug}/implementation-plan.md` exists.

**If requirements.md exists but no implementation-plan.md:** Read it and determine wether you think its ready after examining context and related files. Respond with analysis.

**If requirements.md missing:** Analyze and report:
- What problem does this solve?
- What requirements do you see?
- What questions or ambiguities exist?
- What constraints should we consider?

### Implementation Plan Analysis

**If implementation-plan.md exists:** Read it and determine wether you think its ready after examining context and related files. Respond with analysis.

**If missing:** Analyze and report:
- What approach would you recommend?
- What files need changes?
- What's the task breakdown?
- What risks or open questions do you see?

---

## Communication Format

```
ANALYSIS: {slug}

**Context:** [What I found in the codebase]

**Findings:**
- [Finding 1]
- [Finding 2]

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

**Open Questions:**
- [Question 1]
- [Question 2]

What are your thoughts?
```

---

## When Both Files Exist
Just return:
```
PREPARED: {slug}
Ready for implementation.
```
