---
name: token-efficiency
description: Use when context is getting large, when working on long sessions, or when you notice token consumption is high. Use before dispatching subagents, before reading large files, and during context compaction.
version: 1.0.0
author: Hermes Agent (adapted from Anthropic Prompt Caching + Hermes Context Compression)
license: MIT
metadata:
  hermes:
    tags: [token, efficiency, context, cost, optimization, compaction]
    related_skills: [context-inheritance-subagent, writing-plans, subagent-driven-development]
  triggers:
    - token cost
    - context full
    - too long
    - compression
    - token budget

---

# Token Efficiency

## Overview

Reduce token consumption by being intentional about what goes into context. Every token costs money and fills the context window. Smart context management can reduce costs by 30-50% without sacrificing quality.

**Core principle:** Only put in context what's needed for the current task. Everything else is noise.

## When to Use

- Context is approaching the window limit
- You notice tool outputs are getting large
- Before dispatching subagents (don't send all context)
- When working on a long-running session (many turns)
- When the user mentions cost concerns
- Before and after context compaction

## Techniques

### 1. Deferred Reading

Don't read files until you need them:

```python
# ❌ Bad: read everything upfront
read_file("src/models/user.py")  # 200 lines
read_file("src/models/product.py")  # 300 lines
read_file("src/models/order.py")  # 250 lines
# → 750 lines in context before you even start

# ✅ Good: read only what you need now
# Start with just the file structure
search_files("*.py", target="files", path="src/models/")
# Read only the file you're about to modify
read_file("src/models/user.py")
```

### 2. Summarize Before Saving

Instead of saving raw tool output, summarize:

```python
# ❌ Bad: save raw terminal output
# 200 lines of irrelevant log messages

# ✅ Good: save only the summary
# "Build completed: 45 passed, 0 failed, 3 warnings (all pre-existing)"
```

### 3. Use delegate_task for Heavy Lifting

Heavy operations burn token in a separate context, not the main session:

```python
# ❌ Bad: do heavy search in main session
# browser_navigate → browser_snapshot → browser_scroll × 10
# → hundreds of lines of HTML in main context

# ✅ Good: delegate to subagent
delegate_task(goal="Search GitHub trending...", toolsets=['browser'])
# → only the summary enters main context
```

### 4. Progressive Disclosure for Skills

Skills should use progressive disclosure (load metadata first, full content only when needed):

```
# Skill name + 1-line description → Agent decides if relevant
# → Only then load full SKILL.md
# → Only then load reference files
```

This is already built into Hermes skills system — make sure descriptions are specific enough for accurate matching.

### 5. Avoid "Just in Case" Context

```python
# ❌ Bad: "let me read this file just in case I need it"
read_file("src/config/settings.py")
read_file("src/config/database.py")
read_file("src/config/cache.py")
# User only asked to fix a button color

# ✅ Good: read the specific UI file first
read_file("src/ui/components/Button.tsx")
# Only read config files if debugging reveals they're relevant
```

### 6. Structure Context for Subagents

When dispatching subagents, use the context-inheritance pattern (see `references/context-inheritance.md` in the subagent-driven-development skill):

```
Context Package:
- Project: 2-3 lines
- Task: what to do
- Shared State: what's done
- Files: relevant ones only
- Constraints: gotchas to avoid
```

This reduces subagent context by 60-80% compared to dumping everything.

### 7. Use Terminal Filters

When running commands, pipe through filters to reduce output:

```bash
# ❌ Bad: full output
pytest tests/ -v

# ✅ Good: only failures and summary
pytest tests/ -q --tb=short 2>&1 | tail -20
```

## Cost Estimation

Rough token costs (approximate):

| Operation | Tokens | Cost (DeepSeek) |
|-----------|--------|-----------------|
| Read a 200-line file | ~2,000 | ~$0.0003 |
| `pytest -v` full output | ~5,000 | ~$0.0007 |
| Browser snapshot (full) | ~8,000 | ~$0.0011 |
| delegate_task (typical) | ~5,000 input / ~1,000 output | ~$0.0005 |
| Context compaction | ~10,000 | ~$0.0014 |

**Rule of thumb:** If it's not directly relevant to the current action, don't put it in context.

## Context Compaction

When Hermes triggers context compaction, it's because the window is getting full. Help by:

1. **Summarizing** what was accomplished so far
2. **Dropping** old tool outputs that are no longer relevant
3. **Keeping** only the current task state and next steps
4. **Recommending** checkpoint save so nothing is lost

## Integration

- **context-inheritance-subagent** reference — context package for delegate_task
- **subagent-driven-development** — uses delegate_task for heavy work
- **writing-plans** — plans should be concise, not verbose
- **checkpoints-and-rewind** — save before compaction so nothing lost
