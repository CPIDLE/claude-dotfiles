使用者需求：$ARGUMENTS

請使用 **md-to-deck** skill 將 Markdown 文件轉為 GYRO 品牌 single-file HTML 投影片（可選擇再印 PDF）。

## 用途定位

- **md-to-deck**（本 skill）= MD → GYRO 品牌投影片 HTML（→ puppeteer PDF）
- **md-to-paper** = MD → A4 直/橫 白皮書 HTML（長文閱讀用）
- **md-to-pptx** = MD → PptxGenJS .pptx

## 流程

1. **讀取** skill 規範：`~/.claude/skills/md-to-deck/SKILL.md`（11 種 slide type mapping、品牌 CSS、puppeteer PDF 步驟）
2. **讀取** 來源 `.md`，依 H1/H2/H3 + table/list/mermaid/image 結構切 slide
3. **內嵌** `assets/gyro_css_template.css` 整份至 `<style>`，並加 Mermaid runtime + 鍵盤/觸控導航 JS
4. **輸出** single-file `.html`（外部圖片走相對路徑 `images/`）
5. **（選用）** 動態產 `_gen_pdf.js`，跑 `node _gen_pdf.js` 印 A4 PDF，最後清掉腳本
6. **（選用）** 抽出計算參數 → `params.json` → `python scripts/gen_verification.py` 產 `verification.xlsx`

## 用法

```
/md-to-deck <source.md> [output.html]
```

## 注意

- `@media print` 必須同時 override `html` 與 `body` 背景，否則 dark `--bg` 會 bleed 成黑頁（`gyro_css_template.css` L227-237 已修）
- puppeteer-core 可重用 marp-cli 自帶的版本：`%APPDATA%\npm\node_modules\@marp-team\marp-cli\node_modules\puppeteer-core`
- system Chrome 路徑：`C:\Program Files\Google\Chrome\Application\chrome.exe`
