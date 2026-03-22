# Bye — 收工告別

結束工作 session 時使用，自動整理進度、提醒 commit/push、保存工作狀態。

## 執行步驟

請依序完成以下所有步驟，不要跳過：

### Step 0：檢查 progress.md

使用 Glob 搜尋 `**/memory/progress.md` 定位 progress.md。

**如果 progress.md 不存在：**
```
⚠️ 找不到 progress.md。
📁 目前位置：<完整路徑>
沒有需要儲存的專案進度，跳過 /bye。👋
```
**直接結束（輸出 `/exit`）。**

**如果 progress.md 存在 → 繼續 Step 1。**

---

### Step 1：回顧本次對話

回顧整個對話歷史，整理出：
- **完成事項**：本次 session 中完成的所有工作
- **進行中工作**：開始但尚未完成的事項
- **已知問題**：發現但未解決的問題
- **下次建議**：建議下次 session 優先處理的事項

### Step 2：掃描 Git 狀態

執行以下命令取得客觀資訊：
```bash
git status --short
git diff --stat
git log --oneline -5
git log @{u}..HEAD --oneline 2>/dev/null
git remote -v
```

將 git 狀態資訊補充到 Step 1 的整理結果中（例如：有未追蹤的新檔案、有未 commit 的變更等）。

### Step 3：提醒 Smart Commit

如果有未 commit 的變更（dirty files），提醒使用者：
```
💡 偵測到未 commit 的變更，要執行 /smart-commit 嗎？
```

如果使用者同意，執行 `/smart-commit`。
完成後重新執行 `git status --short` 和 `git log @{u}..HEAD --oneline` 更新狀態。

### Step 4：檢查未 Push Commits

如果有未 push 的 commits，提醒使用者：
```
📤 有 N 個 commit 尚未 push，要現在 push 嗎？
```

如果使用者同意，執行 `git push`。

### Step 5：檢查 Git Remote

檢查是否有設定 git remote：
```bash
git remote -v
```

如果沒有任何 remote，詢問使用者：
```
🔗 這個專案還沒有設定 remote。
   要建立一個 GitHub private repo 嗎？（使用 gh repo create）
```

如果使用者同意，執行：
```bash
gh repo create <folder-name> --private --source=. --push
```

### Step 6：寫入 progress.md

將整理好的進度寫入 memory 資料夾中的 `progress.md`（覆寫，只保留最新狀態）。
此時 git 操作（commit/push）已完成，progress.md 會反映最終的 Git 狀態。

> progress.md 的位置在 memory 資料夾中（與其他 memory 檔案相同位置）。
> 使用 Glob 工具搜尋 `**/memory/progress.md` 來定位既有檔案，若不存在則在當前專案的 memory 資料夾中建立。

使用以下格式：

```markdown
## 最後工作：YYYY-MM-DD

### 本次完成
- item ✅

### 進行中
- item 🔄

### 已知問題
- issue description

### 下次建議
- next step

### Git 狀態
- Branch: `branch-name`
- 未 push commits: N
- Remote: origin → url
```

### Step 7：自動執行 /sc 1 完整同步

如果 progress.md 中有 `### Slack Canvas` 區段且包含 `Canvas ID`：
- 執行 `/sc 1` 的完整流程（Canvas 同步 + Channel 摘要 + Dashboard 更新）
- 顯示：`📤 已同步 Canvas、Channel、Dashboard！`

如果沒有 Canvas ID → 跳過此步驟，不提示。

> 注意：此步驟自動執行，不需要使用者確認（收工時減少互動）。

### Step 8：顯示進度摘要

將寫入的內容以格式化方式顯示給使用者確認：
```
📋 本次工作摘要

✅ 完成：
- item 1
- item 2

🔄 進行中：
- item 1

⚠️ 已知問題：
- issue 1

📌 下次建議：
- next step 1

🌿 Git 狀態：
- Branch: branch-name
- 未 push commits: N
```

### Step 9：告別並退出

顯示告別訊息後，使用 `/exit` 退出 Claude Code：
```
👋 收工！進度已儲存。
   下次開工用 /pm 或 /hello 👋
```

然後立即輸出 `/exit` 讓 Claude Code 結束。

> 注意：Step 0 防誤觸結束時也要輸出 `/exit` 退出 Claude Code。

## 注意事項

- 所有輸出使用繁體中文
- progress.md 覆寫而非 append（只保留最新狀態，歷史由 git 管理）
- 如果不在 git repo 中，跳過所有 git 相關步驟
- Step 3-5 需要使用者確認才執行，不要自動執行
- Step 7（/sc 1 完整同步）自動執行，不需確認
- `/bye` 完成後一律自動退出 Claude Code
