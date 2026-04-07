# Report Gyro Skill — Claude Desktop 手動載入 SOP

## 前置條件

確認 skill 目錄結構完整：

```
.claude/skills/report-gyro/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   └── gyro-marp-theme.css               ← Marp theme
└── scripts/
    └── gen_verification.py               ← Excel 驗算產生器
```

## 載入步驟（Claude Desktop）

1. 開啟 **Claude Desktop**
2. 進入 **Customize** > **Skills**
3. 點擊右上角 **+** 按鈕
4. 選擇本 repo 內的 SKILL.md，例如：

   ```
   E:\github\claude-dotfiles\skills\report-gyro\SKILL.md
   ```

5. 確認 "My skills" 列表出現 **report-gyro**
6. 展開確認子資料夾（assets、scripts）也被載入

## 驗證

載入後輸入：

```
/report-gyro test.md test.html
```

或觸發詞：「產生 GYRO 簡報」、「GYRO presentation」、「鑫蒂斯簡報」。

## 注意事項

- Desktop 若只載入 SKILL.md 而沒複製 assets/，需要手動將整個 `report-gyro/` 目錄複製到：
  ```
  %APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\...\skills\report-gyro\
  ```
  並在 manifest.json 中新增：
  ```json
  {
    "skillId": "report-gyro",
    "name": "report-gyro",
    "description": "Generate GYRO Systems presentation drafts (Marp / Gamma / Excel)",
    "creatorType": "user",
    "updatedAt": "<當前 ISO 時間>",
    "enabled": true
  }
  ```

## Claude Code CLI 使用方式（已設定）

```
/report-gyro <source.md> <output.html>
```

不需額外設定 — install.ps1 會把 commands/ 與 skills/ 同步到 `~/.claude/`。
