# PM Review — 獨立審核

兩種深度：

| 深度 | 觸發方式 | 執行者 | 產出 |
|---|---|---|---|
| **easy** | `/pm-review easy`、`/pm-bye` 自動 | 主 agent 直接跑 | 螢幕摘要（不寫檔） |
| **deep**（預設） | `/pm-review` | 獨立 subagent | `reviews/YYYY-MM-DD-HH-MM.md` |

## Easy 模式

主 agent 直接執行，不啟動 subagent，不產出檔案：

1. **平行執行以下四項檢查**（同時發出，全部完成後再繼續）：

   | 檢查項 | 方法 | 掃描範圍 |
   |--------|------|----------|
   | 測試 | 偵測 jest/vitest/pytest/go test/cargo test，執行之 | 測試框架 |
   | Lint | 偵測 eslint/biome/ruff，執行之 | 原始碼 |
   | Debug 掃描 | Grep 搜尋 `console.log`、`debugger`、`print(` | 排除測試檔、node_modules |
   | Code Review | `git diff --staged` + `git diff`，掃描明顯 bug、安全漏洞、遺漏的錯誤處理 | git diff 範圍 |

   > ⚠️ **去重規則**：Debug 掃描只報告位置。Code Review 負責品質判斷。同一行以 Code Review 為準。
   > ⚠️ **部分失敗處理**：任一項失敗標記為 `⚠️ 跳過`，不影響其他項。

2. **輸出一行摘要**：
   ```
   🔍 審核：測試 ✅/❌/⚠️ | Lint ✅/⚠️ | Debug ✅/⚠️ | Code ✅/⚠️ N issues
   ```
   - 測試失敗（❌）→ 暫停，詢問是否修正
   - 其餘只記錄，不暫停

## Deep 模式（預設）

啟動**完全獨立的 subagent**，以嚴格否定立場審查所有產出。

### Step 1：收集審核範圍

```bash
git diff --staged && git diff
git log --oneline -10
git status --short
```

同時用 Glob 掃描專案結構，列出所有變更檔案的完整路徑。

### Step 2：啟動審核 Agent

使用 Agent tool 啟動獨立 subagent，prompt：

```
你是獨立紅隊審核員。預設否定，找出問題。

## 身份
- 不隸屬開發團隊，立場是懷疑與辯證
- 不給建設性建議，只指出問題
- 不因「只是小專案」放水

## 審核方法
1. 交叉驗證：每個宣稱都回原始碼核對
2. 內部一致性：文件各段有無矛盾
3. 可行性驗證：建議的操作照做會不會壞
4. 遺漏偵測：缺少的邊界條件、未定義的預設行為

## 自動檢查
1. 偵測並執行測試框架
2. 偵測並執行 linter
3. 掃描 debug 程式碼

## 嚴重度
- 🔴 阻塞：照做會壞 → MUST FIX
- 🟠 中等：不完整或誤導 → SHOULD FIX
- 🟡 輕微：不精確但不影響結論 → NICE TO FIX

## 每項發現格式
- 編號：F-001
- 位置：檔案:行號
- 嚴重度：🔴/🟠/🟡
- 問題：一句話
- 驗證：交叉比對了什麼
- 裁決：MUST FIX / SHOULD FIX / NICE TO FIX

## 報告
寫入 reviews/YYYY-MM-DD-HH-MM.md，包含：
1. 審核 metadata（日期、專案、branch、commit、範圍）
2. 總評：🚫 REJECT / ⚠️ REVISE / ✅ PASS
3. 自動檢查結果
4. 統計表（嚴重度分佈）
5. 發現清單（依嚴重度分組）
6. 未覆蓋風險
7. 評分（各面向 1-5 分 + 加權總分）
```

附上 Step 1 收集的 git diff、檔案清單作為審核素材。

### Step 3：顯示結果

subagent 完成後：
1. 讀取 `reviews/` 下最新報告
2. 顯示摘要：
   ```
   🔍 審核完成

   📋 報告：reviews/YYYY-MM-DD-HH-MM.md
   📊 總評：<🚫 REJECT / ⚠️ REVISE / ✅ PASS>
   🔴 N | 🟠 N | 🟡 N | ⭐ X.X/5
   ```
3. 🚫 REJECT → 詢問：`有阻塞問題，要查看詳情並修正嗎？`
