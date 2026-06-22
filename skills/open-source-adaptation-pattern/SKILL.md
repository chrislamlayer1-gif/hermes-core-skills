---
name: open-source-adaptation-pattern
description: Use when evaluating whether an open-source project fits our needs.
---

# 開源項目分析與落地模式

## 3 層判斷流程

### 第1層：可以直接用嗎？
檢查工具生態是否兼容。唔兼容就跳第2層。

### 第2層：設計理念可以參考嗎？
如果唔可以直接用，睇佢嘅核心理念係咪通用嘅。通用理念就可以借鑒。

### 第3層：落地執行
將理念轉化為自己生態嘅實現方式，唔好1:1抄襲。

## 多層次分析模式（2026-06-16 CUA 經驗補充）

大 project 通常由**多個子組件**組成，唔同組件可能有唔同嘅可用性層次。要逐個分析，唔好一刀切：

### 4 個層次
1. **🔧 可直接裝** — binary/app，一條 command 搞掂（如 Cua Driver）
2. **📦 可 pip/brew 裝但有限制** — Python package 或 library，但可能要額外 runtime（如 QEMU、雲端 API key）
3. **📚 可學習設計** — 源碼公開，可以參考架構同 API 設計（如 MCP Server 模式、Background input 技術）
4. **☁️ 要錢/要賬號** — 雲端服務，免費版有限制（如 Cua Sandbox 雲端版要 CUA_API_KEY）

### 執行方式
- 逐個子組件 run 一次呢個 4 層 filter
- 最後對師兄匯報時用 Emoji 標記（✅ 裝到 / ⚠️ 有條件 / 📚 學設計 / ☁️ 要錢）
- 重點係：**搞清楚「裝咗之後具體做到咩」**，唔好剩係話「裝到」

## 執行步驟

1. 快速掃描：README、安裝方式、目錄結構、核心文件
2. 對比分析：建立「佢點做 vs 我哋點做」對比表
3. 制定落地計劃：P0（立即）+ P1（今週）+ P2（規劃）
4. 實作：適應自己生態，建立完整性驗證
5. 匯報：用白話+比喻向師兄解釋變化

## 實作指引（2026-06-05 ECC 經驗補充）

### 深度分析階段
除咗 README 表面，一定要睇：
- **Shortform/Longform guide**（ECC 有 the-shortform-guide.md + the-longform-guide.md，入面先有真嘅使用哲學）
- **目錄結構**（ECC 嘅 .agents/、hooks/、skills/、.claude/ 結構反映咗佢點組織 agent workflow）
- **Install script**（ECC 嘅 install.sh 揭示咗佢依存 Node.js runtime，唔係純 config pack）

### Adaptation 核心原則
- **唔好直接 clone workspace** — ECC 251 skills 大部分同你嘅項目無關，clone 落嚟佔幾百 MB
- **抽象核心理念** — ECC 嘅「subagents + hooks + skills + memory persistence」係通用理念，每個 harness 實現方式唔同
- **適應自己生態** — Hermes Agent 冇 Claude Code 嘅 hooks framework，所以要用 boot.sh 模式 + .agents/.md 文件代替

### 對師兄匯報方式
- 先講結論：「用唔用到 / 參考到」
- 然後「之前 vs 現在」對比
- 最後「師兄只需要記住 XX 一句話就得」

## 驗證項目
- 所有新元件存在且可執行
- boot.sh已更新（如果 boot.sh 係落地一部分）
- STATE.md已記錄
- git commit已做
- 已用白話+比喻向師兄匯報

## 實戰測試方法論（2026-06-06 headroom 經驗補充）

當工具聲稱可以「慳錢/加速/壓縮」時，**必須做實際 workload 測試**先好決定留唔留：

### headroom-ai 測試案例
**聲稱**：壓縮 tool output 60-95% token，唔影響質量
**實際測試結果**：
1. **user messages**（對話內容）→ 0% 壓縮（protected，跳過）
2. **短 tool output**（JSON 回傳）→ 0% 壓縮（router判斷為 `protected:recent_code`）
3. **長 prose 文章**（RSS 文章）→ -10% 壓縮（反而大了，router唔擅長純文字）
4. **重複性 verbose tool output** → 0-95%（95% 係因為 router 判斷「太短」直接極簡，唔係有意義壓縮）
**結論**：headroom 真係好，但設計場景係 CI logs / code search / build output，唔係我哋嘅 prose 文章或對話

### 測試 protocol
Step 1: 用真實數據整 3 個 test case（得意見、短 output、長 prose）
Step 2: 每個 case 用工具處理，量度效果（壓縮率/準確度/速度）
Step 3: 對比聲稱效果 vs 實際效果
Step 4: 判斷「啱唔啱我哋用」先決定安裝
Step 5: 如果唔啱用就 uninstall（`pip3 uninstall` / `brew uninstall`）

## 常見陷阱
- 直接clone大型project落workspace
- 1:1抄襲（格式唔兼容）
- 一次性落地太多
- 冇用白話向師兄解釋
- 只睇README，冇睇 shortform/longform guide（ECC 嘅真正精華喺 guides 入面）
- 冇考慮自己 harness（Claude Code vs Hermes Agent）嘅差異就照抄
- **信咗聲稱數字就裝，冇用自己嘅真實數據做測試**（headroom case）
- **冇 check 個工具係咪設計俾自己嘅使用場景**（headroom 係為 tool output 設計，唔係 prose/dialogue）
