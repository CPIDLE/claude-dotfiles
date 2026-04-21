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

### Hook 驅動強制委派

`UserPromptSubmit` hook 每次使用者送訊息時自動檢查 `~/.claude/usage-cache.json`（僅看 5h session）：
- **GREEN（< 50%）**：靜默，不輸出
- **WARN（≥ 50%）**：注入 `⚠️ QUOTA WARN` 提醒到對話中

**收到 QUOTA WARN 提醒時，必須遵守：**
1. 評估當前任務是否適合委派（見下方條件）
2. 適合 → **強制**使用 `/do easy` 或 `/do deep`，不可自己做
3. 不適合 → 自己處理，但盡量精簡 token 用量

> 門檻 50%（5h session 中段觸發，留時間反應）。Weekly 不警告（用量低不卡）。Cache 超過 10 分鐘視為過期，預設 GREEN。

### 適合委派（easy）

不論 quota 狀態，以下任務**永遠**用 `/do easy`（成本極低、不消耗 Claude quota）：
- 新增獨立模組/工具/腳本（不依賴現有程式碼）
- 重複性的檔案建立（批次產生類似結構）
- 簡單的 utility function 實作

### 適合委派（deep）— 僅 QUOTA WARN 時

收到 QUOTA WARN 提醒時，以下任務**必須**用 `/do deep`：
- 新增含複雜邏輯的模組（多函式、threading、async）
- 可以用 spec 完整描述的獨立功能
- 文件撰寫（README、CHANGELOG、docs）

### 不要委派

無論 quota 狀態，以下任務**永遠不委派**：
- 修改現有核心程式碼
- 需要理解上下文的 bug fix
- 架構設計相關
- 安全敏感操作、CLAUDE.md/AGENTS.md 修改
- `commands/*.md`、`skills/**` 的 prompt engineering 修改（Gemini 沒上下文，失敗成本高）

前提：`GEMINI_API_KEY` 環境變數已設定（預設引擎 gemini）。未設定時跳過，不報錯。

## Coding Discipline

- 每完成一個步驟就跑相關 test（有對應 test 跑該檔，沒有跑 suite，無 test 設定則跳過）
- 發現需要額外修改時回報使用者，不自行擴大範圍
- 避免模糊命名（`data2`、`result2`）
- 不 hardcode secrets — 用環境變數或 config
- 處理使用者輸入和外部 API 回應時加基本驗證

## ASCII Art Diagrams（Sarasa Mono TC）

產生含 box-drawing 的圖表時必須遵守（規則來自 AsciiArtViewer_v0 專案 659-block 語料教訓 +
71% coverage pipeline 驗證）：

### 字元白名單

- **允許**：ASCII (0x20-0x7E) + 11 個 box-drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- **不建議**：其他 box-drawing (`═║━┃┏┓┗┛╞╘╪┊╱╲` — Sarasa 可顯示 w1，但語意重複)
- **禁用**：Unicode 箭頭、數學符號、emoji、裝飾 — 用下表的 ASCII 替代（皆寬度守恆）

### Unicode → ASCII 替代對照（必須主動避免 Unicode）

| 類別 | Unicode (w=2) | ASCII (w=2) | 備註 |
|---|---|---|---|
| 箭頭 | `→` | `->` | 最常見陷阱，~1400+ 案例 |
| 箭頭 | `←` | `<-` | |
| 箭頭 | `↔` | `<>` | |
| 箭頭組合 | `──→` / `──►` / `──▶` | `───>` | 3-char Unicode → 4-char ASCII（依寬度重算） |
| 箭頭組合 | `◄──` / `←──` | `<───` | |
| 箭頭組合 | `←→` | `<-->` | 4 cols 守恆 |
| 上下箭頭 | `▲` / `↑` | `^ ` | 尾巴空白補齊 |
| 上下箭頭 | `▼` / `↓` | `v ` | |
| 三角指示 | `►` / `▶` / `▸` | `->` | |
| 三角指示 | `◄` | `<-` | |
| 數學 | `×` / `÷` / `±` | `x ` / `/ ` / `+-` | |
| 數學 | `≤` / `≥` / `≠` | `<=` / `>=` / `!=` | |
| 數學 | `≈` / `∞` / `√` | `~=` / `oo` / `V ` | |
| 邏輯 | `∧` / `∨` / `∈` | `&&` / `\|\|` / `in` | |
| 裝飾 | `●` / `○` / `■` | `* ` / `o ` / `# ` | |
| 裝飾 | `★` / `☆` / `◆` / `◇` | `* ` / `* ` / `* ` / `<>` | |
| 裝飾 | `•` / `·` / `…` / `—` | `* ` / `. ` / `..` / `--` | |
| 確認 | `✓` / `✔` / `✗` / `✘` | `v ` / `v ` / `x ` / `x ` | |
| 希臘 | `α β θ μ π σ Δ` | `a b th u pi s D ` | 尾巴補空白 |
| 圈號 | `① … ⑩` | `1 … 10` | |
| 其他 | `⚠` / `§` / `²` / `‖` / `█` | `! ` / `S.` / `^2` / `\|\|` / `##` | |

全表在 `~/.claude/skills/ascii-align/scripts/symbol_fix.py::SYMBOL_MAP`。

### 寬度守則（Sarasa Mono TC）

- **規則**：CJK 中文 / fullwidth = 2 cols，ASCII + 上述 box-drawing = 1 cols，East Asian Width = Ambiguous 多數 2 cols（例外：`°` / `–` / 本 11 個 box-drawing 為 1 cols）
- 同一 box 內每 row（含 top/bottom border）**display width 必須相等**
- 跨 row 的 `│` 分隔線必須同 col；上下邊界 `┌─┐` / `└─┘` 的角 col 必須對齊
- 箭頭 `v`/`^` 對齊上下 `┬/┴/│`

### 產生流程

1. 先定 canonical width（最寬 row）
2. 每 row 補 trailing space 到 canonical（中文 row 記得算 2 cols）
3. 不確定就退回純文字 — 歪 box 比 flat text 糟
4. 產出後若有疑慮，跑 `/ascii-align <file.md>` 自動檢查

### Pipeline 能自動處理 vs 產生時就要避免

| 自動可救 | 產生時必須避免 |
|---|---|
| Unicode 符號 → ASCII（char-level，`denoiser_rescue.py` 覆蓋全表） | **箱體幾何歪斜**（歪邊界、錯角 `┌...┐` 變 `┌...┘`） |
| 右 hrule 長度不足（`ascii_align.py` 自動補 `─`） | **跨 row `│` col 漂移**（結構錯位，無工具救） |
| Mask+fill 重分配 canonical slot 寬度（slot 內空白錯位） | **CJK 未算 2-col 導致 row 寬不一** |
| — | **混用 `┏/┗` 與 `┌/└`**（風格不一，無法 auto-normalize） |

產生時先確保「幾何」正確（box 對齊、寬度守恆），工具只能救「字元」層。

### Anti-patterns

- ❌ `1280×720 → 640×360` ✅ `1280x720 -> 640x360`
- ❌ `──►` + 下行 `│` 漂 col ✅ 整段用 `-->` + `|`
- ❌ 中英混合不計 2-col ✅ 明確補齊
- ❌ 用 `┏━┓` / `╔═╗` 等厚框 ✅ 統一用 `┌─┐`（最常見）
