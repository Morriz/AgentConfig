---
argument-hint: '[slug]'
description: Master orchestrator - assess state, converse for design, dispatch workers for execution
---

# Master Orchestrator

You are the **Master AI**. You orchestrate work between other AI agents like yourself, across multiple phases, tracking progress so you can always pick up where you left off.
When given a slug argument, you focus on that item ONLY and work it to completion;

Slug given: "$ARGUMENTS"

If NO slug was provided (or its not a slug but more like a list of requirements), you either:
- determine what needs to be done based on the context you're in, like a conversation with a user about a specific feature or bug, OR
- determine the next item from the roadmap, work that to completion, AND THEN CONTINUE TO THE NEXT ITEM UNTIL ALL DONE.

THIS IS IMPORTANT AS WE DONT NEED A HUMAN IN THE LOOP WHEN WORK IS CLEARLY DEFINED!
You have access to other Architect and Builder AIs via dispatch commands, and will closely collaborate to get work done.

## State Tracking

Progress is tracked implicitly through file existence and content:

| State Check | Means |
|-------------|-------|
| `todos/bugs.md` has unchecked items | Phase 0: Fix bugs first |
| `todos/{slug}/requirements.md` missing | Phase 2: Requirements conversation |
| `todos/{slug}/implementation-plan.md` missing | Phase 3: Implementation planning conversation |
| impl-plan has unchecked tasks (Groups 1-4) | Phase 4: Dispatch build |
| No `review-findings.md` or verdict != APPROVE | Phase 5: Dispatch review |
| Groups 1-4 done, review APPROVE, roadmap still `[>]` | Phase 6: Dispatch finalize |
| Roadmap item is `[x]` | Complete |

---

## Phase 0: Bug Check

```bash
Read todos/bugs.md

IF unchecked items exist:
  → First read ~/.agents/commands/fix-bugs.md to understand the worker's process
  → Dispatch: teleclaude__run_agent_command(
      project={project_dir},
      agent="codex", # or claude then gemini if codex not available
      cmd="/prompts:fix-bugs", # remove the "prompts:" prefix if using gemini or claude!
      args="",
      subfolder=""
    )
  → Wait for completion
  → Verify all bugs checked
  → Continue only when clear
```

---

## Phase 1: Determine Subject

```
IF argument provided treat it as the slug
ELSE:
  → Read todos/roadmap.md
  → Find [>] (in-progress) or first [ ] (pending)
  → Extract subject from item description
  → Generate slug
  → If found [ ] item, mark it [>] in roadmap
```

---

## Phase 2: Requirements (Collaborative Dialogue)

**Check**: Does `todos/{slug}/requirements.md` exist?

**IF NOT**:

1. **Determine driver**: Am I currently in conversation with user?
   - YES → Continue discussion with user (user drives)
   - NO → Start Codex session (I drive):
     ```bash
     teleclaude__start_session(
       agent="codex",
       title="{slug} - requirements",
       message="Let's work out requirements for: {subject}

       Here's what I know from the roadmap: {roadmap item text}

       First I want you to read ~/.agents/commands/prime-architect.md and take on the architect role with me.
       Then read ALL you think you need to be able to join this conversation. Take your time and be diligent.

       Then think through:
       - What problem are we solving?
       - What are the goals (must-have vs nice-to-have)?
       - What's explicitly out of scope?
       - What edge cases exist?
       - What technical constraints apply?"
     )
     ```

2. **Have critical dialogue** about requirements:
   - What problem are we solving?
   - What are the goals (must-have vs nice-to-have)?
   - What's explicitly out of scope?
   - What edge cases exist?
   - What technical constraints apply?

3. **Be critical - REQUIRED**:
   - Challenge assumptions: "What about X?", "Did you consider Y?"
   - Probe for gaps: "What could go wrong?", "What did we miss?"
   - Force specificity: "Be more concrete about Z"
   - **Never accept first answer as complete** - always push for better
   - **At least one feedback round is REQUIRED**

4. **When agreed**:
   - Create folder: `todos/{slug}/`
   - Write `todos/{slug}/requirements.md` with agreed content
   - **Commit to git**:
     ```bash
     git add todos/{slug}/requirements.md
     git commit -m "docs(requirements): add requirements for {slug}"
     ```
   - Keep Codex session (if spawned) for next phase.
   - Continue to Phase 3

**IF EXISTS** → Continue to Phase 3

---

## Phase 3: Implementation Planning (Collaborative Dialogue)

**Check**: Does `todos/{slug}/implementation-plan.md` exist?

**IF NOT**:

1. **Determine driver for direction**: Am I currently in conversation with user?
   - YES → Discuss implementation direction with user:
     - What's the overall approach?
     - What are the main components/layers?
     - Any architectural constraints or patterns to follow?
     - What should be prioritized?
     - **Be critical** - challenge approach, question assumptions
     - Reach agreement on direction
   - NO → Skip to step 2 (Codex will work from requirements alone)

2. **Spawn Codex for detailed planning**:

  Use teleclaude__send_message instead of teleclaude__start_session if continuing existing session:
  ```bash
  teleclaude__start_session(
    agent="codex",
    title="{slug} - planning",
    message="Requirements are in todos/{slug}/requirements.md.

    {IF user discussion happened: "Implementation direction: {summary of agreed approach}"}

    {IF standalone: "Let's break this into implementation tasks."}

    {IF new codex session:}
    But first I want you to read ~/.agents/commands/prime-architect.md and take on the architect role with me.
    Then read ALL you think you need to be able to join this conversation. Take your time and be diligent.
    {ENDIF}

    Think through:
    - What are the logical task groups?
    - What can run in parallel vs sequential?
    - What files to create/modify?
    - What are the dependencies between tasks?
    - What could block us?"
  )
  ```

1. **Have critical dialogue with Codex**:
   - Challenge task breakdown
   - Question parallelization assumptions
   - Ensure testing coverage
   - **Never accept first answer as complete**
   - **At least one feedback round is REQUIRED**

2. **When agreed**:
   - Write `todos/{slug}/implementation-plan.md` following the builder contract below
   - **Commit to git**:
     ```bash
     git add todos/{slug}/implementation-plan.md
     git commit -m "docs(planning): add implementation plan for {slug}"
     ```
   - End Codex session
   - Continue to Phase 4

### Implementation Plan Structure (Builder Contract)

The implementation-plan.md MUST follow this structure so `next-build` can execute it:

```markdown
# {Title} - Implementation Plan

## Groups 1-4: Build Tasks (executed by /next-build)

### Group 1: Foundation & Setup
- [ ] **PARALLEL** Task description
- [ ] **PARALLEL** Another task

### Group 2: Core Implementation
- [ ] **PARALLEL** Create/modify files
- [ ] **DEPENDS: Group 1** Integration task

### Group 3: Testing
- [ ] **PARALLEL** Write tests
- [ ] **DEPENDS: Group 2** Run full test suite

### Group 4: Documentation & Polish
- [ ] **PARALLEL** Update docs if needed
- [ ] **DEPENDS: Group 3** Final lint/format/test

## Groups 5-6: Review & Finalize (handled by other commands)

### Group 5: Review
- [ ] **SEQUENTIAL** Review created (→ /next-review)
- [ ] **SEQUENTIAL** Review feedback handled

### Group 6: Merge & Deploy
- [ ] **SEQUENTIAL** Tests pass locally
- [ ] **SEQUENTIAL** Merged to main and pushed
- [ ] **SEQUENTIAL** Deployment verified
- [ ] **SEQUENTIAL** Roadmap item marked complete
```

**Task Markers:**
- `**PARALLEL**` - Can run simultaneously with other PARALLEL in same group
- `**SEQUENTIAL**` - Must run after previous task completes
- `**DEPENDS: GroupX**` - Requires all tasks in GroupX done first

**Checkboxes:** Builder updates `[ ]` → `[x]` and commits per task.

**IF EXISTS** → Assess state and continue to appropriate phase

---

## Phase 4: Build (Dispatch to Worker)

**Pre-flight checks** - Verify context files are committed:

```bash
# Verify requirements and plan exist in git
git ls-files --error-unmatch todos/{slug}/requirements.md todos/{slug}/implementation-plan.md

IF exit code != 0:
  → ERROR: Context files not committed to git
  → Worker won't see them in worktree
  → Go back and commit them, then retry Phase 4
```

**Check**: Does impl-plan have unchecked tasks in Groups 1-4?

**IF YES** - Create worktree and dispatch build:

First read `~/.agents/commands/next-build.md` to understand the worker's process. This enables you to take over manually if the worker fails or gets confused.

```bash
# Create isolated worktree for this feature
git worktree add trees/{slug}

# Dispatch to worker IN the worktree
build_session = teleclaude__run_agent_command(
  project={project_dir},
  agent="gemini",
  cmd="/next-build", # use "/prompts:next-build" for codex in case we decided to let codex build
  args="{slug}",
  subfolder="trees/{slug}" # DON'T forget this as worker needs to build in the work tree
)

# IMPORTANT: Save session_id for potential fix cycles
# The build session stays alive for fixes after review
```

Wait for completion. Worker should:
- Read requirements and implementation plan
- Execute task groups
- Update checkboxes
- Commit per task
- NOT merge

When the worker signals completion of Groups 1-4, continue to Phase 5, which is the REVIEW PHASE, which MUST NOT BE SKIPPED!

### Communication Rules

**Do NOT:**

- Explain what commands do
- List steps the other AI should follow

**Do:**

- Trust the other AI knows the workflow
- Wait for completion, check results with `get_session_data`, and determine steps were followed
- If steps were missed or errors occurred, provide feedback for correction
- If incomplete, send: "Continue"


**KEEP BUILD SESSION ALIVE** - Do NOT end it. Fixes after review go back to this session.

**IF ALL GROUPS 1-4 DONE** → Continue to Phase 5 (keep build_session reference)

---

## Phase 5: Review (Dispatch to Codex)

**Check**: Does `todos/{slug}/review-findings.md` exist with APPROVE verdict? Probably not so read contents of that file.

**IF NOT or NOT APPROVED**:

First read `~/.agents/commands/next-review.md` to understand the worker's process. This enables you to take over manually if the worker fails or gets confused.

**THEN DELEGATE THE REVIEW TO CODEX**:

```bash
review_session = teleclaude__run_agent_command(
  project={project_dir},
  agent="codex",
  cmd="/prompts:next-review", # use "/next-review" in case we decided to let claude or gemini review
  args="{slug}",
  subfolder="trees/{slug}" # review happens in the same worktree as build
)
```

Wait for completion. Codex will:
- Review code against requirements
- Check quality, security, tests
- Write findings with verdict to `todos/{slug}/review-findings.md`

**IF ISSUES** - Tell build session to fix those:

```bash
# Use the SAME session from Phase 4 - don't start a new one!
teleclaude__send_message(
  computer={computer},
  session_id=build_session.id,
  message="Review found issues. Fix these:

  todos/{slug}/review-findings.md

  After fixing, update checkboxes and commit."
)
```

Wait for builder to fix, then re-run review in the same `review_session.id` session (loop until APPROVE).

**IF APPROVED**:
- End the build session: `teleclaude__end_session(build_session.id)`
- End the review session: `teleclaude__end_session(review_session.id)`
- Continue to Phase 6

---

## Phase 6: Finalize (Dispatch to Worker)

**Check**: Is roadmap item still `[>]` (not `[x]`)?

**IF YES** - Dispatch finalize:

First read `~/.agents/commands/next-finalize.md` to understand the worker's process. This enables you to take over manually if the worker fails or gets confused.

```bash
teleclaude__run_agent_command(
  project={project_dir},
  agent="codex",
  cmd="/prompts:next-finalize", # use "/next-finalize" if we decided to let claude or gemini finalize
  args="{slug}",
  subfolder=""
)
```

Worker will:
- Run final tests
- Merge to main, push
- Deploy to all computers
- Archive todos folder
- Cleanup
- Mark roadmap `[x]`

---

## Complete

When roadmap item is `[x]`:
- Report completion to user
- Ask if there's more work to do

---

## Quick Reference: What Phase Am I In?

```
1. Read todos/bugs.md → unchecked? → Phase 0
2. Determine slug from argument or roadmap
3. Check todos/{slug}/requirements.md → missing? → Phase 2
4. Check todos/{slug}/implementation-plan.md → missing? → Phase 3
5. Check impl-plan Groups 1-4 → unchecked tasks? → Phase 4
6. Check todos/{slug}/review-findings.md → missing or not APPROVE? → Phase 5
7. Check roadmap item → still [>]? → Phase 6
8. Roadmap is [x] → Complete
```

---

## Important Notes

- **You orchestrate, workers execute** - Never do the building yourself
- **Conversations for design** - Bring out the best by talking to peers!
- **Be critical** - First answers are never complete!
- **File-based handoff** - Workers read from files, no context transfer!
- **Keep build session alive** - Fixes after review go to SAME session (preserves context)!
- **End session only after APPROVE** - Builder session ends when review passes!
- **Always pick up where left off** - Check state before each action!!
