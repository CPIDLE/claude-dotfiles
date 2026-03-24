# PM v2 — 專案管理統一入口

統一管理開工、中期同步、收工的完整工作流程。整合 Code Review、QA 檢查、Retro to Memory 等進階功能。

## 快捷參數

| 指令 | 行為 |
|---|---|
| `/pm` | 開工（自動判斷首次/正常模式） |
| `/pm new` | 首次開工（掃描專案 + 建立 progress.md） |
| `/pm sync` | 中期選單（同步/review/QA/調整） |
| `/pm sync 2` | 直接同步 Canvas（跳過選單） |
| `/pm bye` | 收工全流程（review + QA + git + sync + retro） |
| `/pm status` | 快速查看進度（唯讀） |
| `/pm resume` | 接續上次 session |

## Status Line 整合（必要）

每個子命令在 **開始前** 和 **完成後** 必須更新 `~/.claude/pm-last.txt`。

| 時機 | 指令 |
|---|---|
| `/pm` 或 `/pm new` 開始 | `bash ~/.claude/pm-update.sh pm running` |
| `/pm` 或 `/pm new` 完成 | `bash ~/.claude/pm-update.sh pm done` |
| `/pm sync` 開始 | `bash ~/.claude/pm-update.sh sync running` |
| `/pm sync` 完成 | `bash ~/.claude/pm-update.sh sync done` |
| `/pm bye` 開始 | `bash ~/.claude/pm-update.sh bye running` |
| `/pm bye` 完成 | `bash ~/.claude/pm-update.sh bye done` |

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
3. 有專案指標 + 無 `progress.md` → 顯示提醒：
   ```
   📁 偵測到專案：<資料夾名稱>
   📝 尚未建立進度追蹤（無 progress.md）。
   如果要初始化，請使用：/pm new
   ```
   **直接結束，不建立任何檔案。**
4. 以上皆不符合 → 顯示警告並結束：
   ```
   ⚠️ 目前目錄不像是一個專案（無 .git、無專案設定檔）。
   📁 目前位置：<完整路徑>
   如果要在此建立新專案，請使用：/pm new
   ```

> progress.md 位置：使用 Glob 搜尋 `**/memory/progress.md`，路徑格式 `~/.claude/projects/<project-key>/memory/progress.md`。

---

### 首次模式（`new` 參數）

1. 告知使用者將進行首次專案掃描
2. 掃描專案狀態：
   ```bash
   git log --oneline -20
   git branch -a
   git remote -v
   ```
3. 使用 Glob 快速掃描專案檔案結構
4. 整理首次進度摘要（專案概述、目前 branch、建議下一步）
5. 寫入 `progress.md`（memory 資料夾中）
6. 顯示摘要讓使用者確認
7. 如果是全新空目錄，額外詢問：目標、技術棧、參考範例

---

### 正常模式（有 progress.md）

1. 讀取 `progress.md`
2. 如果有 `### Session` 區段含 Resume 指令，顯示：
   ```
   💡 上次 session 可續：claude --resume <sessionId>
   ```
3. 顯示進度摘要：
   ```
   📋 上次工作：YYYY-MM-DD

   ✅ 已完成：
   - item 1

   🔄 進行中：
   - item 1

   ⚠️ 已知問題：
   - issue 1

   📌 下次建議：
   - next step 1
   ```
4. 顯示 Git 狀態摘要：
   ```bash
   git status --short
   git log --oneline -5
   git log @{u}..HEAD --oneline 2>/dev/null
   ```
5. 如果有 dirty files 或未 push commits → 特別提醒
6. 如果有 `### Slack Canvas` 區段 → 顯示：`💡 工作中可用 /pm sync 同步進度，收工用 /pm bye`
7. 詢問使用者：
   ```
   要做什麼？
   1. 繼續上次的工作（預設）
   2. 開始新任務
   3. 查看完整進度
   ```
8. 進入 Plan-Execute Workflow（依 CLAUDE.md 的三階段流程）

---

## `/pm status` — 快速查看進度

不做任何同步或互動，只顯示目前狀態：

1. 使用 Glob 搜尋 `**/memory/progress.md`
2. 如果不存在：`⚠️ 尚未建立進度追蹤。使用 /pm new 初始化。`
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

**不更新 status line。**

---

## `/pm resume` — 接續上次 session

1. 從 progress.md 的 `### Session` 區段讀取 session ID
2. 如果找到：
   - 顯示：`🔄 正在接續上次 session...`
   - 執行：`claude --resume <sessionId>`
   - **注意**：這會結束當前 session
3. 如果找不到：
   ```
   ⚠️ 找不到上次的 session ID。
   💡 請使用 /pm 正常開工。
   ```

---

## `/pm sync` — 中期同步 + 動作選單

### 自動偵測狀態

顯示目前工作狀態：
```
📊 目前狀態
├─ Tasks: N/M completed
├─ Git: X modified, Y untracked
├─ 上次同步：<時間 或「—」>
└─ Canvas: <已連結 / 未連結>
```

狀態資訊來源：
- Tasks：從 TodoWrite 目前的 task 狀態計算
- Git：執行 `git status --short` 統計
- 上次同步：從 progress.md 的 `### Slack Canvas` 區段讀取
- Canvas：檢查 progress.md 是否有 Canvas ID

### 選單

如果有 `2` 參數（`/pm sync 2`）→ 直接跳到選 2（同步進度），不顯示選單。

否則顯示：
```
你想做什麼？
1. 繼續執行（預設，直接回到工作）
2. 同步進度 → Slack Canvas + Channel
3. Code Review — 審查目前所有改動
4. QA 檢查 — 跑測試 + 安全掃描
5. 調整計畫 — 修改 scope 或重新排序
```

---

### 選 1：繼續執行

- 不做任何事，回到工作流程
- 如果有 TodoWrite tasks，顯示下一個 pending task

---

### 選 2：同步進度

#### Step A：檢查 progress.md

使用 Glob 搜尋 `**/memory/progress.md`。如果不存在：
```
⚠️ 找不到 progress.md。
💡 請先執行 /pm new 建立專案進度。
```
直接結束。

#### Step B：判斷 Canvas 狀態

讀取 progress.md，檢查是否有 `### Slack Canvas` 區段且包含 Canvas ID。

**已連結（有 Canvas ID）：**
1. 使用 `slack_read_canvas` 讀取 Canvas 最新內容
2. 將 progress.md 內容（排除 `### Slack Canvas` 區段和 frontmatter）轉為 Canvas Markdown
3. 使用 `slack_update_canvas`（action=replace）更新 Canvas
4. 更新 progress.md 中的「最後同步」時間
5. 顯示：`✅ 已同步到 Canvas！🔗 <Canvas URL>`

**未連結（無 Canvas ID）：**
```
📋 專案：<資料夾名稱>
🔗 尚未連結 Slack Canvas

請選擇：
1. 🆕 建立新 Canvas
2. 🔗 連結既有 Canvas（輸入 ID 或 URL）
3. ⏭️ 跳過
```

- 選 1：標題 `📋 <資料夾名稱> 進度追蹤`，用 `slack_create_canvas` 建立，寫回 Canvas ID
- 選 2：詢問 Canvas ID（`F08XXXXXXXX`）或 URL，用 `slack_read_canvas` 驗證後寫回
- 選 3：跳過

#### Step C：發送摘要到 #all-cpidle（防洗版）

Channel ID: `C0AN35HJQ8L`

1. 用 `slack_search_public` 搜尋 `from:<@U0AMZHMH3HQ> in:<#C0AN35HJQ8L> <專案名稱>` 找今天是否已有摘要
2. 已有 → 跳過，顯示 `ℹ️ 今日已發送過摘要，跳過`
3. 沒有 → 發送新訊息，格式：
   ```
   📋 *<專案名稱> — 進度更新*

   • <重點 1>
   • <重點 2>
   • <重點 3>

   🔗 <Canvas URL|完整進度>
   ```

擷取重點規則：優先已完成（✅）→ 進行中（🔄）→ 下一步，不超過 5 項。

#### Step D：更新 Dashboard Canvas

Dashboard Canvas ID: `F0AMWD1GAD9`

1. 用 `slack_read_canvas` 讀取 Dashboard
2. 從 section_id_mapping 找當前專案的 `## 🔹` header
3. 已存在 → 用 `slack_update_canvas`（action=replace, section_id）更新整個區段
4. 不存在 → 用 `slack_update_canvas`（action=append）新增
5. 單獨更新「最後更新」時間戳

每個專案區段格式：
```markdown
## 🔹 <專案名稱>
狀態：<開發中 / 規劃中 / 已完成 / 維護中>
- ✅ <最近完成 1-2 項>
- 🔄 <進行中 1-2 項>
- 📌 <待辦 1-2 項>
🔗 [完整進度](<Canvas URL>)
```

---

### 選 3：Code Review

以**資深工程師**角色審查所有改動：

1. 收集改動：
   ```bash
   git diff --staged
   git diff
   git log --oneline -5
   ```
   如果有未 staged 的改動也一併審查。

2. 審查四個面向：
   - **邏輯正確性**：是否有 bug、邊界條件遺漏、race condition
   - **安全性**：OWASP top 10 常見問題（注入、XSS、敏感資料外洩等）
   - **效能**：N+1 查詢、不必要的重複計算、記憶體洩漏風險
   - **程式碼風格**：命名一致性、死碼、過度複雜的邏輯

3. 產出審查報告：
   ```
   🔍 Code Review 報告

   🔴 Critical（必須修正）：
   - [檔案:行號] 問題描述

   🟡 Warning（建議修正）：
   - [檔案:行號] 問題描述

   🔵 Info（參考）：
   - [檔案:行號] 建議

   📊 總結：X critical, Y warnings, Z info
   ```

4. 如果有 Critical 或 Warning → 詢問：`要自動修正這些問題嗎？`
5. 如果使用者同意 → 逐一修正並顯示修正摘要

---

### 選 4：QA 檢查

1. **偵測測試框架**（依序檢查）：
   - `jest.config.*` / `package.json` 含 jest → `npx jest`
   - `vitest.config.*` → `npx vitest run`
   - `pytest.ini` / `pyproject.toml` 含 `[tool.pytest]` → `pytest`
   - `go.mod` → `go test ./...`
   - `Cargo.toml` → `cargo test`
   - 都沒有 → 顯示 `ℹ️ 未偵測到測試框架，跳過測試`

2. **執行測試**（如果偵測到框架）

3. **偵測 Linter**（依序檢查）：
   - `.eslintrc*` / `eslint.config.*` → `npx eslint .`
   - `biome.json` → `npx biome check .`
   - `ruff.toml` / `pyproject.toml` 含 `[tool.ruff]` → `ruff check .`
   - 都沒有 → 跳過

4. **執行 Linter**（如果偵測到）

5. **掃描 Debug 程式碼**：
   - 在非測試檔案中搜尋：`console.log`、`console.debug`、`debugger`、`print(`（Python）、`fmt.Println`（Go debug）
   - 排除：`console.error`、`console.warn`、測試檔案、node_modules
   - 列出找到的項目

6. **產出 QA 報告**：
   ```
   🧪 QA 檢查報告

   測試：✅ 通過（X passed）/ ❌ 失敗（X passed, Y failed）/ ⏭️ 跳過
   Lint：✅ 無問題 / ⚠️ N 個警告 / ⏭️ 跳過
   Debug 程式碼：✅ 未發現 / ⚠️ 發現 N 處

   📊 總結：<整體狀態>
   ```

7. 如果有測試失敗或 lint 錯誤 → 詢問：`要自動修正嗎？`

---

### 選 5：調整計畫

- 進入 Plan Mode（`EnterPlanMode`）
- 讓使用者重新規劃剩餘工作
- 完成後更新 TodoWrite tasks

---

## `/pm bye` — 收工

依序自動執行以下步驟，有問題才暫停：

### Step 1：回顧本次對話

回顧整個對話歷史，整理出：
- **完成事項**：本次 session 完成的所有工作
- **進行中工作**：開始但未完成的事項
- **已知問題**：發現但未解決的問題
- **下次建議**：建議下次優先處理的事項

### Step 2：Code Review（自動，僅摘要）

如果在 git repo 中且有改動：
1. 執行與 `/pm sync` 選 3 相同的審查邏輯
2. **僅顯示摘要**（不顯示完整報告）：
   ```
   🔍 Code Review：X critical, Y warnings, Z info
   ```
3. **只在有 Critical 問題時暫停**，詢問是否修正
4. Warning 和 Info 只記錄，不暫停

如果不在 git repo 或無改動 → 跳過。

### Step 3：QA 快速檢查（自動）

如果在 git repo 中：
1. 執行與 `/pm sync` 選 4 相同的邏輯
2. **僅顯示摘要**：
   ```
   🧪 QA：測試 ✅/❌ | Lint ✅/⚠️ | Debug ✅/⚠️
   ```
3. **只在測試失敗時暫停**，詢問是否修正
4. Lint 警告和 debug 程式碼只記錄，不暫停

如果無測試框架 → 跳過。

### Step 4：Git 整理

```bash
git status --short
git diff --stat
git log --oneline -5
git log @{u}..HEAD --oneline 2>/dev/null
git remote -v
```

1. 如果有 dirty files → 詢問：`💡 偵測到未 commit 的變更，要執行 smart-commit 嗎？`
   - 同意 → 分析改動，產生合適的 commit message，執行 `git add` + `git commit`
   - 完成後重新檢查 `git status` 和未 push commits
2. 如果有未 push commits → 詢問：`📤 有 N 個 commit 尚未 push，要現在 push 嗎？`
   - 同意 → 執行 `git push`
3. 如果沒有 remote → 詢問：`🔗 要建立 GitHub private repo 嗎？`
   - 同意 → `gh repo create <folder-name> --private --source=. --push`

### Step 5：寫入 progress.md（含 Session ID）

將整理好的進度寫入 memory 資料夾中的 `progress.md`（覆寫，只保留最新狀態）。

**撈取 Session ID：**
1. 列出 `~/.claude/sessions/` 目錄下的 `.json` 檔案
2. 找到 `cwd` 匹配當前工作目錄的檔案
3. 讀取其中的 `sessionId` 欄位
4. 找不到 → 跳過 Session 區段

### Step 6：Slack 同步（自動，不需確認）

如果 progress.md 有 `### Slack Canvas` 區段且包含 Canvas ID：
- 執行選 2 的完整流程（Canvas + Channel + Dashboard）
- 顯示：`📤 已同步 Canvas、Channel、Dashboard！`

如果沒有 Canvas ID → 跳過。

### Step 7：Retro to Memory（自動）

回顧本次 session，檢查是否有值得記住的內容：

| 類型 | 觸發條件 | 範例 |
|---|---|---|
| feedback | 使用者糾正了做法或確認了非顯而易見的做法 | 「用戶偏好 X 而非 Y」 |
| project | 學到新的專案背景或限制 | 「API 限制每分鐘 100 次」 |
| user | 發現使用者偏好或角色資訊 | 「偏好簡潔的 commit message」 |

- 如果有值得記住的內容 → 寫入 memory 檔案（依照標準 memory 格式含 frontmatter）
- 如果沒有 → 跳過，不提示

### Step 8：顯示進度摘要

```
📋 本次工作摘要

✅ 完成：
- item 1
- item 2

🔄 進行中：
- item 1

⚠️ 已知問題：
- issue 1

📌 下次建議：
- next step 1

🌿 Git：branch-name | N unpushed
🔍 Review：X critical, Y warnings
🧪 QA：tests ✅/❌ | lint ✅/⚠️
```

### Step 9：告別並退出

```
👋 收工！進度已儲存。
   💡 續回本次：claude --resume <sessionId>
   下次開工用 /pm 👋
```

然後立即輸出 `/exit` 讓 Claude Code 結束。

---

## 共用邏輯參考

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

### progress.md 擴充格式 — Slack Canvas

```markdown
### Slack Canvas
- Canvas ID: F08XXXXXXXX
- Canvas URL: https://xxx.slack.com/canvas/...
- 最後同步：YYYY-MM-DD HH:MM
```

### Canvas 內容格式轉換

將 progress.md 轉為 Canvas 時：
- 移除 frontmatter（`---` 包圍的 YAML 區塊）
- 移除 `### Slack Canvas` 區段
- 移除與 Canvas 標題重複的頂層標題
- emoji（✅ 🔄 等）保留原樣
- Headers 不超過 3 層（`###`）

### Dashboard 更新規則

- Dashboard Canvas ID: `F0AMWD1GAD9`（固定值）
- 每個專案只能有一個 `## 🔹` 區段
- 更新時用 section_id 精確替換，不影響其他專案
- 如果發現重複區段 → 先清理再更新

---

## 注意事項

- 所有輸出使用繁體中文
- 預設自動 — 每個階段有 happy path，不選就能走完
- 需要時才問 — 只在分歧點或風險點才跳選單
- 關鍵 ID：Channel `C0AN35HJQ8L`、Dashboard `F0AMWD1GAD9`
- `/pm` 是 `/hello`、`/sc`、`/bye` 的升級版，舊指令仍可獨立使用
