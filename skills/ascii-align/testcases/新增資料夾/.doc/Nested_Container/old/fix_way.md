# Fix Log - Nested_Container

> 通用規則見 `../FixRule.md`，本檔僅記錄逐檔修正歷史。

## 修正記錄

### sample_006.md

**類型**：parallel（並排 4 box，左右各 2，上下比較圖）
**檢測**：`↓`×2, `→`×7。替換後 4 box 全部 content 比 hrule 寬（`→`→`-->` +1w/each + CJK 累積）。
**修正**：
- 符號：`↓`→`v`、`→`→`-->`（9 處）
- 對齊：4 box 全部擴展 hrule 配合最寬 content
  - 左上 19→20，右上 19→21，左下 19→22，右下 20→26
  - 右列起始 col 統一為 46（gap 從 12 調為 top=12 / bot=10）
  - 窄行補 trailing space
**驗證**：symbol_fix --check 0 issues ✓，4 box ┐/│/┘ 全在同 col ✓，v 對齊 ┬ ✓

### sample_042.md

**類型**：parallel（並排 2 box + `←→` 連接器）
**檢測**：`←`×1, `→`×1。`←→` 被分別替換成 `<---->` → 語意為雙向，改為 `<->`。
**修正**：
- 符號：`←→` → `<->`
- 對齊：左 box 20→21（inner 18→19），右 box 16→19（inner 14→17），gap=5
**驗證**：0 issues ✓，┐/│/┘ 左@20 右@44 ✓

### sample_043.md

**類型**：multi-box（3 box 並排 + 中央 box 延伸 + 第 4 box 接入）
**檢測**：`→`×2, `←`×1, `→`×1(connector)。`←→` → `<->`，`→` → `-->`。
**修正**：
- 符號：`←→` → `<->`，`→` → `-->`（4 處）
- 對齊：Box2 20→21（CJK 容器/腳本），Box4 17→19。gap=5 統一。
  connector L12: `──│───>` → `───│──>  ` 保持 gap=5 對齊
**驗證**：0 issues ✓，Box1@12 Box2@38 Box3@50 Box4@62 全對齊 ✓

### sample_015.md

**類型**：parallel + flow（2 box 並排 + 箭頭標籤 + 底部 box 垂直連接）
**檢測**：`→`×1, `←`×2, `↕`×1。CJK「主系統」「馬達控制」各推 │ +1。
**修正**：
- 符號：`→`→`>`（箭頭末端），`←`→`<`（箭頭開頭），`↕`→`│`（垂直 connector chain）
- 對齊：左 box 15→16（inner 13→14），右 box 16→17（inner 14→15），gap 19→20
  gap 內 label 與箭頭全部對齊 20 寬
- connector chain: ┬@7 → │@7 → │@7 → │@7 → ┴@7
**驗證**：0 issues ✓，左@15 右@52 下@14 ✓，┬/│/┴ chain @7 ✓

### sample_044.md

**類型**：multi-box（同 043，不同內容）
**檢測**：`→`×2, `←`×1, `→`×1(connector)。
**修正**：
- 符號：`←→`→`<->`，`→`→`-->`（4 處）
- 對齊：Box2 23→24（CJK 生成/搜尋/計算），gap1=5, gap2=5, Box4 gap=9
**驗證**：0 issues ✓，Box1@11 Box2@40 Box3@52 Box4@61 ✓

### sample_142.md

**類型**：parallel + flow（2 box + labeled connectors + 底部 IPC 垂直連接）
**檢測**：`×`×2, `→`×2, `▼`×1。CJK 投影匹配/安全碼/馬達控制 推 │。
**修正**：
- 符號：`×`→`x`，`→`→`>`（connector 末端），`▼`→`v`
- 對齊：Box1 12→13（inner 10→11），Box2 16→17（inner 14→15），gap 19→20
  IPC box 16→17 配合 ┬/┴@40 chain
- connector chain: ┬@40 → │@40 → v@40 → ┴@40
**驗證**：0 issues ✓，Box1@12 Box2@49 IPC@49 ✓，chain @40 ✓

### sample_148.md

**類型**：nested（3 層同心嵌套 + 右側 comment）
**檢測**：`→`×3（全在 comment 區，box 外）。CJK「（外層）」「（中間）」「（內層）」全形括號推 │。
**修正**：
- 符號：`→`→`-->`（3 處，box 外不影響對齊）
- 對齊：三層全部擴展配合 CJK 全形括號
  - Inner: 21→23（inner 19→21），「（內層）」= 8 display
  - Middle: 29→31（inner 27→29），cascade +2
  - Outer: 37→39（inner 35→37），cascade +2
  - 每層 padding = 3sp（"   │...│   "）不變
**驗證**：0 issues ✓，Outer@38 Middle@34 Inner@30 ✓

### sample_157/158/159.md

**同 042/043/044**，不同 source 路徑，相同內容。直接套用已驗證修正。

### sample_045.md

**類型**：parallel + flow（2 box + 帶標籤箭頭 + 內部 ├── 樹 + 底部 Gemini box）
**檢測**：`→`×3, `←`×2。Box2 內 CJK（新增/既有/回應卡片）+ `-->` 路由推 │。
**修正**：
- 符號：`→`→`>`/`-->`，`←`→`<`（5 處）
- 對齊：Box1 12→13（inner 10→11）��Box2 28→32（inner 26→31）
  左右 border 同步調整，gap=19 不變
  底部 Gemini box 20→21（inner 18→20），┴@43 插入 hrule
- connector chain: ┬@43 → │@43 → v@43 → ┴@43
**驗證**：0 issues ✓，Box1@12 Box2@63 Bottom@52 ✓，chain@43 ✓
