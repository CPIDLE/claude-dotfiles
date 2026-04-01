# Claude Dotfiles

Custom commands（`/hello`、`/sc`、`/bye`、`/pm` 等）的原始碼：
- **GitHub**：https://github.com/CPIDLE/claude-dotfiles
- **安裝位置**：`~/.claude/`（由 install script 複製）

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

---

> **User Preferences**（Plan-Execute Workflow、Coding Discipline 等）見全域 `~/.claude/CLAUDE.md`，不在此重複。
