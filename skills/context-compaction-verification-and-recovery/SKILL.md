---
name: context-compaction-verification-and-recovery
description: Use when verifying that tool commands actually executed after compaction.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [context-compaction, recovery, verification, debug]
    platform: [cursor, codex, claude-code]
domain: agent-core
subdomain: efficiency
tokens:
  scan: 150
  load: 3285
  category: detailed
---

# Context Compaction Verification & Recovery Protocol

## When to Use

Use this protocol when:
1. You've issued multiple `patch`, `write_file`, or `create_file` calls in a session
2. Context compaction has occurred (handoff summary mentions "completed" work)
3. User reports "偏翼唔到出嚟" (page doesn't render / doesn't work)
4. You suspect some tool calls were "spoken but not executed" — written in responses but not actually made

## Core Insight

**Tool calls that exist only in your reply text but weren't actually invoked will NOT have modified any files.** This is the most common failure mode during complex multi-step sessions across context compactions.

Pattern: AI describes what it *will* do in markdown text blocks, the user says "繼續", and in the next turn the AI treats that description as already done without having made the actual tool calls.

### Warning Signs of Compaction-Induced Drift

These patterns strongly suggest patches never landed:
1. **Deferred tool calls** — you say "first I'll X, then Y" in prose, then move on without actually calling the tools
2. **"As mentioned above" syndrome** — you reference code that was typed in your response but never written to disk
3. **Excessive prose descriptions of code** — if you're describing implementation in detail rather than *doing* it, check if tools were actually called
4. **User says it doesn't render** after you think you've finished — this is the ultimate signal

### Prevention: The "Did the tool fire?" Check

Before any "繼續" transition, mentally scan: **for every file I claim to have modified, did I actually see a `patch()` or `write_file()` success response in my tool output?** If you only remember typing it in prose, it didn't happen.

## Step 1: Audit — File Existence Check

Before any repairs, run a comprehensive audit:

```bash
# Find all NEW files that should exist
# Check each one with ls or search_files
```

Key files to verify:
- New utility files (`utils/*.js`)
- New page directories (`pages/*/`)
- New component files

## Step 2: Audit — Patch Verification by Keyword Scan

For each file that was supposed to be patched, scan for **distinctive keywords** that would only exist after the patch:

```python
# For each patched file, check that NEW method names, variable names, 
# or import paths exist in the file content
checks = {
    "someFile.js": ["newFunctionName", "newImport", "newVariable"]
}
for fpath, keywords in checks.items():
    content = open(fpath).read()
    for kw in keywords:
        if kw not in content:
            print(f"MISSING: {fpath} — no '{kw}'")
```

**Critical clue:** If the file exists but has a smaller size than expected, or if multiple keywords are missing, the patches likely never executed.

## Step 3: Analyze Root Cause

Common causes:
- **Context compaction** — handoff summary describes work as "done" but tool calls were in a different context and never executed
- **Rate limiting / timeout** — some tool calls in a batch silently failed
- **Wrong file path** — patch was applied to a non-existent path
- **Middle-of-response tool call** — tool call appeared mid-response, earlier compaction truncated it
- **⚠️ 流程規則消失（NEW — 2026-05-01 發現）** — Context compaction 唔只導致 code 冇落地，仲會令 **流程規則完全消失**。最常見：HARD STOP RULES、REVIEW.md 優化授權、Task Size Pre-Judgment Protocol。原因係呢啲規則寫咗落檔案但冇用 memory tool save。Context compaction 後 memory 入面冇呢啲規則，Agent 會當 normal mode 開工，直接 skip boot sequence。

### 流程規則 Recovery（NEW）

當發現自己 skip 咗 boot sequence / HARD STOP / 其他流程規則：

1. **唔好繼續做 code work** — 先修復流程
2. 用 memory tool 重新 save 所有流程規則
3. 行 boot.sh 確認狀態
4. 完成後先開始新 work

### 點樣預防流程規則消失

**永遠用 memory tool 而非寫檔案嚟 save 流程規則。**
- ❌ `database/hermes_memory.json` patch — context compaction 後唔會 inject
- ✅ `memory(action='add', target='memory', ...)` — context compaction 後自動 inject

檢查清單（每次 context compaction handoff 後問自己）：
- [ ] 我記唔記得 boot.sh 係開工第1句？
- [ ] 我記唔記得完成 task 要 update ROADMAP + STATE + git commit？
- [ ] 我記唔記得 REVIEW.md 優化授權？
- [ ] 我記唔記得 task size pre-judgment protocol？
- [ ] 以上規則係咪來自 memory tool？（唔係檔案）

## Step 4: Recovery Strategy

### Approach A — Independent Recovery (preferred)
1. Write a comprehensive plan (`.hermes/plans/YYYY-MM-DD_*recovery*.md`)
2. Include: what exists ✅, what's missing ❌, exact patch operations needed
3. Share plan with user for approval before executing
4. Execute **in strict dependency order**: new files first, then config changes (app.json), then patches to existing files
5. **After every batch of 3-4 patches, do a focused syntax check** — don't wait until the end to discover a mistake

### Approach A.1 — Progressive Recovery (for 10+ missing items)
When the recovery plan has 10+ operations:
1. Split into **phases** (e.g., Phase 1: new files, Phase 2: patches, Phase 3: syntax check)
2. Within each phase, group by **dependency** (a file that other files import from must be created first)
3. After each phase, do a focused verification: "Phase 1: 5/5 files created" before moving on
4. Keep the todo list granular — one item per file or per logical group, not one "do everything" item

### Approach A.1 — Progressive Recovery (new, for 10+ missing items)
When the recovery plan has 10+ operations:
1. Split into **phases** (e.g., Phase 1: new files, Phase 2: patches, Phase 3: syntax check)
2. Within each phase, group by **dependency** (a file that other files import from must be created first)
3. After each phase, do a focused verification: "Phase 1: 5/5 files created" before moving on
4. Keep the todo list granular — one item per file or per logical group, not one "do everything" item

### Approach B — Clean Re-implementation (when patches are too numerous)
1. Identify which files need full rewrites vs targeted patches
2. For files with 80%+ changes: rewrite entirely
3. For files with <30% changes: patch the missing parts

## Step 5: Verification After Recovery

After all patches are applied:

```bash
# 1. Syntax check all JS files
node -e "require('./utils/new-file')" 2>&1 | head -5

# 2. Check all require() paths resolve
# 3. Check all WXML has matching WXSS classes
# 4. Check app.json has all page paths
```

## Step 6: DevTools Testing

For WeChat Mini Program specifically:
1. Clear DevTools cache: `~/Library/Application Support/微信开发者工具/<hash>/WeappCache/`
2. Close DevTools completely
3. Reopen via `open -a "wechatwebdevtools" /path/to/project`
4. Cmd+R compile
5. Route to each new/modified page

## Common Pitfalls

- **"routeTo appLaunch timeout"** is often a false positive cold-start latency, not a real error — clear WeappCache and retry before debugging
- **Missing `app.json` page entry** won't cause launch timeout, but will crash when navigating to that page
- **WXML `wx:if` with undefined data field** renders nothing (no crash, but empty screen)
- **Mutual require cycles** between utils/ files cause silent undefined exports
- **The "false positive" trap** — during audit, some keywords might already exist from earlier successful patches (recitation.js counter styles were already present even though I thought they were missing). Always verify by reading the actual file, not just keyword grepping.
- **WXSS `display: grid` with `1fr` units** triggers `Cannot read properties of undefined (reading 'MaxCodeSize')` in WeChat DevTools — use flexbox with `calc(33.33% - gap)` for 3-column layouts
- **WXSS `filter: drop-shadow()`** also triggers the same `MaxCodeSize` compile error — replace with `box-shadow` instead
- **`backdrop-filter` in WXSS** is another known DevTools WXSS compiler trigger — works in most files but can cause cascading compile failures when combined with other heavy CSS features

### Audit Report Template

Use this after any "it doesn't work" report:

```
## Pre-Recovery Audit Results

### New Files Status
- [ ] utils/foo.js — EXISTS / MISSING
- [ ] pages/bar/bar.js — EXISTS / MISSING

### Patch Status
- [ ] file1.js — all 8 keywords present / N missing
- [ ] file2.js — all 5 keywords present / N missing

### Config Status
- [ ] app.json — all page paths registered
- [ ] project.config.json — valid

### DevTools Root Cause
- [ ] routeTo appLaunch timeout (likely cold-start latency)
- [ ] require() path mismatch at: _______
- [ ] Missing page config at: _______
```

### Final Recovery Verification

After applying all recovery patches, run this comprehensive check:

1. **Syntax check all modified/new JS files** — `node -c filename.js`
2. **Check all app.json pages exist** — verify js/wxml/wxss triple exists for each
3. **Keyword scan** — re-run the audit against all expected keywords
4. **DevTools cache clear** — remove WeappCache/ and WeappLocalData/ directories
5. **Reopen DevTools** — `open -a "wechatwebdevtools" /path/to/project`

### WXSS Compile Error Debugging

If DevTools shows "编译 .wxss 文件错误，错误信息如上" with `Cannot read properties of undefined (reading 'MaxCodeSize')`:

1. **Most likely cause: `display: grid` with `1fr` units** — replace with flexbox layout
2. Check for `backdrop-filter` usage in recently modified WXSS files
3. Check for unbalanced braces in WXSS files (`{` vs `}` counts)
4. **Check WXML for `=>` arrow functions and `?.` optional chaining** — these WXML errors sometimes manifest as WXSS compile errors in DevTools! Always check WXML first before debugging WXSS.
5. After fixing, **always clear WeappCache/** before recompiling — stale cache compounds WXSS errors
6. Keep WXSS files under ~15KB per file to avoid exceeding the compiler's code size limit

## When to Write a Plan vs Just Fix

| Scenario | Action |
|----------|--------|
| 1-3 missing patches | Just fix, no plan needed |
| 3-8 missing patches | Quick audit + execute |
| 8+ missing patches or new files | Write plan first, get user OK |
| User reported "唔work" | Always audit first, then plan |
