# Claude Dotfiles

Custom commands（`/hello`、`/sc`、`/bye`、`/pm` 等）的原始碼：
- **GitHub**：https://github.com/CPIDLE/claude-dotfiles
- **安裝位置**：`~/.claude/`（由 install script 複製）

## 目錄地圖

| 目錄 / 檔案 | 部署到 | 用途 |
|---|---|---|
| `commands/*.md` | `~/.claude/commands/` | Slash commands（`/pm`、`/do`、`/smart-commit` 等）prompt source |
| `skills/<name>/` | `~/.claude/skills/<name>/` | Skills（含 SKILL.md + scripts/）。**`assets/` 不會被覆蓋**（保護 token / secrets） |
| `hooks/` | `~/.claude/hooks/` | UserPromptSubmit / Stop / 等 hook 腳本 |
| `scripts/` | `~/.claude/scripts/` | 共用 helper |
| `docs/` | `~/.claude/docs/` | 設計文件 |
| `global-claude.md` | `~/.claude/CLAUDE.md` | **全域使用者偏好的 source**。改 deployed 檔會被 install 覆蓋 |
| `settings.json` | `~/.claude/settings.json` | hooks / permissions / env vars |
| `mcp.json` | `~/.claude/mcp.json` | MCP server 設定 |

## 安裝與部署

```bash
# 首次安裝 / 拉取更新後部署
git pull
# Windows
powershell -ExecutionPolicy Bypass -File install.ps1
# macOS / Linux
bash install.sh
```

> **重要**：修改 `commands/`、`CLAUDE.md`、`settings.json` 等原始碼後，**必須重新執行 install script**，否則 `~/.claude/` 下的檔案不會更新，Claude Code 讀取的仍是舊版。
>
> **install 是覆蓋式、不清舊檔**：在 repo 刪掉一個 command/skill 檔，install 不會自動清 `~/.claude/` 下的同名檔 —— 要手動刪。

---

> **User Preferences**（Plan-Execute Workflow、Coding Discipline 等）見全域 `~/.claude/CLAUDE.md`，不在此重複。
