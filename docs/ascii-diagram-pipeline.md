# ASCII Diagram → PNG Pipeline

把 `.md` 內的 box-drawing ASCII 區塊渲染成精美 PNG（支援 CJK），全程本地、零 API。

## 為什麼不直接用 Gemini / DALL·E

歷時多次迭代後（v1～v9 全部丟到 `.bak/`），結論：

| 路線 | 失敗模式 |
|------|---------|
| Gemini image-gen 直繪 | CJK 變形（決策層 → 獎策厙）、英文 token 變形（FastAPI → FastAFI、ZMQ → ZTAP） |
| Gemini polish-only | 仍會「重新詮釋」內容，加假 HTTP/SSH/legend、刪原節點 |
| Gemini 翻 CJK 為英文 + PIL 渲染 | 內容對；但既然要本地 PIL，何必還要翻譯？ |

**最終方案**：純 PIL 渲染（保留原 CJK），Gemini 完全退場。文字保真 100%、零 API cost、可批次。

---

## 流程

```
┌─────────────────────────────────────────────────┐
│  source/*.md  (含 fenced ``` ASCII 區塊)         │
└────────────────┬────────────────────────────────┘
                 │
                 v
        ┌─────────────────────┐
        │  find_blocks()      │ 掃 ``` block 找含 box-drawing 字元的區塊
        └─────────┬───────────┘
                  │
                  v
        ┌─────────────────────┐
        │  align_check_block()│ pairwise row 對齊驗證
        │  (check_align.py)   │ . cell-width CJK=2 / 箭頭=2 / ASCII=1
        │                     │ . 只追 ┌┐┬│├┤┼ 向下延伸字元
        │                     │ . v ^ 視為合法 vertical 終止符
        │                     │ . 報 col 漂移 +/-1~2
        └─────────┬───────────┘
                  │
            drift > 0?
            ─┬──────┬─
             │ no   │ yes (--strict)
             │      │
             │      v
             │   exit 1, fix .md, rerun
             v
        ┌─────────────────────┐
        │  render()           │ 純 PIL 繪圖
        │  (render_v1.py)     │ . Sarasa Mono TC (CJK-safe monospace)
        │                     │ . cell-grid: CJK=2 cell, ASCII=1
        │                     │ . CELL_PX = font.getlength("M")
        │                     │ . box chars 青色, 箭頭紫色, 文字深灰
        │                     │ . 圓角白底面板 + drop shadow
        │                     │ . 漸層 vignette 外背景
        │                     │ . 90px 外白邊
        │                     │ . 右下 footer (檔名 . L<行號> . version)
        └─────────┬───────────┘
                  │
                  v
        ┌─────────────────────────────────────┐
        │ rendered/<stem>_L<line>.md  (mirror) │
        │ rendered/<stem>_L<line>.png          │
        │ rendered/_index.md  (縮圖總表)        │
        └─────────────────────────────────────┘
```

---

## 兩個檔案搞定

### `check_align.py` (~80 行)

校驗 cell-width 對齊。獨立可跑、亦被 render_v1 import。

```python
# 核心 cell_width 規則（與 Sarasa Mono TC 字體一致）
def cell_width(ch):
    cp = ord(ch)
    if 0x2500 <= cp <= 0x257F: return 1   # box drawing
    if 0x20   <= cp <= 0x7E:   return 1   # ASCII
    if 0x3000 <= cp <= 0x9FFF: return 2   # CJK + fullwidth
    if 0xFF00 <= cp <= 0xFFEF: return 2   # halfwidth/fullwidth forms
    if 0x2190 <= cp <= 0x27BF: return 2   # arrows / math / dingbats
    if cp in (0x00B7, 0x00B0, 0x00B1, 0x00B2, 0x00D7, 0x00F7): return 2
    if cp in (0x2014, 0x2026): return 2
    return 1
```

```python
# Drift 偵測：相鄰 row pair
VERT_CHARS = "│┌┐└┘├┤┬┴┼v^"   # vertical / branch / arrow heads
DOWNWARD   = "│┌┐┬├┤┼"        # only these can extend to next row
DRIFT_TOLERANCE = 2            # cells; >2 means truly separate column

# for each row pair (i, i+1):
#   for each DOWNWARD border at col c on row i:
#     find nearest border on row i+1
#     if 1 <= |drift| <= 2: warn
```

### `render_v1.py` (~140 行)

完全本地 PIL 流程。Import `check_align` 的 `cell_width()` 與 `check_block()` 保持一致。

每章 / 每資料夾各自有一份，但共用 check_align。

---

## 部署到任意專案

把這個流程「裝到」一個 .md-heavy 專案：

```bash
PROJ=/path/to/your/project

# 1. 從現有專案複製兩個檔
cp E:/github/TSC_GBD_V0/.meta_analysis/check_align.py  $PROJ/
cp E:/github/TSC_GBD_V0/.meta_analysis/render_v1.py    $PROJ/

# 2. 跑
cd $PROJ
python render_v1.py            # 報警告但繼續
python render_v1.py --strict   # 有 drift 就退出（CI 用）

# 3. 結果
ls $PROJ/rendered/
```

需要 Sarasa Mono TC 字體（Windows 內建路徑 `C:/Windows/Fonts/SarasaMonoTC-Regular.ttf`），其他平台可改裝任何 CJK monospace。

---

## 對齊規則（Sarasa Mono TC）

| 字元類別 | Cell width | 範例 |
|---------|-----------|------|
| ASCII printable | 1 | `A-Z 0-9 +-=` |
| Box drawing | 1 | `─│┌┐└┘├┤┬┴┼` |
| CJK / fullwidth | 2 | `中文 區域 設備` |
| 箭頭 | 2 | `→ ← ↑ ↓ ↔` |
| 幾何 / dingbat | 2 | `▲ ▼ ► ◄ ✓ ✗ ●` |
| 數學 | 2 | `× ÷ ± ≤ ≥ ≠ ∈` |
| EM dash / 中圓點 / 度 | 2 | `— · °` |

**規則**：所有 EAW=Ambiguous 字元在 Sarasa Mono TC 都會渲染成 2 cells（除了 box drawing 與少數 latin-1）。

---

## Drift 偵測案例

實際 catch 過的 bug：

| 來源 | 問題 | drift |
|------|------|-------|
| 01_tsc_mcs_core L122 | `│  MES / 上位 ERP                        │` 多 1 trailing space | +1 |
| 03_ros_amr_navigation L8 | 框寬不一致：top 50 / mid 52 / hrule 53 | +2/+3 |
| 06_industrial_protocols L99 | top 用 `+...+` 純 ASCII，bottom 用 `┌┐└┘` | (字元類，非 drift) |
| 09_equipment_integration L126 | flow 圖最後 row 比上方少 1 leading space | +1 |
| 10_ui_simulator L123 | 中央 ┼ 偏 col 24（其餘 col 25） | -1 |
| 13_synthesis L10 | inside-box 多 1 cell（CJK 寬度算錯） | +1 |
| .interface/diagrams 02 L39/46 | `→` 算 1 cell（實際 Sarasa = 2） | -1 |

第 7 個是檢查器自己 bug，發現後修 cell_width 加箭頭區塊。

---

## False positive 排除

- **終止符**：`└┘┴` 不檢查向下漂移（vertical 自然結束）
- **箭頭頭**：`v ^` 視為合法 vertical 端點（從 │ 接到 v 不算 drift）
- **獨立並列盒**：相鄰 col 差 >2 cells 視為不同 logical column
- **空行 / 純文字行**：無 border char 的 row 跳過比對

---

## 輸出格式

每個 ASCII 區塊產出：

```
rendered/
├── _index.md                    全表 + 內嵌縮圖
├── <stem>_L<line>.md            源 ASCII (含原 CJK)
└── <stem>_L<line>.png           PIL 渲染
```

PNG 範例特徵：
- 1024×N px 解析度（依 ASCII 行數動態）
- 白色圓角面板，`#E1E6F0` 邊框
- Box drawing 線條 `#4A90E2` (cyan blue)
- 箭頭 `#A06CD5` (purple)
- 一般文字 `#283246` (深藍灰)
- 90px 漸層 vignette 外白邊
- 右下 footer：`<檔名>.md . L<行號>  (v1.x)`

---

## 已驗證的部署點

| 專案 | 區塊數 | 通過率 |
|------|--------|--------|
| `.meta_analysis/` (14 章書) | 25 | 100% |
| `.interface/diagrams/` | 11 | 100% |

兩處共用同一份 `check_align.py`，各自有 `render_v1.py`（內容一致，只是 ROOT 不同）。

---

## CI 整合建議

```yaml
# .github/workflows/diagram-lint.yml
- name: ASCII alignment lint
  run: python check_align.py
  # exits 1 if any block has drift -- block PR until source .md is fixed
```

或 pre-commit hook：

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: ascii-align
      name: ASCII align check
      entry: python check_align.py
      files: \.md$
      language: system
```

---

## 結論

**ASCII diagram in .md → polished PNG** 不需要 LLM。需要的只是：
1. 嚴謹的 cell-width 表（CJK / 箭頭 / 數學 = 2 cell）
2. 對齊驗證器（pairwise row pair drift detection）
3. PIL 純本地渲染器（cell-grid offset，避免 PIL `int(getlength)` 截斷漂移）

Gemini / 其他 image-gen 適合：海報、圖示、無精準文字需求的視覺。
**不適合**：技術圖、ASCII 線條重現、CJK 文字、保真度第一的場景。
