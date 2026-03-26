# PM v2 — 統一專案管理入口設計

> 設計日期：2026-03-24（最後更新：2026-03-26）
> 原始碼 Repo：https://github.com/CPIDLE/claude-dotfiles
> 靈感來源：gstack 角色分工 + 現有 `/hello`、`/sc`、`/bye` 流程整合

---

## 設計目標

將 `/hello`、`/sc`、`/bye` 以及 gstack 啟發的 review/QA/retro 能力，收斂成統一入口 `/pm`。

| 指令 | 用途 | 取代 |
|---|---|---|
| `/pm` 或 `/pm new` | 開工 | `/hello` |
| `/pm sync` | 中期同步 + 動作選單 | `/sc` |
| `/pm bye` | 收工 | `/bye` + `/sc` |
| `/pm review` | 獨立審核（easy/deep） | — |
| `/pm status` | 快速查看進度（唯讀） | — |
| `/pm resume` | 顯示接續指令 | — |

原有的 `/hello`、`/sc`、`/bye` 保留但標記為 legacy。

---

## 核心原則

1. **預設自動** — 每個階段有 happy path，不選就能走完
2. **需要時才問** — 只在分歧點或風險點才跳選單
3. **狀態感知** — 讀 progress.md、git status、TodoWrite 進度來判斷 context
4. **單一入口** — 忘記指令？打 `/pm` 就對了

---

## 架構概覽

```
/pm ──────→ 開工（判斷首次/正常模式）
/pm sync ──→ 選單：同步 | 審核 | 調整計畫
/pm bye ───→ 自動：回顧 → easy 審核 → smart-commit → push? → sync → retro → 告別
/pm review → easy（主 agent）或 deep（獨立 subagent 紅隊）
```

### 關鍵資料流

```
progress.md ←→ Slack Canvas（雙向同步）
                ↓
            #all-cpidle（Channel 摘要，防洗版）
                ↓
            Dashboard Canvas（F0AMWD1GAD9，各專案區段）
```

---

## 審核系統（easy/deep 兩層）

原本 Code Review、QA、紅隊審核是三個獨立功能，已合併為兩層：

| 深度 | 觸發方式 | 執行者 | 內容 | 產出 |
|---|---|---|---|---|
| **easy** | sync 選 2、bye 自動、`/pm review easy` | 主 agent | 測試 + lint + debug 掃描 + 快速 code review | 螢幕一行摘要 |
| **deep** | `/pm review`（預設） | 獨立 subagent | easy 全部 + 紅隊 AI 交叉驗證（程式碼+文件） | `reviews/YYYY-MM-DD-HH-MM.md` |

### Deep 模式紅隊 Prompt 設計原則

- 預設否定，找出問題
- 交叉驗證：每個宣稱回原始碼核對
- 內部一致性：文件各段是否矛盾
- 可行性驗證：建議照做會不會壞
- 遺漏偵測：沒寫的比寫了的更危險
- 審查對象包含**程式碼和文件**（如 pm.md 本身）

---

## Status Line 系統

### 顯示格式
```
[Opus 4.6 (1M context)] 專案名 | pm▸sync▸bye | master | ctx:N%
```

### 顏色狀態
| 狀態 | ANSI | 顏色 |
|---|---|---|
| `pending` | `\x1b[90m` | 暗灰 |
| `running` | `\x1b[93m` | 亮黃 |
| `done` | `\x1b[97m` | 亮白 |

### 檔案架構
| 檔案 | 用途 |
|---|---|
| `pm-update.sh` | 寫入 `pm-last.txt`（key:state 格式） |
| `statusline.js` | 讀取 `pm-last.txt` + context JSON，輸出 ANSI status line |
| `statusline.sh` | 呼叫 statusline.js + 注入 git branch |

### 自動化機制
| 機制 | 觸發 |
|---|---|
| `SessionStart` hook | 新 session 啟動 → `pm-update.sh reset`（全部回暗灰） |
| pm.md Step 0 | 各子命令開始 → `pm-update.sh <key> running` |
| pm.md 結束步驟 | 各子命令結束 → `pm-update.sh <key> done` |

### 已知限制
- Status line 只有 3 格（pm/sync/bye），review 不獨立顯示
- pm.md 的 Step 0 bash code block 不保證 agent 會執行（已觀察到跳過的情況）
- `pm-update.sh` 的 sed 替換只能更新已存在的 key

---

## `/pm sync` 同步流程

### 選單（3 項）
```
1. 同步進度 → Slack Canvas + Channel（預設）
2. 審核 — easy 模式
3. 調整計畫
```

### 同步進度流程
```
Step 0: 自動 smart-commit（有 dirty files → 靜默 commit，不問不 push）
Step A: 檢查 progress.md 存在
Step B: Canvas 同步（已連結 → replace | 未連結 → 建立/連結/跳過）
Step C: Channel 通知（防洗版：今日已發 → 跳過）
Step D: Dashboard 更新（replace 不含 header / append 含 header）
```

### Dashboard 更新規則（關鍵防 bug）
- `replace` + `section_id`：內容**不含** `##` header（header 是 section 本身，含則重複）
- `append`：內容**含** `##` header（新增完整區段）
- Canvas emoji 使用 Slack 語法（`:small_blue_diamond:` 非 `🔹`）

---

## `/pm bye` 收工流程

```
Step 0: Status Line → bye running
Step 1: 回顧對話 → 整理完成/進行中/問題/建議
Step 2: Easy 審核（自動，僅摘要，測試失敗才暫停）
Step 3: Git 整理 → 自動 smart-commit + 問 push
Step 4: 寫入 progress.md（含 Session ID）
Step 5: Slack 同步（Canvas + Channel + Dashboard）
Step 6: Retro to Memory（自動，有值得記的才寫）
Step 7: 顯示摘要
Step 8: 告別 + /exit
```

### Smart-commit 行為統一
- sync 和 bye 都是**靜默 commit**（不問使用者）
- push 只在 bye 時詢問

---

## 與 gstack 的對應

| gstack | PM v2 | 備註 |
|---|---|---|
| `/autoplan` | `/pm`（內建 Plan-Execute） | 已有三階段 workflow |
| `/review` | `/pm review easy` 或 deep | easy = 快速，deep = 紅隊 subagent |
| `/qa` | 整合在 review easy 中 | 測試 + lint + debug 掃描 |
| `/ship` | `/pm bye` Step 3 | Git commit + push |
| `/retro` | `/pm bye` Step 6 | 自動 retro to memory |
| `/cso` | `/pm review deep` 涵蓋 | 安全審查整合在紅隊審查中 |

---

## 檔案結構

```
~/.claude/
├── commands/
│   ├── pm.md          ← v2 主指令（~640 行）
│   ├── hello.md       ← legacy（已 deprecated）
│   ├── sc.md          ← legacy（已 deprecated）
│   └── bye.md         ← legacy（已 deprecated）
├── statusline.js      ← status line 渲染
├── statusline.sh      ← status line 入口
├── pm-update.sh       ← status line 狀態更新
├── pm-last.txt        ← status line 狀態檔（runtime）
└── settings.json      ← hooks（SessionStart reset、Stop beep、PreToolUse beep）

GitHub Repo: CPIDLE/claude-dotfiles
├── commands/pm.md     ← 主指令源碼
├── reviews/           ← deep 審核報告
├── pm-v2-design.md    ← 本文件
├── install.ps1        ← Windows 安裝腳本
└── install.sh         ← Linux/Mac 安裝腳本
```

---

## 開發歷程

| 日期 | 階段 | 內容 |
|---|---|---|
| 2026-03-24 | Phase 1 | 核心功能：開工/sync/bye 整合 |
| 2026-03-24 | Phase 2 | Code Review + QA + 紅隊審核加入 sync |
| 2026-03-24 | Phase 3 | Retro to Memory 加入 bye |
| 2026-03-24 | Phase 4 | Legacy commands 標記 deprecated |
| 2026-03-26 | Phase 5 | Code Review + QA + 紅隊合併為 easy/deep 兩層 |
| 2026-03-26 | Phase 6 | 紅隊審核報告：修正 F-007/F-008/F-009 |
| 2026-03-26 | Phase 7 | Status line 修正（SessionStart hook、顏色、Stop hook rm 移除） |
| 2026-03-26 | Phase 8 | PM_v2 repo 合併回 claude-dotfiles，PM_v2 archived |
| 2026-03-26 | Phase 9 | progress.md Glob 路徑修正 |

---

## 已知限制與待辦

- Status line Step 0 的 bash code block 不保證 agent 執行（blockquote 和 Step 0 都試過，agent 可能跳過）
- `/pm resume` 無法在 session 內執行 `claude --resume`，只能顯示指令
- Session ID 撈取依賴 `~/.claude/sessions/` 的內部結構，無官方 API 保證
- Deep review 的 subagent 尚未大量測試
