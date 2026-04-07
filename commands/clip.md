# Clip — 剪貼簿截圖分析

先儲存剪貼簿圖片，再依使用者指示分析。

## 執行步驟

### Step 1：儲存剪貼簿圖片

執行以下命令將剪貼簿圖片存到 Claude Code 工作目錄：

```bash
powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; \$img=[System.Windows.Forms.Clipboard]::GetImage(); if(\$img){ \$p=Join-Path (Get-Location) 'clip.png'; \$img.Save(\$p); Write-Output 'saved' } else { Write-Output 'no_image'; exit 1 }"
```

- 如果輸出 `no_image`，告知使用者「剪貼簿沒有圖片，請先截圖（Win+Shift+S）」然後停止。
- 如果輸出 `saved`，繼續下一步。

### Step 2：讀取圖片

用 Read 工具讀取工作目錄下的 `clip.png`（即 `$CWD/clip.png`）。

### Step 3：分析圖片

根據使用者的附加指示（$ARGUMENTS）分析圖片內容。

- 如果沒有附加指示，預設進行「圖片內容摘要分析」
- 用繁體中文回覆
