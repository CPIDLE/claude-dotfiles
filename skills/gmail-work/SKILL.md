---
name: gmail-work
description: "Work Gmail skill — same Python tooling as the personal `gmail` skill but bound to the work account chipinkuo@gyro.com.tw via a separate OAuth token. Trigger when the user mentions work mail, 公司信箱, 工作信箱, GYRO email, chipinkuo, or explicitly asks to draft/send/read mail from the work account. For personal mail (benthamkuo@gmail.com) use the `gmail` skill instead. This skill uses direct Google API access with its own stored credentials, independent of any MCP connector."
---

# Gmail Work Skill

Same script + commands as the `gmail` skill, but bound to **chipinkuo@gyro.com.tw** via a separate `assets/token.json`. Use this when the user wants to draft / send / read mail from the work account.

## When to use which

| 信箱 | Skill | Token 位置 |
|------|-------|------------|
| benthamkuo@gmail.com（個人） | `gmail` | `~/.claude/skills/gmail/assets/token.json` |
| chipinkuo@gyro.com.tw（工作） | `gmail-work` | `~/.claude/skills/gmail-work/assets/token.json` |

Pick by which sender / inbox the user actually means. If unclear, ask.

## Setup（首次使用）

依賴與 `gmail` skill 相同：

```bash
pip install google-auth-oauthlib google-api-python-client
```

### 一次性認證流程

1. **準備 OAuth client**（兩種選一）
   - **共用**（簡單）：複製 `~/.claude/skills/gmail/assets/client_secret.json` 到 `~/.claude/skills/gmail-work/assets/client_secret.json`
   - **獨立**（GYRO Workspace 政策需要時）：去 Google Cloud Console 建一個 GYRO 專案的 Desktop OAuth client，下載放到 `~/.claude/skills/gmail-work/assets/client_secret.json`

2. **觸發 OAuth 登入**：執行任一指令（會開瀏覽器）：

   ```powershell
   # PowerShell
   $env:PYTHONIOENCODING="utf-8"
   python "$HOME\.claude\skills\gmail-work\scripts\gmail_ops.py" profile
   ```

   ```bash
   # bash / WSL
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/gmail-work/scripts/gmail_ops.py profile
   ```

3. **登入時務必選 chipinkuo@gyro.com.tw**（不是個人 gmail）。token 會存到 `assets/token.json`，之後自動 refresh。

4. 確認綁對帳號：`profile` 應回傳 `emailAddress: chipinkuo@gyro.com.tw`。

## How to use

完全相同的 CLI 介面，只是路徑換成 `gmail-work`：

```bash
PYTHONIOENCODING=utf-8 python "C:/Users/benth/.claude/skills/gmail-work/scripts/gmail_ops.py" <command> [options]
```

可用指令、參數、範例 → 參考 `~/.claude/skills/gmail/SKILL.md`（相同腳本）。

### 常用範例（工作信箱）

```bash
# 寫草稿（HTML）
python gmail_ops.py draft --to "team@gyro.com.tw" --subject "週報" --body "<h1>...</h1>" --html

# 帶附件寄出
python gmail_ops.py send-attach --to "..." --subject "..." --body "..." --attachments report.pdf

# 搜尋未讀
python gmail_ops.py search --query "is:unread newer_than:3d" --max-results 20

# 強制重新登入（換帳號或 token 壞掉）
python gmail_ops.py auth
```

## 注意事項

- **不要混用 token**：兩個 skill 各有自己的 `assets/token.json`，互不影響。
- **install.ps1 會覆蓋 SKILL.md 與 scripts/**，但**不會動 assets/**（token 與 client_secret 安全）。
- **Workspace 限制**：若 GYRO admin 限制第三方 app，OAuth 步驟可能被擋。需請 IT 將 client_id 加白名單，或改用 Workspace 自己的 OAuth client。
- **Scope**：`gmail.modify` + `gmail.compose` + `gmail.send`（與個人版相同）。
