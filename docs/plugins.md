# Claude Code Plugins

`settings.json` 中 `enabledPlugins` 已設定的 plugin 會在 Claude Code 首次啟動時自動安裝。

## 已啟用（自動安裝）

| Plugin | 說明 |
|---|---|
| `skill-creator` | 建立/修改自訂 skill |
| `code-simplifier` | 程式碼品質與重構建議 |
| `context7` | 即時查詢套件/框架文件 |
| `coderabbit` | AI 程式碼審查 |
| `claude-md-management` | CLAUDE.md 審計與改善 |
| `playwright` | 瀏覽器自動化 |

## 可選（手動安裝）

以下 plugin 未放入 `settings.json`，如需使用請手動啟用：

| Plugin | 說明 | 啟用方式 |
|---|---|---|
| `frontend-design` | UI 設計輔助 | 在 Claude Code 中 `/plugins` 搜尋安裝 |
| `code-review` | 程式碼審查 | 同上 |
| `playground` | 實驗性功能 | 同上 |
| `qodo-skills` | 程式碼品質分析 | 同上 |

> 所有 plugin 來源：`claude-plugins-official`，安裝後存放於 `~/.claude/plugins/cache/`。
