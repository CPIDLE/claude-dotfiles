---
description: 唯讀讀取 Claude Code 的進度狀態
---
讀取 Claude Code 的 progress.md 並顯示專案狀態。**不修改任何檔案。**

## 執行步驟

### Step 1：尋找 progress.md

搜尋 `~/.claude/projects/` 下與目前工作目錄對應的 `memory/progress.md`。

如果找不到，顯示：
```
⚠️ 找不到 Claude Code 的進度紀錄。
```
然後停止。

### Step 2：讀取並顯示

讀取 progress.md，顯示：
```
📋 Claude Code 進度同步（唯讀）
================================
✅ 已完成：<列出>
🔄 進行中：<列出>
⚠️ 已知問題：<列出>
📌 下次建議：<列出>
🌿 Branch：<branch>
🕐 最後更新：<日期>
```

### Step 3：Git 狀態

```bash
git status --short
git log --oneline -5
```

顯示目前 Git 狀態讓使用者了解接手點。

### 重要限制

- **僅讀取，絕不寫入**任何檔案
- **不修改** progress.md、pm-last.txt
- 用繁體中文回覆
