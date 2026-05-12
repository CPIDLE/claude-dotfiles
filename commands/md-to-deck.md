使用者需求：$ARGUMENTS

請使用 **md-to-deck** skill 將 Markdown 文件轉為 GYRO 品牌 single-file HTML 投影片（可選擇再印 PDF）。

## 用途定位

- **md-to-deck**（本 skill）= MD → GYRO 品牌投影片 HTML（→ puppeteer PDF）
- **md-to-paper** = MD → A4 直/橫 白皮書 HTML（長文閱讀用）
- **md-to-pptx** = MD → PptxGenJS .pptx

## 流程

0. **Stage 0 — 詢問是否先產生投影片稿**（用 AskUserQuestion）：
   - **選項 A：先產投影片稿** — 讀來源 `.md`，精簡成 ~10 主題、含 ASCII art + Markdown 表格、文字精簡，寫入 `<stem>_slides.md`；給 outline 給使用者 confirm 後再寫；寫完**強制跑 ascii-align**（`python ~/.claude/skills/ascii-align/scripts/ascii_align.py <stem>_slides.md`）校正 ASCII art，未過不續跑；之後再以 `_slides.md` 為來源走步驟 2–5
   - **選項 B：直接產 HTML** — 跳過精簡，直接以原 `.md` 走步驟 2–5
   - **選項 C：只產投影片稿** — 寫完 `_slides.md` 就停，不轉 HTML
   - 來源 `.md` 看起來已經是 slide-friendly（H2/H3 結構清楚、每節短於一頁）時，預設選 B；否則預設 A。投影片稿規格見 SKILL.md「Stage 0：投影片稿精簡」一節
1. **讀取** skill 規範：`~/.claude/skills/md-to-deck/SKILL.md`（11 種 slide type mapping、品牌 CSS、puppeteer PDF 步驟）
2. **讀取** 來源 `.md`（Stage 0 選 A → `_slides.md`；選 B → 原檔）
   - 來源為 **Slide-draft**（檔名 `*_slides.md` / 剛走完 Stage 0 / `##` 區塊 8–12 且每節 ≤ 1 頁）→ 套 SKILL.md「Slide-draft 規則」：**每個 `## ` = 1 頁 content slide，不插 section divider**，預期投影片數 = `##` 數 + 1（封面）
   - 來源為 **Long-form**（章節深、長度不均）→ 套「Long-form 規則」（`##` = section divider、`###` = content slide）
   - **產出前先講一次預期頁數**給使用者確認，避免膨脹
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
