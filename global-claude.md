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

## /do 委派規則

`UserPromptSubmit` hook 讀 `~/.claude/usage-cache.json`（只看 5h session），超過門檻注入 `⚠️ QUOTA WARN` 提醒。

**收到 WARN 時**：適合委派 → **強制** `/do easy` 或 `/do deep`；不適合 → 自己做但省 token。

| 情境 | 類型 | 引擎 |
|---|---|---|
| **永遠** 用 `/do easy` | 新增獨立模組/工具/腳本（不靠現有 code）、批次建檔、簡單 utility | 極低成本，不吃 quota |
| **僅 WARN 時** 用 `/do deep` | 複雜獨立模組（多函式、threading、async）、spec-able 功能、文件撰寫 | deep review |
| **永遠不委派** | 改現有核心程式、需上下文 bug fix、架構設計、安全敏感、CLAUDE.md/AGENTS.md、`commands/*.md`/`skills/**` 的 prompt engineering | Gemini 沒上下文失敗成本高 |

> Cache 過期（> 10 分鐘）視為 GREEN；Weekly 不警告。前提：`GEMINI_API_KEY` 已設定（預設 engine gemini），未設定則跳過。

## Coding Discipline
- 每完成一步驟跑相關 test（有對應 test 跑該檔、沒有跑 suite、無 test 設定則跳過）
- 發現需額外修改先回報，不自行擴大範圍
- 避免 `data2` / `result2` 類模糊命名

## ASCII Art Diagrams（Sarasa Mono TC）

產生含 box-drawing 的圖表時必須遵守（規則來自 AsciiArtViewer_v0 659-block 語料 + 71% coverage pipeline）：

### 字元白名單
- **允許**：ASCII (0x20-0x7E) + 11 個 box-drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- **禁用**：Unicode 箭頭、數學符號、emoji、裝飾、其他 box (`═║━┃┏┓┗┛╔╗╚╝╞╘╪┊╱╲`) — 全改 ASCII 寬度守恆替代

### Unicode → ASCII 替代（主動避免 Unicode）

| 類別 | Unicode (w=2) | ASCII (w=2) |
|---|---|---|
| 箭頭 | `→` / `←` / `↔` | `->` / `<-` / `<>` |
| 箭頭組合 | `──→` / `──►` / `──▶` / `◄──` / `←→` | `───>` / `<───` / `<-->` |
| 上下 | `▲` / `↑` / `▼` / `↓` | `^` + 尾空白 / `v` + 尾空白（補到 2 cols） |
| 三角 | `►` / `▶` / `▸` / `◄` | `->` / `<-` |
| 數學 | `×` `÷` `±` `≤` `≥` `≠` `≈` `∞` `√` | `x ` `/ ` `+-` `<=` `>=` `!=` `~=` `oo` `V ` |
| 邏輯 | `∧` / `∨` / `∈` | `&&` / `\|\|` / `in` |
| 裝飾 | `●` `○` `■` `★` `◆` `•` `·` `…` `—` | `* ` `o ` `# ` `* ` `<>` `* ` `. ` `..` `--` |
| 確認 | `✓` / `✔` / `✗` / `✘` | `v ` / `x ` |
| 希臘 | `α β θ μ π σ Δ` | `a b th u pi s D `（尾空白補 2 cols） |
| 圈號 | `① ~ ⑩` | `1 ~ 10` |
| 其他 | `⚠` / `§` / `²` / `‖` / `█` | `! ` / `S.` / `^2` / `\|\|` / `##` |

全表（含所有數十個符號）：`~/.claude/skills/ascii-align/scripts/symbol_fix.py::SYMBOL_MAP`

### 寬度守則
- CJK / fullwidth = 2 cols；ASCII + 本 11 個 box = 1 col；EAW=Ambiguous 多數 2 cols（例外 `°` / `–` / 本 11 個 box = 1 col）
- 同 box 內每 row（含 top/bottom border）display width 必須相等
- 跨 row `│` 必須同 col；`┌─┐` / `└─┘` 角 col 對齊；箭頭 `v` / `^` 對齊上下 `┬` / `┴` / `│`

### 產生流程
1. 取 canonical width = 最寬 row
2. 每 row 補 trailing space 到 canonical（中文 row 記算 2 cols）
3. 不確定就退回純文字 — 歪 box 比 flat text 糟
4. 產出後跑 `/ascii-align <file.md>` 自動檢查

### Pipeline 救不了的（產生時就要避免）
- **箱體幾何歪斜**（歪邊界、錯角 `┌...┐` 變 `┌...┘`）
- **跨 row `│` col 漂移**（結構錯位）
- **CJK 未算 2-col** 導致 row 寬不一
- **混用 `┏/┗` 與 `┌/└`**（風格不一無法 auto-normalize）

工具只能救「字元」層，「幾何」層必須生成時就對。

### Anti-patterns
- ❌ `1280×720 → 640×360` ✅ `1280x720 -> 640x360`
- ❌ `──►` + 下行 `│` 漂 col ✅ 整段 `-->` + `|`
- ❌ 用 `┏━┓` / `╔═╗` 厚框 ✅ 統一 `┌─┐`
