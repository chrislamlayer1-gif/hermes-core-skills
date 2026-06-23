---
name: skill-slimming-strategy
description: Use when a skill SKILL.md is over 2000 words and needs trimming to the Superpowers standard of under 500 words.
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
---

# Skill Slimming Strategy

## When to Use

When a SKILL.md file exceeds 2000 words and needs to be made more token-efficient per Superpowers standards.

## Classification First

Before slimming, classify the skill into one of these types. Each gets a different treatment:

### Type A: Auto-generated API Reference Doc
**Signs:** Language like "Created On: Jun 06, 2025 | Last Updated On:..." or "This skill auto-generated from official documentation"
**Action:** **Replace entirely.** Keep only the frontmatter + a 200-word summary with links to official docs. The original content is stale anyway — official docs are more current.

**Example:**
```yaml
# Before: 22,733 words of copied PyTorch API docs
# After: 219 words — frontmatter + 3 bullet core concepts + 3 common tasks + links
```

### Type B: Hand-Authored Pipeline / Flow Doc
**Signs:** Has step-by-step phases, checklists, decision trees. Written by a human for a specific project.
**Action:** **Extract details to reference files.** Keep the decision tree / flow diagram + one-sentence-per-phase in SKILL.md. Move detailed checklists, commands, and troubleshooting to `references/` files.

**Example:**
```yaml
# Before: 14,058 words — full paper writing pipeline with all 7 phases detailed
# After: 429 words — flow diagram + phase summary table + links to reference files
```

### Type C: External Package / Vendored Skill
**Signs:** Has `homepage:` or `repository:` pointing to an external GitHub project. Contains vendored Python scripts.
**Action:** **Don't touch.** These are maintained by external authors. The scripts are the real content, not the SKILL.md prose.

**Example:** `last30days` — 19,231 words of scripts + instructions from mvanhorn.

### Type D: Project-Specific Debug Flow
**Signs:** Contains real-world debugging steps learned through painful experience. Lots of "quick fix" ordering.
**Action:** **Abstract to decision tree.** Keep the symptom diagnosis (Case A vs Case B) + quick-fix order in SKILL.md. Move deep-dive explanations and repair procedures to `references/`.

**Example:**
```yaml
# Before: 8,022 words — full Cocos gray screen debug flow with 5 case analyses
# After: 209 words — symptom check + quick-fix order + reference links
```

## The Process

### Step 1: Read first 30 lines + last 10 lines
Understand the structure: is it a flow, a reference, or an external package?

### Step 2: Decide the action
Use the classification above.

### Step 3: Slim
- Type A: Replace entire body with summary
- Type B: Copy detailed sections to `references/` files, keep outline only
- Type C: Skip (add a note "External package, see source for details")
- Type D: Abstract to decision tree

### Step 4: Verify word count
```bash
wc -w skills/path/SKILL.md  # Target: <500 words
```

## Pitfalls

1. **External packages (Type C) look like Type A or B** — always check for `homepage:` or `repository:` in frontmatter before slimming.
2. **Don't delete reference content entirely** — save it to `references/` files so it's still accessible via the Read tool when needed.
3. **Don't slim skills the user actively uses** — `claude-code`, `hermes-agent`, and project-specific debugs are frequently loaded. Slimming them requires care.
4. **Batch approach is better** — use a Python script for multiple skills (see `batch-skill-description-standardization` for the batch approach pattern).
