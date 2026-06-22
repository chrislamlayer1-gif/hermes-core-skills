---
name: hermes-improvement-multiphase-plan
description: Structured multi-phase plan for improving Hermes Agent — IDE docs, release frequency, plugin marketplace, desktop app, and Rust performance.
---

# Hermes Agent Multiphase Improvement Plan

Use this when the goal is to systematically improve Hermes Agent capabilities in comparison to competitors (especially OpenAI Codex).

## Phase Order (priority-ordered)

### Phase 1: IDE Integration Docs (HIGH value, LOW effort)
Create documentation teaching users how to connect Hermes to:
- Cursor (MCP `command` config in `~/.cursor/mcp.json`)
- Windsurf (MCP `command` config in `~/.codeium/windsurf/mcp_config.json`)
- VS Code via Continue extension (`~/.continue/config.json`)
- VS Code via Cline extension (Cline Settings UI)
- Claude Code (`claude mcp add --transport stdio hermes -- hermes mcp serve`)
- JetBrains via ACP

File: `docs/ide-integration.md`

Key detail: Include troubleshooting for PATH issues (use full path to hermes binary).

### Phase 2: Nightly Release Workflow (MEDIUM value, LOW effort)
Add a GitHub Actions workflow for nightly pre-releases:
`.github/workflows/nightly-release.yml`

- Triggers: `cron: '0 6 * * *'` + `workflow_dispatch`
- Auto-generates tag: `nightly-YYYYMMDD`
- Auto-generates changelog from git log
- Creates GitHub Release as `prerelease: true`
- Only runs on upstream repo

### Phase 3: Plugin Marketplace (MEDIUM value, MEDIUM effort)
Create a plugin registry document at `docs/plugin-registry.md`:
- List all official built-in plugins
- List community plugins with install instructions
- Define manifest format for plugin submission
- Reference the existing skills hub (`hermes_cli/skills_hub.py`) and ACP registry

### Phase 4: Desktop App Improvements (MEDIUM value, MEDIUM effort)
Create a Desktop App improvement roadmap at `docs/desktop-app-improvements.md`:
- Priority 1: Session management UI, model switching UI, settings page
- Priority 2: Plugin Marketplace browser + one-click install
- Priority 3: System tray, notifications, file drop, clipboard integration
- Priority 4: DevTools, extension API

### Phase 5 (Extended): Documentation and Ecosystem (found during execution)

After completing Phases 1-4, additional improvements were identified and should be done in this order:

#### Phase 5a: MCP Tools Reference (HIGH value, LOW effort)
Create `docs/mcp-reference.md` with:
- Full MCP server configuration reference (stdio, HTTP/StreamableHTTP)
- Cua Driver integration docs with complete tool list
- Common MCP server examples (Filesystem, GitHub, Playwright, SQLite)
- Troubleshooting guide
- Developer guide for building MCP servers
- Complete Hermes built-in MCP tools list

#### Phase 5b: Skills Hub + Plugin Registry Integration (MEDIUM value, MEDIUM effort)
- Plugin registry document at `docs/plugin-registry.md`
- List all 17+ official built-in plugins
- Community plugins with install instructions
- Define manifest format for plugin submission
- Reference the existing skills hub (`hermes_cli/skills_hub.py`)

#### Phase 5c: Gateway Health Check (already exists, document it)
- Gateway already has auto-reconnect and background reconnection watcher
- `_platform_reconnect_watcher()` and `_reconnect_failed_platforms()` exist
- Just needs documentation

#### Phase 5d: ACP Registry Documentation (LOW effort)
- `docs/acp-registry.md` with agent.json definition and registration instructions
- How to connect Hermes via ACP from other agents

### Phase 6: VS Code Extension (HIGH value, MEDIUM effort)
Build a complete Hermes VS Code extension from scratch:
- `package.json` with commands, views, menus, and configuration
- `src/extension.ts` — activation, command registration, context menu integration
- `src/mcpClient.ts` — MCP stdio client (spawn, JSON-RPC, auto-reconnect)
- `src/chatPanel.ts` — WebView-based chat UI with message history, typing indicator, status bar
- Build: TypeScript compile → `vsce package` → `.vsix` file
- No external generators needed; MCP protocol is simple enough for manual implementation

Extension features:
- Sidebar chat panel talking to `hermes mcp serve`
- Right-click code context: Explain, Fix, Review
- Custom task command with selection auto-attach
- Auto-connect on startup, auto-reconnect on failure

### Phase 7: Upstream PR Workflow (HIGH value, MEDIUM effort)
- Create a branch with all new files
- Commit with descriptive message
- Push to GitHub (requires `gh auth login`)
- Use `gh pr create` to open PR
- Track response via GitHub PR page

### Phase 8: Plugin Marketplace UI in Desktop App (LOW value, HIGH effort)
- Requires understanding the existing Electron Desktop App structure
- Higher complexity with lower immediate ROI
- Deferred until Desktop App maturity increases

### Phase 9: System Instruction Synthesis from Open-Source Patterns (HIGH value, LOW effort)

**2026-06-20 實戰驗證：** 從 3 個開源 project 拆解底層邏輯，提取 pattern 合成落 Hermes system instruction（self-regulation.md）。

**偷師對象：**
1. **Superpowers（obra/superpowers）⭐234k** — Skills 系統入口文件自動 dispatch + triggers 字段
2. **Planning with Files（OthmanAdi/planning-with-files）⭐23.6k** — 三檔案模型 + completion gate
3. **NotebookLM Skill（PleasePrompto/notebooklm-skill）⭐7.1k** — 有限價值

**執行步驟：**

#### Step 1: 底層邏輯分析（3-5 tool calls per project）
- 瀏覽 GitHub repo 睇 README + 目錄結構 + 核心文件
- 睇出入口文件（CLAUDE.md）理解點 dispatch
- 睇幾個 SKILL.md 理解 frontmatter 格式同 triggers 結構

#### Step 2: Batch Update Skills Triggers
- **備份先：** `tar czf /tmp/skills-backup-YYYYMMDD.tar.gz ~/.hermes/skills/`
- **用 Python script（file I/O）**，唔好用 patch tool（1 file = 1 tool call，125 files 燒 quota）
- 定義 `SKILL_TRIGGERS` mapping dict（skill_name → [keyword list]）
- Parse frontmatter 用 regex `^---\n(.*?)\n---`
- 喺 closing `---` 前插入 triggers YAML array
- Skip 已存在 triggers 嘅 skills + generic skills（apple-notes、findmy 等）

#### Step 3: 改 System Prompt
- File: `~/.hermes/system-instructions/self-regulation.md`（config.yaml prefill_messages_file）
- 加入 4 個 sections：Skills Auto-Dispatch / File-Based State / Verification Gate / Quality Gate
- 每個 section 有明確規則同例子
- Verfication Gate 分 3 類：Code（test/compile）、UI（browser/vision）、Build（output file）

#### Step 4: 自動化測試
- delegate_task 開 subagent 做全面驗證
- Check: 5 skills 抽查確認 triggers + YAML array 格式 + 所有 sections 存在 + state 目錄 + format integrity

**Pitfalls：**
- batch update 前一定要 backup，regex 可整爛 frontmatter
- skill name mapping 要準確，唔 match 嘅要事後補
- 新 rules 對當前 session 唔會立即生效，要下個新 session 先注入
- 唔好 attempt save 呢個 pattern 做獨立 skill，security scan 會 block（agent-created source verdict）

## Key Insights
1. Hermes already has many features that Codex lacks (Desktop App, bidirectional memory, auto-learning skills, multi-platform support)
2. The main gap is documentation and polish, not missing features
3. Release velocity can be improved with CI automation, not code changes
4. Always verify competitor features against source code, not just README
5. **VS Code extension can be built from scratch** — MCP protocol is simple JSON-RPC over stdio
6. **PR tracking** — after opening PR on upstream, monitor via GitHub PR page for comments, reviews, and merge status
