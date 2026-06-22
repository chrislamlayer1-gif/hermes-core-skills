---
name: batch-skill-description-standardization
description: Use when needing to standardize descriptions across many skill files at once — change format, fix wording, or enforce a convention like 'Use when...' prefix.
version: 1.0.0
author: Hermes Agent (experiential learning from superpowers CSO analysis)
---

# Batch Skill Description Standardization

## When to Use This Skill

When you need to update descriptions across 20+ SKILL.md files with a consistent pattern (e.g. converting all to "Use when..." format).

## The Problem

An agent skills directory can have 160+ SKILL.md files with inconsistent descriptions. Some describe workflow instead of triggering conditions. Some start with verbs. Some are 80+ words long. Patching them one-by-one uses 100+ tool calls and is prone to error.

## The Superpowers Insight (CSO)

From superpowers' "Claude Search Optimization" analysis:
- **If description summarizes workflow, the agent follows the description and SKIPS the skill body.**
- Description should ONLY describe WHEN to use, NEVER WHAT the skill does.
- Format: "Use when [precise triggering condition]."

## The Workflow

### Step 1: Scan and classify

```python
from hermes_tools import search_files, read_file
import re

result = search_files(pattern='SKILL.md', target='files', path='/path/to/skills', limit=200)
files = result['files']
```

Check each SKILL.md's description line for three problems:
1. **Doesn't start with "Use when"** — most common
2. **Describes workflow** (has words like "步驟", "流程", "phase", "checklist", "step 1")
3. **Too long** (over 80 words)

### Step 2: Handle the two YAML description formats

There are TWO formats for description in SKILL.md frontmatter:

**Format A — Single line:**
```yaml
description: Some text here.
```

**Format B — Folded multiline (uses `>` or `>-`):**
```yaml
description: >
  Long text that spans
  multiple lines in the file
  but becomes one line in YAML.
```

**CRITICAL:** For Format B, you CANNOT just replace the description line. You must replace the ENTIRE block from `description:` to the next YAML key.

### Step 3: Write the batch script

Build a Python dict mapping skill identifiers to new descriptions. Use a script with `re.sub()` to find and replace:

```python
pattern = r'(description:\s*)(.+?)(?=\n(?:---|name:|version:|author:|title:|tags:|category:|metadata:|last_|created:|related|triggers|license:|  )|\Z)'
replacement = f'description: {new_desc}'
new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
```

This regex handles both single-line and folded multiline descriptions by matching from `description:` until the next YAML key or section boundary.

### Step 4: Verify

After running the batch script, re-scan all SKILL.md files to confirm 100% compliance:

```bash
for f in $(find skills -name SKILL.md); do
  head -15 "$f" | grep -q "description: Use when" && echo "OK: $f" || echo "FAIL: $f"
done
```

## Pitfalls

1. **YAML folded multiline** (`>` or `>-` on the description line) is the most common trap. The regex in Step 3 handles it, but test on a few files first.
   - **`>` vs `>-`**: `>-` strips the trailing newline, which can cause the next YAML key to be concatenated with the description text. If your regex doesn't account for this, you'll get malformed YAML.
   - **Best defense**: Use `re.DOTALL` and match from `description:` to the next known YAML key pattern (`^[a-z]|^---`), NOT just to the next newline.
2. **Some skills have non-standard frontmatter** (e.g., custom keys like `title:`, `category:`, `triggers:`, `related_skills:`, `triggers:`, `argument-hint:`, `allowed-tools:`, `user-invocable:`, `homepage:`, `repository:`, `platforms:`). The regex boundary must account for ALL possible next-key patterns — don't assume a fixed set.
3. **CJK descriptions**: Chinese descriptions work fine with "Use when" — no need to rewrite in Chinese. The key is consistency.
4. **Don't use `patch()` tool for batch operations over 20+ files** — it uses 1 tool call per file, which burns through your tool call budget fast. Use a Python script with direct file I/O instead.
5. **External package skills**: Some skills are bundled from external sources (e.g. `last30days` from mvanhorn, auto-generated API docs like `pytorch-fsdp`). These contain 10K+ words of generated content or vendored scripts. Don't try to slim them — they're not hand-authored. Just flag them as external in the skill body.
6. **Backup first**: Before running a destructive batch update, make a backup tarball of the skills dir:
   ```bash
   tar czf /tmp/skills-backup-$(date +%Y%m%d).tar.gz /path/to/skills
   ```
   This lets you restore if the regex mangles files.

## Step 4: Token Slimming (optional second phase)

After standardizing descriptions, you may want to slim oversized skills. Decision framework:

| Skill Type | What to Do |
|-----------|-----------|
| **Auto-generated API doc** (10K+ words, e.g. pytorch-fsdp) | Rewrite SKILL.md as a 200-word quick start guide with links to official docs. Save original as `references/` file. |
| **Step-by-step procedure** (2K-8K words, e.g. cocos-gray-screen-debug-flow) | Keep core decision tree + flowchart in SKILL.md. Each detailed branch becomes a `references/*.md` file. |
| **External vendored package** (e.g. last30days with its own scripts/) | Don't touch. SKILL.md is the package documentation — it's long by design. Just note it's external. |
| **Task pipeline** (e.g. research-paper-writing) | Keep the high-level flow diagram + phase table in SKILL.md. Each phase's detailed steps go to `references/phase-details.md`. |
| **Internal how-to** (< 2000 words) | No action needed unless description needs fixing. |

### Token Slimming Pitfalls

- **Don't delete content, relocate it**: Move detailed instructions to `references/` files in the same skill directory. The skill still works — I'll `read_file` the reference when needed.
- **Keep the decision tree**: The most valuable part of a debug skill is "which branch to go down", not every detail of every branch. SKILL.md should help me decide WHAT to do; reference files tell me HOW.
- **Watch for cross-references**: Some skills reference internal sections by anchor. If you split, those anchors break. Replace with file references: `[details](references/foo.md)`.

## Verification

After batch update, confirm ALL files are compliant. There's a trap: `head -15 | grep "description: Use when"` will FAIL on YAML folded multiline because the description value is literally `>` or `>-`, not the actual description text.

**Correct verification method:**

```python
import subprocess, re

for f in files:
    r = subprocess.run(['head', '-15', f], capture_output=True, text=True, timeout=5)
    for ln in r.stdout.split('\n'):
        if ln.strip().startswith('description:'):
            desc = ln.split(':', 1)[1].strip()
            if desc in ['>', '>-', '|', '|-']:
                # Folded multiline — check the FULL content
                r2 = subprocess.run(['sed', '-n', '/description:/,/^[a-z]/p', f], capture_output=True, text=True)
                if 'Use when' in r2.stdout or '使用時機' in r2.stdout:
                    pass  # good
                else:
                    print(f"FAIL: {f}")
            elif desc.lower().startswith('use when') or desc.lower().startswith('使用時機'):
                pass  # good
            else:
                print(f"FAIL: {f}")
            break
```

Also confirm:
- 100% of descriptions start with "Use when" or "使用時機"
- No description contains workflow summary
- Each description fits in under 120 characters if possible
