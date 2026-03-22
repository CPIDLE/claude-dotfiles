# PM — 專案管理主控

專案管理流程的統一入口，串接 `/hello`、`/sc`、`/bye` 三個 command。

## 快捷參數

| 指令 | 效果 |
|---|---|
| `/pm` | 開工（= `/hello` 流程） |
| `/pm new` | 首次開工（= `/hello new` 流程） |
| `/pm sync` | 同步進度（= `/sc 1` 完整流程） |
| `/pm status` | 快速查看進度（不同步、不互動） |
| `/pm bye` | 收工（= git 整理 + `/sc 1` + `/bye` 流程） |

## 執行步驟

根據參數決定執行哪個流程：

---

### `/pm`（無參數）— 開工

執行 `/hello` 的完整流程（模式 A 或模式 B，依 progress.md 狀態自動判斷）。

等同於直接執行 `/hello`。

---

### `/pm new` — 首次開工

執行 `/hello new` 的完整流程（首次模式，掃描專案並建立 progress.md）。

等同於直接執行 `/hello new`。

---

### `/pm sync` — 同步進度

執行 `/sc 1` 的完整流程：
1. 同步 progress.md → Canvas
2. 發送摘要到 `#all-cpidle`
3. 更新 Dashboard Canvas

等同於直接執行 `/sc 1`。

---

### `/pm status` — 快速查看進度

不做任何同步或互動，只顯示目前狀態：

1. 使用 Glob 搜尋 `**/memory/progress.md`
2. 如果不存在：
   ```
   ⚠️ 尚未建立進度追蹤。使用 /pm new 初始化。
   ```
3. 如果存在，讀取並顯示：
   ```
   📋 <專案名稱> — 進度狀態

   ✅ 已完成：
   - item 1

   🔄 進行中：
   - item 1

   📌 下次建議：
   - next step

   🌿 Branch: <branch-name>
   🔗 Canvas: <Canvas URL 或「未連結」>
   🕐 上次同步：<時間 或「—」>
   ```

---

### `/pm bye` — 收工

執行完整收工流程，串接多個 command：

1. **回顧與整理**：執行 `/bye` 的 Step 1（回顧對話）
2. **Git 整理**：執行 `/bye` 的 Step 2-5（git status → smart-commit → push → remote）
3. **寫入 progress.md**：執行 `/bye` 的 Step 6
4. **完整同步**：執行 `/sc 1` 完整流程（Canvas + Channel + Dashboard）
5. **顯示摘要**：執行 `/bye` 的 Step 8
6. **告別退出**：執行 `/bye` 的 Step 9（顯示告別訊息 + `/exit`）

等同於依序執行 `/bye` 但確保 Step 7 走完整的 `/sc 1` 流程。

---

## Status Line 整合（必要）

每個 `/pm` 子命令在 **開始前** 和 **完成後** 必須更新 `~/.claude/pm-last.txt`，用於 CLI status line 顯示進度。

### 檔案格式

```
YYYY-MM-DD\tpm:<state>,sync:<state>,bye:<state>
```

`<state>` 為 `pending`、`running`、`done` 之一。

### 更新規則

使用 Bash 執行以下邏輯（用一行指令）：

**開始時**：將對應的 key 設為 `running`，保留其他 key 的狀態。
**完成時**：將對應的 key 設為 `done`。

具體操作：

1. 讀取 `~/.claude/pm-last.txt`，如果日期不是今天或檔案不存在，初始化為 `pm:pending,sync:pending,bye:pending`
2. 用 `sed` 替換對應 key 的 state
3. 寫回檔案

**快速參考**（每個子命令要執行的 Bash）：

| 時機 | 指令 |
|---|---|
| `/pm` 或 `/pm new` 開始 | `bash ~/.claude/pm-update.sh pm running` |
| `/pm` 或 `/pm new` 完成 | `bash ~/.claude/pm-update.sh pm done` |
| `/pm sync` 開始 | `bash ~/.claude/pm-update.sh sync running` |
| `/pm sync` 完成 | `bash ~/.claude/pm-update.sh sync done` |
| `/pm bye` 開始 | `bash ~/.claude/pm-update.sh bye running` |
| `/pm bye` 完成 | `bash ~/.claude/pm-update.sh bye done` |

**`/pm status` 不更新狀態檔。**

---

## 注意事項

- 所有輸出使用繁體中文
- `/pm` 是 `/hello`、`/sc`、`/bye` 的快捷封裝，底層邏輯完全相同
- 各子 command 仍可獨立使用，`/pm` 不會取代它們
- `/pm status` 是唯一不需要互動的子命令，適合快速確認狀態
