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
| `/pm index` | 掃描目錄，產生/更新 INDEX.md（獨立使用，不需 /pm 工作流） |
| `/pm health` | 對當前 repo 跑完整 7 項 AI 健檢（唯讀），同意才 scaffold 補強 |

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
5. **健康起手式 scaffold**（詳見下方 §健康起手式 scaffold）
6. 顯示摘要讓使用者確認
7. 全新空目錄 → 額外詢問目標、技術棧 → 補寫

#### 健康起手式 scaffold

從 `~/.claude/templates/new-project/` 把 AI 開發護欄鋪進新專案（對應健檢第 3/4/5 項）。happy path 自動做，**只有檔案衝突才跳一次確認**。

1. **偵測 test runner**（決定 `<TEST_CMD>`）：
   - `pyproject.toml`/`pytest.ini`/`tests/` → `pytest -q`
   - `package.json`（有 `test` script）→ `npm test`
   - `Cargo.toml` → `cargo test`
   - `go.mod` → `go test ./...`
   - 測不到 → 保留 `<TEST_CMD>` 佔位，提醒使用者手填
2. **部署模板**（已存在的檔一律跳過，不覆蓋）：
   - `templates/new-project/CLAUDE.md` → 專案根 `CLAUDE.md`，把 `<TEST_CMD>` 換成偵測結果（已有 CLAUDE.md → 跳過）
   - `templates/new-project/gitignore.snippet` → **append** 進 `.gitignore` 缺的行（逐行比對，已有的不重複；無 `.gitignore` 則新建）
   - `templates/new-project/settings.json` → `.claude/settings.json`（已存在 → 跳過）
   - `templates/new-project/check.sh` → `.claude/check.sh`，把 `<TEST_CMD>` 換成偵測結果（已存在 → 跳過）
3. 一行回報：`🛡️ 健康起手式：CLAUDE.md + .gitignore + .claude/ hook（test=<TEST_CMD>）已就緒`
4. `.claude/settings.json` 與 `.claude/check.sh` 是 **shared、要 commit**；`.claude/settings.local.json` 才是 local（已被 gitignore 擋）。

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
5. **AI 健檢（一行，唯讀）** — 詳見下方 §AI 健檢
6. 如果有 dirty files 或未 push commits → 特別提醒
7. 顯示：`💡 工作中可用 /pm-sync 同步進度，收工用 /pm-bye`
8. 詢問：
   ```
   要做什麼？
   1. 繼續上次的工作（預設）
   2. 開始新任務
   3. 查看完整進度
   ```
9. 進入 Plan-Execute Workflow

#### AI 健檢

開工時對當前 repo 跑一次便宜的唯讀健檢（**不派 subagent**），advisory，**預設不改任何檔**。非 git repo → 跳過。

**快查 7 項**（純 `git ls-files` + 檔案存在性）：

| # | 查法 | ✗ 條件 |
|---|---|---|
| 1 | `git ls-files \| grep -i settings.local.json` | 有結果＝誤入版控 |
| 2 | `.claude/settings.local.json` 的 `allow` | 含 `rm *`/`Bash(*)` 等危險萬用 |
| 3 | 根 `CLAUDE.md` 存在？ | 無 |
| 4 | `CLAUDE.md` 含「修改規則」？ | 無 |
| 5 | `.claude/settings.json` 有 PostToolUse hook？ | 無 |
| 6 | 有測試（`test_*`/`*_test`/`tests/`）？ | 無 |
| 7 | `.env` 誤入版控 / gitignore 沒擋 `.env`+`.claude`？ | `.env` 被 track 或 gitignore 缺防護 |

> 評分與細則見 `~/.claude/docs/repo-health-checklist.md`。

**輸出（一行）**：
- 全綠 → `🩺 健檢 14/14 ✅`
- 有缺 → `🩺 健檢 N/14｜缺：CLAUDE契約, hook, 測試門檻`
- **資安項（1/2/7）有 ✗** → 該項紅字標出並置頂，比照緊急處理（如 `🔴 settings.local.json 已誤入版控`）
- 結尾 advisory：`💡 要補健康起手式跑 /pm health`

**節流**（避免每次開工嘮叨）：把 `健檢 N/14 (YYYY-MM-DD) 缺:<項目>` 記進 `progress.md` 的「🩺 健檢」行。下次開工若 **全綠**、或 **7 天內已顯示過相同缺項** → 靜默跳過（但資安項 ✗ 一律照常出聲）。

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

## `/pm index` — 工作區檔案索引

獨立子指令，可隨時使用，不需 `/pm` 完整工作流。不更新狀態檔。

### 掃描策略

- **首選** PowerShell `Get-ChildItem -Recurse -File`（不受 Glob 截斷限制）
- 排除：`.git/`、`node_modules/`、`__pycache__/`、`.venv/`、`INDEX.md` 本身
- 檔案數 > 80 時，先掃 root，再逐一掃各子目錄（避免單次輸出截斷）
- macOS/Linux 用 Bash `find` 替代

### 行為

1. 依上述掃描策略列出當前目錄所有非隱藏檔
2. 判斷 INDEX.md 是否已存在：
   - **不存在** → 建立新 INDEX.md，含表頭 + 所有檔案
   - **已存在** → 讀取現有內容，只新增未列出的檔案，保留已有 annotations
3. 按版本 lineage 分組：
   - 偵測 `_v0` ~ `_vN`、`-v0` ~ `-vN`、`_v5_1` 等版本化檔名
   - 同一 base name 的版本系列，「來源」欄位填 `← vN-1`
   - 最新版標 `active`，舊版標 `archived`
4. 日期取檔案 mtime（`YYYY-MM-DD`）
5. 「用途」欄：cc 有上下文時自動填入，否則填 `—`

### INDEX.md 格式

```markdown
# INDEX

<!-- cc: 自動維護。hook 自動 append 新檔，/pm index 全量更新，/pm bye 清理掃描 -->

| 檔名 | 用途 | 狀態 | 日期 | 來源 |
|---|---|---|---|---|
| PROPOSAL_v7.md | 機器人轉型提案 | final | 2026-05-25 | ← v6 |
| helper.py | 資料遷移腳本 | one-off | 2026-05-20 | — |
```

### 狀態值

| 狀態 | 意義 |
|---|---|
| `final` | 交付物，不再修改 |
| `active` | 還在使用/迭代中 |
| `draft` | 中間版本，被新版取代後改 `archived` |
| `one-off` | 一次性腳本/工具，用完可刪 |
| `archived` | 已被取代，保留參考但可隨時清 |

---

## `/pm health` — repo AI 健檢 + 補強

手動觸發，對當前 repo 跑完整 7 項 AI 健檢並（同意後）一鍵補強。非 git repo → 提醒並結束。

### Step 1：逐項健檢（唯讀）

依 `~/.claude/docs/repo-health-checklist.md` 的查法，逐項評 ✓/△/✗，輸出表格 + 一句現況/建議：

```
🩺 AI 健檢：<repo>  —  N/14

1 權限衛生   ✓/△/✗  <一句>
2 權限不過寬 ✓/△/✗  <一句>
3 上下文檔   ✓/△/✗  <一句>
4 行為契約   ✓/△/✗  <一句>
5 機器強制   ✓/△/✗  <一句>
6 測試門檻   ✓/△/✗  <一句>
7 揭露與機密 ✓/△/✗  <一句>
```

### Step 2：分流處理

- **資安項（1/2/7）有 ✗ → 立刻提示修**（需明確同意才動）：
  - settings.local.json 誤入版控 → `git rm --cached <path>` + 把 `**/.claude/settings.local.json` 加進 `.gitignore`
  - `.env`/金鑰外洩 → 建/補 `.gitignore`（`git rm --cached` 已 track 的）
  - 萬用權限 → 列出該收斂的條目，交使用者決定（不自動改）
- **品質項（3/4/5/6）缺 → 詢問**：
  ```
  要 scaffold 補上缺的健康起手式（CLAUDE.md / .gitignore / .claude hook）嗎？
  [1] 好 [2] 跳過
  ```
  - 選 1 → 走 §健康起手式 scaffold（同 `/pm new` Step 4.5；已存在的檔一律跳過、不覆蓋）
  - 選 2 → 不改任何檔

> 這是舊專案**唯一**會被改的路徑，且每個動作都需明確同意。不確認就純唯讀回報。

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
