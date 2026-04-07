使用者需求：$ARGUMENTS

請使用 GYRO Report skill 產生 GYRO Systems 品牌化 HTML 簡報。

> **流水線**: `/gyro-kb <客戶需求>` 產 .md 內容 → `/report-gyro <.md> <.html>` 產 HTML/PDF/Excel 排版
> 本 command 負責排版，不負責報告內容撰寫。輸入必須是已完成的 .md 檔。要產報告內容請先用 `/gyro-kb`。

## 工作流程

1. **讀取** skill 規範：`.claude/skills/report-gyro/SKILL.md`
2. **讀取** Marp theme：`.claude/skills/report-gyro/assets/gyro-marp-theme.css`
3. **讀取** 使用者指定的 Markdown 來源檔
4. **收集圖片** 如果 MD 中有 `![alt](path)` 引用，收集圖片檔案
5. **分析** 文件結構，將各段落對應到投影片類型（cover、section、content、table、two-column、stats、feature-grid、**full-image**、**image-content**、closing 等 11 種）
6. **產生** HTML + images/ 資料夾（folder mode，預設）
7. **寫入** 輸出檔案

## 用法

```
/report-gyro <source.md> <output.html>
```

若使用者只提供來源檔，輸出檔名預設為同名 `.html`。

## 圖片處理

- **Folder mode (預設)**：圖片存放於 `images/` 子資料夾，HTML 使用相對路徑 `images/xxx.png`
  - 輸出結構：`output_folder/presentation.html` + `output_folder/images/*.png`
  - HTML 僅 ~50-60KB，輕量好管理
- **Single-file mode**：使用者明確要求時，圖片嵌入為 base64
- MD 中的 `![alt](path)` + 後續說明文字 → **image-content** slide（圖文並排）
- MD 中的 `![alt](path)` 單獨出現 → **full-image** slide（全幅圖片）

## 注意事項

- Marp theme 從 `gyro-marp-theme.css` 載入（不嵌入，由 `--theme` 指定）
- 流程圖優先使用 D2 (`d2 --layout=elk in.d2 out.png`)；不適合 D2 的圖（時序圖、gantt、ER、心智圖、圓餅圖等）才使用 Mermaid
- 遵循 skill 規範中的 11 種投影片類型與品牌色彩 (#BD442C)
- 大型 HTML 檔案修改時使用 Grep + offset Read + Edit 技巧
