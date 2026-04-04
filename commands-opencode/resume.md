---
description: 接續上次的工作（等同 Claude Code 的 /resume）
---

## 接續上次工作

先顯示提示：
```
💡 如需切換到舊 session，請按 /sessions
```

然後自動銜接上次進度：

1. 讀取 `.opencode/session-notes.md`（如果存在），顯示上次工作摘要
2. 執行 `git log --oneline -5` 顯示最近變更
3. 執行 `git diff --stat` 顯示未 commit 的改動
4. 顯示摘要：

```
📋 上次工作狀態
================
✅ 已完成：<從 session-notes 讀取>
🔄 進行中：<從 session-notes 讀取>
📌 下一步：<從 session-notes 讀取>

🌿 Git：<最近 commit 摘要>
📝 未 commit：<modified/untracked 檔案數>
```

5. 詢問：「要繼續上次的工作，還是開始新任務？」

## 限制
- 用繁體中文回覆
- 不修改任何檔案
