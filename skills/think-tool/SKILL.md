---
name: think-tool
description: Use when facing a complex decision, multiple possible approaches, or before making irreversible changes. Use when the best course of action is not obvious and requires reasoning before acting. Use before running destructive operations, before large refactors, or when you catch yourself rushing.
version: 1.0.0
author: Hermes Agent (adapted from Anthropic Claude Code Think Tool)
license: MIT
metadata:
  hermes:
    tags: [thinking, decision-making, reasoning, safety, planning]
    related_skills: [spec-driven-development, systematic-debugging, security-hardening-checklist]
  triggers:
    - decision
    - pros cons
    - trade-off
    - compare
    - should i
    - weigh up
    - what if

---

# Think Tool

## Overview

Before making complex or irreversible decisions, **stop and think**. The Think Tool is a structured reasoning step that happens *before* you act — not after. It's the difference between guessing and understanding.

**Core principle:** If you're not sure, think first. If you're sure, think again.

## When to Use

Use Think Tool whenever:

- **Multiple approaches exist** — "I could do X or Y" → Stop, think, decide
- **Irreversible changes** — Deleting files, modifying database, pushing to main branch
- **Complex multi-step operations** — More than 3 tool calls in sequence
- **Error recovery** — Something failed and you're about to try a fix
- **Before using potentially destructive tools** — `rm -rf`, `git reset --hard`, `DROP TABLE`
- **You catch yourself rushing** — "Just try this and see" is a red flag
- **Ambiguous requirements** — Not sure what the user actually wants

**Do NOT use for:** Simple, obvious operations (single file edit, reading a file, running tests)

## How to Think

When you call Think Tool, work through these steps in order:

### Step 1: State the Situation

In one sentence, what's happening?

> "I need to refactor the ChantingHall feature from 4 files to 2 files."

### Step 2: List the Options

What are the possible approaches?

> Option A: Merge Manager + UI into one file, keep Types separate
> Option B: Merge everything into one file
> Option C: Keep current 4-file structure, just add new features

### Step 3: Evaluate Each Option

For each option, answer:
- **Pros** — What's good about this?
- **Cons** — What's the risk?
- **Effort** — How much work?
- **Alignment** — Does it match the project's existing patterns?

### Step 4: Make a Decision

State clearly what you're going to do and why. Then proceed.

> "I'll go with Option A because it reduces complexity while keeping type definitions clean and reusable."

## Output Format

When using Think Tool, output your reasoning in this format:

```
🧠 Think Tool
─────────────
Situation: [one sentence]

Options:
1. [Option A] — [brief description]
   → Pros: [...]
   → Cons: [...]
   → Effort: [small/medium/large]

2. [Option B] — [brief description]
   → Pros: [...]
   → Cons: [...]
   → Effort: [small/medium/large]

Decision: [Option X]
Reason: [why this one wins]
```

## Integration with Other Skills

- **systematic-debugging** — Use Think Tool before attempting any fix (Phase 3 hypothesis formation)
- **spec-driven-development** — Use Think Tool during Phase 1 (Specify) when requirements are ambiguous
- **security-hardening-checklist** — Use Think Tool before making security-relevant decisions
- **requesting-code-review** — Use Think Tool before dispatching the reviewer (check your own work first)

## Examples

### Example 1: Choosing a refactor approach

```
🧠 Think Tool
─────────────
Situation: Need to refactor data-manager.js to support both localStorage and wx.setStorage

Options:
1. Adapter pattern — Create a StorageAdapter interface with two implementations
   → Pros: Clean separation, easy to add new storage backends
   → Cons: More files, may be over-engineering for 2 backends
   → Effort: Medium

2. if/else in existing code — Add platform detection and branch
   → Pros: Quick, minimal files changed
   → Cons: Messy, hard to test, violates SRP
   → Effort: Small

3. Abstract base class — Create StorageProvider base, LocalProvider + WxProvider
   → Pros: Clean, follows existing class patterns in the project
   → Cons: More boilerplate than adapter
   → Effort: Medium

Decision: Option 1 (Adapter pattern)
Reason: Despite being slightly more code, it keeps the codebase clean and makes future storage backends trivial to add. Option 2 is a debt we'd pay later.
```

### Example 2: Debugging a gray screen

```
🧠 Think Tool
─────────────
Situation: Cocos Creator scene shows gray screen, no error in console

Options:
1. Check Canvas node — Most common cause: Canvas has no children or camera issue
   → Pros: Fastest check, high probability
   → Cons: None

2. Check scene JSON integrity — corrupted __id__ references
   → Pros: Catches structural issues
   → Cons: Slower, must parse JSON

3. Check component bindings — script reference broken
   → Pros: Catches bindings issues
   → Cons: Need to check each component

Decision: Option 1 first, then 3, then 2
Reason: Follow probability order — Canvas/camera is the most common cause and fastest to verify.
```

### Example 3: Before destructive operation

```
🧠 Think Tool
─────────────
Situation: User asked me to "clean up old files" — which files?

Options:
1. Ask user to specify exact files — safest
   → Pros: No risk of deleting wrong files
   → Cons: User has to come back

2. List files with last-modified dates, let user confirm
   → Pros: User sees what they're approving
   → Cons: Slower

3. Guess and delete — dangerous
   → Pros: Fast
   → Cons: High risk of deleting something important

Decision: Option 2
Reason: Balances speed with safety. User sees the list, I explain what's safe to delete.
```

## Pitfalls

- **Over-thinking** — Don't use Think Tool for obvious decisions. If the answer is clear, just do it.
- **Analysis paralysis** — Set a mental timer: 30 seconds for small decisions, 2 minutes for big ones.
- **Confirmation bias** — Don't use Think Tool to justify what you already decided. Be genuinely open to the other options.
- **Skipping the "why"** — The decision without the reasoning is useless. Always state why you chose one option.
- **Not updating the plan** — After thinking, if your plan changes, update the user or the task list.
