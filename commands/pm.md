# PM v2 — 專案管理統一入口

統一管理開工、中期同步、收工的完整工作流程。整合審核（easy/deep）、Retro to Memory 等進階功能。

## 快捷參數

| 指令 | 行為 |
|---|---|
| `/pm` | 開工（自動判斷首次/正常模式） |
| `/pm new` | 首次開工（掃描專案 + 建立 progress.md） |
| `/pm sync` | 中期選單（同步/審核/調整） |
| `/pm sync 2` | 直接同步 Canvas（跳過選單） |
| `/pm bye` | 收工全流程（easy 審核 + git + sync + retro） |
| `/pm review` | 獨立審核（預設 deep） |
| `/pm review easy` | 快速審核（主 agent 直接跑，不產報告） |
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
| `/pm review` 開始 | `bash ~/.claude/pm-update.sh review running` |
| `/pm review` 完成 | `bash ~/.claude/pm-update.sh review done` |
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
2. 使用 **Explore agent**（thoroughness: `very thorough`）掃描專案，prompt 包含：
   - 專案結構、技術棧、主要模組
   - Git 歷史（最近 20 commits、branches、remotes）
   - 入口點、設定檔、CI/CD
3. 根據 Explore agent 回傳的結果，整理首次進度摘要（專案概述、目前 branch、建議下一步）
4. 寫入 `progress.md`（memory 資料夾中）
5. 顯示摘要讓使用者確認
6. 如果是全新空目錄，額外詢問：目標、技術棧、參考範例

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
1. 同步進度 → Slack Canvas + Channel（預設）
2. 審核 — 獨立 agent 跑測試 + lint + AI 審查
3. 調整計畫 — 修改 scope 或重新排序
```

---

### 選 1：同步進度

#### Step 0：自動 Smart-Commit

如果在 git repo 中，執行 `git status --short`：
- 有 dirty files → 自動分析改動、產生 commit message、執行 `git add` + `git commit`（不問、不 push）
- 無改動 → 跳過

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

#### Step C+D：發送 Channel 通知 + 更新 Dashboard（平行）

SB 完成後，**同時執行**以下兩項（互不依賴，寫入不同的 Slack 目標）：

> ⚠️ **硬依賴**：SB 必須在 C+D 之前完成。SB 可能建立新 Canvas，C 和 D 都需要 Canvas URL。
> ⚠️ **部分失敗處理**：C 或 D 任一失敗，顯示 `⚠️ <Channel/Dashboard> 同步失敗：<原因>`，不影響另一項。

**C — 發送摘要到 #all-cpidle（防洗版）**

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

**D — 更新 Dashboard Canvas**

Dashboard Canvas ID: `F0AMWD1GAD9`

1. 用 `slack_read_canvas` 讀取 Dashboard，取得 `section_id_mapping`
2. 在 mapping 中搜尋包含當前專案名稱的 `## :small_blue_diamond:` header
3. **已存在** → 用 `slack_update_canvas`（action=replace, section_id=該 header 的 ID）替換區段。**替換內容不包含 `##` header 行**（header 是 section 本身，會被保留），只寫 header 以下的內容（狀態 + 項目 + 連結 + 時間戳）
4. **不存在** → 用 `slack_update_canvas`（action=append）新增完整區段（含 `##` header）
5. **不要**單獨寫「最後更新」— 時間戳必須包含在區段內容的最後一行

replace 時的內容格式（**不含** `##` header）：
```markdown
狀態：<開發中 / 規劃中 / 已完成 / 維護中>
- :white_check_mark: <最近完成 1-2 項>
- :arrows_counterclockwise: <進行中 1-2 項>
- :pushpin: <待辦 1-2 項>
:link: [完整進度](<Canvas URL>)

最後更新：YYYY-MM-DD HH:MM
```

append 時的內容格式（**含** `##` header）：
```markdown
## :small_blue_diamond: <專案名稱>
狀態：<開發中 / 規劃中 / 已完成 / 維護中>
- :white_check_mark: <最近完成 1-2 項>
- :arrows_counterclockwise: <進行中 1-2 項>
- :pushpin: <待辦 1-2 項>
:link: [完整進度](<Canvas URL>)

最後更新：YYYY-MM-DD HH:MM
```

> ⚠️ Canvas 使用 Slack emoji 語法（`:white_check_mark:` 非 `✅`），header 用 `:small_blue_diamond:` 非 `🔹`。
> ⚠️ `replace` + `section_id` 時如果內容包含 `##` header 會產生重複！只有 `append` 時才加 header。

---

### 選 2：審核

執行 `/pm review easy`（見下方「獨立審核」區段）。

---

### 選 3：調整計畫

- 進入 Plan Mode（`EnterPlanMode`）
- 讓使用者重新規劃剩餘工作
- 完成後更新 TodoWrite tasks

---

## `/pm review` — 獨立審核

兩種深度：

| 深度 | 觸發方式 | 執行者 | 產出 |
|---|---|---|---|
| **easy** | `/pm review easy`、sync 選 2、bye 自動 | 主 agent 直接跑 | 螢幕摘要（不寫檔） |
| **deep**（預設） | `/pm review` | 獨立 subagent | `reviews/YYYY-MM-DD-HH-MM.md` |

### Easy 模式

主 agent 直接執行，不啟動 subagent，不產出檔案：

1. **平行執行以下四項檢查**（同時發出，全部完成後再繼續）：

   | 檢查項 | 方法 | 掃描範圍 |
   |--------|------|----------|
   | 測試 | 偵測 jest/vitest/pytest/go test/cargo test，執行之 | 測試框架 |
   | Lint | 偵測 eslint/biome/ruff，執行之 | 原始碼 |
   | Debug 掃描 | Grep 搜尋 `console.log`、`debugger`、`print(` | 排除測試檔、node_modules |
   | Code Review | `git diff --staged` + `git diff`，掃描明顯 bug、安全漏洞、遺漏的錯誤處理 | git diff 範圍 |

   > ⚠️ **去重規則**：Debug 掃描只報告 debug 語句的存在與位置。Code Review 負責判斷所有程式碼品質問題（含 debug 語句的影響）。同一行若同時被標記，以 Code Review 的描述為準。
   > ⚠️ **部分失敗處理**：任一項檢查失敗（如指令不存在、timeout），標記為 `⚠️ 跳過`，不影響其他項的結果。全部完成或失敗後統一進入下一步。

2. **輸出一行摘要**：
   ```
   🔍 審核：測試 ✅/❌/⚠️ | Lint ✅/⚠️ | Debug ✅/⚠️ | Code ✅/⚠️ N issues
   ```
   - 測試失敗（❌）→ 暫停，詢問是否修正
   - 其餘只記錄，不暫停

### Deep 模式（預設）

啟動**完全獨立的 subagent**，以嚴格否定立場審查所有產出。

#### Step 1：收集審核範圍

```bash
git diff --staged && git diff
git log --oneline -10
git status --short
```

同時用 Glob 掃描專案結構，列出所有變更檔案的完整路徑。

#### Step 2：啟動審核 Agent

使用 Agent tool 啟動獨立 subagent，prompt：

```
你是獨立紅隊審核員。預設否定，找出問題。

## 身份
- 不隸屬開發團隊，立場是懷疑與辯證
- 不給建設性建議，只指出問題，修正是開發者的事
- 不因「只是小專案」放水

## 審核對象
主 agent 產出的所有成果物：程式碼、文件、指令定義檔。

## 審核方法
1. **交叉驗證**：每個宣稱都回原始碼/原始文件核對
2. **內部一致性**：文件 A 段說的和 B 段說的有沒有矛盾
3. **可行性驗證**：建議的操作照做會不會壞掉
4. **遺漏偵測**：缺少的邊界條件、未定義的預設行為、遺漏的連動修改

## 自動檢查（先跑工具再做 AI 審查）
1. 偵測並執行測試框架（jest/vitest/pytest/go test/cargo test）
2. 偵測並執行 linter（eslint/biome/ruff）
3. 掃描 debug 程式碼

## 嚴重度
- 🔴 阻塞：照做會壞 → MUST FIX
- 🟠 中等：不完整或誤導 → SHOULD FIX
- 🟡 輕微：不精確但不影響結論 → NICE TO FIX

## 每項發現格式
- **編號**：F-001
- **位置**：檔案:行號 或 檔案:section
- **嚴重度**：🔴/🟠/🟡
- **問題**：一句話
- **驗證**：交叉比對了什麼
- **裁決**：MUST FIX / SHOULD FIX / NICE TO FIX

## 報告
寫入 `reviews/YYYY-MM-DD-HH-MM.md`，包含：
1. 審核 metadata（日期、專案、branch、commit、範圍）
2. 總評：🚫 REJECT / ⚠️ REVISE / ✅ PASS（一段話說明最大風險）
3. 自動檢查結果（測試/lint/debug）
4. 統計表（程式碼/文件 × 嚴重度）
5. 發現清單（依嚴重度分組）
6. 未覆蓋風險
7. 評分（各面向 1-5 分 + 加權總分）
```

附上 Step 1 收集的 git diff、檔案清單作為審核素材。

#### Step 3：顯示結果

subagent 完成後：
1. 讀取 `reviews/` 下最新報告
2. 顯示摘要：
   ```
   🔍 審核完成

   📋 報告：reviews/YYYY-MM-DD-HH-MM.md
   📊 總評：<🚫 REJECT / ⚠️ REVISE / ✅ PASS>
   🔴 N | 🟠 N | 🟡 N | ⭐ X.X/5
   ```
3. 🚫 REJECT → 詢問：`有阻塞問題，要查看詳情並修正嗎？`

---

## `/pm bye` — 收工

依序自動執行以下步驟，有問題才暫停：

### Step 1：回顧本次對話

回顧整個對話歷史，整理出：
- **完成事項**：本次 session 完成的所有工作
- **進行中工作**：開始但未完成的事項
- **已知問題**：發現但未解決的問題
- **下次建議**：建議下次優先處理的事項

### Step 2：審核（review easy，自動）

執行 review easy 流程（見上方「Easy 模式」）：
- 測試 + lint + debug 掃描 + 快速 code review
- 輸出一行摘要：`🔍 審核：測試 ✅/❌ | Lint ✅/⚠️ | Debug ✅/⚠️ | Code ✅/⚠️`
- 測試失敗 → 暫停詢問，其餘只記錄
- 額外：如果 `reviews/` 有今日 deep 報告 → 顯示 `🔴 Deep：<總評> | ⭐ X.X/5`

無 git repo 或無改動 → 跳過。

### Step 3：Git 整理

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

### Step 4：寫入 progress.md（含 Session ID）

將整理好的進度寫入 memory 資料夾中的 `progress.md`（覆寫，只保留最新狀態）。

**撈取 Session ID：**
1. 列出 `~/.claude/sessions/` 目錄下的 `.json` 檔案
2. 找到 `cwd` 匹配當前工作目錄的檔案
3. 讀取其中的 `sessionId` 欄位
4. 找不到 → 跳過 Session 區段

### Step 5：Slack 同步（自動，不需確認）

如果 progress.md 有 `### Slack Canvas` 區段且包含 Canvas ID：
- 執行選 2 的完整流程（Canvas + Channel + Dashboard）
- 顯示：`📤 已同步 Canvas、Channel、Dashboard！`

如果沒有 Canvas ID → 跳過。

### Step 6：Retro to Memory（自動）

回顧本次 session，檢查是否有值得記住的內容：

| 類型 | 觸發條件 | 範例 |
|---|---|---|
| feedback | 使用者糾正了做法或確認了非顯而易見的做法 | 「用戶偏好 X 而非 Y」 |
| project | 學到新的專案背景或限制 | 「API 限制每分鐘 100 次」 |
| user | 發現使用者偏好或角色資訊 | 「偏好簡潔的 commit message」 |

- 如果有值得記住的內容 → 寫入 memory 檔案（依照標準 memory 格式含 frontmatter）
- 如果沒有 → 跳過，不提示

### Step 7：顯示進度摘要

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
🔍 審核：測試 ✅/❌ | Lint ✅/⚠️ | Code ✅/⚠️
🔴 Deep：<總評> | ⭐ X.X/5（如有 deep 報告）
```

### Step 8：告別並退出

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
- 每個專案只能有一個 `## :small_blue_diamond:` 區段
- **replace 時不含 `##` header**（header 是 section 本身會被保留，內容含 header 會產生重複）
- **append 時含 `##` header**（新增完整區段）
- 區段內容必須完整自包含（狀態 + 項目 + 連結 + 時間戳），不可拆成多次 update
- 如果 section_id_mapping 中發現同一專案有多個 header → 先用整個 Canvas replace（無 section_id）清理重複，再正常更新
- Canvas 內容使用 Slack emoji 語法（`:small_blue_diamond:` `:white_check_mark:` `:arrows_counterclockwise:` `:pushpin:` `:link:`），不使用 Unicode emoji

---

## 注意事項

- 所有輸出使用繁體中文
- 預設自動 — 每個階段有 happy path，不選就能走完
- 需要時才問 — 只在分歧點或風險點才跳選單
- 關鍵 ID：Channel `C0AN35HJQ8L`、Dashboard `F0AMWD1GAD9`
- `/pm` 是 `/hello`、`/sc`、`/bye` 的升級版，舊指令仍可獨立使用
