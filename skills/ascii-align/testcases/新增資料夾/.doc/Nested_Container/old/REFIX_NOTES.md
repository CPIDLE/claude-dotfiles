# Re-fix Issues Record (2026-04-16)

## 分類

### A. 自動 review 沒抓到但 user 看出來的問題

#### A1. 垂直連接線 column 不一致
**檔案**: 365, 401, 404, 409, 412, 426 (UR/TM Analysis 系列)

問題：outer box 寬度一致（w=61），但從 box 底部延伸的垂直連接 `│` 在不同段落 column 位置不同。例如 365 的 L12 `│` 在 col 13，後續段落 L17 在 col 12（差 1）。

根本原因：fix agent 只看 outer box 對不對，沒有驗證 inner vertical flow 的 column 一致性。

---

#### A2. 連接箭頭寬度 vs 空格寬度不同步
**檔案**: 376, 415 (PM v2 Workflow)

問題：內部 flow 連接器 `────>` (5 cols) 比 content row 的間隙 `    ` (4 cols) 多 1，導致 inner box 左邊框在 connector row 和 content row 的 column 位置相差 1。outer box 總寬 98 一致所以 auto-review 通過。

根本原因：symbol_fix 的 `→`→`>` 替換使連接器縮短，但 gap width 沒有同步調整。

---

#### A3. 平行 inner box 尾端 trailing space 不一致
**檔案**: 360 (DuelEngineSOP)

問題：兩個並排 inner box（Claude Code / OpenCode），connector row 在 inner box 之間有 `───>` (4 cols)，但 content row 只有 3 spaces。導致 OpenCode box 右邊後的 trailing spaces 在 connector row (2 spaces) vs content row (4 spaces) 不同。outer box w=61 一致所以通過。

---

#### A4. Inner table 的 column separator `│` 垂直未對齊
**檔案**: 382, 418 (win_drive MCP — 同圖)

問題：inner box 內有 table 結構，`screenshot/keyboard/window` 的欄位分隔 `│` 在 col 25，但 `inspect │ find │ click` 的 `│` 位置完全不同（col 11, 17）。視覺上像亂掉。

說明：這可能是原始圖就這樣設計（不同 section 有不同 layout）。需要 user 確認是否需要對齊。

---

#### A5. 完全破裂的結構
**檔案**: 337 (API GW → Fargate → S3)

問題：S3 box 的 L8-L9 缺少右邊框 `│`，整個 box 結構已破裂（width 從 39 到 60 差距極大）。

---

### B. 自動 review 抓到的

#### B1. Width mismatch
**檔案**: 277 (工廠平面圖)

問題：Group L13-L16 target=50，L13/L14 w=49 (-1)

---

### C. 連續被 re-x 的

#### C1. User 多次 re-x 後仍有問題
**檔案**: 124, 314 (同圖，flow + file tree)

問題未明確：第一次修完 automated review PASS，user 又 re-x。可能原因：
- 標記行 `關鍵字│` 和 `分類│` 的 `│` 與 `┬` 的 column 不對齊
- 這兩行不是 box 邊框，但 review 工具誤算為 box group

---

### D. 其他

**202**: 正常/雪崩兩個平行 box，可能 box inner width 不一致（兩側 box 本來就設計不同，分別驗證）

**224**: 同 202/198 類型

**371, 373**: 大型 nested flow，需細查

---

---

## 實際 Re-fix 統計（本輪）

| 原因 | 檔案數 | 具體問題 |
|------|--------|---------|
| 垂直 connector column 不一致 | 6 | 365,401,404,409,412,426 — `│`/`v` 偏 1 col |
| Connector 寬 vs gap 寬不同步 | 6 | 376,415 (────> 5 vs 4), 360,407,424 (───> 7 vs 5) |
| 完全破裂結構 | 1 | 337 — S3 box 缺右邊框 |
| Inner box column alignment | 2 | 202 top hrule +1, 373 label scrambled |
| Flow connector column | 2 | 124,314 — `│` 與 `┬` 不對齊 |
| Width mismatch (auto fail) | 2 | 277 (x2 rounds), 468 |
| Symbol fix 漏掉 | 7 | 426,429,430,431,432,433,434 — ▼未替換 |
| 無問題直接 rename | 4 | 198,224,278,382/418 |

---

## 結論：prompt 與 review 改進方向

### Prompt 需要加入

1. **Vertical connector alignment**: `│` 和 `v` 在 flow 中必須在同一 column，且與上方 box `┬` 對齊
2. **Connector vs gap parity**: `────>` 連接器的寬度必須等於 content row 的 inter-box gap 寬度
3. **Inner table column alignment**: box 內有 `│` 欄位分隔時，所有 section 的 `│` 必須在同 column

### Review 需要加強

1. **Inner `│` column check**: 偵測 box 內容行中出現的 `│` 分隔符，驗證跨行是否在同 column
2. **Connector/gap parity check**: 偵測 `────>` 連接器後的 column 位置是否與 hrule 一致
3. **Flow connector column check**: 偵測 `│...│` 和 `│...v` 的 `│`/`v` column 是否一致
