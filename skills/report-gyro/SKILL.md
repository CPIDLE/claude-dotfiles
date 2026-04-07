---
name: report-gyro
description: >
  Generate GYRO Systems presentation drafts from Markdown source.
  Two output paths: (A) Marp CLI for quick local PDF/PPTX drafts,
  (B) Gamma-ready condensed MD for the user to paste into Gamma.app for final polish.
  Also handles Excel verification sheet generation.
  Trigger when: GYRO 簡報, GYRO presentation, GYRO report, 投影片, slide deck,
  or any GYRO-related deliverable.
argument-hint: <source.md> [output.pptx|output.pdf|gamma]
---

# GYRO Report — MD → Presentation Draft

## 兩大 Skill 關係

```
/gyro-kb ── 負責「內容產出」── 知識庫搜尋 + 報告撰寫
  │
  │  產出 .md 報告
  ▼
/report-gyro ── 負責「排版呈現」── 三條路線
                 ↑ 你在這裡
```

| 定位 | 說明 |
|---|---|
| **本 skill** | 將 .md 轉為投影片初稿（Marp）或精簡摘要（Gamma 用） |
| **輸入** | `/gyro-kb` 產出的 `.md` 檔（或任何 Markdown） |
| **不負責** | 報告內容撰寫、知識庫搜尋 — 那是 `/gyro-kb` 的工作 |

---

## 路線 A：Marp 快速初稿（本地免費）

**用途**：快速產出 PDF/PPTX 初稿，內部預覽或不需要精美設計的場景。

### 指令

```bash
# PPTX
marp --no-stdin input.md --html --allow-local-files \
  --theme "$CLAUDE_SKILL_DIR/assets/gyro-marp-theme.css" \
  --pptx -o output.pptx

# PDF
marp --no-stdin input.md --html --allow-local-files \
  --theme "$CLAUDE_SKILL_DIR/assets/gyro-marp-theme.css" \
  --pdf --pdf-outlines -o output.pdf

# HTML 預覽
marp --no-stdin input.md --html --allow-local-files \
  --theme "$CLAUDE_SKILL_DIR/assets/gyro-marp-theme.css" \
  -o output.html
```

### Marp MD 格式

```yaml
---
marp: true
theme: gyro
paginate: true
header: ''
footer: ''
---
```

- 用 `---` 分隔每一頁
- 用 `<!-- _class: cover -->` 設定頁面類型（cover / section）
- 用 `<!-- _header: 章節名 -->` 設定頁首
- 支援 HTML 元件（stats-grid、callout、hero-number 等）
- 詳細語法見 `marp_usage_guide.md`

### Workflow

1. 讀取源 `.md` 報告
2. 轉換為 Marp 格式的 MD（加入 frontmatter、分頁、頁面類型）
3. 執行 `marp` CLI 產出 PPTX/PDF
4. 輸出到 `/PKB/workspace/`

---

## 路線 B：Gamma-ready MD（精修用）

**用途**：產出精簡摘要，使用者貼入 [Gamma.app](https://gamma.app) 由 AI 自動排版，產出高品質投影片。

### Workflow

1. 讀取源 `.md` 報告
2. 產出「Gamma-ready 精簡版」：
   - 保留章節結構（## 標題）
   - 每章節精簡為 3-5 個 bullet points
   - 移除 RAG 佐證標註（`[RAG: ...]`、`[來源: ...]`）
   - 移除 changelog、附錄等非核心內容
   - 保留關鍵數據（KPI、客戶名、技術等級）
   - 總長度控制在 2000-3000 字（Gamma 最佳輸入長度）
3. 將精簡版寫入 `*_gamma.md` 檔案
4. 提示使用者：「請將此內容貼入 Gamma.app → Paste in text → Presentation → Generate」

### 精簡規則

- **保留**：標題、核心結論、KPI 數字、客戶名稱、技術等級、路線圖
- **移除**：詳細技術描述、RAG 來源標註、changelog、附錄、重複內容
- **壓縮**：表格→bullet list、長段落→一句話摘要

---

## 路線 C：Excel 驗算表

**用途**：從報告中提取計算參數，產生驗算用 Excel。

### Workflow

1. 從 `.md` 報告中提取數值參數 → `params.json`
2. 執行 `gen_verification.py`：
   ```bash
   python gen_verification.py params.json output.xlsx
   ```
3. 產出三 sheet Excel（參數輸入 / 計算驗證 / 敏感度分析）

---

## 品牌色系參考

| Token | Value | 用途 |
|-------|-------|------|
| Primary | `#BD442C` | 主色（磚紅） |
| Accent 1 | `#4472C4` | Info（藍） |
| Accent 2 | `#ED7D31` | Warning（橘） |
| Accent 3 | `#FFC000` | Highlight（金） |
| Text | `#333333` | 標題 |
| Body | `#404040` | 內文 |

字體：Inter + Noto Sans TC（Latin + CJK）

---

## 流程圖規範（D2/ELK 優先）

需要嵌入流程圖、架構圖、決策樹時，**優先用 D2 + ELK layout** 渲染 PNG，僅在 D2 無法表達語意（gantt、sequence、ER、pie 等）時退回 Mermaid。詳細對應表與 D2 reserved keywords 注意事項見 `report-easy` skill 的 SKILL.md 第 1 節。

```bash
d2 --layout=elk in.d2 out.png
```

---

## 檔案結構

```
skills/report-gyro/
├── SKILL.md                          ← 本檔案
├── README_載入SOP.md
├── assets/
│   └── gyro-marp-theme.css           ← Marp 唯一 theme
└── scripts/
    └── gen_verification.py           ← Excel 驗算產生器
```

相關參考：
- `PKB/templates/00_報告產生流程/marp_usage_guide.md` — Marp 語法指南
- `PKB/templates/00_報告產生流程/sample_marp.md` — Marp 範例
