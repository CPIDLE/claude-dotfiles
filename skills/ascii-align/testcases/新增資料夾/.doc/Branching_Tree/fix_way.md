# Fix Log - Branching_Tree

> 通用規則見 `../FixRule.md`，本檔僅記錄逐檔修正歷史。

## 修正記錄

### sample_012.md

**檢測**：無違規符號。L13/L14 w=68 (+1)，L16 w=66 (-1)。target=67。
**修正**：L13/L14 移除 1 trailing space，L16 新增 1 trailing space。
**驗證**：全 17 行 w=67 ✓

### sample_025.md / sample_030.md（內容相同）

**檢測**：`→` ×3, `↔` ×1。頂部 box L2 w=57 (+2), L4 w=56 (+1)。TCP box L21 w=38 (-1)。
**修正**：
- 符號：`→`→`-->`（box 外，無需補償），`↔`→`<->`（box 內，-1 trailing space）
- 寬度：L2 -2sp, L4 -1sp, L21 +1sp
**驗證**：頂部 box 全 5 行 w=55 ✓，兩個內部 box 各 4 行 w=39 ✓

### sample_073.md

**跳過** — 純文字說明，`▼▲→←●○■□◆` 是字元範例文件，非 box 結構。

### sample_084.md

**檢測**：無違規符號。表格 L10-L14 w=77 (-1)，target=78。
**修正**：Cell 5 (Range 欄) 各加 1 trailing space（14→15 對齊 hrule）。
**驗證**：全 10 行 w=78 ✓

### sample_087.md

**檢測**：`▼` ×16, `→` ×6。嵌套結構：外框+_get_frames box+三欄區+neural_stereo box+底部 tree。
**修正**（三階段）：
1. `symbol_fix.py` 替換符號
2. 結構分析：推導每個 inner│ 的 target column
   - 外框 │@5/│@56, _get_frames │@15/│@36, 三欄右│@41, neural_stereo │@10/│@47
3. 逐層對齊：inner│ → outer gap → outer│
   - bottom ├@23 對齊 ┬@23（原 ├@16 錯位）
   - bottom ┬@11/┬@31 對齊 ┼@11/┼@31
   - hrule 用 `─` 延伸（不用空格）
**驗證**：外框 41 行 w=56 ✓，所有 inner│ column 對齊 ✓

### sample_089.md

**檢測**：`►` ×6, `▼` ×5, `→` ×6, `²` ×1。Post-processing pipeline 內框 content│@30 vs hrule┐@29。
**修正**：
- 符號替換（tree 結構保留可讀性）
- hrule `┌──────v──────┐`：去 trailing space，保持 ┐@29
- L12/L15/L18/L21 content│：各移除 1 trailing space（│@30→│@29）
**驗證**：全部 ┐/│/┘ 對齊 col 29 ✓

### sample_140.md

**檢測**：`▼` ×2（box 外）。外框 L7/L9/L11 w=58-59 (+3-4)。底部雙框 CJK 溢出多處。
**修正**（一次性重建）：
- 外框 (target=55)：L7 CJK title 調 trailing，L9 三個 inner box content 重算 pad 寬度，L11 調 trailing
- 底部 RPi5+Jetson 雙框 (target=51)：
  - L15 Jetson title 重算 CJK pad
  - L17-L19 inner-inner box content 重算（路徑/魚眼/LiDAR CJK 寬度）
  - L21 connector 重算 CJK pad
  - L22 底部 hrule ┘@52→┘@51
  - L14 ┴@27→┴@28（對齊 L12 ┼@28 和 L13 │@28）
  - L24 v@37→v@36（對齊 L23 │@36）
**驗證**：外框 7 行 w=55 ✓，底部 9 行 w=51 ✓，三條垂直鏈 (col 11/28/36) 全對齊 ✓

### sample_143.md — `parallel` + `single`

**類別**：上半 3 個平行 box (`parallel`)，下半 1 個 IPC box (`single`)，tree 連接
**檢測**：`×`×1, `▼`×6, `←`×1, `→`×8。Box1 CJK 溢出（`C++ / RPi` 9w vs inner 8），IPC box 需擴展容納 CJK
**修正**：
- `4×`→`4x`（特殊：不加 trailing space），其餘符號正常替換
- Box1 擴展 inner 8→9（`┌────────┐`→`┌─────────┐`）匹配 bottom `└────┬────┘`=11
- 3 個 box content 全部 `pad(content, inner_w)` 重算 CJK 寬度
- IPC box 擴展 inner 41→48 容納「差異化安全策略（未來）」
- v 箭頭位置修正：L10 v@22/v@39→v@21/v@37，L22 同（對齊 │@21/│@37）
**驗證**：parallel boxes w=43 ✓，IPC box w=50 ✓，v-to-│ col 5/6/21/37 全對齊 ✓

### sample_180.md — `nested` + `parallel` + `tree`

**類別**：外框含 2 個 inner box (`nested`)，底部 2 個並排 box (`parallel`)，tree 連接 3 個 cloud service box
**檢測**：`·`×1, `→`×3, `▼`×3。外框 top hrule ┐@64 vs bottom ┘@65 mismatch。Inner box2 ┐@58 vs content│@59。底部 box L49/L51/L55 右│@28 (should@29)。
**修正**：
- 符號替換：`·`→`. `，`→`→`-->`，`▼`→`v `
- 外框 top hrule：┐@64→┐@65（加 1─）
- Inner box2 hrule：┐@58→┐@59（加 1─，減 1 trailing space）
- L14/L15 inner box1：`→`→`-->` 後移除 2 trailing space（content 緊貼│）
- 底部 box L49/L51/L55：box1 +1sp，box2 -1sp（│@28→@29，│@34→@35）
- **v-to-│ 偏移修正**：L24 和 L32 的 `v ` 後多 1 空格（因 `▼`(1char,w2)→`v `(2chars,w2) string 變長），各移除 1sp 使右側│對齊 @35/@46
- 教訓：`▼`→`v ` 即使 display width 相同，string 變長會擠壓同行後面的│位置。每次替換後必須驗 v 後方所有│的 column。
**驗證**：外框 w=65 ✓，底部 w=62 ✓，所有│column 對齊 ✓，v-to-│ 鏈對齊 ✓

### sample_208.md — `table`

**類別**：表格（與 012 相同結構）
**修正**：L13/L14 -1sp，L16 +1sp。
**驗證**：全 17 行 w=67 ✓

### sample_230.md — `tree` + `flow`

**類別**：tree 分支結構 + 多個小 box + `<--` 外部註解
**檢測**：`▼`×10, `←`×6, `↕`×1。CJK 溢出（通訊/方向/目標）。多個 box ┐ vs content│ off-by-1。
**修正**：
- 符號替換：`▼`→`v`/`v `，`←`→`<--`，`↕`→`| `
- hrule v+space：`┌──────────v ──────────┐` → `┌──────────v──────────┐`
- CJK content：AMR box `通訊` -1sp，Gateway box `方向/目標` -1sp
- Gateway bottom hrule：`└─┬────┬────┬────┬───┘` +1─ 對齊 top inner=21
- Operation bottom hrule：`└────────────────────┘` -1─ 對齊 top ┐@23
- Vision box hrule：`┌──────────────┐` +1─ 對齊 content│@21
- **v-to-junction 偏移**（▼→v 後累積偏移）：
  - L20: 4 個 v 各修正 @29→28, @35→33, @50→47（對齊 L19 │@28/│@33/┐@47）
  - L24: 3 個 v 各修正 @12→11, @19→17, @25→22（對齊 L23 ┬@11/┬@17/┐@22）
**驗證**：5 個 box 全部 ┐/│ 對齊 ✓，v-to-junction 全對齊 ✓

### sample_258.md — `tree` + `parallel`

**類別**：top box + UR30 box + 3 parallel bottom boxes，tree 連接，外部 `◄───►│` 雙向箭頭
**檢測**：`◄`×1, `►`×1, `▼`×3。L8 外部連接線 `◄───►│` 的 ► 在 box │@21 位置。UR30 底部 ┘@36 vs content│@37。
**修正**：
- 符號：全部替換（嚴格規則，即使 box 外也替換）
- L8 `◄───►│` → `<───>│`：移除 1─ 使 `>` 在 col 20、`│` 保持 @21（box border）
- L17 v@29/v@35/v@50 → v@28/v@33/v@47（對齊 L16 junction）
- UR30 底部 `└──┬───┬───┬───┘` +1─ → ┘@37 對齊 ┐@37
- 教訓：`◄►`(w2) 替換成 `<>`(w1) 時，arrow 與 box │ 的連接需手動調整 ─ 數量
**驗證**：所有 box ┐/│/┘ 對齊 ✓，v-to-junction 對齊 ✓

### sample_282.md — `nested`

**類別**：外框含 7 個 inner box（IPC/TM手臂/End Module/觸控螢幕/CAN Board/按鈕面板/大CAN），box 間有 `◄───►` 雙向連接和 connector chains
**檢測**：`◄`×2, `►`×3, `→`×1。7 個 box CJK 溢出（13 個 width issue）。多條 connector chain off-by-1。
**修正**：
- 符號替換 + L10/L13 arrow-to-box│ 手動重建
- 7 個 box hrule 逐一校正：IPC ┐@15→@16、觸控/按鈕 ┐@16→@17、CAN ┐@38→@39
- CJK content trailing space 逐行調整（TM 主機、觸控螢幕、馬達、電池、Lidar）
- 3 條 connector chain 修正：
  - IPC ┬ col 10: L21 ┴@11→@10
  - 100PIN/CAN col 33: L19 ┴@32→@33, L23 │@32→@33, L24 ┴@32→@33
  - CAN left col 27: 已對齊
- FixRule 新增：**connector chain（┬→│→┴ 垂直鏈）必須逐行驗 column**
**驗證**：7 box 右 border 全對齊 ✓，3 條 connector chain 全對齊 ✓，w=67 ✓

### sample_285.md — `nested` + `table`

**類別**：外框含 2 個 inner table（8-pin / 5-pin）
**檢測**：`←`×3, `►`×3。外框 CJK 溢出 19 行。Inner table 4th column CJK/arrow 內容寬度不一致（@44~@46）。
**修正**：
- 外框擴展 w=47→50（容納最寬 content `夾爪控制 ───────> 電動夾爪`）
- Inner table 4th column 統一：hrule ┐@43→@46（+3─），content│ 全部 pad 到 @46
- 漏補 4 行（電源×2, GND×2）col4│@44→@46（trailing space 不足）
- 教訓：table 每一欄的每一行都要驗│position，不能只看 hrule 和第一行
**驗證**：外框 w=50 ✓，inner table col4│@46 全 14 content + 5 hrule 對齊 ✓
