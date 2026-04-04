# Dual Engine SOP

Claude Code + opencode 分層委派架構。Claude Code 當決策者產 spec，opencode 當執行者按 spec 實作。

## 安裝

```bash
# Claude Code 端
cp commands/claude-code/opencode-do.md ~/.claude/commands/

# opencode 端
cp commands/opencode/do.md ~/.config/opencode/commands/
```

## 使用流程

```
手動模式：
1. Claude Code:  /opencode-do <任務描述>    → 產 spec 到 .opencode-task.md
2. opencode:     /do                        → 讀取 spec 並執行
3. Claude Code:  /opencode-do review        → 自動審核交付結果

全自動模式：
1. Claude Code:  /opencode-do auto <任務>   → 產 spec + 自動執行 + 自動審核
```

## 子指令

| 指令 | 工具 | 說明 |
|---|---|---|
| `/opencode-do <任務>` | Claude Code | 產出 spec |
| `/opencode-do auto <任務>` | Claude Code | 產 spec + 自動執行 + 自動審核（支援並行，上限 5） |
| `/opencode-do agents` | Claude Code | 列出所有 agent 狀態 |
| `/opencode-do review` | Claude Code | 審核交付結果 |
| `/opencode-do review <id>` | Claude Code | 審核指定 agent |
| `/opencode-do review all` | Claude Code | 批次審核所有已完成 agent |
| `/opencode-do status` | Claude Code | 查看等級與歷史 |
| `/opencode-do set-level <1-3>` | Claude Code | 手動設定等級 |
| `/do` | opencode | 讀取 spec 並執行 |

## 委派等級

| Level | 模式 | 允許操作 |
|---|---|---|
| L1 | 新模組委派 | 只准新增檔案 |
| L2 | 受控修改委派 | 可改指定檔案 + 新增 |
| L3 | 任務級委派 | 只描述目標，自行決定結構 |

## 檔案結構

```
DuelEngineSOP_v0/
├── README.md                       # 本文件
├── dual-engine-sop.md              # SOP 完整規格
├── commands/
│   ├── claude-code/
│   │   └── opencode-do.md          # Claude Code /opencode-do 指令
│   └── opencode/
│       └── do.md                   # opencode /do 指令
```

安裝位置：

| 檔案 | 安裝到 |
|---|---|
| `commands/claude-code/opencode-do.md` | `~/.claude/commands/opencode-do.md` |
| `commands/opencode/do.md` | `~/.config/opencode/commands/do.md` |

## 狀態檔案

| 檔案 | 位置 | 說明 |
|---|---|---|
| `.opencode-task.md` | 專案根目錄 | 當前 spec（opencode 讀取） |
| `.opencode-task-N.md` | 專案根目錄 | 歷史 spec |
| `opencode_level.md` | `~/.claude/projects/*/memory/` | 當前等級 |
| `opencode_history.md` | `~/.claude/projects/*/memory/` | 任務歷史紀錄 |

## 修改後重新安裝

修改 `commands/` 下的檔案後，重新執行安裝指令覆蓋即可：

```bash
cp commands/claude-code/opencode-do.md ~/.claude/commands/
cp commands/opencode/do.md ~/.config/opencode/commands/
```
