---
description: Windows GUI 自動化操作
---
接收自然語言指令，透過 win_drive MCP 操作 Windows 桌面程式。

使用方式：`/win-gui <指令>`

---

## 執行步驟

收到使用者指令 `$ARGUMENTS` 後，依照以下 4 Phase 模型拆解並執行。

### Phase 1：啟動程式

1. 先用 `computer_window_list` 檢查目標程式是否已在執行
2. **已執行** → `computer_window_focus(title="<視窗標題>")`
3. **未執行** → 用 Bash 啟動（`powershell -c "Start-Process <exe>"`），再用 batch `wait_for_window` 等待視窗出現

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
- 所有 `key` / `type` action **必須帶 `window_title`**
- 盡量用 `computer_batch` 合併多個動作為一次呼叫
- 不確定 UI 結構時，先用 `computer_ui_inspect` 探索控件樹

### Phase 3：存檔

**通用 Windows 另存新檔流程**：
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

### Phase 4：關閉

```json
{"type": "key", "key": "alt+f4", "window_title": "<app>"}
```

---

## 執行原則

1. **最少 MCP 呼叫數** — batch 合併順序動作，parallel call 並行獨立動作
2. **不要盲猜座標** — 先 `ui_inspect` 或截圖確認，再操作
3. **僅最終截圖** — 中間不截圖，只在 error 時截圖診斷
4. **出錯時回報** — 分析失敗步驟並嘗試替代方案
5. **繁體中文回覆**
