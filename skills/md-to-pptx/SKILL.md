---
name: md-to-pptx
description: >
  Auto-generate a complete PptxGenJS slide deck (`<stem>_create_pptx.js` + `.pptx`) from a
  Markdown source, using the GYRO branded helper library. H1 → titleSlide, H2 → sectionSlide,
  H3 → contentSlide. Every MD construct underneath is auto-emitted with real content:
  tables → native PPTX `makeTable` (with **bold** cells turning red+bold), card-style lists
  (`- **title**: desc` × 3-9) → `cardsGrid`, bullet lists → `bulletList`, blockquotes →
  `addInfoBox` (warn/info auto-picked from keywords), images → `imageWithCaption`, ASCII code
  blocks → monospaced `addText`, H4 → inline sub-headings. Overflow auto-splits into
  `（續）` continuation pages. Mermaid code blocks are flagged for manual visual rendering.
  Trigger when: MD 轉 PPTX, MD 變簡報, /md-to-pptx, PptxGenJS, 產 GYRO 簡報.
argument-hint: <source.md> [--run]
---

# md-to-pptx — MD → PptxGenJS deck (Auto v2, content-filled)

走 **V1 playbook** 描述的 pipeline：MD 是 single source of truth，HTML 當樣式參考，PPTX 由 PptxGenJS 腳本獨立產出。本 skill 自動產**腳本骨架**，內容靠 cc + 使用者一頁一頁手工編排。

## 自動化邊界

**可自動**（v2 已實作）：
- MD 結構 → slides：H1=title / H2=section divider / H3=content
- 表格內容（含 `**xxx**` → `{color: C.red, bold: true}` highlight）
- Cards 偵測：3-9 個 `- **title**: desc` list → cardsGrid（3 欄）
- 一般 bullet list → bulletList
- Blockquote → addInfoBox，bg 由關鍵字選（`⚠/注意/警告/重要/更新/確認` → warnBg）
- Image → imageWithCaption，路徑走 `path.join(__dirname, ...)`
- ASCII code block → monospace `addText`（Sarasa Mono TC 字型 + 淺灰背景）
- H4 sub-heading → 段內紅字粗體標題
- **Overflow 自動拆續頁**：當 y 超過 4.95，自動 `++pageNum` 開新頁，標題加 `（續）/（續 2）`
- Table colW 估算（依各欄字數比例分配 9.2 in）

**不能自動**（仍需手動）：
- Mermaid code blocks（`graph LR/TD`、`sequenceDiagram` 等）：skill 印 `// MERMAID block skipped` 註解，使用者要手繪 `addShape` 流程圖
- 客製化視覺頁（場域 Layout、CAD 疊圖、機台格子陣列）：MD 沒有座標資訊
- 真實照片插入（MD 沒有 `![]()` 引用的圖）

## 流程（嚴格依序，V1 playbook §0）

```
source.md
   │  Stage 0a: emit Marp MD（auto-split 過的內容、加 frontmatter + `---` 分頁）
   ▼
<stem>_marp.md
   │  Stage 0b: marp --theme gyro-marp-theme.css --html
   │    （重用 report-gyro skill 的 GYRO 樣式，不重複造輪）
   ▼
<stem>_slides.html  ← **視覺基準**，Marp 內建翻頁 / GYRO 配色 / 1280×720
   │  人工 review：版型 / 配色 / 表格 / 切點 OK 嗎？
   │    NO  → 回 source.md 改內容、重跑
   │    YES ↓
   │  Stage 1: MD → PptxGenJS scaffold（與 Stage 0 共用 split 邏輯）
   ▼
<stem>_create_pptx.js
   │  人工 Edit：對照 HTML，補 mermaid flowChain、客製視覺頁
   ▼
<stem>_create_pptx.js (patched)
   │  Stage 2: node + global pptxgenjs
   ▼
<stem>.pptx
```

**為什麼必須先 HTML**：PPTX 在腳本裡硬寫座標（PptxGenJS 是 imperative，沒 flex/grid），錯了重跑慢。HTML 即時在瀏覽器看，調整成本低 — **先 HTML 定樣式省下大量試錯**。版型有問題優先在 .md / .html 階段修。

**為什麼用 Marp**：`report-gyro` skill 已有 `gyro-marp-theme.css`（GYRO 磚紅 #BD442C、Inter+Noto Sans TC、16:9）+ `marp` CLI 內建翻頁、PDF/PPTX/HTML 三合一匯出。**重用，不重複造輪**。

剩下手動工作（Stage 1 產出後）：mermaid block 改手繪 `flowChain`、客製化視覺頁、補真實照片。

## 用法

```bash
# 預設：自動跑 Stage 0 (HTML) + Stage 1 (JS)
python "$CLAUDE_SKILL_DIR/scripts/scaffold.py" path/to/source.md

# 產出三個檔（同層）：
#   path/to/source_橫.html          ← 先打開這個 review！
#   path/to/source_create_pptx.js   ← Stage 1 自動產的腳本
#   (尚未 .pptx — Stage 2 需另外跑或加 --run)

# 加 --run 連 Stage 2 一起跑（產 .pptx）— 但 V1 playbook 建議先 review HTML
python ".../scaffold.py" source.md --run

# 已經 review 過 HTML、跳過 Stage 0
python ".../scaffold.py" source.md --skip-html --run
```

## Helper 參考

`template/pptx_helpers.js` 匯出（從 V2.1 抽出）：

| Helper | 用途 |
|---|---|
| `titleSlide({title, subtitle, date, tagline})` | 封面：GYRO 標題 + 副標 + 日期 + 一行 tagline |
| `sectionSlide(title, subtitle)` | 章節分隔頁：紅底白字大標 |
| `contentSlide(section, num, title)` | 內容頁：頭頂紅 header bar + 橘色編號圈 + 標題 + footer |
| `makeTable(s, headers, rows, opts)` | 品牌紅標頭表格，rows 支援 `{text, color, bold}` cell options |
| `addInfoBox(s, text, {bg: C.warnBg / C.infoBg})` | 內容下方的提示/警告框 |
| `cardsGrid(s, items, {cols})` | N 欄卡片佈局（3-9 items），上方有紅/橘色 accent bar |
| `bulletList(s, items)` | 子彈點列 |
| `imageWithCaption(s, path, caption)` | 居中圖 + 下方 caption |

色票：`C.red, C.orange, C.darkText, C.gray, C.lightGray, C.tableHead, C.warnBg, C.infoBg`。

## scaffold 偵測規則

| MD 結構 | 注釋提示 | 建議 helper |
|---|---|---|
| `# H1` (第一個) | — | `titleSlide` |
| `## H2` | — | `sectionSlide` |
| `### H3` | 一張 content slide | `contentSlide` |
| H3 底下 `\| ... \|` table | `table (NxM)` | `makeTable` |
| H3 底下 `- **xxx**: yyy` list 3-9 items | `cards (N items)` | `cardsGrid` |
| H3 底下其他 list | `bullets (N items)` | `bulletList` |
| H3 底下 `> ...` blockquote | `infobox` | `addInfoBox` |
| H3 底下 `![](path)` | `image: filename` | `imageWithCaption` |
| H3 底下 ```` ```code``` ```` | `code block` | （手寫 addText） |

每個 H3 後面會印一行 `// MD hints: ...; ...` 列出該 H3 底下偵測到的全部 block，以及一串 `// TODO:` helper 呼叫範本。

## 依賴

| 套件 | 安裝 |
|---|---|
| Python ≥ 3.10 | 標準 lib only |
| Node.js ≥ 18 | scaffold 跑 `--run` 時才需要 |
| `pptxgenjs` ≥ 4.0 | `npm install -g pptxgenjs`（或 local） |

`--run` 模式會用 `npm root -g` 找全域 node_modules，自動設 `NODE_PATH`。

## 編排建議（從 V1 playbook §5 借鑑）

骨架產出後，**永遠不要直接重新 scaffold 覆蓋手寫過的檔**。改寫順序：

1. **填封面 placeholder**：titleSlide 的 subtitle / date / tagline
2. **填章節副標**：sectionSlide 的 subtitle
3. **逐張 content slide**：對照原 MD，把 `// TODO: makeTable(...)` 改成完整呼叫
4. **客製化視覺頁**：場域 Layout、流程 block 等 — 直接在該 slide 下手寫 `s.addShape / s.addText / s.addImage`，helper 救不了

## 注意事項

- skill **不**負責內容濃縮（HTML 長文 → PPTX 卡片化）。MD 顆粒度怎麼寫，PPTX 顆粒度就跟著走，每個 H3 = 一張 slide
- 如果 MD 一個 H3 內容超過一頁能塞，產出的 slide 會擠 — 此時要回 MD 把 H3 切成 H3a / H3b，重新 scaffold（小心覆蓋手寫）
- pptxgenjs 是 imperative 沒 flex/grid，座標都靠人估。HTML 版印出來放旁邊當視覺基準
- 生成的 JS 第一行 require pptxgenjs，**全域裝**才不用每個專案 npm install
