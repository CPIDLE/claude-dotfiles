# PM Bye — 收工

依序自動執行以下步驟，有問題才暫停。

> 共用邏輯（progress.md 格式、Dashboard 規則、Google 可用性）請參照 `commands/pm.md` 的「共用邏輯參考」區段。

## Status Line

```bash
bash ~/.claude/pm-update.sh bye running
```

**結束前**（告別之前）也必須執行：`bash ~/.claude/pm-update.sh bye done`

## Step 1：回顧本次對話

回顧整個對話歷史，整理出：
- **完成事項**：本次 session 完成的所有工作
- **進行中工作**：開始但未完成的事項
- **已知問題**：發現但未解決的問題
- **下次建議**：建議下次優先處理的事項

## Step 1.5：README 新鮮度檢查（自動）

如果專案根目錄有 `README.md`，檢查是否需要更新：

1. 用 `git log -1 --format="%ai" -- README.md` 取得最後修改日期
2. 用 `git diff --stat $(git log -1 --format="%H" -- README.md)..HEAD` 統計期間檔案變動數

**觸發條件**（同時滿足）：README 最後修改距今 ≥ 1 天 且 期間檔案變動 ≥ 5 個

**觸發時**：
```
📝 README.md 已 N 天未更新，期間有 M 個檔案變動，建議更新。
   要現在更新嗎？
```
- 同意 → 讀取現有 README，**只更新固定範本區段**，非範本區段完整保留
- 不同意 → 跳過

**不觸發時**：靜默跳過。**無 README.md 或非 git repo** → 跳過。

## Step 2：審核（review easy，自動）

執行 `/pm-review easy` 的流程：
- 測試 + lint + debug 掃描 + 快速 code review
- 輸出一行摘要：`🔍 審核：測試 ✅/❌ | Lint ✅/⚠️ | Debug ✅/⚠️ | Code ✅/⚠️`
- 測試失敗 → 暫停詢問，其餘只記錄
- 額外：如果 `reviews/` 有今日 deep 報告 → 顯示 `🔴 Deep：<總評> | ⭐ X.X/5`

無 git repo 或無改動 → 跳過。

## Step 3：Git 整理

```bash
git status --short
git diff --stat
git log --oneline -5
git log @{u}..HEAD --oneline 2>/dev/null
git remote -v
```

1. 如果有 dirty files → 自動 smart-commit（不問、不 push）
   - 完成後重新檢查 `git status` 和未 push commits
2. 如果有未 push commits → 詢問：`📤 有 N 個 commit 尚未 push，要現在 push 嗎？`
   - 同意 → 執行 `git push`
3. 如果沒有 remote → 詢問：`🔗 要建立 GitHub private repo 嗎？`
   - 同意 → `gh repo create <folder-name> --private --source=. --push`

## Step 4：寫入 progress.md（含 Session ID）

將整理好的進度寫入 memory 資料夾中的 `progress.md`（覆寫，只保留最新狀態）。

**撈取 Session ID：**
1. 列出 `~/.claude/sessions/` 目錄下的 `.json` 檔案
2. 找到 `cwd` 匹配當前工作目錄的檔案
3. 讀取其中的 `sessionId` 欄位
4. 找不到 → 跳過 Session 區段

## Step 5：Google 同步（自動，不需確認）

先依 `/pm-sync` Step PRE 的方式，從 `~/.claude/.env` 讀取 `CHAT_WEBHOOK_URL` / `DASHBOARD_SHEET_ID` / `APPS_SCRIPT_WEB_APP_ID`。
如果任一 ID 未設定或為 placeholder → 跳過 Google 同步。

執行 `/pm-sync` 選 1 的 Step PRE → Step B → Step C+D（**跳過 Step 0 smart-commit**，已在 Step 3 完成）：
- 顯示：`📤 已同步 Dashboard Sheet、Chat Space！`

## Step 6：Retro to Memory（自動）

回顧本次 session，檢查是否有值得記住的內容：

| 類型 | 觸發條件 |
|---|---|
| feedback | 使用者糾正了做法或確認了非顯而易見的做法 |
| project | 學到新的專案背景或限制 |
| user | 發現使用者偏好或角色資訊 |

- 有值得記住的 → 寫入 memory 檔案（依標準格式含 frontmatter）
- 沒有 → 跳過，不提示

## Step 6.5：Hookify 候選檢查（自動）

掃描本次 session 寫入或更新的 memory feedback 檔，挑出能變成硬阻擋 hook 的紅線。

**掃描範圍：**
1. 找出 memory 資料夾下 mtime 在本次 session 期間內的 `feedback_*.md`
   - 用 `find <memory_dir> -name 'feedback_*.md' -newer <session_start_marker>` 或 mmin 近似
   - 若無法判定 session 起點 → fallback 掃今日（mtime < 1 day）新增/修改的 feedback
2. 沒有新 feedback → 一行帶過「🪝 Hookify：本次無新候選」，直接跳到 Step 7

**分類規則：**

| 等級 | 判準 | 行為 |
|---|---|---|
| 🔴 強 | 規則能對應到具體 tool call regex（Bash command 含特定字串、Write/Edit 目標檔副檔名 + 內容 pattern） | 列出來、附建議 regex、問 user 要不要寫 |
| 🟡 中 | pattern 鬆（如「不要用 `data2` 變數名」）或誤擋率高 | 列出來但標註「斟酌」，預設不問 |
| ⚪ 工作流 | 需 sequence/context 判斷、純人工流程、judgment call | 不列 |

**輸出範例：**

```
🪝 Hookify 候選（本次 session 新增 3 條 feedback）

🔴 強候選：
  1. 禁 reqty 改量
     pattern: Bash/Write/Edit 含 `reqty|FunctionCode\s*=\s*0?5|TradeKind\s*=\s*0?3`
     來源: feedback_no_reqty.md

🟡 中候選（斟酌）：
  - feedback_pre_trade_protocol.md（workflow 層，hookify 易誤擋合法流程）

要把強候選寫成 hookify rule 嗎？
[1] 全部 [2] 選擇 [3] 跳過（記錄到 progress.md 下次再說）
```

**選 1 / 2 → 接著跑 `/hookify` 把 rule 寫進 `.claude/hookify.*.local.md`**
**選 3 → 把候選清單追加到 progress.md 「📌 下次建議」區段**

無強候選 → 顯示 `🪝 Hookify：本次無強候選（N 條中候選已略過）`，不打斷流程。

## Step 7：顯示進度摘要

```
📋 本次工作摘要

✅ 完成：
- item 1

🔄 進行中：
- item 1

⚠️ 已知問題：
- issue 1

📌 下次建議：
- next step 1

🌿 Git：branch-name | N unpushed
🔍 審核：測試 ✅/❌ | Lint ✅/⚠️ | Code ✅/⚠️
🔴 Deep：<總評> | ⭐ X.X/5（如有 deep 報告）
```

## Step 8：告別並退出

```
👋 收工！進度已儲存。
   💡 續回本次：claude --resume <sessionId>
   👉 按 /exit 離開 或 /clear + /pm 接續執行
```

---

## 注意事項

- 所有輸出使用繁體中文
- 預設自動 — 每個階段有 happy path，不選就能走完
- 需要時才問 — 只在分歧點或風險點才跳選單
