# Claude Code Dotfiles

Claude Code 個人設定框架 — 提供 `/pm` 專案管理指令與即時 Status Line，自動化開工→同步→收工的完整工作流程。

## 功能特色

### Status Line

安裝後 Claude Code 狀態列會顯示即時資訊：

```
claude-dotfiles │ master │ pm▸sync▸bye     Opus 4.6 │ ctx:6% 5h:2%▸03:00 7d:78%▸4/3
```

逐項說明：

| 項目 | 範例 | 說明 |
|------|------|------|
| 目錄名稱 | `claude-dotfiles` | 目前工作目錄 |
| Git branch | `master` | 目前分支 |
| 工作流狀態 | `pm▸sync▸bye` | /pm 各階段完成指示器（pm=開工、sync=同步、bye=收工） |
| 模型版本 | `Opus 4.6` | 目前使用的 Claude 模型 |
| Context | `ctx:6%` | Context window 使用率 |
| 5h 配額 | `5h:2%▸03:00` | 5 小時滾動配額使用率 + 重置時間 |
| 7d 配額 | `7d:78%▸4/3` | 7 天滾動配額使用率 + 重置日期 |

數字顏色依用量自動變化：綠（<50%，安全）→ 黃（50-80%，注意）→ 紅（>80%，警告）。

### /pm 專案管理指令

| 指令 | 說明 |
|------|------|
| `/pm` | 開工 — 自動偵測專案狀態，顯示上次進度，進入工作模式 |
| `/pm new` | 首次開工 — 掃描專案結構，建立 progress.md + README |
| `/pm sync` | 中期同步 — 儲存進度、自動 commit、同步到外部服務 |
| `/pm bye` | 收工 — 自動審核（測試+lint+code review）+ git 整理 + 進度儲存 |
| `/pm status` | 快速查看目前進度（唯讀） |
| `/pm resume` | 接續上次 session |
| `/pm review` | 獨立程式碼審核（啟動 AI 紅隊審核員） |

## 安裝

```bash
git clone https://github.com/CPIDLE/claude-dotfiles.git
cd claude-dotfiles

# Windows
powershell -ExecutionPolicy Bypass -File install.ps1

# macOS / Linux
bash install.sh
```

安裝腳本會將 commands、settings、statusline 等檔案複製到 `~/.claude/`。

## 專案結構

```
├── CLAUDE.md            # 全域指令（Plan-Execute workflow、通知 hooks）
├── settings.json        # Hooks、plugins、permissions
├── statusline.sh        # Status line 主腳本
├── statusline.js        # Status line quota 查詢
├── pm-update.sh         # /pm 狀態更新腳本
├── commands/            # Slash commands（pm.md、hello.md、bye.md、sc.md）
├── docs/                # 設定指南
│   └── google-workspace-setup.md
├── install.ps1          # Windows 安裝腳本
└── install.sh           # macOS/Linux 安裝腳本
```

## Google Workspace 整合（選用）

`/pm sync` 和 `/pm bye` 可額外同步進度到：

- **Google Chat Space** — 自動發送進度通知到指定頻道（via Webhook）
- **Google Sheet Dashboard** — 自動更新專案總覽表（via Apps Script）

此功能為選用，不設定不影響其他功能。設定步驟請參考 [`docs/google-workspace-setup.md`](docs/google-workspace-setup.md)。

## 更新

```bash
cd claude-dotfiles
git pull

# 重新執行安裝腳本
powershell -ExecutionPolicy Bypass -File install.ps1  # Windows
bash install.sh                                        # macOS / Linux
```

> **重要**：修改原始碼後必須重新執行安裝腳本，否則 `~/.claude/` 下的檔案不會更新。

## 注意事項

- Marketplace plugins 和 MCP connectors 不受影響，安裝腳本不會動到它們
- 安裝時已存在的同名檔案會備份為 `.bak`
- Status line 的配額資訊需要 Anthropic OAuth token（首次使用時自動取得）
