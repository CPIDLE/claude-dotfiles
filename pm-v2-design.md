# PM v2 — 統一專案管理入口設計

> 設計日期：2026-03-24
> 靈感來源：gstack 角色分工 + 現有 `/pm`、`/hello`、`/sc`、`/bye` 流程整合
> 原始碼 Repo：https://github.com/CPIDLE/claude-dotfiles
> gstack 參考：https://github.com/garrytan/gstack

---

## 設計目標

將 `/hello`、`/sc`、`/bye` 以及 gstack 啟發的 review/QA/retro 能力，收斂成 **3 個指令**：

| 指令 | 用途 | 取代 |
|---|---|---|
| `/pm` 或 `/pm new` | 開工 | `/hello`、`/hello new` |
| `/pm sync` | 中期同步 + 動作選單 | `/sc`、`/sc 1`、`/sc 2` |
| `/pm bye` | 收工 | `/bye` + `/sc 1` |

原有的 `/hello`、`/sc`、`/bye` **保留但標記為 legacy**，底層邏輯由 `/pm` 統一管理。

---

## 核心原則

1. **預設自動** — 每個階段有 happy path，不選就能走完
2. **需要時才問** — 只在分歧點或風險點才跳選單
3. **狀態感知** — 讀 progress.md、git status、TodoWrite 進度來判斷 context
4. **單一入口** — 忘記指令？打 `/pm` 就對了

---

## `/pm` 或 `/pm new` — 開工

### 自動判斷邏輯

```
使用者輸入 /pm
  │
  ├─ 有 `new` 參數？ → 首次模式（掃描 + 建立 progress.md）
  ├─ 有 progress.md？ → 正常模式（顯示進度 + 問要做什麼）
  └─ 都沒有？       → 提醒使用 /pm new
```

### 步驟

1. **問候 + 環境資訊**
   ```
   👋 嗨！開工囉！
   📅 2026-03-24（一）  ⏰ 14:30
   📁 專案：my-project
   ```

2. **狀態判斷**（同現有 `/hello` 的模式 A / B 邏輯）

3. **正常模式額外步驟** — 快速 context 掃描：
   - 讀取 progress.md 顯示上次進度
   - `git status --short` + 未 push commits
   - 如有 dirty files 或未 push commits → 特別提醒

4. **詢問使用者**
   ```
   要做什麼？
   1. 繼續上次的工作（預設）
   2. 開始新任務
   3. 查看完整進度
   ```

5. **進入 Plan-Execute Workflow**（依 CLAUDE.md 的三階段流程）

6. **更新 Status Line**
   ```bash
   bash ~/.claude/pm-update.sh pm running  # 開始
   bash ~/.claude/pm-update.sh pm done     # 完成
   ```

### 首次模式（`/pm new`）

同現有 `/hello new`：掃描專案 → 建立 progress.md → 詢問目標和技術棧。

---

## `/pm sync` — 中期同步 + 動作選單

### 設計理念

`/pm sync` 不只是同步 Canvas，而是「工作中的萬用選單」。自動偵測目前狀態，提供最相關的動作。

### 自動偵測 + 選單

```
📊 目前狀態
├─ Tasks: 3/7 completed
├─ Git: 2 modified, 1 untracked
├─ 上次同步：30 分鐘前
└─ Canvas: 已連結

你想做什麼？
1. 繼續執行（預設，直接回到工作）
2. 同步進度 → Slack Canvas + Channel
3. Code Review — 審查目前所有改動
4. QA 檢查 — 跑測試 + 安全掃描
5. 調整計畫 — 修改 scope 或重新排序
```

### 各選項行為

#### 選 1：繼續執行
- 不做任何事，回到工作流程
- 如果有 TodoWrite tasks，顯示下一個 pending task

#### 選 2：同步進度（= 現有 `/sc 1` 流程）
- progress.md → Canvas（`slack_update_canvas`）
- 發送/更新摘要到 `#all-cpidle`（防洗版機制）
- 更新 Dashboard Canvas（`F0AMWD1GAD9`）
- 如果 Canvas 尚未連結 → 自動進入連結/建立流程（= 現有 `/sc` 2B 模式）

#### 選 3：Code Review（gstack 啟發）
```
執行審查流程：
1. git diff --staged + git diff（收集所有改動）
2. 以「資深工程師」角色審查：
   - 邏輯正確性
   - 安全性（OWASP top 10）
   - 效能問題
   - 程式碼風格一致性
3. 產出審查報告（直接在終端顯示）
4. 如有問題 → 詢問是否自動修正
```

#### 選 4：QA 檢查（gstack 啟發）
```
執行 QA 流程：
1. 偵測測試框架（jest/vitest/pytest/go test 等）
2. 執行測試套件
3. 如有 lint 設定 → 執行 linter
4. 檢查是否有遺漏的 console.log / debug 程式碼
5. 產出 QA 報告
6. 如有失敗 → 詢問是否自動修正
```

#### 選 5：調整計畫
- 進入 Plan Mode（`EnterPlanMode`）
- 讓使用者重新規劃剩餘工作
- 更新 TodoWrite tasks

### Status Line 更新
```bash
bash ~/.claude/pm-update.sh sync running  # 開始
bash ~/.claude/pm-update.sh sync done     # 完成
```

---

## `/pm bye` — 收工

### 設計理念

收工流程應最大程度自動化，減少互動。依序執行，有問題才停。

### 步驟（自動依序執行）

```
/pm bye
  │
  ├─ Step 1：回顧對話，整理完成/進行中/問題/建議
  │
  ├─ Step 2：Code Review（自動，僅顯示摘要）
  │   └─ 有嚴重問題 → 暫停，詢問是否修正
  │
  ├─ Step 3：QA 快速檢查（自動）
  │   └─ 測試失敗 → 暫停，詢問是否修正
  │
  ├─ Step 4：Git 整理
  │   ├─ 有 dirty files → 詢問是否 smart-commit
  │   ├─ 有未 push commits → 詢問是否 push
  │   └─ 無 remote → 詢問是否建立 GitHub repo
  │
  ├─ Step 5：寫入 progress.md（含 Session ID）
  │
  ├─ Step 6：Slack 同步（自動，不需確認）
  │   ├─ 更新 Canvas
  │   ├─ 發送/更新 #all-cpidle 摘要
  │   └─ 更新 Dashboard
  │
  ├─ Step 7：寫 Retro 到 memory（gstack 啟發）
  │   └─ 如果本次 session 有值得記住的 feedback/pattern → 自動存 memory
  │
  ├─ Step 8：顯示進度摘要
  │
  └─ Step 9：告別 + /exit
```

### 新增：Retro to Memory（Step 7）

收工時自動回顧本次 session，如果發現以下情況就寫入 memory：

| 類型 | 觸發條件 | 範例 |
|---|---|---|
| feedback | 使用者糾正了做法 | 「用戶偏好 X 而非 Y」 |
| project | 學到新的專案背景 | 「API 限制每分鐘 100 次」 |
| user | 發現使用者偏好 | 「偏好簡潔的 commit message」 |

如果本次 session 沒有值得記住的內容，跳過此步驟。

### Status Line 更新
```bash
bash ~/.claude/pm-update.sh bye running  # 開始
bash ~/.claude/pm-update.sh bye done     # 完成
```

---

## 快捷參數完整對照

| 指令 | 行為 | 等同舊指令 |
|---|---|---|
| `/pm` | 開工（自動判斷首次/正常） | `/hello` |
| `/pm new` | 首次開工 | `/hello new` |
| `/pm sync` | 中期選單（同步/review/QA/調整） | `/sc` |
| `/pm sync 2` | 直接同步 Canvas（跳過選單） | `/sc 1` |
| `/pm bye` | 收工全流程 | `/bye` + `/sc 1` |
| `/pm status` | 快速查看進度（唯讀） | — |
| `/pm resume` | 接續上次 session | — |

---

## 檔案結構

```
~/.claude/commands/
├── pm.md          ← v2 主檔（本設計的實作）
├── hello.md       ← legacy，保留但加 deprecation notice
├── sc.md          ← legacy，保留但加 deprecation notice
└── bye.md         ← legacy，保留但加 deprecation notice
```

---

## 與 gstack 的對應

| gstack 指令 | PM v2 對應 | 備註 |
|---|---|---|
| `/autoplan` | `/pm`（內建 Plan-Execute） | 已有三階段 workflow |
| `/review` | `/pm sync` → 選 3 | Code Review |
| `/qa` | `/pm sync` → 選 4 | QA 檢查 |
| `/ship` | `/pm bye` Step 4 | Git commit + push |
| `/retro` | `/pm bye` Step 7 | 自動 retro to memory |
| `/plan-ceo-review` | 不採用 | 個人/小團隊不需要 |
| `/cso` | `/pm sync` → 選 3 涵蓋 | 安全審查整合在 review 中 |
| `/land-and-deploy` | 不採用 | 視專案需求未來再加 |

---

## 實作優先順序

1. **Phase 1**：改寫 `pm.md`，整合 `/hello`、`/sc`、`/bye` 核心邏輯
2. **Phase 2**：加入 Code Review（選 3）和 QA（選 4）到 `/pm sync`
3. **Phase 3**：加入 Retro to Memory 到 `/pm bye`
4. **Phase 4**：標記舊 commands 為 legacy，加 redirect 提示

---

## 不變的部分

- progress.md 格式和位置不變
- Slack Canvas / Dashboard 同步機制不變
- Status Line（pm-update.sh）機制不變
- Plan-Execute Workflow（CLAUDE.md 三階段）不變
- 所有輸出使用繁體中文
