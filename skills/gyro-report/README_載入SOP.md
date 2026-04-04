# GYRO Report Skill — Claude Desktop 手動載入 SOP

## 前置條件

確認 skill 目錄結構完整：

```
.claude/skills/gyro-report/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   ├── gyro_css_template.css             ← CSS 模板（必須）
│   ├── gyro_style_template.json          ← 品牌設計規範
│   └── content_sample.json              ← JSON schema 範例
└── scripts/
    └── gyro_html_generator.js            ← Legacy JSON→HTML 產生器
```

## 載入步驟

1. 開啟 **Claude Desktop**
2. 進入 **Customize** > **Skills**
3. 點擊右上角 **+** 按鈕
4. 選擇以下檔案：

   ```
   C:\Users\benth\Documents\Project\.doc\.claude\skills\gyro-report\SKILL.md
   ```

5. 確認 "My skills" 列表出現 **gyro-report**
6. 展開確認子資料夾（assets、scripts）也被載入

## 驗證

載入後，在 Claude Desktop 對話中輸入：

```
/gyro-report test.md test.html
```

或直接輸入以下觸發詞測試自動觸發：
- 「產生 GYRO 簡報」
- 「GYRO presentation」
- 「鑫蒂斯簡報」

## 注意事項

- 如果 Desktop 只載入 SKILL.md 而**沒有複製 assets 資料夾**，需要手動將整個 `gyro-report/` 目錄複製到：
  ```
  %APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\...\skills\gyro-report\
  ```
  並在同層的 `manifest.json` 中新增一筆：
  ```json
  {
    "skillId": "gyro-report",
    "name": "gyro-report",
    "description": "Generate GYRO Systems branded HTML slide presentations...",
    "creatorType": "user",
    "updatedAt": "<當前 ISO 時間>",
    "enabled": true
  }
  ```

## Claude Code CLI 使用方式（已設定）

在 Claude Code 中直接輸入：
```
/gyro-report <source.md> <output.html>
```
不需要額外設定。
