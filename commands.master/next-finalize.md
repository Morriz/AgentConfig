---
argument-hint: '[slug]'
description: Worker command - merge, deploy, archive, cleanup after review passes
---

# Finalize Worker

You are a **Worker AI**. Handle post-review bookkeeping: merge, deploy, archive, cleanup.

**Prerequisites**: Review must have APPROVE verdict in `todos/{slug}/review-findings.md`.

Slug given: "$ARGUMENTS"

---

## Step 2: Verify Prerequisites

```
1. Read todos/{slug}/review-findings.md
2. Verify verdict is APPROVE
3. If not APPROVE, STOP and report: "Review not approved. Cannot finalize."
```

---

## Step 3: Final Tests

```
make test
```

Or equivalent test command. All tests must pass before proceeding.

---

## Step 4: Merge to Main

```bash
git checkout main
git pull origin main
git merge {slug} --no-edit
```

If merge conflicts:
1. Resolve conflicts
2. Run tests again
3. Commit resolution

---

## Step 5: Push to Remote

```bash
git push origin main
```

---

## Step 6: Deploy

Deploy to all computers:

```bash
/deploy
```

Or use teleclaude__deploy_to_all_computers if available.

Verify deployment succeeded on all machines.

---

## Step 7: Archive Todo Folder

```
1. Determine next archive number:
   - Check done/ folder for existing {NNN}-* folders
   - Take highest NNN, add 1
   - Zero-pad to 3 digits (e.g., 001, 002, 042)

2. Create archive folder:
   mkdir -p done/{NNN}-{slug}

3. Move todo folder:
   mv todos/{slug}/ done/{NNN}-{slug}/
```

---

## Step 8: Log Delivery

Append to `todos/delivered.md`:

```
| {date} | {slug} | {title} | DELIVERED | {commit-hash} | done/{NNN}-{slug} |
```

Create file with header if it doesn't exist:

```markdown
# Delivered Items

| Date | Slug | Title | Outcome | Commit | Archive |
|------|------|-------|---------|--------|---------|
```

---

## Step 9: Update Roadmap

```
1. Read todos/roadmap.md
2. Find the item for {slug} (marked [>])
3. Change [>] to [x]
4. Save file
```

---

## Step 10: Final Commit and Push

```bash
git add -A
git commit -m "chore({slug}): finalize delivery

- Archived to done/{NNN}-{slug}
- Updated roadmap
- Logged to delivered.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

---

## Step 11: Report Completion

```
✅ Finalized: {slug}

- Merged to main: ✓
- Deployed: ✓
- Archived to: done/{NNN}-{slug}
- Roadmap updated: [x]

Item complete. Ready for next work.
```

---

## Error Handling

**If merge fails:**
- Report conflict details
- Do NOT force merge
- Wait for Master guidance

**If deploy fails:**
- Report which computer(s) failed
- Do NOT mark roadmap complete
- Wait for Master guidance

**If any step fails:**
- Document what failed
- Do NOT proceed to later steps
- Report to Master

---

## What You Do NOT Do

- ❌ Build code (that's `/next-build`)
- ❌ Review code (that's `/next-review`)
- ❌ Fix bugs (that's `/fix-bugs`)
- ❌ Create requirements or plans (Master does that)

You ONLY handle post-review finalization.
