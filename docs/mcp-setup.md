# OpenCode MCP 設定指南

## 什麼是 MCP

MCP（Model Context Protocol）是一個開放協議，讓 AI 工具能與外部服務和系統整合。

## 設定架構

OpenCode 的 MCP 設定分為兩層：

| 層級 | 路徑 | 用途 |
|------|------|------|
| 全域 | `~/.config/opencode/opencode.json` | 所有專案共用，預設關閉 |
| 專案 | `<專案根目錄>/opencode.json` | 專案層級覆蓋，可啟用特定 MCP |

### 設定格式（正確寫法）

```json
{
  "mcp": {
    "<mcp-name>": {
      "type": "local",
      "enabled": false,
      "command": ["可執行檔", "參數1", "參數2"]
    }
  }
}
```

> **重要限制（v1.3.13 驗證）：**
> - `type` 只支援 `"local"`，不支援 `"stdio"`
> - `command` 必須是陣列，不可用字串 + `args` 分開寫
> - **不支援 `env` 欄位**（會導致 config validation 失敗）
> - `enabled` 支援 `true`/`false`

---

## 全域設定（預設關閉）

檔案：`~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "google/gemini-3.1-pro-preview",
  "provider": {
    "google": {
      "options": {
        "apiKey": "{env:GEMINI_API_KEY}"
      },
      "models": {
        "gemini-3.1-pro-preview": {},
        "gemini-3-flash-preview": {},
        "gemini-2.5-pro": {},
        "gemini-2.5-flash": {}
      }
    }
  },
  "mcp": {
    "playwright": {
      "type": "local",
      "enabled": false,
      "command": ["npx", "-y", "@playwright/mcp"]
    },
    "windows-mcp": {
      "type": "local",
      "enabled": false,
      "command": ["<uvx.exe 絕對路徑>", "windows-mcp"]
    },
    "google-workspace": {
      "type": "local",
      "enabled": false,
      "command": ["npx", "-y", "google-workspace-mcp", "serve"]
    }
  }
}
```

> `windows-mcp` 的 `uvx.exe` 路徑因電腦不同而異，需替換為實際路徑。
> 查詢方式：`where uvx` 或 `Get-Command uvx`

## 專案層級啟用

在專案的 `opencode.json` 加入需要的 MCP 並設 `enabled: true`：

```json
{
  "mcp": {
    "windows-mcp": {
      "type": "local",
      "enabled": true,
      "command": ["<uvx.exe 絕對路徑>", "windows-mcp"]
    }
  }
}
```

---

## 目前可用的 MCP

### 1. playwright

瀏覽器自動化（網頁操作、截圖、測試）。

```
npx -y @playwright/mcp
```

無需額外設定。

### 2. windows-mcp

作業系統層級控制（檔案、系統管理、PowerShell）。

```
uvx windows-mcp
```

前置安裝：
```bash
# 安裝 uv（如尚未安裝）
pip install uv
```

### 3. google-workspace

整合 Gmail、Calendar、Docs、Drive、Sheets 等 Google 服務。

```
npx -y google-workspace-mcp serve
```

#### 前置設定步驟

1. **建立 Google Cloud OAuth 憑證**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 建立或選擇專案
   - 啟用所需 API（Gmail API、Calendar API 等）
   - 前往 **API 和服務** > **OAuth 同意畫面**：User Type 選「外部」，在「測試使用者」加入自己的 Email
   - 前往 **API 和服務** > **憑證** > **建立憑證** > **OAuth 用戶端 ID**
   - 類型選「電腦版應用程式」，建立後下載 JSON

2. **放置憑證檔案**
   ```powershell
   mkdir -Force ~/.google-mcp
   # 將下載的 JSON 複製並改名為 credentials.json
   cp ~/Desktop/client_secret_*.json ~/.google-mcp/credentials.json
   ```

3. **新增帳號並授權**
   ```bash
   npx -y google-workspace-mcp accounts add <帳號名稱>
   ```
   瀏覽器會自動開啟，完成 Google 帳號授權即可。

---

## 新電腦快速設定

```powershell
# 1. 環境變數（加到系統或 .env）
$env:GEMINI_API_KEY = "your_key"
$env:GOOGLE_GENERATIVE_AI_API_KEY = "your_key"

# 2. 安裝 opencode
winget install SST.opencode

# 3. 複製全域設定
mkdir -Force ~/.config/opencode
# 將本 repo 的 opencode-config/global-opencode.json 複製過去
cp opencode-config/global-opencode.json ~/.config/opencode/opencode.json
# 編輯 windows-mcp 的 uvx.exe 路徑（執行 where uvx 取得）

# 4. Google Workspace 憑證（如需使用）
mkdir -Force ~/.google-mcp
# 放入 credentials.json（從 Google Cloud 下載）
npx -y google-workspace-mcp accounts add <帳號名稱>

# 5. 專案 .env
cp opencode-config/.env.example .env
# 編輯 .env 填入 API key
```

## 常見問題

| 問題 | 原因 | 解法 |
|------|------|------|
| `Invalid input mcp.<name>` | 使用了不支援的欄位（`env`、`args`、`type: "stdio"`） | 改用 `type: "local"` + `command` 陣列，移除 `env`/`args` |
| opencode 無法啟動 | MCP config validation 失敗 | 檢查 JSON 格式和欄位名稱 |
| google-workspace 認證失敗 | 缺少 credentials.json 或未授權 | 依前置設定步驟操作 |
| uvx 找不到 | 路徑不對或未安裝 | `pip install uv` 後用 `where uvx` 確認路徑 |

## 相關檔案

- 全域設定範本：`opencode-config/global-opencode.json`
- 專案設定範本：`opencode-config/opencode.json`
- 環境變數範本：`opencode-config/.env.example`
- Google 憑證目錄：`~/.google-mcp/`
