---
name: context-aware-task-decomposition
description: Use when the context window is getting full and tasks need breaking down.
version: 2.0.0
author: Hermes Agent
tags: [context, decomposition, task-management, efficiency, subagent]
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
  triggers:
    - complex task
    - break down
    - decompose
    - task break
    - too big
    - split

---

# Context-Aware Task Decomposition

Self-regulate task size based on context window capacity. When generating multi-step work, estimate if it fits in the remaining context and decompose accordingly.

## Decision Flow

```
Is the task > 10 steps or likely > 2000 lines?
  ├─ Yes: Decompose into sub-tasks, dispatch via delegate_task()
  │       Each sub-task gets its own full context window
  └─ No: Execute directly
```

## When to Decompose

- Complex code generation (multi-file)
- Long research with many sources
- Refactoring across multiple modules
- Any task with > 5 independent sub-steps

## Decomposition Template

```markdown
## Task: [name]
### Sub-task 1: [specific deliverable]
### Sub-task 2: [specific deliverable]
### Sub-task 3: [specific deliverable]
### Merge & Verify
```

Each sub-task becomes a `delegate_task()` call with its own context.
