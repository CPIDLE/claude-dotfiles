# Retired: `report-gyro` skill

**Retired date**: 2026-05-11
**Replaced by**: Notepad++ MarkdownPanel（外部工具，CSS template 印 PDF）
**Not replaced by**: `md-to-deck`（功能不同 — md-to-deck 是客製化 single-file HTML slide deck，report-gyro 走的是 Marp / Gamma 路線）

## 為什麼退場

`report-gyro` 原本做三件事：
1. **Marp 路線** — MD → Marp HTML/PPTX/PDF
2. **Gamma 路線** — MD → 精簡 MD 給 Gamma.app 貼上
3. **Excel 驗算** — 抽參數 → `gen_verification.xlsx`

實際工作流變遷後：
- (1) Marp 路線 → 直接用 Notepad++ MarkdownPanel 看 `.md` 然後 print PDF 更快
- (2) Gamma 路線 → 沒在用
- (3) Excel 驗算 → 抽進 `md-to-deck`（因為跟 GYRO 簡報伴隨產出）

## 殘留依賴處理

退場前 `md-to-pptx/scripts/scaffold.py` 的 Stage 0 (Marp HTML 預覽當 PPTX 視覺基準) 引用 `report-gyro/assets/gyro-marp-theme.css`。退場時把該 CSS 搬進 `md-to-pptx/assets/gyro-marp-theme.css`，scaffold.py 預設路徑同步改。

## 命名整理

同日把報告類 skill 統一為「依輸出格式」命名：

| 舊名 | 新名 | 輸出 |
|---|---|---|
| `report-easy` | `md-to-paper` | A4 直/橫 HTML（長文白皮書） |
| `gyro-report`（從 Reporter_v0 引入） | `md-to-deck` | GYRO 品牌 single-file HTML → PDF |
| `md-to-pptx` | `md-to-pptx`（不變） | PptxGenJS `.pptx` |
| `report-gyro` | （退場） | — |

也順便解決 `report-gyro` ↔ `gyro-report` 撞名問題。

## 上游 repo 處理

`CPIDLE/claude-skill-gyro-report`（GitHub）是 2026-02-27 凍結快照，本次 `md-to-deck` source 來自較新的 `Reporter_v0\.doc\.claude\skills\gyro-report\`（多 98 行 SKILL.md + `gen_verification.py`）。GitHub repo 後續應 archive。
