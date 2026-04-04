---
description: 快速程式碼審核（test/lint/debug/code review）
---
快速審核目前的程式碼變更，平行執行四項檢查。

## 執行步驟

### Step 1：平行執行四項檢查

同時執行以下四項，全部完成後再繼續：

| 檢查項 | 方法 | 掃描範圍 |
|--------|------|----------|
| 測試 | 偵測 jest/vitest/pytest/go test/cargo test，執行之 | 測試框架 |
| Lint | 偵測 eslint/biome/ruff，執行之 | 原始碼 |
| Debug 掃描 | Grep 搜尋 `console.log`、`debugger`、`print(` | 排除測試檔、node_modules |
| Code Review | `git diff --staged` + `git diff`，掃描明顯 bug、安全漏洞、遺漏的錯誤處理 | git diff 範圍 |

> ⚠️ 去重規則：Debug 掃描只報告位置。Code Review 負責品質判斷。同一行以 Code Review 為準。
> ⚠️ 部分失敗處理：任一項失敗標記為 `⚠️ 跳過`，不影響其他項。

### Step 2：輸出一行摘要

```
🔍 審核：測試 ✅/❌/⚠️ | Lint ✅/⚠️ | Debug ✅/⚠️ | Code ✅/⚠️ N issues
```

- 測試失敗（❌）→ 暫停，詢問是否修正
- 其餘只記錄，不暫停
