# AGENTS.md — OpenCode Enhance v0

> 此 repo 記錄 OpenCode 工具的安裝、設定與使用優化。Claude Code 使用 `~/.claude/CLAUDE.md`。

---

## Build / Lint / Test

本 repo 為**文件與設定記錄用途**，無編譯目標。偶有 TypeScript plugin 程式碼。

| 語言 | 測試 | Lint | Format |
|------|------|------|--------|
| TypeScript | `cd .opencode && bun test` | `bun run lint` | `bun run format` |
| Python | `pytest -q` | `ruff check .` | `ruff format .` |

---

## Response Style

- 回應精簡，直接給結果，不複述問題、不加開場白
- 改完檔案不逐行解釋 — 使用者看 diff 就懂
- 不重複輸出檔案完整內容，除非使用者要求
- 錯誤訊息只貼關鍵行 + 修正方式
- 使用繁體中文回覆

---

## 文件品質要求

產生任何文件（README、CHANGELOG、commit message、code comments）時：
- **具體**：用精確的技術術語，不用「各種」「一些」「相關」等模糊詞
- **結構化**：用標題、列表、表格組織內容，不寫大段落
- **可操作**：安裝步驟必須可直接複製執行
- **不灌水**：不加無意義的開場白、不重複已知資訊
- **程式碼範例**：必須是可執行的完整片段，不用 `...` 省略關鍵部分

### Markdown 規範

- 標題層級遞增（`#` → `##` → `###`），不跳層
- 程式碼區塊指定語言：` ```typescript `、` ```python `、` ```bash `
- 表格要有表頭；路徑用反引號包起來

---

## 程式碼品質要求

- 不加不必要的註解 — 程式碼本身應該自解釋
- 不加不必要的 type annotation — 能推導的就不寫
- 不加 feature flags、backwards-compatibility shims
- 不做 speculative abstraction
- 命名要精確：`getUserById` 不叫 `fetchData`
- 避免模糊命名（`data2`、`result2`）
- 不 hardcode secrets — 用環境變數

---

## Session 銜接

每次開始新 session，主動檢查：
1. `.opencode/session-notes.md`（如果存在）— 上次工作摘要
2. `git log --oneline -5` — 最近的變更
3. `git diff --stat` — 未 commit 的改動

完成一段工作後寫入 `.opencode/session-notes.md`：

```markdown
## 最後工作：YYYY-MM-DD HH:MM

### 完成
- ...

### 進行中
- ...

### 下一步
- ...
```

---

## 思考模式

收到指令時，不要直接執行。先思考：

1. **理解意圖**：使用者真正想達成什麼？
2. **補完指令**：有沒有隱含的前置條件或邊界情況？
3. **優化方案**：有沒有更好的做法？
4. **預判問題**：這樣做可能會碰到什麼問題？

指令模糊或多義時，**主動問清楚**，不要猜。

---

## Plan-Execute Workflow

多檔案 / 架構性 / 多步驟任務 follow 3 phases：

### Phase 1: Plan（等使用者核准）

計畫須列出：
- **Goal**：要達成什麼
- **Steps**：編號動作，含檔案路徑
- **Scope boundary**：in scope / out of scope

### Phase 2: Permission Reminder

核准後、執行前印 `--- Permission Summary ---`（工具權限），僅通知不等確認。

### Phase 3: Autonomous Execution

在核准範圍內自主執行，不逐步問。
- **STOP only when**：超出 scope、步驟失敗、需大幅修改計畫

---

## Coding Discipline

- 禁止使用 `# ...` 或 `// ...` 佔位語法
- 禁止在 edit 時省略未修改的部分導致截斷
- 發現測試失敗，立刻停下修復，不繼續往後改

---

## Git Attribution

所有透過 OpenCode 產生的 commit 必須在 message 尾部加上：

```
Tool: OpenCode (Ollama local)
```

---

## 檔案產生規則

- 所有產生的檔案預設放在**目前工作目錄**（`$CWD`）下
- 不要在家目錄、桌面、下載資料夾建立檔案

---

## Google Workspace MCP

已設定 `google-workspace-mcp`（Gmail + Calendar + Docs + Sheets + Drive + Slides + Forms）。

### 首次設定

1. 建立 Google Cloud 專案：https://console.cloud.google.com/
2. 啟用 APIs：Docs, Sheets, Drive, Gmail, Calendar, Slides, Forms
3. 建立 OAuth 2.0 Client ID（Desktop app），下載 `credentials.json`
4. 放置於 `~/.google-mcp/credentials.json`
5. 設定帳號：
   ```bash
   npx google-workspace-mcp accounts add <帳號名稱>
   ```

### 使用方式

- 讀取郵件：`listGmailMessages`、`searchGmail`、`readGmailMessage`
- 傳送郵件：建立草稿 → 人類審核 → 發送（安全流程）
- 日曆：`listCalendarEvents`、`createCalendarEvent`、`deleteCalendarEvent`
- 文件：`readGoogleDoc`、`appendToGoogleDoc`、`createDocument`

---

## 邊界（嚴格遵守）

- **禁止**修改 `~/.claude/` 下的任何檔案
- **禁止**修改 `pm-last.txt`、`progress.md`
- OpenCode 狀態寫入 `.opencode/` 目錄
- **禁止**呼叫 Google Chat Webhook 或 Apps Script

---

## OpenCode 設定檔結構

```
.opencode/              # OpenCode 工作目錄設定
├── plugins/            # TypeScript plugins（hook 系統）
│   └── git-attribution.ts
├── skills/             # Skill definitions
│   └── project-status/
│       └── SKILL.md
└── package.json

opencode-config/        # 可分發的設定套件
├── AGENTS.md          # 主要的 agent 指示
├── AGENTS-ur.md       # UR_Program_Analysis 專用指示
├── opencode.json      # 模型、agent、permission、MCP 設定
└── .opencode/         # 副本（plugins/skills）
```
