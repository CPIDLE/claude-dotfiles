---
description: 分析 git staged 變更，自動整理文件並 commit
---
分析目前的 git staged 變更，自動整理專案文件，然後執行 commit。

## 執行步驟

請依序完成以下所有步驟，不要跳過：

### Step 1：分析變更內容
```bash
git diff --staged
git diff --staged --stat
```
仔細閱讀所有變更，理解：
- 新增了什麼功能
- 修改了什麼邏輯
- 刪除了什麼
- 影響哪些模組

### Step 2：更新 CHANGELOG.md
在 `CHANGELOG.md` 最上方新增一筆記錄（如果檔案不存在則建立）：

```markdown
## [YYYY-MM-DD HH:MM] — 簡短標題

### 變更內容
- 具體說明改了什麼（條列式）

### 影響範圍
- 哪些功能或模組受到影響
```

### Step 3：更新 README.md
檢查 README.md 是否需要更新：
- 如果新增了新功能 → 更新「功能說明」章節
- 如果改了安裝方式 → 更新「安裝步驟」
- 更新「最後更新」日期
- 如果 README 不存在則建立基本版本

### Step 4：產生 Commit Message
使用 Conventional Commits 格式：

```
<type>(<scope>): <簡短描述（中文可）>

<詳細說明（選填）>

Tool: OpenCode (Ollama local)
```

type 對照：
- feat     → 新增功能
- fix      → 修復 bug
- docs     → 只改文件
- refactor → 重構，不影響功能
- chore    → 雜務（依賴更新等）
- test     → 新增或修改測試

**重要**：commit message 結尾必須加上 `Tool: OpenCode (Ollama local)` trailer。

### Step 5：確認並執行
列出即將 commit 的內容摘要，詢問使用者確認：

```
📋 Smart Commit 摘要
====================
變更檔案：X 個
建議訊息：feat(xxx): ...

更新文件：
  ✅ CHANGELOG.md — 新增記錄
  ✅ README.md — 更新功能說明

確認執行 commit？(Y/n)
```

收到確認後執行：
```bash
git add CHANGELOG.md README.md
git commit -m "<產生的 commit message>"
```

### Step 6：完成回報
```
✅ Commit 完成！
   ID: <commit hash>
   訊息: <commit message>

💡 提示：執行 git push 將變更上傳到 GitHub
```
