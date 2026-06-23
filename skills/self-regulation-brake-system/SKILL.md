---
name: self-regulation-brake-system
description: Brake system that auto-stops the agent after N repeated failures, prevents token burning on loops.
tags: [self-regulation, brake, efficiency, feedback, timeout]
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
  triggers:
    - brake
    - fail limit
    - stop retry
    - regulation

domain: agent-core
subdomain: safety
tokens:
  scan: 210
  load: 2340
  category: detailed
---

# Self-Regulation Brake System

## Problem

Agent can burn thousands of tokens repeating the same failed action (GitHub login, OAuth, browser loops). The user only discovers this when they see the bill.

## Solution: brake.sh

A lightweight shell script at `~/.hermes/scripts/brake.sh` that:
- Tracks failure count per action name across sessions
- Exits with code 2 when limit (default: 3) is exceeded
- Resets on success

## Integration Points

### 0. System-Level Injection（最強保證 — config.yaml prefill_messages_file）

Brake rules 已寫入 system instructions file，透過 config.yaml 嘅 `prefill_messages_file` 注入：
- System instructions file: `~/.hermes/system-instructions/self-regulation.md`
- 呢個 file 每次新 session 開波會自動 inject 做 system instruction
- 因為係 config-level injection，Agent 無法跳過或忽略

### 1. session-start.sh hook

Already updated. Every new session shows brake status:
```
=== 🧠 SELF-REGULATION CONTEXT ===
⚠️  BRAKE SYSTEM IS ACTIVE
```

### 2. Agent memory

Injected as self-regulation rules. Ensures the agent knows about brakes even after context compaction.

### 3. Manual usage (agent self-enforces)

Whenever the agent encounters a failing loop:

```bash
# Before retrying, check if brake is triggered
bash ~/.hermes/scripts/brake.sh check "github-login-by-browser"
# exit 0 = safe, count = N
# exit 2 = STOP, ask user

# After a failure
bash ~/.hermes/scripts/brake.sh record "github-login-by-browser"

# After success
bash ~/.hermes/scripts/brake.sh reset "github-login-by-browser"
```

## Brake Trigger Rules（hard-coded in memory，亦注入 system instructions）

| Condition | Action |
|-----------|--------|
| Same action fails ≥3 times | STOP → clarify user（用 clarify tool，唔好自己估） |
| 5 min of no progress | STOP → clarify user |
| Third-party auth (GitHub/Google/OAuth) | First failure → STOP, don't retry |
| Complex multi-step auth | Delegate to subagent first |
| **卡住咗唔出聲** | 違反 HARD RULE 2 — 失敗咗必須即刻報告，唔可以靜雞雞轉彎 |

## 🚩 CUA-Specific Auto-Stop Rules（2026-06-17 確立）

### Terminal First 原則

做任何動作之前，先問「terminal 做唔做到」：
- **terminal 做到嘅**（開app、build、git、curl、cp/mv、改 code、compile）→ 用 terminal
- **terminal 做唔到嘅**（㩒GUI掣、睇畫面效果、OAuth login、系統對話框）→ 先用 CUA

### CUA 紅旗自動停機制

CUA 操作見到以下任何一個紅旗，**即停 CUA，轉用 terminal/其他方法**：

| 紅旗 | 原因 |
|------|------|
| 同一 CUA 操作失敗 **2 次** | Pixel coord 唔準/AX tree 太複雜→唔會越試越準 |
| Accessibility tree > **500 elements** | DevTools/Chrome/Electron 內部→AX tree 大得滯，無用 |
| Vision 座標 **明顯唔合理** | 如話座標喺畫面範圍之外 |
| 畫面係 **Canvas/WebGL 自繪** | CUA 睇唔到入面啲掣 |

### CUA 適用地區

CUA 只應該用喺以下場景：
- ✅ 睇畫面效果（vision screenshot）—— 純觀察，唔操作
- ✅ 㩒系統對話框（權限請求、save dialog）
- ✅ OAuth login（browser 登入流程）
- ✅ Drag & drop

### 實戰案例：DevTools 操作反面教材

```
❌ 失敗做法：
  用 CUA pixel click 操作 DevTools 內部 UI（頁面路徑selector）
  → AX tree 971 elements，pixel coord 錯晒，失敗 5+ 次
  → 浪費大量 token，0 成果

✅ 正確做法：
  改 code → terminal `bash boot.sh pre-commit` compile
  → 出錯直接改 code，唔使郁 DevTools 掣
```

### 點解要咁嚴？

因為 CUA 嘅 vision 同 AX tree 喺複雜 UI（DevTools、Electron app）入面**非常唔可靠**，而且每失敗一次就燒大量 token（screenshot + vision analysis + 再去試）。Terminal command 反而係 deterministic，成功失敗都 cheap 好多倍。

## Architecture

```
Session Start
  ├─ session-start.sh
  │    └─ brake.sh status → context injection
  │
  Agent working
  ├─ action fails → brake.sh record
  ├─ before retry → brake.sh check
  │    ├─ count < 3 → retry
  │    └─ count ≥ 3 → BRAKE! → clarify user
  │
  Action succeeds → brake.sh reset
```

## 🧠 Why This Works（防止 Agent 忽視嘅設計原理）

呢個 system 嘅關鍵唔係 script 本身，而係 **注入層級**：

1. **System-level（config.yaml prefill_messages_file）** → 每次 session 開波 server 端自動注入，Agent 無法跳過
2. **Session-level（session-start.sh hook）** → 每次開工自動執行，輸出 HARD RULES 硬提示
3. **Agent-level（memory + skills）** → 長期記憶有記錄，context compaction 後仍然存在

**點解 Agent 理論上可以「忽略」system instruction？**
- 冇錯，某啲 LLM provider 嘅 system message 可以被 user message override
- 但 brake.sh 係一個**實際存在嘅 script**，唔係純文字指令
- agent 如果 brake.sh 卡咗 3 次但繼續做，係**違反咗自己嘅 tool call 結果**（exit code 2）
- 呢個係「validate by execution」嘅設計 — 規則唔係用講嘅，而係用 tool 嘅行為嚟強制執行

## File Locations

- Script: `~/.hermes/scripts/brake.sh`
- State dir: `~/.hermes/state/brake/` (persists across sessions)
- Hook: `~/.hermes/hooks/session-start.sh`
