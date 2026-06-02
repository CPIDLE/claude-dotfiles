# Claude Code Plugins

`settings.json` 的 `enabledPlugins` 是一份 **allowlist**：值為 `true` 才會在 Claude Code 首次啟動時自動安裝並啟用；值為 `false` 代表已知這個 plugin 但刻意停用（同時抗拒被自動 re-install 復活）。

## 已啟用（`true`）

| Plugin | 說明 |
|---|---|
| `context7` | 即時查詢套件/框架文件 |
| `coderabbit` | AI 程式碼審查 |
| `playwright` | 瀏覽器自動化 |
| `pyright-lsp` | Python 型別檢查 LSP（改 .py 自動回報錯誤/警告） |
| `hookify` | 用 markdown rule 建 hook 硬擋不該做的事（regex 比對 tool call） |

## 已停用（`false`）

為精簡 context 成本而關閉（低頻或未使用）。需要時把 `settings.json` 對應值改成 `true` 再重跑 install。

| Plugin | 說明 | 停用原因 |
|---|---|---|
| `skill-creator` | 建立/修改自訂 skill | 低頻，需要時才開 |
| `code-simplifier` | 程式碼品質與重構建議 | 與 `/code-review`、`coderabbit` 功能重疊 |
| `claude-md-management` | CLAUDE.md 審計與改善 | 低頻 |
| `frontend-design` | UI 設計輔助 | 未使用 |
| `code-review` | 程式碼審查 | 已有內建 `/code-review` |
| `playground` | 實驗性功能 | 未使用 |
| `qodo-skills` | 程式碼品質分析 | 未使用 |

> 所有 plugin 來源：`claude-plugins-official`，安裝後存放於 `~/.claude/plugins/cache/`。
> `enabledPlugins` 是 allowlist —— installed ≠ enabled；把值釘成 `false` 可避免它被自動安裝流程復活。
