# SC (Slack Canvas) — Slack Canvas 進度同步

將專案 `progress.md` 與 Slack Canvas 雙向同步，自動判斷狀態並引導操作。

## 執行步驟

請依序完成以下所有步驟，不要跳過：

### Step 0：檢查 progress.md

使用 Glob 搜尋 `**/memory/progress.md` 定位 progress.md。

**如果 progress.md 不存在：**
```
⚠️ 找不到 progress.md。
💡 請先執行 /hello new 建立專案進度，再使用 /sc 同步。
```
**直接結束。**

---

### Step 1：讀取 progress.md 並判斷狀態

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

### Step 3：發送摘要到 #all-cpidle

每次 `/sc` 完成同步操作（Step 2A 選 1 或選 2、Step 2B 選 1）後，自動發送摘要訊息到 `#all-cpidle`（Channel ID: `C0AN35HJQ8L`）。

**摘要訊息格式：**
```
📋 *<專案名稱> — 進度更新*

<從 progress.md 擷取 3-5 個重點，每項一行，使用 bullet points>

🔗 <Canvas URL|完整進度>
```

**擷取重點規則：**
- 優先列出「今日完成」或最近的已完成項目（✅）
- 其次列出「進行中」項目（🔄）
- 最後列出「下一步」或待辦項目
- 總共不超過 5 項，保持精簡
- 每項不超過一行

**注意：**
- Step 2A 選 3（只看）和選 4（取消連結）不發送摘要
- 使用 `slack_send_message` 發送，不需額外確認（同步操作本身已經確認過）

---

### Step 4：更新專案總覽 Dashboard

每次 `/sc` 完成同步操作後（與 Step 3 同時機），自動更新「📊 專案總覽 Dashboard」Canvas（ID: `F0AMWD1GAD9`）。

**流程：**
1. 使用 `slack_read_canvas`（canvas_id: `F0AMWD1GAD9`）讀取 Dashboard 現有內容
2. 取得 section_id_mapping，找到當前專案名稱對應的 section
3. 根據 progress.md 內容，產生該專案的摘要區段

**每個專案區段格式：**
```markdown
## 🔹 <專案名稱>
狀態：<開發中 / 規劃中 / 已完成 / 維護中>
- ✅ <最近完成的 1-2 項>
- 🔄 <進行中的 1-2 項>
- 📌 <待辦的 1-2 項>
🔗 [完整進度](<該專案的 Canvas URL>)
```

**更新邏輯：**
- **專案已存在於 Dashboard**：使用 `slack_update_canvas`（action=replace, section_id=對應區段）更新該專案區段
- **專案不存在於 Dashboard**：使用 `slack_update_canvas`（action=append）新增該專案區段
- 在 Dashboard 最末尾更新「最後更新：YYYY-MM-DD HH:MM」

**注意：**
- Dashboard Canvas ID（`F0AMWD1GAD9`）為固定值
- 只更新當前專案的區段，不影響其他專案
- Step 2A 選 3（只看）和選 4（取消連結）不更新 Dashboard

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
- **移除與 Canvas 標題重複的頂層標題**（例如 progress.md 開頭的 `# 專案名稱` 如果跟 Canvas 標題相同或相似，必須移除，避免標題重複顯示）
- emoji（✅ 🔄 等）保留原樣
- Headers 不超過 3 層（`###`）

## 注意事項

- 所有輸出使用繁體中文
- 每個選擇都需要使用者明確確認才執行
- 同步操作會覆寫目標內容，操作前已透過差異摘要讓使用者知情
- 如果 `slack_read_canvas` 或 `slack_create_canvas` 失敗，顯示錯誤訊息並建議使用者檢查 Slack 連線
