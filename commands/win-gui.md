# win-gui — Windows GUI 自動化操作

接收自然語言指令，透過 win_drive MCP 操作 Windows 桌面程式。

使用方式：`/win-gui <指令>`
範例：`/win-gui 開啟記事本輸入 Hello World 存到桌面然後關閉`

---

## 執行步驟

收到使用者指令 `$ARGUMENTS` 後，依照以下 4 Phase 模型拆解並執行。

### Phase 1：啟動程式

1. 先用 `computer_window_list` 檢查目標程式是否已在執行
2. **已執行** → `computer_window_focus(title="<視窗標題>")`
3. **未執行** → 用 Bash 啟動（`powershell -c "Start-Process <exe>"`），再用 batch `wait_for_window` 等待視窗出現：
```json
{"type": "wait_for_window", "window_title": "<標題>", "timeout": 5000}
```

### Phase 2：操作

**元素定位優先順序**（嚴格遵守）：

1. **`ui_click` 按名稱**（最可靠）— 原生 Win32/WPF 程式的按鈕、選單、工具列
2. **鍵盤快捷鍵** — Ctrl+S、Ctrl+Z、Alt+F4 等通用操作
3. **視窗截圖 → 推算座標** — Electron app 內部元素、畫布區域
4. **全螢幕截圖 → 推算座標** — 最後手段

**程式類型判斷**：
- **原生 Win32/WPF**（小畫家、記事本、Office）→ UIA 元素完整，優先 `ui_click`
- **Electron**（VS Code、Discord、Slack）→ UIA 只有視窗層級，內部元素必須用座標
- **瀏覽器**（Chrome、Edge）→ 類似 Electron，可用 Tab/Enter 鍵盤導航，Ctrl+L 輸入 URL

**關鍵規則**：
- 所有 `key` / `type` action **必須帶 `window_title`**，否則按鍵會送到前景視窗（可能是 Claude Code 終端）
- 盡量用 `computer_batch` 合併多個動作為一次呼叫，減少 round-trip
- 不確定 UI 結構時，先用 `computer_ui_inspect` 探索控件樹

### Phase 3：存檔

**通用 Windows 另存新檔流程**（適用大多數程式）：
```json
[
  {"type": "key", "key": "ctrl+s", "window_title": "<app>"},
  {"type": "sleep", "ms": 1500},
  {"type": "key", "key": "ctrl+a"},
  {"type": "type", "text": "<完整檔案路徑含副檔名>"},
  {"type": "sleep", "ms": 300},
  {"type": "key", "key": "Enter"},
  {"type": "sleep", "ms": 1000},
  {"type": "key", "key": "alt+y"},
  {"type": "sleep", "ms": 500}
]
```
- 檔名欄可直接輸入完整路徑（如 `C:\Users\benth\Desktop\test.txt`），免手動切換資料夾
- 覆蓋確認用 `alt+y` 快捷鍵

### Phase 4：關閉

```json
{"type": "key", "key": "alt+f4", "window_title": "<app>"}
```
- 若有未存檔提示，用 `alt+y` 或 `ui_click` 確認

---

## 聚焦與控件操作（重要）

### 聚焦視窗：永遠用 `window_focus`
- **禁止用 click 點擊工作區來聚焦**。若當前工具處於編輯/繪圖模式，click 會產生副作用（畫點、插入游標、選取文字等），且這些副作用可能無法 Ctrl+Z 還原
- 正確做法：`computer_window_focus(title="<app>")` → 再執行後續操作

### 對話框可能不出現時的防禦策略
- 確認對話框（儲存、覆蓋、關閉）**不一定每次都出現**（例如檔案未修改時不會提示儲存）
- `ui_click` 找不到元素 → batch 中斷 → 後續步驟全部丟失
- **策略 A**（優先）：用鍵盤快捷鍵替代 `ui_click`（如 `alt+n` 代替 `ui_click("不要儲存")`），即使對話框沒出現也無害
- **策略 B**：把不確定步驟拆成獨立 batch，失敗不影響後續

### 調整控件前先切換到安全工具
- Slider、色盤等 UI 控件的 click 可能同時觸發工作區操作（例如繪圖工具啟用時點 slider 會在畫布留痕）
- **做法**：先切到「選取」或其他非輸入工具 → 調整控件 → 再切回目標工具
- `ui_set_value` 對某些控件可能有非預期效果，優先用 click + 方向鍵微調

---

## 並行與效率

### 獨立 MCP 呼叫可並行發出
- 多個互不依賴的工具呼叫（如多個 `draw_path`、多個 `ui_find`）可在同一輪 parallel tool call 同時發出
- `computer_batch` 合併的是**順序相依**的動作；**互不相依**的操作用 parallel tool call 更快

### 截圖策略
- **僅最後一步截圖**確認最終結果（`screenshot: true`）
- 中間步驟全部 `screenshot: false`
- **唯一例外**：batch 回傳 error 時，截圖診斷失敗原因

---

## 座標系統

| 來源 | 換算公式 | 說明 |
|------|----------|------|
| `ui_find` 回傳 | 直接用 `click_x`, `click_y` | 最可靠 |
| 全螢幕截圖（半尺寸 960x600） | `螢幕座標 = 圖片座標 * 2` | 常見模式 |
| 全螢幕截圖（原尺寸） | `螢幕座標 = 圖片座標` | 直接使用 |

---

## batch action types 速查

| type | 必要參數 | 說明 |
|------|----------|------|
| `key` | `key` | 按鍵組合，如 `"ctrl+c"`, `"Enter"` |
| `type` | `text` | Unicode 文字輸入 |
| `click` | `x`, `y` | 座標點擊，可加 `button`, `action` |
| `ui_click` | `name` | 按 UI 元素名稱點擊，可加 `role`, `index` |
| `scroll` | `x`, `y`, `direction` | 滾輪，可加 `amount` |
| `sleep` | `ms` | 固定等待（上限 30s） |
| `wait_for_window` | `window_title` | 等視窗出現，可加 `timeout` |
| `wait_for_element` | `name` | 等 UI 元素出現，可加 `timeout` |
| `ui_set_value` | `name`, `value` | 設定元素值（Edit/ComboBox） |

所有 action 可加 `"window_title"` 指定視窗、`"screenshot": true` 拍中間截圖。
batch 遇錯即停，回傳 `{completed, total, error, log}`。

---

## 執行原則

1. **最少 MCP 呼叫數** — batch 合併順序動作，parallel call 並行獨立動作
2. **不要盲猜座標** — 先 `ui_inspect` 或截圖確認，再操作
3. **僅最終截圖** — 中間不截圖不輸出分析文字，只在 error 時截圖診斷
4. **出錯時回報** — 如果 batch 回傳 error，分析失敗步驟並嘗試替代方案
5. **繁體中文回覆**
