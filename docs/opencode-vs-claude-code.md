# OpenCode vs Claude Code 比較

基於 2026-04-02 實際使用經驗的對照。

---

## 基本資訊

| | OpenCode | Claude Code |
|---|---|---|
| 開發者 | SST（開源社群） | Anthropic |
| 授權 | MIT | 商業 |
| 版本 | v1.3.13 | 最新版 |
| 安裝 | WinGet / npm / brew | npm |
| 設定檔 | opencode.json + AGENTS.md | CLAUDE.md + settings.json |

## LLM 支援

| | OpenCode | Claude Code |
|---|---|---|
| 預設模型 | 可自選（無預設） | Claude Opus/Sonnet |
| 本地模型 | Ollama（任意模型） | 不支援 |
| 雲端模型 | Anthropic、Google、OpenAI 等 | 僅 Anthropic |
| 模型切換 | opencode.json 設定 | 內建切換 |
| API Key | .env 或環境變數 | 內建 OAuth |

## 功能對照

| 功能 | OpenCode | Claude Code |
|---|---|---|
| 檔案讀寫 | 有 | 有 |
| Bash 執行 | 有 | 有 |
| 搜尋（glob/grep） | 有 | 有 |
| Permission 系統 | opencode.json 設定 | settings.json + 互動式 |
| Agent 系統指示 | AGENTS.md | CLAUDE.md |
| 自訂 Agent | opencode.json agent 區段 | 不直接支援 |
| Plugin 系統 | .opencode/plugins/ | hooks（settings.json） |
| Skill 系統 | .opencode/skills/ | ~/.claude/commands/ |
| MCP 支援 | 有 | 有 |
| Sub-agent | 有（subagent mode） | 有（AgentTool） |
| Plan Mode | 無內建 | 有（EnterPlanMode） |
| Memory 系統 | 無內建 | 有（~/.claude/memory/） |
| Session 續接 | 手動（session-notes.md） | claude --resume |
| Git 整合 | 基本 | 深度整合 |
| IDE 整合 | 無 | VS Code、JetBrains |

## 品質比較（實測）

| 維度 | OpenCode + Gemini 3.1 Pro | Claude Code + Opus |
|---|---|---|
| 文件產生 | 優 | 優 |
| Code Review | 良 | 優 |
| 單檔修改 | 良 | 優 |
| 多檔重構 | 差（容易改壞） | 優 |
| 錯誤修復 | 中（需詳細指示） | 優（可自主診斷） |
| 遵循指示 | 中（容易忽略規則） | 優（嚴格遵守） |
| 程式碼截斷 | 常見（`# ...` 佔位） | 罕見 |
| 幻覺 API | 偶爾（新增不存在的 class） | 罕見 |

## 成本比較

| | OpenCode | Claude Code |
|---|---|---|
| Ollama 本地 | 免費（需 GPU） | N/A |
| Gemini 3.1 Pro | 免費額度 + 按量計費 | N/A |
| Claude API | 可設定（需 API Key） | 訂閱制（$20/月 Pro） |
| 總成本 | 低（本地免費 + Gemini 免費額度） | 中高 |

## 最佳搭配策略

```
Claude Code（主力）
├── 複雜任務：多檔重構、架構設計、深度 debug
├── 品質要求高：production code、PR review
└── 需要工具整合：IDE、memory、plan mode

OpenCode（輔助）
├── 簡單任務：文件產生、格式轉換、git 操作
├── Claude Code 限流時：備案（Gemini 雲端）
├── 離線工作：Ollama 本地模型
└── 省錢：免費額度內的日常小任務
```

## 結論

OpenCode 不是 Claude Code 的替代品，而是**互補工具**：
- Claude Code 勝在品質、穩定性、工具整合
- OpenCode 勝在成本、模型彈性、開源可控
- 最佳策略是 Claude Code 為主 + OpenCode 為輔
