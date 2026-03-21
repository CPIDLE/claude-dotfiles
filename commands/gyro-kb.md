使用者需求：$ARGUMENTS

請使用 gyro-kb skill 處理 PKB v2 知識庫相關工作。

本 skill 會根據輸入自動判斷模式（搜尋 / 客戶關聯 / 工程計算 / 完整報告 / 快速草稿），不需指定子命令。

> **流水線**: `/gyro-kb <客戶需求>` 產 .md 內容 → `/gyro-report <.md> <.html>` 產 HTML/PDF/Excel 排版

## 用法範例

```
/gyro-kb Stocker AMR                    → 搜尋模式（ChromaDB 語義搜尋）
/gyro-kb 錼創                           → 客戶關聯模式（ChromaDB + raw_phase3 歸納）
/gyro-kb --demo                         → 工程計算模式（內嵌 Python）
/gyro-kb 客戶需求.pdf                    → 完整報告模式（基本版 6 階段）
/gyro-kb 報告 深度研究 TSC MCS 軟體整合  → 完整報告模式（深度研究版 A→B→C）
/gyro-kb 草稿 友達面板廠 AGV 搬運        → 快速草稿模式（6 節）
```

## 執行

智慧路由 — 詳細規範請讀取 `~/.claude/skills/gyro-kb.md`。
