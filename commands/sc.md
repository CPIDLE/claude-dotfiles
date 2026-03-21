# SC (Slack Canvas) — Slack Canvas 進度同步

將專案 `progress.md` 與 Slack Canvas 雙向同步，自動判斷狀態並引導操作。

## 執行步驟

請依序完成以下所有步驟，不要跳過：

### Step 0：專案驗證

先檢查當前目錄是否為有效專案。

**專案指標檔案**（任一存在即視為有效專案）：
`.git`、`package.json`、`Cargo.toml`、`pyproject.toml`、`go.mod`、`pom.xml`、`build.gradle`、`Makefile`、`CMakeLists.txt`、`*.sln`、`*.csproj`、`composer.json`、`Gemfile`、`pubspec.yaml`、`CLAUDE.md`

**如果以上皆不存在：**
```
⚠️ 目前目錄不像是一個專案（無 .git、無專案設定檔）。
📁 目前位置：<完整路徑>
無法同步進度，跳過 /canvas。
```
**不建立任何檔案，直接結束。**

**如果驗證通過 → 繼續 Step 1。**

---

### Step 1：讀取 progress.md 並判斷狀態

使用 Glob 搜尋 `**/memory/progress.md` 定位 progress.md。

**如果 progress.md 不存在：**
```
⚠️ 找不到 progress.md。
💡 請先執行 /hello 建立專案進度，再使用 /canvas 同步。
```
**直接結束。**

**如果 progress.md 存在：** 讀取內容，檢查是否有 `### Slack Canvas` 區段且包含 `Canvas ID`。

- **有 Canvas ID** → 進入 **Step 2A（已連結模式）**
- **無 Canvas ID** → 進入 **Step 2B（未連結模式）**

---

### Step 2A：已連結模式

1. 使用 `slack_read_canvas` 讀取 Canvas 最新內容
2. 與本地 progress.md 內容比對，產生差異摘要
3. 顯示狀態：
   ```
   🔗 已連結 Canvas
   📋 Canvas：<Canvas 標題>
   🔗 連結：<Canvas URL>
   🕐 上次同步：<最後同步時間>

   📊 差異摘要：
   - <列出主要差異，例如「本地多了 2 項完成事項」或「Canvas 上有新的備註」>
   - 或顯示「✅ 本地與 Canvas 內容一致」
   ```
4. 詢問使用者：
   ```
   請選擇操作：
   1. 📤 同步本地 → Canvas（用本地 progress.md 更新 Canvas）
   2. 📥 同步 Canvas → 本地（用 Canvas 內容更新本地 progress.md）
   3. 👀 只看 Canvas 完整內容
   4. 🔗 取消連結（移除 Canvas ID，不刪除 Canvas）
   ```

**選 1（本地 → Canvas）：**
- 將 progress.md 內容（排除 `### Slack Canvas` 區段）轉為 Canvas Markdown 格式
- 使用 `slack_update_canvas`（action=replace）更新 Canvas 全部內容
- 更新 progress.md 中的「最後同步」時間
- 顯示：`✅ 已同步到 Canvas！🔗 <Canvas URL>`

**選 2（Canvas → 本地）：**
- 將 Canvas 內容轉回 progress.md 格式
- 覆寫 progress.md（保留 frontmatter 和 `### Slack Canvas` 區段）
- 更新「最後同步」時間
- 顯示：`✅ 已從 Canvas 同步到本地！`

**選 3（只看）：**
- 顯示 Canvas 完整內容，不做任何修改

**選 4（取消連結）：**
- 從 progress.md 中移除 `### Slack Canvas` 區段
- 顯示：`🔗 已取消連結。Canvas 本身不會被刪除。`

---

### Step 2B：未連結模式

顯示狀態並詢問使用者：
```
📋 專案：<資料夾名稱>
🔗 尚未連結 Slack Canvas

請選擇操作：
1. 🆕 建立新 Canvas（從 progress.md 內容建立）
2. 🔗 連結既有 Canvas（輸入 Canvas ID 或 URL）
3. ⏭️ 跳過
```

**選 1（建立新 Canvas）：**
- 標題：`📋 <資料夾名稱> 進度追蹤`
- 內容：將 progress.md 內容（排除 frontmatter 和 `### Slack Canvas` 區段）轉為 Canvas Markdown 格式
- 使用 `slack_create_canvas` 建立
- 將回傳的 Canvas ID 和 URL 寫入 progress.md 的 `### Slack Canvas` 區段
- 顯示：`✅ Canvas 已建立！🔗 <Canvas URL>`

**選 2（連結既有 Canvas）：**
- 詢問使用者輸入 Canvas ID（格式如 `F08XXXXXXXX`）或 Canvas URL
- 如果輸入的是 URL，從中擷取 Canvas ID
- 使用 `slack_read_canvas` 驗證 Canvas 存在且可讀取
- 將 Canvas ID 和 URL 寫入 progress.md 的 `### Slack Canvas` 區段
- 顯示：`✅ 已連結！🔗 <Canvas URL>`

**選 3（跳過）：**
- 顯示：`⏭️ 已跳過。下次可以再使用 /canvas 連結。`

---

## progress.md 擴充格式

在 progress.md 現有內容的最後，新增以下區段：

```markdown
### Slack Canvas
- Canvas ID: F08XXXXXXXX
- Canvas URL: https://xxx.slack.com/canvas/...
- 最後同步：YYYY-MM-DD HH:MM
```

> 注意：同步到 Canvas 時，排除 frontmatter（`---` 區塊）和 `### Slack Canvas` 區段本身，只同步實際進度內容。

## Canvas 內容格式轉換

將 progress.md 轉為 Canvas 時，保持 Markdown 格式，但注意：
- 移除 frontmatter（`---` 包圍的 YAML 區塊）
- 移除 `### Slack Canvas` 區段
- emoji（✅ 🔄 等）保留原樣
- Headers 不超過 3 層（`###`）
- 不在內容中重複 Canvas 標題

## 注意事項

- 所有輸出使用繁體中文
- 每個選擇都需要使用者明確確認才執行
- 同步操作會覆寫目標內容，操作前已透過差異摘要讓使用者知情
- 如果 `slack_read_canvas` 或 `slack_create_canvas` 失敗，顯示錯誤訊息並建議使用者檢查 Slack 連線
