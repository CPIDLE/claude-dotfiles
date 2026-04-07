---
name: report-easy
description: >
  Convert a plain ASCII Markdown report into a print-ready deliverable in 3 stages:
  (1) ASCII .md → diagram-enriched .md (D2/ELK PNGs preferred, Mermaid only when D2 is unsuitable),
  (2) diagram-enriched .md → A4 portrait HTML (`_直.html`),
  (3) same .md → A4 landscape HTML (`_橫.html`).
  Fully self-contained: HTML templates and helper script live inside this skill folder,
  so it works on any machine without external file dependencies.
  Trigger when: 報告轉 HTML, 直橫版本, 產生白皮書, ASCII 報告加圖, report-easy, /report-easy.
argument-hint: <source.md>
---

# Report Easy — ASCII MD → D2/ELK Diagrams → 直/橫 HTML

## 三階段流程

```
source.md (純文字)
   │
   │  Stage 1: 圖表化（D2/ELK 為主，Mermaid 為輔）
   ▼
source_elk.md  +  ./assets/*.d2  +  ./assets/*_elk.png
   │
   │  Stage 2: 套白皮書 HTML 模板（直 + 橫）
   ▼
source_elk_直.html (A4 portrait)
source_elk_橫.html (A4 landscape)
```

---

## Stage 1：ASCII MD → 圖表化 MD

### 1.1 識別可圖表化段落

讀完整份 `.md`，標記下列適合視覺化的內容：

| 類型 | 工具 |
|---|---|
| 流程 / pipeline / 步驟 | **D2 layered (ELK)** |
| 系統架構分層 | **D2 container + layered** |
| 決策樹 / 條件分支 | **D2 mrtree / 含 diamond** |
| 時間線（事件序列） | **D2 right direction** |
| 比較表（多選項屬性對照） | **D2 卡片並排** |
| 數值曲線 / log-log / 散布圖 | **保留原表格或 matplotlib**（D2/Mermaid 都不適合） |
| 圓餅 / 環形 | **Mermaid pie** |
| 甘特 / 排程 | **Mermaid gantt** |
| 序列圖 (A→B→A) | **Mermaid sequenceDiagram** |
| ER / class | **Mermaid erDiagram / classDiagram** |

> **預設選 D2/ELK**。只有當 D2 無法表達語意時才用 Mermaid。

### 1.2 為每個圖表產生 D2 source

- 檔名：`<source_dir>/assets/<diagram_name>.d2`
- 第一行 `direction: down` 或 `direction: right`
- 共用樣式可複製本 skill 的 `./assets/d2_common.d2`
- **避開 D2 reserved keywords**：`start`, `end`, `near`, `far`, `mid`, `top`, `bottom`, `left`, `right`, `center`, `source`, `target` — 用於節點名稱會導致 `reserved keywords are prohibited in edges` 錯誤。改用 `root`, `n_start`, `band_near` 等
- 含 `$` 符號的標籤必須用 `\$` 跳脫並雙引號包住
- 內聯邊樣式 `a -> b: 標籤 {style.x: y}` 不可用；改為兩行：
  ```
  a -> b: 標籤
  (a -> b)[0].style.stroke-dash: 4
  ```

### 1.3 渲染 PNG（D2 用 ELK layout）

```bash
d2 --layout=elk assets/<name>.d2 assets/<name>_elk.png
```

Mermaid 直接以 ```` ```mermaid ```` fenced block 寫入 MD（marked.js 模板可由 mermaid.js 渲染），或用 `mmdc` 預先生成 PNG。

### 1.4 寫回 MD

- 複製 `source.md` → `source_elk.md`
- 將原本的圖片占位（`![alt](assets/foo.png)`）替換為 `![alt](assets/foo_elk.png)`
- 若原檔無圖片占位但內容適合視覺化，在對應段落插入新的圖片引用

---

## Stage 2/3：MD → 直/橫 HTML

**用本 skill 內附的 build 腳本，無需任何外部路徑：**

```bash
python "$CLAUDE_SKILL_DIR/scripts/build_html.py" path/to/source_elk.md "選用標題"
```

或在腳本所在目錄：
```bash
python build_html.py /abs/path/source_elk.md
```

腳本會：
1. 讀取本 skill `./assets/template_直.html` 與 `template_橫.html`（已內建 marked.js + A4 列印 CSS + 強化 img sizing）
2. 自動提取 MD 第一個 `# H1` 作為 title（或使用第二參數）
3. 將 markdown 內嵌進 `<script id="md">` 標籤，並跳脫內含的 `</script>`
4. 輸出 `<stem>_直.html` 與 `<stem>_橫.html` 至 `source.md` 同目錄

**HTML 圖片載入**：MD 內 `assets/foo_elk.png` 為相對路徑，HTML 必須與 `assets/` 同層放置才能載入。

---

## 檔案結構（自包含）

```
skills/report-easy/
├── SKILL.md                  ← 本檔案
├── assets/
│   ├── template_直.html      ← A4 portrait 模板（含 {{TITLE}} / {{MARKDOWN_CONTENT}} 占位）
│   ├── template_橫.html      ← A4 landscape 模板
│   └── d2_common.d2          ← 共用 D2 樣式 classes
└── scripts/
    └── build_html.py         ← 一鍵產生 直/橫 HTML
```

> 整個 skill 目錄可直接複製到任何機器，無外部檔案依賴。

---

## 注意事項

- **不要**把 log-log 數值圖、誤差曲線、散布圖強行轉成 D2 — 概念化方塊圖會丟失精確資訊。保留原 matplotlib PNG。
- **每渲染一張 D2 就驗證**：編譯失敗時先檢查 reserved keywords 與 `$` 跳脫
- 大型 MD 用 Grep + offset Read 分段處理，避免一次讀超過 token 上限
- 完成後告訴使用者開啟哪個 HTML 預覽，並列出新增的 D2/PNG 檔案
