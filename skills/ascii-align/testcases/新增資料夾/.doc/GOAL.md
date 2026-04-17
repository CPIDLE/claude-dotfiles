# ASCII Art Regeneration Pipeline — Goal

## 目標

產生一個 **prompt**，讓 Claude Code 讀取現有（可能歪掉的）ASCII art，**重新正確產生**對齊版本。

不手動逐行修改，而是：
1. 自動分析問題
2. 組合成完整 prompt（含乾淨圖 + hints）
3. 交給 Claude Code 執行

---

## Pipeline

```
[原始 .md]
    │
    ▼ Step 1: symbol_fix
              非法 Unicode → ASCII 等價
              ▼→v, →→-->, ←→<--, ×→x, ●→*, ✓→OK ...
[乾淨 .md]
    │
    ▼ Step 2: 寬度分析
              - 找 target width（多數決）
              - 找哪些行寬度不符
              - 識別問題類型：
                  A. hrule ≠ content width（box 內部不一致）
                  B. connector 比 gap 寬（需擴 gap 或縮 connector）
                  C. CJK 推偏 border（trailing space 不足）
                  D. 跨行 border column 不對齊
[issues list]
    │
    ▼ Step 3: gen_prompt
              組合：
              - 字元寬度規則說明（Sarasa Mono TC）
              - 禁用符號替換表
              - 乾淨圖（已 symbol_fix）
              - Hints（per-issue 說明）
[完整 prompt]
    │
    ▼ 使用者貼給 Claude Code
              → 輸出正確 markdown（fenced code block）
```

---

## 交付物

### `gen_prompt.py`

```
用法：python gen_prompt.py <file.md>
輸出：prompt.txt（可直接複製貼給 Claude Code）
```

內部步驟：
1. 讀檔 → symbol_fix → 取得乾淨圖
2. 計算每行 display width（Sarasa Mono TC 規則）
3. 找 target width（most common）
4. 分析 issues（A/B/C/D 四類）
5. 組合 prompt template + hints

### Prompt 結構

```markdown
# ASCII Art Fix

## Character Width Rules (Sarasa Mono TC)
[寬度規則表]

## Forbidden Symbols (already replaced)
[替換表 — 已完成，說明為何]

## Input (cleaned)
\```
[乾淨 ASCII art]
\```

## Issues Found
[自動產生的 per-issue hints]
- Line X: hrule inner=N but content display width=M → expand hrule by K
- Line X: connector `-->` (3w) exceeds gap (2w) → expand gap to 3
- Lines X-Y: border column inconsistent (col A vs col B)
- ...

## Task
Rewrite the ASCII art with all issues fixed.
Output the corrected art as a fenced code block only. No explanation.
```

---

## 驗證方法

用已手動修好的檔案驗證：
- Input: `_sample_161.md`（原始歪版）→ gen_prompt → 給 Claude Code
- Expected: 與手動修好版完全一致

---

## 字元寬度規則（Sarasa Mono TC）

| 類別 | 範例 | 寬度 |
|------|------|------|
| ASCII printable | A-Z, 0-9, 標點 | 1 |
| Box drawing | `─│┌┐└┘├┤┬┴┼` | 1 |
| CJK 漢字 | 中日韓 | 2 |
| 全形括號 | `（）` | 2 |
| `°` `–` | U+00B0, U+2013 | 1 |
| 其他 EAW=A/W/F | `→×▼●★✓` | 2（禁用） |

## 禁用符號替換表

| 禁用 | 替換 | 說明 |
|------|------|------|
| `→` `←` | `-->` `<--` | 方向箭頭 w2 |
| `↑` `↓` | `^` `v` | 垂直箭頭 w2 |
| `▼` `▲` | `v` `^` | 實心箭頭 w2 |
| `×` | `x` | 乘號 w2 |
| `●` `○` | `*` `o` | 圓點 w2 |
| `✓` `✗` | `OK` `NG` | 勾叉 w2 |
| `·` `•` | `.` `*` | 點 w2 |

---

## 進度

- [ ] symbol_fix.py（已存在於 `scripts/`）
- [ ] gen_prompt.py（待建）
- [ ] prompt template（草稿見上）
- [ ] 驗證：sample_161, sample_164
