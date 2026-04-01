# PM Sync — 中期同步 + 動作選單

> 共用邏輯（progress.md 格式、Dashboard 規則、Google 可用性）請參照 `commands/pm.md` 的「共用邏輯參考」區段。

## Status Line

```bash
bash ~/.claude/pm-update.sh sync running
```

**結束前**也必須執行：`bash ~/.claude/pm-update.sh sync done`

## 自動偵測狀態

顯示目前工作狀態：
```
📊 目前狀態
├─ Tasks: N/M completed
├─ Git: X modified, Y untracked
├─ 上次同步：<時間 或「—」>
└─ Dashboard: <已同步 / 未同步>
```

狀態資訊來源：
- Tasks：從 TodoWrite 目前的 task 狀態計算
- Git：執行 `git status --short` 統計
- 上次同步：從 progress.md 的「最後同步」時間讀取
- Dashboard：檢查 CLAUDE.md 中的 `Dashboard Sheet` 和 `Apps Script Web App` ID 是否已設定

## 選單

如果有 `2` 參數（`/pm-sync 2`）→ 直接跳到選 1（同步進度），不顯示選單。

否則顯示：
```
你想做什麼？
1. 同步進度 → Dashboard Sheet + Chat Space（預設）
2. 審核 — 執行 /pm-review easy
3. 調整計畫 — 修改 scope 或重新排序
```

---

## 選 1：同步進度

### Step 0：自動 Smart-Commit

如果在 git repo 中，執行 `git status --short`：
- 有 dirty files → 自動分析改動、產生 commit message、執行 `git add` + `git commit`（不問、不 push）
- 無改動 → 跳過

### Step A：檢查 progress.md

使用 Glob 搜尋 `~/.claude/projects/**/memory/progress.md`。如果不存在：
```
⚠️ 找不到 progress.md。
💡 請先執行 /pm new 建立專案進度。
```
直接結束。

### Step PRE：Google 工具可用性檢查

讀取 CLAUDE.md 中的 `Dashboard Sheet`、`Chat Webhook`、`Apps Script Web App` ID。
如果任一 ID 仍為 placeholder（包含 `<` 字元）或缺少 → 視為未設定。

**若 ID 未設定：**
```
⚠️ Google Workspace 尚未完成設定。
   缺少：<列出未設定的項目>
⏭️ 跳過 Google 同步，僅更新本地 progress.md。
```
更新 progress.md 中的「最後同步」時間，然後跳過 Step C/D。

**若 ID 已設定 → 繼續 Step C+D。**

### Step B：更新本地 progress.md

將目前工作進度寫入 progress.md（見 pm.md「共用邏輯參考」的 progress.md 標準格式）。

### Step C+D：發送 Chat 通知 + 更新 Dashboard Sheet（平行）

**同時執行**以下兩項（互不依賴）：

> ⚠️ **部分失敗處理**：C 或 D 任一失敗，顯示 `⚠️ <Chat/Dashboard> 同步失敗：<原因>`，不影響另一項。

**C — 發送摘要到 Google Chat Space（via Webhook）**

Chat Webhook URL：從 CLAUDE.md 的關鍵 ID 表讀取。

1. 構建 JSON body：
   ```json
   {"text":"📋 *<專案名稱> — 進度更新*\n\n• <重點 1>\n• <重點 2>\n• <重點 3>"}
   ```
2. 使用 Bash curl 發送（必須用 heredoc + printf 確保 UTF-8）：
   ```bash
   BODY=$(cat <<'ENDJSON'
   {"text":"📋 *<專案名稱> — 進度更新*\n\n• <重點 1>\n• <重點 2>"}
   ENDJSON
   )
   printf '%s' "$BODY" | curl -s -X POST '<Chat Webhook URL>' \
     -H 'Content-Type: application/json; charset=UTF-8' -d @-
   ```
3. 如果 curl 回應不含 `"name":"spaces/` → 顯示 `⚠️ Chat 通知失敗` 並繼續

擷取重點規則：優先已完成（✅）→ 進行中（🔄）→ 下一步，不超過 5 項。

**D — 更新 Dashboard Sheet（via Apps Script）**

`APPS_SCRIPT_URL` = `https://script.google.com/macros/s/<Apps Script Web App ID>/exec`

1. 從 progress.md 擷取精簡資訊，構建 JSON payload：
   ```json
   {
     "description": "<一句話專案簡述>",
     "status": "<開發中/轉型中/規劃中/已完成/維護中>",
     "completed": "<本次完成項目，逗號分隔>",
     "next": "<下次預計項目，逗號分隔>",
     "notes": "<重要記事，可空>",
     "updatedAt": "<YYYY-MM-DD HH:MM>"
   }
   ```
2. Base64 編碼 payload，URL encode（`+`→`%2B`、`/`→`%2F`、`=`→`%3D`）
3. 呼叫 `curl -s -L "<APPS_SCRIPT_URL>?action=upsert&project=<專案名稱>&payload=<URL_ENCODED_BASE64>"`
4. 如果 curl 回應不含 `"status":"ok"` → 顯示 `⚠️ Dashboard 更新失敗` 並繼續

> ⚠️ Dashboard 是總覽，每個欄位用最短的詞描述，不寫完整句子。

---

## 選 2：審核

執行 `/pm-review easy`。

---

## 選 3：調整計畫

- 進入 Plan Mode（`EnterPlanMode`）
- 讓使用者重新規劃剩餘工作
- 完成後更新 TodoWrite tasks

---

## 注意事項

- 所有輸出使用繁體中文
- 預設自動 — 每個階段有 happy path
- 需要時才問 — 只在分歧點或風險點才跳選單
