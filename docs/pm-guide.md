# `/pm` — 專案管理統一入口

整合開工、同步、收工、Code Review、QA 檢查及 Memory 歸檔的完整工作流。

---

## 子指令一覽

| 指令 | 用途 |
|---|---|
| `/pm` | 開始工作（自動偵測首次 or 一般模式） |
| `/pm new` | 首次設定（掃描專案 + 建立 `progress.md`） |
| `/pm sync` | 中途同步選單（同步 / Review / 調整計畫） |
| `/pm sync 2` | 直接同步 Canvas（跳過選單） |
| `/pm bye` | 完整收工流程（Review → Git → Sync → Retro） |
| `/pm review` | 獨立 Code Review（預設 deep 模式） |
| `/pm review easy` | 快速 Review（主 agent 直接執行） |
| `/pm status` | 快速檢視進度（唯讀） |
| `/pm resume` | 恢復上次 session |

---

## 1. `/pm` / `/pm new` — 開工

**流程：**

1. 顯示問候（日期、專案資料夾、時間）
2. 偵測專案類型（`.git`、`package.json`、`Cargo.toml` 等）
3. 根據模式執行：

| 條件 | 模式 | 行為 |
|---|---|---|
| 有 `new` 參數 | 首次模式 | 掃描 git log / 專案結構 → 建立 `progress.md` |
| 有專案標記 + `progress.md` | 一般模式 | 讀取進度 → 顯示摘要 + git 狀態 → 詢問下一步 |
| 有專案標記 + 無 `progress.md` | — | 提示先執行 `/pm new` |
| 無專案標記 | — | 顯示警告並結束 |

**首次模式額外動作：**
- 掃描 git log、branches、remotes
- 使用 Glob 掃描專案結構
- 空目錄時詢問目標、技術棧、參考資料

**一般模式顯示：**
- 進度摘要（已完成、進行中、已知問題、下一步）
- Git 狀態（modified files、commits、unpushed commits）
- Resume 選項（若有 Session ID）
- 進入 Plan-Execute Workflow

---

## 2. `/pm status` — 快速檢視

唯讀操作，不更新 status line。

**顯示內容：**
- 已完成項目
- 進行中項目
- 下一步建議
- Branch 名稱
- Canvas 狀態
- 上次同步時間

---

## 3. `/pm resume` — 恢復 Session

- 從 `progress.md` 的 `### Session` 區段讀取 Session ID
- 找到 → 執行 `claude --resume <sessionId>`
- 找不到 → 提示改用 `/pm` 正常開工

---

## 4. `/pm sync` — 中途同步

### 選單選項

| # | 選項 | 說明 |
|---|---|---|
| 1 | **Sync Progress**（預設） | 同步到 Slack Canvas + Channel + Dashboard |
| 2 | **Review** | 執行 easy review |
| 3 | **Adjust Plan** | 進入 Plan Mode 重新規劃 |

> 使用 `/pm sync 2` 可直接跳到 Canvas 同步，略過選單。

### 同步流程

| 步驟 | 動作 |
|---|---|
| Step 0 | 若有 dirty files → 自動 smart-commit |
| Step A | 確認 `progress.md` 存在 |
| Step B | 更新 Slack Canvas（progress.md → Canvas markdown） |
| Step C | 發摘要到 `#all-cpidle`（含防重複機制） |
| Step D | 更新 Dashboard Canvas（`F0AMWD1GAD9`） |

**Canvas 狀態處理：**
- 已連結 → 讀取 Canvas → 轉換 → 更新 → 記錄同步時間
- 未連結 → 提議建立新 Canvas 或連結現有 Canvas

**Dashboard 更新規則：**
- 以 `:small_blue_diamond:` 作為專案區段標題
- 有 section_id → 用 `replace`（避免標題重複）
- 無 section_id → 用 `append`（含標題）

---

## 5. `/pm review` — Code Review

### 兩種模式

| 模式 | 觸發方式 | 執行方式 |
|---|---|---|
| **Easy** | `/pm review easy`、`/pm sync` 選項 2、`/pm bye` 自動 | 主 agent 直接執行 |
| **Deep** | `/pm review`（預設） | 啟動獨立 subagent，紅隊思維 |

### Easy Review

自動偵測並執行：
- **Tests**：jest / vitest / pytest / go test / cargo test
- **Lint**：eslint / biome / ruff
- **Debug code 掃描**：`console.log`、`debugger`、`print(`、`fmt.Println`
- **Quick code review**：git diff 檢查明顯 bug / 安全問題

**輸出格式（一行摘要）：**
```
🔍 Review: Tests ✅ | Lint ✅ | Debug ✅ | Code ✅ 0 issues
```

僅在測試失敗時暫停。

### Deep Review

**Subagent 執行內容：**
- 收集 git diffs、file lists
- 交叉驗證、一致性檢查、可行性驗證、缺口偵測

**嚴重度分類：**
- 🔴 **MUST FIX** — 必須修復
- 🟠 **SHOULD FIX** — 建議修復
- 🟡 **NICE TO FIX** — 可改善

**報告輸出：** `reviews/YYYY-MM-DD-HH-MM.md`

**報告內容：**
- Metadata + 最終判定（REJECT / REVISE / PASS）
- 自動檢查結果
- 統計表
- 發現清單（按嚴重度分組）
- 未覆蓋風險
- 評分（各維度 1-5 分 + 加權總分）

僅在 REJECT 時暫停。

---

## 6. `/pm bye` — 完整收工

| 步驟 | 動作 | 說明 |
|---|---|---|
| ① | **Review 對話** | 掃描整個對話歷史 → 提取完成 / 進行中 / 問題 / 下一步 |
| ② | **Easy Review** | 若有 git 變更 → 自動執行，僅測試失敗時暫停 |
| ③ | **Git 整理** | dirty files → smart-commit；unpushed → 提議 push；無 remote → 提議建 GitHub private repo |
| ④ | **寫 progress.md** | 含 Session ID + review 結果 + git 狀態 |
| ⑤ | **Slack 同步** | Canvas + Channel + Dashboard（自動，不需確認） |
| ⑥ | **Retro → Memory** | 若有學習紀錄（feedback / project / user）→ 寫入 memory file |
| ⑦ | **顯示工作摘要** | 完成項目、進行中、問題、下一步、git info、review 結果 |
| ⑧ | **說再見** | 顯示 resume 指令 → 輸出 `/exit` 結束 session |

---

## Status Line 整合

透過 `~/.claude/pm-update.sh` 更新 `~/.claude/pm-last.txt`。

| 事件 | 指令 |
|---|---|
| `/pm` 開始 | `bash ~/.claude/pm-update.sh pm running` |
| `/pm` 完成 | `bash ~/.claude/pm-update.sh pm done` |
| `/pm sync` 開始 | `bash ~/.claude/pm-update.sh sync running` |
| `/pm sync` 完成 | `bash ~/.claude/pm-update.sh sync done` |
| `/pm bye` 開始 | `bash ~/.claude/pm-update.sh bye running` |
| `/pm bye` 完成 | `bash ~/.claude/pm-update.sh bye done` |

> `/pm status` 和 `/pm resume` 不更新 status file。

---

## `progress.md` 標準格式

```markdown
## 最後工作：YYYY-MM-DD

### 本次完成
- item ✅

### 進行中
- item 🔄

### 已知問題
- issue description

### 下次建議
- next step

### Git 狀態
- Branch: `branch-name`
- 未 push commits: N
- Remote: origin → url

### Session
- Resume: `claude --resume <sessionId>`

### Slack Canvas
- Canvas ID: F08XXXXXXXX
- Canvas URL: https://xxx.slack.com/canvas/...
- 最後同步：YYYY-MM-DD HH:MM
```

---

## 關鍵 ID

| 項目 | ID |
|---|---|
| Slack Channel `#all-cpidle` | `C0AN35HJQ8L` |
| Dashboard Canvas | `F0AMWD1GAD9` |

---

## Canvas Emoji 語法

- Dashboard 標題使用 `:small_blue_diamond:`（非 `🔹`）
- 狀態 emoji：`:white_check_mark:`、`:arrows_counterclockwise:`、`:pushpin:`、`:link:`

---

## 取代的 Legacy 指令

| Legacy 指令 | 替代為 | 差異 |
|---|---|---|
| `/hello` | `/pm` 或 `/pm new` | 功能相同，更多選項 |
| `/sc` | `/pm sync` | 額外含 Review、調整計畫選項 |
| `/bye` | `/pm bye` | 額外含自動 Code Review、QA 檢查、Retro |
