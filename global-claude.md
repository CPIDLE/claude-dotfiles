# User Preferences

> Dotfiles 專案說明、安裝步驟、關鍵 ID 見 repo CLAUDE.md 和 `~/.claude/.env`。本檔只放全域行為偏好。

## Nickname
使用者暱稱我（Claude Code）為 **cc / CC**。訊息中第一人稱的「cc」「CC」皆指我。

## Response Style
- 直接給結果，不複述問題、不加開場白
- 改檔後不逐行解釋（看 diff 就懂）；不重複輸出檔案完整內容
- 錯誤貼關鍵行 + 修正方式，不貼完整 stack

## Notification Sounds
Beep 由 `settings.json` hooks 處理（AskUserQuestion → 1 聲、Stop → 3 聲）。**不要手動 beep**。

## 關鍵 ID / Secrets
所有 webhook、Sheet ID、Apps Script ID 都在 `~/.claude/.env`（`CHAT_WEBHOOK_URL` / `DASHBOARD_SHEET_ID` / `APPS_SCRIPT_WEB_APP_ID`）。**絕不把這些值寫進 CLAUDE.md 或任何會 commit 的檔**。

## Plan-Execute Workflow

Non-trivial tasks 走三階段：

1. **Plan** — 多檔/架構/多步用 EnterPlanMode，列 Goal / Steps（含檔案路徑）/ Scope boundary / 權限 / 影響；ExitPlanMode 等使用者核准。
2. **Permission Summary** — 核准後執行前印一段 `--- Permission Summary ---`（列需要的工具權限），僅通知不等確認。
3. **Autonomous Execution** — 核准範圍內自主執行，用 TaskCreate 追蹤進度。**STOP** 時機：超出 scope、步驟失敗無法自修、未核准的破壞性操作、需大幅修改計畫。

## Coding Discipline
- 每完成一步驟跑相關 test（有對應 test 跑該檔、沒有跑 suite、無 test 設定則跳過）
- 發現需額外修改先回報，不自行擴大範圍
- 避免 `data2` / `result2` 類模糊命名
- **Edit/Write 前必先 Read 該檔**（即使你「以為記得」內容或檔案剛被你建立）。Edit tool 會 reject 未 Read 的檔，硬上一定失敗 — 第一次就 Read，不要靠重試

## ASCII Art Diagrams（Sarasa Mono TC）

### 字元白名單
- **允許**：ASCII (0x20-0x7E) + 11 個 box-drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- **禁用**：Unicode 箭頭/數學/emoji/裝飾、厚框 (`═║━┃┏┓┗┛╔╗╚╝`)、斜線盒 (`╱╲`) — 全改 ASCII
- 替代對照表（箭頭 `→`→`->`、`▲/▼`→`^/v` 補空白、數學/裝飾/希臘等數十項）：`~/.claude/skills/ascii-align/scripts/symbol_fix.py::SYMBOL_MAP`

### 寬度守則
- CJK / fullwidth = 2 cols；ASCII + 本 11 個 box = 1 col；EAW=Ambiguous 多數 2 cols（例外 `°` `–` 本 11 個 box = 1 col）
- 同 box 內每 row display width 必須相等；跨 row `│` 同 col；`┌─┐`/`└─┘` 角對齊；箭頭 `v`/`^` 對齊上下 `┬`/`┴`/`│`
- 產出後跑 `/ascii-align <file.md>` 自動檢查；不確定就退回純文字（歪 box 比 flat text 糟）

### Pipeline 救不了的（生成時就要對）
工具只救「字元」層，「幾何」層必須生成時對：箱體歪斜、跨 row `│` col 漂移、CJK 沒算 2 cols、混用 `┏/┗` 與 `┌/└`。
