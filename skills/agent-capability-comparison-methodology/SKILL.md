---
name: agent-capability-comparison-methodology
metadata:
  hermes:
    platform: [cursor, codex, claude-code]

---

# AI Agent 能力比較方法論

## 適用場景

用戶想比較兩個 AI agent/tool 嘅能力差異，例如「Hermes Agent vs OpenAI Codex」、「CUA vs Codex Desktop Control」。

## 核心原則

**唔靠「聽講」，用證據說話。** 三層驗證：

1. **官方文件** — GitHub README、docs 目錄、官方網站
2. **原始碼證據** — 直接睇 source code 確認功能存在與否
3. **實測驗證** — 真係裝黎用、試下得唔得

## 比較流程

### 第一層：快速掃描（30 分鐘）

1. 睇 GitHub README 了解定位
2. 睇 docs/ 目錄了解功能列表
3. 記錄 GitHub stats（stars、forks、commits、issues、branches、tags）

### 第二層：深入驗證（1-2 小時）

逐個功能查原始碼：

| 功能類別 | 要 check 嘅嘢 |
|---------|-------------|
| 記憶系統 | source code 有冇 memory/memories 目錄？點樣跨 session？ |
| Cron/排程 | 有冇 scheduler/cron crate/module？ |
| 多平台支援 | 有冇 telegram/discord/slack module？ |
| 模型自由度 | model provider 係硬編碼定可配置？ |
| Computer Use | 有冇 screenshot/click/type_text 工具？ |
| MCP 整合 | 有冇 mcp server/client 實作？ |
| Skills | 係 static 定 dynamic learning？ |
| Desktop App | 係咪真係有 Electron/Tauri app？ |

**檢查方法：**
- `ls -d */` 睇目錄結構
- `grep -r "keyword" --include="*.py" --include="*.rs" --include="*.ts"` 搜尋關鍵字
- 睇 GitHub Issues 用 label 過濾（如 `computer-use`、`memory`、`cron`）
- 睇 Discussions 嘅 feature requests

### 第三層：實測驗證（按需要）

- 真係裝黎用
- 試核心功能
- 紀錄成功/失敗嘅 case

### 關鍵：Always distinguish CLI vs Desktop App features
- Codex Desktop has Computer Use + Automations; Codex CLI does NOT
- Hermes CLI has cron/scheduling; no official Desktop App yet
- Check which variant each feature belongs to before comparing

### 關鍵：Memory systems may be read-only
- Codex has a two-phase memory pipeline (rollout extraction + global consolidation)
- But the agent is explicitly instructed: "Never update memories. You can only read them."
- Hermes has bidirectional memory — agent can both read AND write
- This is a meaningful functional difference

### 關鍵：「Desktop App」嘅定義要查原始碼
- Codex「Desktop」可能只係 npm CLI 包裝，唔係 Electron/Tauri GUI
- Hermes 嘅 Electron app 可能已存在但未公開（`apps/desktop/` 目錄）
- **要 check**：有冇 `electron/`、`tauri/`、`gui/` 目錄，或者睇 package.json/CMakeLists.txt

### 陷阱 5：Skills 系統是否自動學習？
- Some agents have static skills (user writes SKILLS.md, never changes)
- Some agents auto-create skills from experience and improve them during use
- Check the source code for auto-learning logic vs static definition

### 陷阱 6：Model Provider 支援要查原始碼定義
- README 可能冇列出所有 provider
- Check `model-provider` crate/module 嘅 enum/struct 定義
- Codex supports: openai, amazon-bedrock, ollama, lmstudio, and custom OpenAI-compatible
- Hermes supports: 200+ via OpenRouter + direct OpenAI, Anthropic, DeepSeek, Ollama, etc.

## 常見陷阱（實測教訓）

### 陷阱 1：「Desktop App」嘅定義
- Codex「Desktop」可能只係 npm CLI 包裝，唔係 Electron/Tauri GUI
- **要 check**：有冇 `electron/`、`tauri/`、`gui/` 目錄，或者睇 package.json/CMakeLists.txt

### 陷阱 2：「有 feature request = 有功能」
- GitHub issue 話「add X feature」唔代表已經實作
- **要 check**：source code 有冇相關實作，issues 係咪 open/closed

### 陷阱 3：Tag 數量 = Release 頻率？
- 1,045 tags 可能包含大量 pre-release/CI tags
- **要 check**：實際 release notes、正式版 vs pre-release 比例

### 陷阱 4：官方網站需要 login
- developers.openai.com/codex 回傳 403
- 呢啲情況要 rely on source code

## 報告格式

用表格對比，每個功能一行：

| 功能 | Agent A | Agent B | 贏家 |
|-----|:------:|:-------:|:----:|
| 功能名 | ✅ 有 / ❌ 冇 | ✅ 有 / ❌ 冇 | A/B/平手 |

最後加一段總結，講清楚：
- 邊個適合咩場景
- 最重要嘅差距係咩
- 有冇誤解需要澄清
