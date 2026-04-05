# Claude Dotfiles

Custom commands（`/pm`、`/pm-sync`、`/pm-bye`、`/pm-review` 等）的原始碼：
- **GitHub**：https://github.com/CPIDLE/claude-dotfiles
- **安裝位置**：`~/.claude/`（由 install script 複製）

## 安裝與部署

```bash
git pull
# Windows
powershell -ExecutionPolicy Bypass -File install.ps1
# macOS / Linux
bash install.sh
```

> **重要**：修改原始碼後必須重新執行 install script，否則 `~/.claude/` 下的檔案不會更新。

## 關鍵 ID

| 項目 | ID |
|---|---|
| Chat Webhook | `https://chat.googleapis.com/v1/spaces/AAQAYB_uT0M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=WnDNMALPegG-JGsZjqeBpil0-BnwdgAimDvgJKP_0uQ` |
| Dashboard Sheet | `19Wn3U4kbQw712SZGN7eKJDYGa5JYUUYofDi-zuakuPI` |
| Apps Script Web App | `AKfycbz-a6vGaQ1bucB4MGtCZ80ICnkCqHWQ2VFbL2yM8B_dGK8_HLlVURDpNKI1OvUjdTONnw` |

---

# User Preferences

## Response Style
- 回應盡量精簡，直接給結果，不複述問題、不加開場白
- 改完檔案不需要逐行解釋改了什麼 — 使用者看 diff 就懂
- 不重複輸出檔案完整內容，除非使用者要求
- 錯誤訊息直接貼關鍵行 + 修正方式，不需完整 stack trace 分析

## Notification Sounds
- When asking the user a question or needing user input/selection: handled by PreToolUse hook on AskUserQuestion in settings.json (auto beep before question). No need to manually beep.
- When task is completed: handled by Stop hook in settings.json (auto beep 3 times). No need to manually beep.

## Plan-Execute Workflow

Non-trivial tasks follow 3 phases：

### Phase 1: Plan
- Use **EnterPlanMode** for multi-file / architectural / multi-step tasks
- Plan 須列出：Goal、Steps（含檔案路徑）、Scope boundary、Permissions needed、Estimated impact
- **ExitPlanMode** 提交，等使用者核准才動手

### Phase 2: Permission Reminder
核准後、執行前，印一段 `--- Permission Summary ---`（列出所有需要的工具權限），僅通知不等確認。

### Phase 3: Autonomous Execution
在核准範圍內自主執行，不逐步問。用 TodoWrite 追蹤進度。
- **STOP** only when：超出 scope、步驟失敗無法自修、未核准的破壞性操作、需大幅修改計畫

## /do 委派規則

### Quota-aware 自動切換（deep 任務）

執行 deep 等級任務前，讀取 `~/.claude/usage-cache.json`：
- `session.utilization >= 80` **或** `week.utilization >= 80`（紅區）→ 委派給 `/do deep`
- 否則（綠/黃區）→ Claude Code 自己處理（更快 4x、品質一次到位）
- cache 不存在或讀取失敗 → 視為綠區（不委派）

### Easy 任務（永遠委派）

遇到以下情形，主動使用 `/do easy` 委派：
- 新增獨立模組/工具/腳本（不依賴現有程式碼）
- 重複性的檔案建立（批次產生類似結構）
- 簡單的 utility function 實作

### 不要委派

- 修改現有核心程式碼
- 需要理解上下文的 bug fix
- 架構設計相關
- 安全敏感操作、CLAUDE.md/AGENTS.md 修改

前提：`GEMINI_API_KEY` 環境變數已設定（預設引擎 gemini）。未設定時跳過，不報錯。

## Coding Discipline

- 每完成一個步驟就跑相關 test（有對應 test 跑該檔，沒有跑 suite，無 test 設定則跳過）
- 發現需要額外修改時回報使用者，不自行擴大範圍
- 避免模糊命名（`data2`、`result2`）
- 不 hardcode secrets — 用環境變數或 config
- 處理使用者輸入和外部 API 回應時加基本驗證
