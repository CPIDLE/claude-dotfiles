# ASCII Art Fix Rules

## 流程

```
0. 分類 → 1. 替換 → 2. 對齊 → 3. 驗證
```

## 0. 分類

| 類別 | 修正難度 | 關鍵 |
|------|---------|------|
| `single` | 低 | trailing space |
| `parallel` | 中 | 各 box 獨立寬度 |
| `nested` | 高 | 多層│column 對齊 |
| `flow` | 中 | junction 對齊 |
| `table` | 中 | 在正確欄位補 space |
| `tree` | 低 | 內嵌 box ┐ 對齊 |

## 1. 替換（嚴格，無例外）

```powershell
python symbol_fix.py <path>        # 自動替換 + 寬度診斷
```

所有違規 Unicode **一律替換**，包括 box 外。替換後的寬度陷阱：

| 替換 | 陷阱 | 修法 |
|------|------|------|
| `▼`→`v ` | string +1 char，擠壓同行後方│ | 移除 v 後 1 space |
| `►◄`→`->` `<-` | w2→w2 但 char 數不同 | 調整 ─ 數量對齊 box│ |
| `→`→`-->` | w2→w3，+1 width | 移除同 cell 1 trailing space |
| `×`→`x ` | `4×` 特殊處理為 `4x`（不加 space） | |
| `v` 在 hrule | `┌──v ──┐` 多 1 space | 去 space：`┌──v──┐` |

## 2. 對齊

### 核心原則

1. **target width** = hrule `┌─┐`/`└─┘` 行的 display width
2. **│ column** = 從 hrule ┐ 推導，所有 content│ 必須在同一 col
3. **junction 鏈** = ┬/│/v 必須在同一 col（逐行驗證）
4. **由內而外** = nested 先對齊 inner│，再調 outer gap
5. **hrule 用 ─** = 延伸/縮短 hrule 用 ─，不用空格

### 常見 bug

| 症狀 | 原因 | 修法 |
|------|------|------|
| content│ 比 ┐ 多 1 col | CJK content 比 hrule 寬 | -1 trailing space 或擴展 hrule |
| └┘ 比 ┌┐ 寬 1 | 底部 ┬ 多佔 1 col | +1─ 在 hrule 對齊 |
| v 比上方│ 多 1-N col | `▼`→`v ` 累積偏移 | 逐 v 調間距，對齊 junction col |
| connector chain ┬→│→┴ 不齊 | CJK/hrule 偏移 | 逐行驗 column，統一到 ┬ 定義的 col |
| 表格某欄差 1 | 非最後欄不足 | 在正確欄位補 space |
| 表格某行│偏移 | CJK/ASCII 混合行 pad 不同 | 每欄每行都驗│position |

## 3. 驗證

```powershell
python symbol_fix.py --check <path>    # 零 symbols + 零 width issues
python ascii_align.py --check <path>   # 零 warnings
```

### 否定自查（每次修正後必做）

1. **所有 box**: ┐/│/┘ 在同一 col？
2. **所有 v**: 對齊上方 │/┬/┼？
3. **替換行**: v 後方的│有沒有被擠？
4. 確認無問題後才通知使用者
