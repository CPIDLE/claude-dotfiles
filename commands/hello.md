# Hello — 開工打招呼

每次開始新的工作 session 時使用，自動判斷專案狀態並提供對應的引導。

## 執行步驟

請依序完成以下所有步驟，不要跳過：

### Step 1：問候與環境資訊

顯示以下資訊：
```
👋 嗨！開工囉！
📅 日期：YYYY-MM-DD（星期X）
📁 專案：<資料夾名稱>
⏰ 時間：HH:MM
```

### Step 2：判斷模式

依以下條件判斷進入哪種模式：

**專案指標檔案**（任一存在即視為有效專案）：
`.git`、`package.json`、`Cargo.toml`、`pyproject.toml`、`go.mod`、`pom.xml`、`build.gradle`、`Makefile`、`CMakeLists.txt`、`*.sln`、`*.csproj`、`composer.json`、`Gemfile`、`pubspec.yaml`、`CLAUDE.md`

**判斷邏輯（依序檢查）：**
1. 使用者指定 `new` 參數 → 進入 **首次模式**（掃描專案並建立 `progress.md`）
2. 當前目錄有專案指標檔案，且 memory 中有 `progress.md` → 進入 **正常模式**
3. 當前目錄有專案指標檔案，但無 `progress.md` → **不建立任何檔案**，顯示提醒並結束：
   ```
   📁 偵測到專案：<資料夾名稱>
   📝 尚未建立進度追蹤（無 progress.md）。

   如果要初始化此專案的進度追蹤，請使用：/hello new
   ```
   **直接結束，不建立任何檔案。**
4. **以上皆不符合**（無專案指標、也沒 `new`）→ 顯示警告並結束：
   ```
   ⚠️ 目前目錄不像是一個專案（無 .git、無專案設定檔）。
   📁 目前位置：<完整路徑>

   如果要在此建立新專案，請使用：/hello new
   ```
   **不建立任何檔案，直接結束。**

> 注意：progress.md 的位置在 memory 資料夾中（與其他 memory 檔案相同位置）。
> 使用 Glob 工具搜尋 `**/memory/progress.md` 來定位，路徑格式為 `~/.claude/projects/<project-key>/memory/progress.md`。

---

### 模式 A：首次模式（使用者指定 `new` 參數）

使用者明確要求初始化進度追蹤。執行以下流程：

1. 告知使用者將進行首次專案掃描
2. 掃描專案狀態：
   ```bash
   git log --oneline -20
   git branch -a
   git remote -v
   ```
3. 使用 Glob 快速掃描專案檔案結構（列出主要目錄和檔案）
4. 整理成首次進度摘要，包含：
   - 專案概述（從檔案結構和 git 歷史推斷）
   - 目前 branch 和最近的工作方向
   - 建議的下一步
5. 將摘要寫入 `progress.md`（memory 資料夾中）
6. 顯示摘要讓使用者確認
7. 如果當前目錄沒有專案指標檔案（全新空目錄），額外詢問：
   - 這個專案的目標是什麼？
   - 想用什麼技術棧？
   - 有參考範例嗎？

---

### 模式 B：正常模式（有 progress.md）

這是持續開發中的專案。執行以下流程：

1. 讀取 `progress.md`
2. 顯示進度摘要：
   ```
   📋 上次工作：YYYY-MM-DD

   ✅ 已完成：
   - item 1
   - item 2

   🔄 進行中：
   - item 1

   ⚠️ 已知問題：
   - issue 1

   📌 下次建議：
   - next step 1
   ```
3. 顯示 Git 狀態摘要：
   ```bash
   git status --short
   git log --oneline -5
   git log @{u}..HEAD --oneline 2>/dev/null  # 未 push 的 commits
   ```
4. 如果有 dirty files 或未 push commits，特別提醒
5. 詢問使用者：「要繼續之前的工作，還是有新的任務？」

---

## 注意事項

- 所有輸出使用繁體中文
- progress.md 使用下方定義的標準格式
- 探索模式中，不要急著寫 code，先充分討論
- 正常模式中，讀取 progress.md 後要與 git 實際狀態交叉比對，若有衝突以 git 為準

## progress.md 標準格式

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
```
