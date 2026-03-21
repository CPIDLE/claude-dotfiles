---
name: gyro-report
description: >
  Generate GYRO Systems branded HTML slide presentations directly from Markdown source.
  ALWAYS use this skill whenever the user mentions GYRO Systems, GYRO 簡報, GYRO presentation,
  GYRO report, or asks to create a presentation/slide deck for GYRO, 鑫蒂斯, or any GYRO-related
  customer deliverable. Also trigger when referencing the GYRO style template, GYRO brand colors
  (#BD442C), or producing professional HTML slides matching GYRO's corporate identity.
  Produces single-file HTML presentations with fullscreen slides, keyboard/touch navigation,
  progress bar, print support, Mermaid diagrams, and full GYRO brand styling.
argument-hint: <source.md> <output.html>
---

# GYRO Report — MD to HTML Slide Deck

## 兩大 Skill 關係

```
/gyro-kb ── 負責「內容產出」── 知識庫管理 + 搜尋 + 計算 + 報告撰寫
  │
  │  產出 .md 報告
  ▼
/gyro-report ── 負責「排版呈現」── MD → HTML 簡報 + PDF + Excel 驗算
                 ↑ 你在這裡
```

| 定位 | 說明 |
|---|---|
| **本 skill** | **排版呈現**，將 .md 轉為品牌化 HTML 簡報 + PDF + Excel 驗算 |
| **輸入** | `/gyro-kb` 產出的 `.md` 檔（或任何符合格式的 Markdown） |
| **不負責** | 報告內容撰寫、知識庫搜尋、工程計算 — 這些是 `/gyro-kb` 的工作 |
| **不要混淆** | 本 skill 做排版不寫內容。要產報告內容請先用 `/gyro-kb` |

> **典型工作流**: `/gyro-kb <客戶需求>` → `.md` → `/gyro-report <.md> <.html>` → HTML + PDF + Excel

---

Read a Markdown source document and generate a professional GYRO-branded HTML slide presentation.

## Workflow

1. **Read** the source `.md` file
2. **Analyze** the document structure — map sections to slide types
3. **Generate** a single-file HTML with all CSS/JS/Mermaid embedded
4. **Write** the output `.html` file
5. **Extract** calculations from report.md → produce `params.json`
6. **Generate** `verification.xlsx` from params.json
7. **(Optional)** Generate PDF from HTML

> **No JSON intermediate step needed for HTML.** Claude reads MD and produces HTML directly.
> **Excel requires a JSON intermediate.** Claude extracts params → runs `gen_verification.py`.

## MD to Slide Mapping Rules

| MD Pattern | Slide Type | HTML Class |
|------------|-----------|------------|
| Document header (title, meta, blockquote) | **cover** | `title-slide` |
| `## Section Title` | **section** (red gradient divider) | `section-slide` |
| `### Subsection` + table | **table** | standard slide |
| `### Subsection` + bullet list | **content** | standard slide |
| `### Subsection` + ` ```mermaid ``` ` | **content with mermaid** | standard slide + `mermaid-wrap` |
| `### Subsection` + ASCII diagram | **content with diagram** | standard slide + `pre.diagram` |
| Stats/KPI data | **stats** cards | `stat-card` grid |
| Feature comparison | **feature-grid** cards | `feature-card` grid |
| `### Subsection` + `![alt](src)` alone | **full-image** | `slide-image` |
| `### Subsection` + `![alt](src)` + bullets | **image-content** (side-by-side) | `image-slide-layout` |
| End of document | **closing** | `closing-slide` |

### Slide Splitting Guidelines

- Each `### Subsection` generally maps to **one slide**
- Large tables (>10 rows) should be **split across multiple slides**
- Multiple mermaid diagrams in one section → **separate slides**
- A `## Section` heading creates a section divider slide, then content slides follow
- Images (`![alt](src)`) with accompanying text → **image-content** slide (side-by-side)
- Images alone or with only a caption → **full-image** slide
- Use judgment on content density — aim for readability, not compression

## Mermaid Diagrams

All flowcharts, architecture diagrams, and process flows from MD **must use Mermaid**.

### MD Source
````
```mermaid
graph LR
  A["Step 1"] --> B["Step 2"]
```
````

### HTML Output
```html
<div class="mermaid-wrap"><div class="mermaid">
graph LR
  A["Step 1"] --> B["Step 2"]
</div></div>
```

### ASCII Diagrams (Layout/Floorplan)
ASCII art like layout diagrams that cannot be expressed in Mermaid → use `<pre class="diagram">`:
```html
<pre class="diagram">
 ┌────┐ ┌────┐
 │P-1 │ │P-2 │
 └────┘ └────┘
</pre>
```

## Brand Design System

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#BD442C` | Header bars, card accents, nav |
| Primary Dark | `#B93A21` | Gradients |
| Primary Light | `#D4563E` | Gradients |
| Accent 1 | `#4472C4` | Info callouts |
| Accent 2 | `#ED7D31` | Warning callouts |
| Accent 3 | `#FFC000` | Gold highlights |
| Text | `#333333` | Headings |
| Body | `#404040` | Body text |

### Fonts
- **CJK**: Microsoft YaHei UI
- **Latin**: Calibri / Segoe UI

## 11 Slide Types Reference

### 1. cover (title-slide)
```html
<div class="slide title-slide active">
  <div class="slide-inner">
    <div class="title-company">GYRO SYSTEMS, INC.</div>
    <div class="title-main">Main Title</div>
    <div class="title-sub">Subtitle</div>
    <div class="title-meta">Date</div>
  </div>
  <div class="title-bar-bottom"></div>
</div>
```

### 2. section (section-slide)
```html
<div class="slide section-slide">
  <div class="slide-inner">
    <div class="section-main-title">Section Title</div>
    <div class="section-subtitle">Subtitle</div>
  </div>
</div>
```

### 3. content (standard slide)
```html
<div class="slide">
  <div class="slide-header-bar"><span class="section-label">Section Name</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">N</div>
      <h2>Slide Title</h2>
    </div>
    <!-- body: ul, mermaid-wrap, pre.diagram, callout, table, etc. -->
  </div>
  <div class="slide-footer"><span class="brand">GYRO SYSTEMS, INC.</span><span>Deck Title</span></div>
</div>
```

### 4. table slide
Same as content, with `<table>` in body:
```html
<table>
  <thead><tr><th>Col1</th><th>Col2</th></tr></thead>
  <tbody><tr><td>Data</td><td>Data</td></tr></tbody>
</table>
```

### 5. two-column
```html
<div class="two-col">
  <div><!-- left: h4, ul, p --></div>
  <div class="col-divider"><!-- right: h4, ul, p --></div>
</div>
```

### 6. feature-grid
```html
<div class="feature-grid">
  <div class="feature-card"><h4>Title</h4><p>Description</p></div>
  <!-- more cards -->
</div>
```

### 7. stats
```html
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-value">100+</div>
    <div class="stat-label">Label</div>
    <div class="stat-desc">Description</div>
  </div>
</div>
```

### 8. full-image slide
Image displayed full-width with optional caption. Used when MD has `![alt](src)` without accompanying bullet text.
```html
<div class="slide-image">
  <img src="IMAGE_SRC" alt="Description">
  <div class="image-caption">Caption text</div>
</div>
```
Add `.compact` or `.large` class to `slide-image` to control height:
- `.slide-image` — default max-height 420px
- `.slide-image.compact` — max-height 280px
- `.slide-image.large` — max-height 520px

### 9. image-content (image + text side-by-side)
Image on one side, text on the other. Used when MD has `![alt](src)` followed by bullet list or description.
```html
<div class="image-slide-layout">
  <div class="image-side">
    <img src="IMAGE_SRC" alt="Description">
    <div class="image-caption">Caption text</div>
  </div>
  <div class="text-side">
    <ul><li>Point 1</li><li>Point 2</li></ul>
  </div>
</div>
```

### 10. callout (used inside any slide)
```html
<div class="callout info">Blue info box</div>
<div class="callout warn">Orange warning box</div>
<div class="callout ok">Green success box</div>
<div class="callout">Red default box</div>
```

### 11. closing (closing-slide)
```html
<div class="slide closing-slide">
  <div class="slide-inner">
    <div class="closing-title">Thank You</div>
    <div class="closing-sub">Subtitle</div>
    <div class="closing-company">GYRO SYSTEMS, INC.</div>
  </div>
</div>
```

## Image Handling

### Image Source Strategy

When the MD source contains images (`![alt](path)` or references to uploaded files):

| Scenario | Strategy | Result |
|----------|----------|--------|
| User provides image file paths | Use relative path `images/filename.png` | HTML + `images/` folder |
| User uploads images in conversation | Embed as `data:image/png;base64,...` | Single HTML (larger file) |
| User explicitly requests single-file | Embed as base64 | Single HTML |
| User explicitly requests separated images | Use relative `images/` paths | HTML + `images/` folder |

**Default behavior**: Use relative `images/` paths. This keeps the HTML small (~50-60KB) instead of bloating to 1MB+ with base64.

### Output Structure (when using external images)

```
output_folder/
├── presentation.html      ← slim HTML (~50-60KB)
└── images/
    ├── img_01.png
    ├── img_02.png
    └── ...
```

### MD Image Syntax Mapping

```markdown
### 2.1 FOUP 規格
![FOUP 六面圖](image.png)
- 尺寸：224×203×200 mm
- 重量：5-8 kg
```
→ Maps to **image-content** slide (image left, bullets right)

```markdown
### 1.2 場域 Layout
![場域 Layout](layout.png)
```
→ Maps to **full-image** slide (image full-width)

### Image Processing Steps

1. Collect all `![alt](path)` image references from MD source
2. **Only use images that are explicitly referenced in the source MD** — do NOT guess or infer image placements from context alone. If there is no `![alt](path)` in the MD, do not add images to the HTML slide.
3. If images are uploaded files: copy to `images/` folder (or embed as base64)
4. Replace MD `![alt](path)` with appropriate HTML slide type
5. Set `alt` and `image-caption` from the MD alt text
6. Match image filename from the MD reference to the actual file in the images folder

## HTML Skeleton Template

Every generated HTML must follow this exact structure. Copy the CSS and JS blocks verbatim — only the slide content `{SLIDES_HTML}` changes per document.

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{DECK_TITLE}</title>
<style>
{CSS — copy from .claude/skills/gyro-report/assets/gyro_css_template.css}
</style>
</head>
<body>

<div class="progress" id="progress"></div>

<div class="deck" id="deck">
{SLIDES_HTML}
</div>

<div class="nav">
  <button id="prev">&#9664;</button>
  <span class="counter" id="counter">1 / N</span>
  <button id="next">&#9654;</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#fef4f2',
    primaryBorderColor: '#BD442C',
    primaryTextColor: '#333333',
    lineColor: '#BD442C',
    secondaryColor: '#e8f4fd',
    tertiaryColor: '#F8F8F8',
    fontFamily: '"Microsoft YaHei UI","Segoe UI","Noto Sans TC",Calibri,Arial,sans-serif',
    fontSize: '13px'
  },
  flowchart: { curve: 'basis', padding: 12 },
  sequence: { mirrorActors: false }
});
async function renderMermaids() {
  const els = document.querySelectorAll('.mermaid');
  for (let i = 0; i < els.length; i++) {
    const el = els[i];
    const id = 'mermaid-' + i;
    try {
      const { svg } = await mermaid.render(id, el.textContent.trim());
      el.innerHTML = svg;
    } catch(e) { console.warn('Mermaid render error:', e); }
  }
}
renderMermaids();
</script>
<script>
(function() {
  const slides = document.querySelectorAll('.slide');
  const total  = slides.length;
  let cur = 0;

  function go(n) {
    if (n < 0 || n >= total) return;
    slides[cur].classList.remove('active');
    cur = n;
    slides[cur].classList.add('active');
    document.getElementById('counter').textContent = (cur + 1) + ' / ' + total;
    document.getElementById('progress').style.width = ((cur + 1) / total * 100) + '%';
  }

  document.getElementById('prev').onclick = function() { go(cur - 1); };
  document.getElementById('next').onclick = function() { go(cur + 1); };

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); go(cur + 1); }
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                    { e.preventDefault(); go(cur - 1); }
    if (e.key === 'Home') { e.preventDefault(); go(0); }
    if (e.key === 'End')  { e.preventDefault(); go(total - 1); }
  });

  let startX = 0;
  document.addEventListener('touchstart', function(e) { startX = e.changedTouches[0].screenX; });
  document.addEventListener('touchend', function(e) {
    const dx = e.changedTouches[0].screenX - startX;
    if (dx < -50) go(cur + 1);
    if (dx >  50) go(cur - 1);
  });

  go(0);
})();
</script>
</body>
</html>
```

## CSS Template File

The full CSS is stored at `.claude/skills/gyro-report/assets/gyro_css_template.css`. Read and embed it in every generated HTML `<style>` block. This CSS is extracted from the JS generator and must be used verbatim.

## Editing Large HTML Output

Generated HTML files are single-file presentations containing all CSS/JS/content, typically **500KB-1MB+**. This exceeds the Read tool's 256KB limit, so **cannot be read in one pass**.

### Recommended Technique

1. **Grep to locate** — Use `Grep` to search for keywords/content in the HTML and get line numbers
2. **Read with offset/limit** — Use `Read` with `offset` + `limit` to read only the relevant section
3. **Edit to modify** — Use `Edit` with exact `old_string` match to surgically update content

### Key Points
- **Never** attempt to read the entire HTML file at once — it will fail with size error
- **Never** rewrite the entire file with Write tool — use targeted Edit instead
- Grep + offset Read + Edit is the standard pattern for all large HTML modifications
- The slide counter (`1 / N`) auto-updates via JavaScript, no manual fix needed

## Excel 驗算檔產生

Generate a `verification.xlsx` that cross-checks all numerical calculations in the report. The Excel file has 3 sheets with live formulas so stakeholders can modify parameters and see results update.

### Step 1: Extract Parameters from report.md

Read the report and extract ALL numerical values into a JSON file (`params.json`):

```json
{
  "title": "錼創顯示 2026 Q1 V0.3b",
  "params": {
    "WIP": 1000,
    "FOUP_capacity": 6,
    "AMR_moves_per_hr": 18,
    "AMR_availability": 0.95,
    "peak_factor": 1.5,
    "charge_power_kw": 1.5,
    "energy_per_move_kwh": 0.025,
    "port_dwell_min_sec": 90,
    "port_dwell_max_sec": 180,
    "AMR_count": 2
  },
  "process_times": [
    {"id": "F1_A1", "flow": "流程 1", "pt_min": 8},
    {"id": "F2_A1", "flow": "流程 2", "pt_min": 15},
    {"id": "F2_P",  "flow": "流程 2", "pt_min": 90},
    {"id": "F3_A1", "flow": "流程 3", "pt_min": 8},
    {"id": "F3_A2", "flow": "流程 3", "pt_min": 10},
    {"id": "F3_L",  "flow": "流程 3", "pt_min": 15},
    {"id": "F4_A11","flow": "流程 4", "pt_min": 8},
    {"id": "F4_A12","flow": "流程 4", "pt_min": 5},
    {"id": "F4_PK", "flow": "流程 4", "pt_min": 5}
  ],
  "machines": { "P": 7, "A1": 10, "A2": 3, "L": 3, "PK": 1 },
  "stk": { "columns": 15, "layers": 6, "sides": 2, "io_ports": 12 },
  "ts_sorter": { "ts_full": 6, "ts_empty": 6, "sorter_buffer": 6, "sorter_ports": 6 },
  "report_values": {
    "1": 167, "2": 84, "3": 2
  },
  "sensitivity": {
    "scenario_A": {"label": "情境 A\nP Pt=70min", "P_pt": 70, "A1_machines": 10, "WIP": 1000, "capacity": 6},
    "scenario_B": {"label": "情境 B\nA1 +2台", "P_pt": 90, "A1_machines": 12, "WIP": 1000, "capacity": 6},
    "scenario_C": {"label": "情境 C\nWIP=1500", "P_pt": 90, "A1_machines": 10, "WIP": 1500, "capacity": 6},
    "scenario_D": {"label": "情境 D\n裝載量=12", "P_pt": 90, "A1_machines": 10, "WIP": 1000, "capacity": 12}
  }
}
```

**Key fields:**
| Field | Description |
|-------|-------------|
| `params` | Basic parameters (10 items) — all blue-editable cells in Sheet 1 |
| `process_times` | Per-station process time per piece (9 stations) |
| `machines` | Equipment count per station type |
| `stk` | Stocker configuration |
| `ts_sorter` | Tower Stocker / Sorter configuration |
| `report_values` | Actual values from report for Pass/Fail comparison (keyed by item #) |
| `sensitivity` | Scenario parameters for Sheet 3 sensitivity analysis |

### Step 2: Run gen_verification.py

```bash
# Install dependency if needed
pip install openpyxl

# Generate Excel
python .claude/skills/gyro-report/scripts/gen_verification.py params.json verification.xlsx
```

### Step 3: Verify Output

After generation, verify:
1. Open with Python to count Pass/Fail:
```python
from openpyxl import load_workbook
wb = load_workbook("verification.xlsx")
ws = wb["計算驗證"]
pass_count = sum(1 for row in ws.iter_rows(min_col=7, max_col=7) if row[0].value == "Pass")
print(f"Pass: {pass_count}")
```
2. Confirm 3 sheets exist: 參數輸入, 計算驗證, 敏感度分析
3. Confirm blue cells in Sheet 1 are editable and formulas recalculate

### Output Structure

The generated xlsx has:
- **Sheet 1 (參數輸入)**: All input parameters with blue-fill editable cells
- **Sheet 2 (計算驗證)**: Verification items with Excel formulas linking to Sheet 1, report value comparison, and Pass/Fail conditional formatting (green/red)
- **Sheet 3 (敏感度分析)**: Baseline (linked to Sheet 1) + scenario columns with derived calculations

## PDF Generation

Use `puppeteer-core` with the system Chrome to generate PDF from the HTML slide deck. Supports both A4 portrait and A4 landscape.

### Prerequisites
- System Chrome installed at `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `puppeteer-core` (no bundled browser, uses system Chrome)

### Generation Script (`_gen_pdf.js`)

```javascript
const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const HTML   = 'file:///' + path.resolve('index.html').replace(/\\/g, '/');

async function generate(outFile, landscape) {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.goto(HTML, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for Mermaid diagrams to render
  await page.waitForFunction(() => {
    const els = document.querySelectorAll('.mermaid');
    return Array.from(els).every(el => el.querySelector('svg') || el.innerHTML.includes('<svg'));
  }, { timeout: 15000 }).catch(() => {});

  await page.pdf({
    path: outFile, format: 'A4', landscape: landscape,
    printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });
  await browser.close();
}

(async () => {
  await generate('report_a4_portrait.pdf', false);
  await generate('report_a4_landscape.pdf', true);
})();
```

### Workflow
1. `npm install puppeteer-core` (in output folder)
2. `node _gen_pdf.js`
3. Clean up: `rm _gen_pdf.js && rm -rf node_modules package.json package-lock.json`

### Print CSS — Critical Notes

The `@media print` CSS **must** override `html` background in addition to `body`. The `html` element inherits `background: var(--bg)` (`#1a1a1a` dark) from the base styles. If only `body` is set to white, the dark `html` background bleeds through in PDF rendering, causing **black pages**.

Required print CSS (already included in `gyro_css_template.css`):

```css
@media print {
  .nav, .progress { display: none !important; }
  html, body { background: #fff !important; overflow: visible; }
  .deck { overflow: visible; height: auto; background: #fff !important; }
  .slide { position: relative !important; opacity: 1 !important; pointer-events: auto !important;
    page-break-after: always; min-height: 100vh; background: #fff !important; }
  .slide.section-slide, .slide.closing-slide {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%) !important;
  }
  .slide::after { display: none !important; }
}
```

Key fixes vs original:
| Issue | Old | Fixed |
|-------|-----|-------|
| `html` dark background bleeds in PDF | `body { background: #fff; }` only | `html, body { background: #fff !important; }` |
| `.deck` container not white | not set | `.deck { background: #fff !important; }` |
| `.slide` default not forced white | not set | `.slide { background: #fff !important; }` |
| Section/closing slides lost gradient | overridden by `.slide` white | Re-applied with `!important` |
| Watermark pseudo-element artifacts | not handled | `.slide::after { display: none !important; }` |

## Alternative: JSON Workflow (Legacy)

The Node.js generator script is still available for JSON-based generation:
```bash
node .claude/skills/gyro-report/scripts/gyro_html_generator.js <content.json> <output.html>
```
See `.claude/skills/gyro-report/assets/content_sample.json` for JSON schema reference.

## Output Modes

### Single-file mode (default for Claude.ai)
All content embedded in one HTML file. Images encoded as base64.
- Pros: One file to share, works anywhere
- Cons: Large file size (1MB+ with images)

### Folder mode (default for Claude Code CLI)
HTML file + `images/` subfolder with external image files.
- Pros: Small HTML, easy to edit, version-control friendly
- Cons: Must keep folder structure together

When using folder mode, create the output directory and `images/` subdirectory, then write both the HTML and extracted image files.

## Files

| File | Purpose |
|------|---------|
| `.claude/skills/gyro-report/assets/gyro_css_template.css` | **CSS template** — embed verbatim in every HTML (includes print CSS fix) |
| `.claude/skills/gyro-report/assets/gyro_style_template.json` | Brand design system spec (reference) |
| `.claude/skills/gyro-report/scripts/gyro_html_generator.js` | Legacy JSON→HTML generator |
| `.claude/skills/gyro-report/assets/content_sample.json` | Legacy JSON schema example |
| `.claude/skills/gyro-report/scripts/gen_verification.py` | Excel 驗算檔產生腳本 (需 openpyxl) |

> **PDF generation**: Use inline `_gen_pdf.js` script (see "PDF Generation" section above). The script is created on-the-fly, run, then cleaned up — no permanent file needed.
