---
name: cross-session-execution-framework
description: Use when managing a long-term project across multiple Hermes sessions.
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
---

# 🪷 跨 Session 執行框架

## 問題

Hermes Agent 每次 Session 有 token/context 限制，跨 Session 開發有以下痛點：

| 問題 | 症狀 |
|------|------|
| Context 遺失 | 新 Session 唔記得上次做咗乜 |
| 任務偏差 | 開始做 A，做到一半改做 B，最後 A 未完成 |
| 進度遺失 | 用戶唔知做到邊一步 |
| 決定遺失 | 之前用戶確認嘅決定，新 Session 要再問一次 |

## 解決方案：檔案系統實體化

喺 project root 建立 3 個追蹤檔案：

```
project/
├── ROADMAP.md    ← 用戶睇進度
├── STATE.md      ← Agent 記錄狀態
└── boot.sh       ← 自動行，開工匯報
```

---

## 1. ROADMAP.md — 總路線圖

### 格式
```markdown
# 🪷 專案名 — 優化路線圖

> 整體執行進度。✅ = 完成，⬜ = 未開始

## 階段一：XXX
- [x] 1.1 已完成任務（簡短說明）
- [ ] 1.2 未完成任務

## 階段二：XXX
- [ ] 2.1 ...
```

### 規則
- 任務用 checkbox 格式 `- [ ]` / `- [x]`
- 分階段（P0/P1/P2 或 基建/功能/優化）
- 每個 checkbox 對應一個可獨立完成嘅 task
- 唔好放太細粒度（唔好一個 task 就係「改一行 code」）

---

## 2. STATE.md — 當前執行狀態

### 格式
```markdown
# 🪷 當前執行狀態

## 基本資訊
- **最後更新**：YYYY-MM-DD（Session N）
- **當前階段**：階段一 — ✅ 完成 / 🔄 進行中
- **當前 Task**：XXX

## 已完成
重點 list 已完成嘅 task，每個 task 下面有具體改動 summary

## 已修改／新增檔案
| 檔案 | 狀態 | 說明 |

## 下一個要做
清晰描述下一個 task 係乜

## 待確認事項
1. **問題描述** — 需要用戶決定嘅事
   - 選項 A
   - 選項 B
   
## Git 狀態
（如有）
```

### 更新規則
- **每次 Session 完結前**必須 update
- 「已修改／新增檔案」記錄 exact path，方便下個 Session 快速定位
- 「待確認事項」係最關鍵嘅 section——確保用戶決定唔會 lost

---

## 3. boot.sh — 開機腳本

### 範例
```bash
#!/bin/bash
PROJECT_DIR="/path/to/project"

echo "=== 🪷 Boot Sequence ==="

# Check ROADMAP
if [ -f "$PROJECT_DIR/ROADMAP.md" ]; then
    echo "✅ ROADMAP.md 存在"
    grep -n "\[ \]" "$PROJECT_DIR/ROADMAP.md" | head -10
fi

# Check STATE
if [ -f "$PROJECT_DIR/STATE.md" ]; then
    echo "✅ STATE.md 存在"
    grep -A 2 "當前階段\|當前 Task\|下一個\|待確認" "$PROJECT_DIR/STATE.md"
fi

# Git status
if [ -d "$PROJECT_DIR/.git" ]; then
    git -C "$PROJECT_DIR" status --short
fi
```

### 執行時機
- 每次用戶講「開工」時自動執行
- 如果 boot.sh 唔存在，要手動 read_file ROADMAP.md + STATE.md

---

## 每次 Session 標準流程

```
用戶講「開工」
  ↓
行 boot.sh（或手動檢查 ROADMAP + STATE）
  ↓
讀 STATE.md → 知道上次進度 + 未確認事項
  ↓
如果有「待確認事項」→ 先問用戶決定
  ↓
開始做當前 Task（一個 task 一個 Session）
  ↓
完成後：
  1. 更新 ROADMAP.md（check box）
  2. 更新 STATE.md（完成記錄 + 修改檔案 + 下個 task + 新待確認）
  ↓
匯報完成 + 列出待確認事項
  ↓
（Session end — 下次重複）
```

---

## 與其他技能配合

| 技能 | 配合方式 |
|------|---------|
| `buddha-heart-boot-sequence` | 擴展 boot sequence，加入 ROADMAP/STATE 讀取 |
| `story-data-migration-wechat` | 用 STATE 記錄 story migration 嘅進度同陷阱 |
| `context-aware-task-decomposition` | 每個 task 拆到一個 Session 搞得掂嘅大小 |

---

## ⚠️ 2026-05-01 實戰教訓：框架存在 ≠ 框架執行

### 發現嘅問題

喺一個長期項目中，雖然呢個 framework 完整定義咗 ROADMAP.md / STATE.md / boot.sh，但實際執行咗多個 Session 之後發現：

| 有做嘅 | 冇做嘅 |
|--------|--------|
| ✅ 每個 task 後 update ROADMAP（checkbox） | ❌ **boot.sh 從未執行過** |
| ✅ 每個 Session 後 update STATE.md | ❌ **Git repo 從未 init**（改咗幾十個 file 冇版本控制） |
| ✅ 拆細 task 做 | ❌ **subagent review / TDD 從未執行** |
| | ❌ **「待確認事項」section 從未用過** |

### 根本原因

1. **框架係「被動建議」，唔係「強制系統」** — Agent 嘅預設行為係直接做嘢，唔會先 check 機制
2. **沒有實體 boot.sh 執行** — skill 文件入面嘅 boot.sh 範例只係文字，冇真正嘅可執行腳本
3. **memory 冇強制注入** — 新 Session 時 memory 只有 project 資訊，冇提醒「開工必行 boot.sh」
4. **冇 punishment for skipping** — skip 咗流程冇任何後果，所以每次 Optimize for 直接產出

### 修復措施（已落地）

1. **建立實體 boot.sh 腳本**（非 skill 入面嘅範例文字）
2. **Git init + 強制 commit per task**
3. **改寫 boot sequence skill + HARD STOP RULES**（明確寫明「❌ 嚴禁：未行 boot.sh 就直接開始改 code」）
4. **memory 注入開工規則** — 每次新 Session 自動提醒「開工第1句行 boot.sh」

### 關鍵規則（所有跨 Session 項目必須遵守）

```
⚠️ HARD STOP — 不可違反：
1. 開工必行實體 boot.sh（唔係睇 skill 文件）
2. 完成每個 task 必 git commit
3. 完成每個 task 必 update ROADMAP + STATE
4. Git repo 必須在 project 第1個 Session 就 init
```

> **呢啲規則點解要寫兩次（呢度 + boot sequence skill）？**
> 因為呢個 framework 係通用嘅，boot sequence skill 係 project-specific。
> 任何新 project 用呢個 framework 時，頭 30 分鐘就要做好上述 4 點，
> 否則 Session 3 之後就會同上面描述嘅情況一樣 — 框架喺度但從未執行。

---
