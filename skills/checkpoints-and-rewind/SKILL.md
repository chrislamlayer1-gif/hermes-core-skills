---
name: checkpoints-and-rewind
description: Use before making irreversible changes (deleting files, destructive git operations, large refactors). Use when you need the ability to roll back if something goes wrong. Use at the start of any task that modifies multiple files.
version: 1.0.0
author: Hermes Agent (adapted from Anthropic Claude Code Checkpoints)
license: MIT
metadata:
  hermes:
    tags: [checkpoints, rewind, safety, git, recovery, undo]
    related_skills: [think-tool, systematic-debugging, subagent-driven-development]
  triggers:
    - backup
    - rollback
    - undo
    - revert
    - snapshot
    - checkpoint
    - before change

---

# Checkpoints & Rewind

## Overview

Before making risky or irreversible changes, create a checkpoint. If things go wrong, rewind to the checkpoint. This gives you the confidence to experiment without fear of breaking things.

**Core principle:** Every multi-file change starts with a safety net.

## When to Use

- **Before large refactors** — Moving code, renaming files, changing architecture
- **Before deleting anything** — Files, directories, database data
- **Before destructive git operations** — `git reset`, `git rebase`, `git clean`
- **Before trying experimental approaches** — "Let's see if this works"
- **At the start of any task that modifies 3+ files**
- **Before running auto-fix in code review** (Step 7 of requesting-code-review)

**Do NOT use for:** Single-file edits, reading files, running tests, or any operation that's trivially undoable.

## How to Create a Checkpoint

### Method 1: Git Commit (Recommended)

```bash
# Before making changes
git add -A && git commit -m "[checkpoint] before <description>"

# Make your changes...

# If things go wrong:
git reset --hard HEAD~1

# If things go right:
# Keep the checkpoint commit, or squash it later
```

### Method 2: Git Stash (For Experiments)

```bash
# Before making changes
git stash push -m "checkpoint: <description>"

# Make your changes... (starting from clean state)

# If things go wrong:
git stash pop  # restore the checkpoint (undoes your changes)

# If things go right:
git stash drop  # discard the checkpoint
```

### Method 3: Manual Backup (No Git)

```bash
# Before making changes
cp -r important_file.ts important_file.ts.checkpoint

# Make your changes...

# If things go wrong:
cp important_file.ts.checkpoint important_file.ts

# Clean up after success:
rm important_file.ts.checkpoint
```

## Naming Convention

Always include:
- `[checkpoint]` prefix (easy to search in git log)
- What you're about to do
- Date/time if helpful

Good:
```
[checkpoint] before refactoring ChantingHall to adapter pattern
[checkpoint] before trying experimental rendering approach
[checkpoint] before deleting old story-data.js
```

Bad:
```
[checkpoint] save
[checkpoint] before changes
wip
```

## Rewind Process

When you need to undo:

### Step 1: Assess the Damage

```bash
# See what changed
git status
git diff --stat

# See recent commits
git log --oneline -5
```

### Step 2: Choose Rewind Method

**Scenario A: Just checkpointed, no other commits in between**
```bash
git reset --hard HEAD~1
```

**Scenario B: Checkpoint was several commits ago**
```bash
# Find the checkpoint commit
git log --oneline --grep="\[checkpoint\]"

# Revert to it
git reset --hard <commit-hash>
```

**Scenario C: Need to keep some changes, undo others**
```bash
# Reset specific files
git checkout <commit-hash> -- path/to/file.ts

# Or use interactive reset
git reset -p HEAD~1
```

**Scenario D: Already pushed to remote**
```bash
# DON'T force push. Instead:
git revert <commit-hash>
# This creates a new commit that undoes the changes (safe for shared repos)
```

### Step 3: Verify the Rewind

```bash
# Check the project still works
npm test -- --passWithNoTests 2>&1 | tail -5
# Or
npm run build 2>&1 | tail -5
```

## Integration with Other Skills

- **think-tool** — Use Think Tool before deciding whether to checkpoint
- **subagent-driven-development** — Each subagent should checkpoint before starting its task
- **requesting-code-review** — Auto-fix loop (Step 7) should checkpoint before attempting fixes
- **spec-driven-development** — Checkpoint before Phase 4 (Implement)

## Best Practices

1. **Checkpoint early, checkpoint often** — Better to have too many than too few
2. **Use descriptive messages** — "before refactor" not "save"
3. **Don't rely on the undo buffer** — Editor undo only works within the same session
4. **Clean up old checkpoints** — After a successful task, squash or drop checkpoint commits
5. **Combine with Think Tool** — Think first, then checkpoint, then act

## Common Mistakes

- **Not checkpointing before destructive operations** — "I'll just be careful" is not a strategy
- **Checkpointing after starting changes** — The checkpoint must be BEFORE, not during
- **Forgetting to clean up** — Old checkpoint files and commits accumulate
- **Skipping verification** — Always verify after rewind to make sure it worked

## Quick Reference

| Action | Command | When |
|--------|---------|------|
| Git checkpoint | `git add -A && git commit -m "[checkpoint] ..."` | Before changes |
| Stash checkpoint | `git stash push -m "checkpoint: ..."` | Before experiments |
| File backup | `cp file file.checkpoint` | No git / single file |
| Rewind (last commit) | `git reset --hard HEAD~1` | Undo all changes |
| Rewind (specific) | `git reset --hard <hash>` | Undo to specific point |
| Selective undo | `git checkout <hash> -- <file>` | Undo specific file |
| Safe undo (pushed) | `git revert <hash>` | Don't force push |
| Clean checkpoint commit | `git rebase -i HEAD~N` | Squash during cleanup |
