# PM — 開工

每次開始新的工作 session 時使用，自動判斷專案狀態並提供對應引導。

> **子指令已拆分**：`/pm-sync`（同步）、`/pm-bye`（收工）、`/pm-review`（審核）。

## 快捷參數

| 指令 | 行為 |
|---|---|
| `/pm` | 開工（自動判斷首次/正常模式） |
| `/pm new` | 首次開工（掃描專案 + 建立 progress.md + README.md） |
| `/pm status` | 快速查看進度（唯讀） |
| `/pm resume` | 接續上次 session |

## Status Line

```bash
bash ~/.claude/pm-update.sh reset && bash ~/.claude/pm-update.sh pm running
```

**結束前**也必須執行：`bash ~/.claude/pm-update.sh pm done`

**`/pm status` 和 `/pm resume` 不更新狀態檔。**

---

## `/pm` 或 `/pm new` — 開工

### Step 1：問候與環境資訊

```
👋 嗨！開工囉！
📅 日期：YYYY-MM-DD（星期X）
📁 專案：<資料夾名稱>
⏰ 時間：HH:MM
```

### Step 2：判斷模式

**專案指標檔案**（任一存在即視為有效專案）：
`.git`、`package.json`、`Cargo.toml`、`pyproject.toml`、`go.mod`、`pom.xml`、`build.gradle`、`Makefile`、`CMakeLists.txt`、`*.sln`、`*.csproj`、`composer.json`、`Gemfile`、`pubspec.yaml`、`CLAUDE.md`

**判斷邏輯（依序）：**
1. 使用者指定 `new` 參數 → **首次模式**
2. 有專案指標 + 有 `progress.md` → **正常模式**
3. 有專案指標 + 無 `progress.md` → 顯示提醒並結束：
   ```
   📁 偵測到專案：<資料夾名稱>
   📝 尚未建立進度追蹤（無 progress.md）。請使用：/pm new
   ```
4. 以上皆不符合 → 顯示警告並結束：
   ```
   ⚠️ 目前目錄不像是一個專案。請使用：/pm new
   ```

> progress.md 位置：Glob 搜尋 `~/.claude/projects/**/memory/progress.md`。

---

### 首次模式（`new` 參數）

支援參數：`/pm new --lang=en`（指定 README 語言為英文，預設繁體中文）。

1. 告知使用者將進行首次專案掃描
2. 使用 **Explore agent**（thoroughness: `very thorough`）掃描專案
3. 整理首次進度摘要（專案概述、目前 branch、建議下一步）
4. 產生文件：
   - 寫入 `progress.md`（memory 資料夾中）
   - 產生 `README.md`（專案根目錄，已存在則跳過）
5. 顯示摘要讓使用者確認
6. 全新空目錄 → 額外詢問目標、技術棧 → 補寫

#### README.md 固定範本

```markdown
# <專案名稱>

<一段話專案簡述>

## 功能特色
## 技術棧
## 開始使用
### 前置需求
### 安裝
### 使用方式
## 專案結構
## 授權條款（偵測到 LICENSE 時）
```

> AI 可依掃描結果省略不適用區段。使用者可自行擴充，後續維護時保留。

---

### 正常模式（有 progress.md）

1. 讀取 `progress.md`
2. 如果有 Session 區段含 Resume 指令 → 顯示 `💡 上次 session 可續：claude --resume <sessionId>`
3. 顯示進度摘要（✅ 已完成、🔄 進行中、⚠️ 已知問題、📌 下次建議）
4. 顯示 Git 狀態摘要（`git status --short`、`git log --oneline -5`、未 push commits）
5. 如果有 dirty files 或未 push commits → 特別提醒
6. 顯示：`💡 工作中可用 /pm-sync 同步進度，收工用 /pm-bye`
7. 詢問：
   ```
   要做什麼？
   1. 繼續上次的工作（預設）
   2. 開始新任務
   3. 查看完整進度
   ```
8. 進入 Plan-Execute Workflow

---

## `/pm status` — 快速查看進度

不做任何同步或互動，只顯示目前狀態：

1. Glob 搜尋 progress.md，不存在 → `⚠️ 尚未建立進度追蹤。使用 /pm new 初始化。`
2. 存在 → 讀取並顯示：✅ 已完成、🔄 進行中、📌 下次建議、🌿 Branch、🕐 上次同步

---

## `/pm resume` — 接續上次 session

1. 從 progress.md 的 Session 區段讀取 session ID
2. 找到 → `💡 請在終端機執行：claude --resume <sessionId>`
3. 找不到 → `⚠️ 找不到 session ID。請使用 /pm 正常開工。`

---

## 共用邏輯參考

> 以下區段供 `/pm-sync`、`/pm-bye` 按需讀取。

### progress.md 標準格式

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
```

### Dashboard 更新規則

- Dashboard 使用 Google Sheet（ID 從 `~/.claude/.env` 的 `DASHBOARD_SHEET_ID` 讀取）
- 以 B 欄「專案名稱」為唯一鍵，更新 C~H 欄
- 新增時在最後列 append，A 欄自動分配 ID（`A-001` 格式）
- Dashboard 是總覽，每欄用最短的詞描述
- Sheet 欄位：ID | 專案名稱 | 簡述 | 狀態 | 本次完成 | 下次預計 | 重要記事 | 最後更新

### Google 工具可用性

Google 同步依賴：Apps Script Web App + Chat Webhook（`~/.claude/.env` 裡的 `APPS_SCRIPT_WEB_APP_ID` / `CHAT_WEBHOOK_URL`）。
任一不可用時 graceful skip，本地 progress.md 照常更新。

---

## 注意事項

- 所有輸出使用繁體中文
- 預設自動 — 每個階段有 happy path
- 需要時才問 — 只在分歧點才跳選單
- `/pm` 是 `/hello` 的升級版；收工用 `/pm-bye`，同步用 `/pm-sync`，審核用 `/pm-review`
