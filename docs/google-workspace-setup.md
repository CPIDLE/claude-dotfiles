# Google Workspace 整合設定指南

本文件說明如何設定 `/pm sync` 和 `/pm bye` 所需的兩個 Google 外部整合：
1. **Google Chat Webhook** — 進度更新通知
2. **Google Sheet + Apps Script** — Dashboard 專案總覽

完成後將三個 ID 填入 `~/.claude/CLAUDE.md` 的關鍵 ID 表即可啟用。

---

## 架構概覽

```
/pm sync
  ├── curl POST ──────────────────→ Google Chat Space (Webhook)
  └── curl GET (Base64 payload) ──→ Apps Script Web App
                                          └── Google Sheet (Dashboard)
```

- **Chat 通知**：純 curl，不依賴任何 MCP，所有 session 均可用
- **Dashboard 更新**：Google Apps Script doGet，不需 OAuth，匿名存取即可

---

## Part 1：Google Chat Webhook

### 步驟

1. 開啟 [Google Chat](https://chat.google.com)
2. 點選目標 **Space**（或新建一個）
3. 點右上角 **Space 名稱** → **管理 Webhook**
4. 點 **新增 Webhook**，輸入名稱（例如 `Claude PM`），點儲存
5. 複製產生的 Webhook URL，格式如下：

```
https://chat.googleapis.com/v1/spaces/<SPACE_ID>/messages?key=<KEY>&token=<TOKEN>
```

### 測試

```bash
WEBHOOK_URL="<貼上你的 Webhook URL>"

BODY=$(cat <<'EOF'
{"text":"🧪 測試通知 — Claude PM Webhook 設定成功！"}
EOF
)
printf '%s' "$BODY" | curl -s -X POST "$WEBHOOK_URL" \
  -H 'Content-Type: application/json; charset=UTF-8' \
  -d @-
```

成功回應會包含 `"name":"spaces/..."`。

### 填入 CLAUDE.md

```markdown
| Chat Webhook | `https://chat.googleapis.com/v1/spaces/xxx/messages?key=yyy&token=zzz` |
```

---

## Part 2：Google Sheet Dashboard

### 2-1. 建立 Sheet

1. 開啟 [Google Sheets](https://sheets.google.com) → **建立新試算表**
2. 命名為 `Claude Project Dashboard`（或任意名稱）
3. 在第一列輸入欄位標題：

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| ID | 專案名稱 | 簡述 | 狀態 | 本次完成 | 下次預計 | 重要記事 | 最後更新 |

4. 複製網址列中的 **Sheet ID**（`/d/` 後面到 `/edit` 前面的部分）：

```
https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
```

---

### 2-2. 建立 Apps Script

1. 在該 Sheet 中，點選選單 **擴充功能** → **Apps Script**
2. 刪除預設的 `myFunction`，貼上以下完整程式碼：

```javascript
var SHEET_ID = '<貼上你的 SHEET_ID>';  // ← 替換這裡

function doGet(e) {
  try {
    var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : 'read';

    if (action === 'upsert') {
      return handleUpsert(e);
    } else if (action === 'read') {
      return handleRead();
    } else {
      return jsonResponse({ status: 'error', message: 'Unknown action: ' + action });
    }
  } catch (err) {
    return jsonResponse({ status: 'error', message: err.toString() });
  }
}

function handleRead() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheets()[0];
  var data = sheet.getDataRange().getValues();
  return jsonResponse({ status: 'ok', rows: data });
}

function handleUpsert(e) {
  var projectName = e.parameter.project || '';
  var payloadB64 = e.parameter.payload || '';

  if (!projectName) {
    return jsonResponse({ status: 'error', message: 'Missing project name' });
  }

  // Base64 decode
  var payloadJson = Utilities.newBlob(
    Utilities.base64Decode(payloadB64)
  ).getDataAsString();
  var data = JSON.parse(payloadJson);

  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheets()[0];
  var allValues = sheet.getDataRange().getValues();

  // 搜尋 B 欄（index 1）找到專案名稱
  var foundRow = -1;
  for (var i = 1; i < allValues.length; i++) {  // 從第 2 列開始（跳過標題）
    if (allValues[i][1] === projectName) {
      foundRow = i + 1;  // 1-indexed
      break;
    }
  }

  var now = data.updatedAt || Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm');

  if (foundRow > 0) {
    // 更新現有列（C~H 欄，index 3~8）
    sheet.getRange(foundRow, 3).setValue(data.description || '');
    sheet.getRange(foundRow, 4).setValue(data.status || '');
    sheet.getRange(foundRow, 5).setValue(data.completed || '');
    sheet.getRange(foundRow, 6).setValue(data.next || '');
    sheet.getRange(foundRow, 7).setValue(data.notes || '');
    sheet.getRange(foundRow, 8).setValue(now);
    return jsonResponse({ status: 'ok', action: 'updated', row: foundRow });
  } else {
    // 新增列：自動分配 ID
    var lastRow = sheet.getLastRow();
    var newId = generateId(sheet, lastRow);
    sheet.appendRow([
      newId,
      projectName,
      data.description || '',
      data.status || '',
      data.completed || '',
      data.next || '',
      data.notes || '',
      now
    ]);
    return jsonResponse({ status: 'ok', action: 'inserted', id: newId });
  }
}

function generateId(sheet, lastRow) {
  // 格式：A-001, A-002...
  if (lastRow <= 1) return 'A-001';
  var lastId = sheet.getRange(lastRow, 1).getValue();
  var match = String(lastId).match(/^([A-Z]+)-(\d+)$/);
  if (match) {
    var prefix = match[1];
    var num = parseInt(match[2]) + 1;
    return prefix + '-' + String(num).padStart(3, '0');
  }
  return 'A-' + String(lastRow).padStart(3, '0');
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. 將 `var SHEET_ID = '<貼上你的 SHEET_ID>';` 中的值替換為你的 Sheet ID
4. 點選上方的 **儲存** 圖示（或 Ctrl+S）

---

### 2-3. 部署 Web App

1. 點選右上角 **部署** → **新增部署**
2. 點選齒輪圖示 → 選 **網路應用程式**
3. 設定：
   - **說明**：`Claude PM Dashboard`
   - **以下列身分執行**：`我（你的 Google 帳號）`
   - **誰可以存取**：`所有人`（必須選這個，否則 curl 無法匿名存取）
4. 點 **部署**
5. 複製 **網路應用程式 URL** 中的**部署 ID**（`/s/` 後面到 `/exec` 前面的部分）：

```
https://script.google.com/macros/s/<DEPLOYMENT_ID>/exec
```

### 測試

```bash
DEPLOYMENT_ID="<貼上你的部署 ID>"
APPS_URL="https://script.google.com/macros/s/${DEPLOYMENT_ID}/exec"

# 測試 read
curl -s -L "${APPS_URL}?action=read"
```

成功回應會包含 `"status":"ok"`。

### 填入 CLAUDE.md

```markdown
| Apps Script Web App | `AKfycbz-...` |
```

---

## Part 3：填入 CLAUDE.md

編輯 `~/.claude/CLAUDE.md`，將三個 ID 填入關鍵 ID 表：

```markdown
## 關鍵 ID

| 項目 | ID |
|---|---|
| Chat Webhook | `https://chat.googleapis.com/v1/spaces/xxx/messages?key=yyy&token=zzz` |
| Dashboard Sheet | `1aBcDeFgHiJkLmNoPqRsTuVwXyZ...` |
| Apps Script Web App | `AKfycbz-...` |
```

完成後執行 `/pm sync` 即可驗證整合是否正常。

---

## 常見問題

### curl 回傳 `{"error":{"code":400}}`
→ Webhook URL 不正確，重新從 Chat Space 複製。

### curl 回傳 302 但內容空白
→ Apps Script 部署設定中「誰可以存取」未選「所有人」，重新部署。

### Dashboard 更新後 Chat 沒有通知（或反之）
→ 兩者互相獨立，任一失敗不影響另一個。查看 `/pm sync` 輸出的錯誤訊息。

### Windows 上中文/emoji 在 Chat 顯示亂碼
→ 必須使用 `printf '%s' "$BODY" | curl ... -d @-` 的 heredoc 寫法，不可用 `-d '{"text":"..."}'` 直接內嵌。

### Apps Script 改了程式碼後沒有生效
→ 必須重新 **部署 → 管理部署 → 建立新版本**，舊的部署 ID 對應的是舊版本。

---

## 相關檔案

| 檔案 | 說明 |
|---|---|
| `~/.claude/CLAUDE.md` | 存放三個關鍵 ID |
| `~/.claude/commands/pm.md` | `/pm` 指令完整邏輯（含 sync/bye 流程） |
| `docs/google-workspace-setup.md` | 本文件 |
