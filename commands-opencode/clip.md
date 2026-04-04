---
description: 剪貼簿截圖分析
---
先儲存剪貼簿圖片，再依使用者指示分析。

## 執行步驟

### Step 1：儲存剪貼簿圖片

執行以下命令將剪貼簿圖片存到工作目錄：

```bash
python -c "from PIL import ImageGrab; img=ImageGrab.grabclipboard(); exit(1) if not img else (img.save('clip.png'), print('saved'))"
```

- 如果輸出 `no_image`，告知使用者「剪貼簿沒有圖片，請先截圖（Win+Shift+S）」然後停止。
- 如果輸出 `saved`，繼續下一步。

### Step 2：讀取圖片

讀取工作目錄下的 `clip.png`。

### Step 3：分析圖片

根據使用者的附加指示（$ARGUMENTS）分析圖片內容。

- 如果沒有附加指示，預設進行「圖片內容摘要分析」
- 用繁體中文回覆
