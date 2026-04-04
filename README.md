# Claude Code Dotfiles

Claude Code + opencode 個人設定框架 — 一次安裝，完整配置所有 commands、skills、MCP、plugins。提供 `/pm` 專案管理指令與即時 Status Line，自動化開工→同步→收工的完整工作流程。

## 功能特色

### One-Stop Install

一個 repo 管理所有 Claude Code 和 opencode 的設定：

| 安裝項目 | 目標位置 |
|---|---|
| CLAUDE.md、settings.json | `~/.claude/` |
| 8 個 slash commands | `~/.claude/commands/` |
| 8 個 custom skills | `~/.claude/skills/` |
| MCP server config | `~/.claude/.mcp.json` |
| Status Line 腳本 | `~/.claude/` |
| opencode config + commands | `~/.config/opencode/` |
| Docs | `~/.claude/docs/` |

### Status Line

安裝後 Claude Code 狀態列會顯示即時資訊：

```
claude-dotfiles │ master │ pm▸sync▸bye     Opus 4.6 │ ctx:6% 5h:2%▸03:00 7d:78%▸4/3
```

| 項目 | 範例 | 說明 |
|------|------|------|
| 目錄名稱 | `claude-dotfiles` | 目前工作目錄 |
| Git branch | `master` | 目前分支 |
| 工作流狀態 | `pm▸sync▸bye` | /pm 各階段完成指示器 |
| 模型版本 | `Opus 4.6` | 目前使用的 Claude 模型 |
| Context | `ctx:6%` | Context window 使用率 |
| 5h / 7d 配額 | `5h:2%▸03:00` | 配額使用率 + 重置時間 |

數字顏色依用量自動變化：綠（<50%）→ 黃（50-80%）→ 紅（>80%）。

### 專案管理指令

| 指令 | 說明 |
|------|------|
| `/pm` | 開工 — 自動偵測專案狀態，顯示上次進度 |
| `/pm new` | 首次開工 — 掃描專案，建立 progress.md + README |
| `/pm-sync` | 中期同步 — 儲存進度、自動 commit、同步到外部服務 |
| `/pm-bye` | 收工 — 自動審核 + git 整理 + 進度儲存 |
| `/pm-review` | 獨立程式碼審核（AI 紅隊審核員） |
| `/opencode-do` | 委派任務給 opencode（auto 模式支援 inline spec） |
| `/smart-commit` | 智慧 commit |

### Dual Engine（Claude Code + opencode）

透過 `/opencode-do` 指令，Claude Code 可自動產 spec 並委派給 opencode 執行：

- **快速模式**（`/opencode-do auto`）：pipe inline spec，零檔案 I/O
- **持久模式**（`/opencode-do auto --persist`）：寫檔案，支援並行監控
- 自動審核交付物，結果記錄到 `opencode_history.md`

### 建議工作流程

```
/pm                          # 開工
  ↓
  工作
  ├─ 完成功能 → /smart-commit
  ├─ 簡單任務 → /opencode-do auto <任務>
  ├─ ctx ≈ 60% → /pm-bye → /clear → /pm
  ↓
/pm-bye                      # 收工
```

## 安裝

```bash
git clone https://github.com/CPIDLE/claude-dotfiles.git
cd claude-dotfiles

# Windows
powershell -ExecutionPolicy Bypass -File install.ps1

# macOS / Linux
bash install.sh
```

安裝後需要：
1. 複製 `.env.example` → `~/.claude/.env` 並填入 API keys
2. Plugins 在 Claude Code 首次啟動時自動安裝

## 專案結構

```
├── global-claude.md         # 全域指令（→ ~/.claude/CLAUDE.md）
├── settings.json            # Hooks、plugins、statusline
├── mcp.json                 # MCP server config（→ ~/.claude/.mcp.json）
├── statusline.sh / .js      # Status Line 腳本
├── pm-update.sh             # /pm 狀態更新
├── commands/                # Claude Code slash commands（8 個）
├── commands-opencode/       # opencode slash commands（7 個）
├── skills/                  # Custom skills（8 個）
├── opencode-config/         # opencode 全域設定
│   ├── opencode.json        # Model + MCP + permissions
│   ├── AGENTS.md            # opencode 行為指引
│   └── tui.json             # 主題設定
├── dual-engine/             # Dual Engine SOP + 範例
├── docs/                    # 設定指南
│   ├── google-workspace-setup.md
│   ├── plugins.md
│   ├── mcp-setup.md
│   └── ...
├── install.ps1              # Windows 安裝
└── install.sh               # macOS/Linux 安裝
```

## Google Workspace 整合（選用）

`/pm-sync` 和 `/pm-bye` 可額外同步進度到：

- **Google Chat Space** — 自動發送進度通知（via Webhook）
- **Google Sheet Dashboard** — 自動更新專案總覽表（via Apps Script）

設定步驟：[`docs/google-workspace-setup.md`](docs/google-workspace-setup.md)

## 更新

```bash
cd claude-dotfiles
git pull
powershell -ExecutionPolicy Bypass -File install.ps1  # Windows
bash install.sh                                        # macOS / Linux
```

> **重要**：修改原始碼後必須重新執行安裝腳本。

## 注意事項

- 安裝時已存在的同名檔案會備份為 `.bak`
- Marketplace plugins 在 `settings.json` 中設定，首次啟動自動安裝（見 [docs/plugins.md](docs/plugins.md)）
- Status line 的配額資訊需要 Anthropic OAuth token（首次使用時自動取得）
- opencode 相關設定在 opencode CLI 未安裝時自動跳過
