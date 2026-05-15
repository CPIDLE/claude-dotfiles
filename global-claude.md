# User Preferences

> Dotfiles 專案說明、安裝步驟、關鍵 ID 見 repo CLAUDE.md 和 `~/.claude/.env`。本檔只放全域行為偏好。

## Nickname
使用者暱稱我（Claude Code）為 **cc / CC**。訊息中第一人稱的「cc」「CC」皆指我。

## Response Style
- 直接給結果，不複述問題、不加開場白
- 改檔後不逐行解釋（看 diff 就懂）；不重複輸出檔案完整內容
- 錯誤貼關鍵行 + 修正方式，不貼完整 stack

## AskUserQuestion 選單
cc 有偏好時，**該選項排第一位** + label 結尾加「**（建議）**」（繁中括號）。中立題（純偏好）才不標。

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

## Memory（補充 harness 預設規則）

### Frontmatter 強制日期
寫 memory 時 `metadata:` 區塊**必填** `created` / `updated`（`YYYY-MM-DD`）：

```yaml
---
name: ...
description: ...
metadata:
  type: feedback   # 或 user / project / reference
  created: 2026-05-15   # 第一次寫入日期，永不變
  updated: 2026-05-15   # 每次改 body 都要同步
---
```

`created` 一旦寫入永遠不改（除非主題整個重定義 → 等於新 memo）。`updated` 反映最後一次 body 修改。

### Body 事件日期
`**Why:**` 段若引用 incident / session / decision，**必須帶絕對日期**（不要寫「上週」「之前」）。事件日期可早於 `created`（例如先發生後寫 memo）。

### 重整動作規範

| 動作 | `created` | `updated` | Body 加註 |
|---|---|---|---|
| 改寫內容（同主題 refine） | 保留 | 今天 | — |
| 合併 A+B → C | 取較早 | 今天 | `**Merged from:** [[a]] + [[b]] on YYYY-MM-DD` |
| 拆分 A → A1/A2 | 都繼承 A | 今天 | `**Split from:** [[a]] on YYYY-MM-DD` |
| 主題重定義 | 改成今天 | 今天 | 等於新 memo，舊的砍掉 |
| 過時刪除 | — | — | 直接砍 + 同步 MEMORY.md |

### 週期保養（人工為主）
- **觸發式**：cc 引用 memo 後發現過時 → **當下就改/砍**，不留到下次
- **每月一次**：使用者主動或 `/pm-bye` 觸發時，掃 `updated` > 30 天未動的 memo 問「還準嗎？」
- **紅旗 pattern**（看到就提醒使用者收）：
  - 檔名含 `progress` / `wip` / `_v2` 或具體日期（多半結案後該收）
  - body 出現「待」「下一步」「TODO」（進行式，結案後該刪）
  - feedback / project 缺 `**Why:**` / `**How to apply:**`（結構不完整）
  - `created == updated` 且 > 60 天（寫完沒人碰，可能根本沒用）
- 同主題 memo > 1 個 → 合併（依重整動作規範）

## ASCII Art Diagrams（Sarasa Mono TC）

### 字元優先序
1. **首選**：`─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`（連續框線）
2. **可用**：`- | +`（ASCII，當不確定渲染環境時）
3. **禁用**：厚框 `═║━┃┏┓┗┛╔╗╚╝`、斜線盒 `╱╲`、Unicode 箭頭/數學/emoji

對齊不確定就跑 `/ascii-align`，不行才退回 ASCII。
替代對照表：`~/.claude/skills/ascii-align/scripts/symbol_fix.py::SYMBOL_MAP`

### 寬度守則
- CJK / fullwidth = 2 cols；ASCII + 本 11 個 box = 1 col；EAW=Ambiguous 多數 2 cols（例外 `°` `–` 本 11 個 box = 1 col）
- 同 box 內每 row display width 必須相等；跨 row `│` 同 col；`┌─┐`/`└─┘` 角對齊；箭頭 `v`/`^` 對齊上下 `┬`/`┴`/`│`
- 產出後跑 `/ascii-align <file.md>` 自動檢查；不確定就退回純文字（歪 box 比 flat text 糟）

### Pipeline 救不了的（生成時就要對）
工具只救「字元」層，「幾何」層必須生成時對：箱體歪斜、跨 row `│` col 漂移、CJK 沒算 2 cols、混用 `┏/┗` 與 `┌/└`。
