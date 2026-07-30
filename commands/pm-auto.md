# PM Auto — 自主執行 + 紅隊仲裁收尾

opt-in 的**單次任務**自主模式：卡點不停下來問使用者，改派獨立仲裁 subagent 頂替判斷；只有真正的安全紅線才停下問使用者本人。全部做完後再送一次紅隊 review，把發現的問題自動修正掉。

> **不是常駐行為**：一般任務仍走 global `Plan-Execute Workflow` 預設（會照常在 STOP 條件停下問使用者）。只有使用者明確打 `/pm-auto` 這次任務才套用本流程。

## 觸發

`/pm-auto <任務描述>`

---

## Phase 1：Plan

沿用既有 `EnterPlanMode`：列 Goal / Steps（含檔案路徑）/ Scope boundary / 權限 / 影響。`ExitPlanMode` 等使用者核准。

**這是整個流程唯一一次事前確認關卡**——核准之後直到任務結束都不會再為了「該怎麼做」停下來問使用者，只有 Phase 3 的硬停條件例外。

## Phase 2：Permission Summary

核准後執行前印 `--- Permission Summary ---`（列需要的工具權限），僅通知不等確認，同全域慣例。

## Phase 3：Autonomous Execution — 仲裁分流

沿用 global CLAUDE.md 既有 4 個 STOP 條件，分流處理：

| STOP 條件 | 處理方式 |
|---|---|
| 未核准的破壞性操作 | **硬停，不可仲裁** —— 直接停下問使用者，這條紅線不因 `/pm-auto` 鬆動（呼應系統層 Git Safety Protocol） |
| 超出 scope（邊界模糊）/ 步驟失敗無法自修 / 需修改計畫 | **可仲裁** —— 呼叫 Agent tool 派獨立仲裁 subagent 決策，不停下問使用者 |

### 仲裁 subagent

**一律 `model: opus`**（頂替使用者判斷，屬於高階推理，不可用 haiku）。

Prompt：

```
你是獨立仲裁者。你的任務是在這個卡點頂替使用者做決定，不是來找方便答案討好任務推進。

## 輸入素材
- 原始任務目標（Phase 1 核准的 Plan 內容）
- 目前卡在哪一步、卡點的具體描述
- 已經試過的選項、為什麼卡住

## 決策空間（三選一）
(a) 選一個方案繼續執行
(b) 判斷這個卡點其實已經超出原任務精神／原 Plan 核准範圍 → 不要自己決定，回報「建議升級問使用者」
(c) 判斷應放棄某個步驟但不影響整體目標 → 記錄理由後跳過該步驟

## 輸出格式
- 決策：(a)/(b)/(c) 之一 + 具體內容
- 理由：1-2 句
- 信心程度：高/中/低
```

每次仲裁決定 append 進 `reviews/YYYY-MM-DD-HH-MM-pmauto.md`（新檔，同一次 `/pm-auto` 執行共用一份）：

```markdown
## 仲裁記錄

| 時間 | 卡點描述 | 仲裁決策 | 理由 |
|---|---|---|---|
| HH:MM | ... | (a)/(b)/(c) ... | ... |
```

仲裁者判斷 (b) → 主 agent 用 `AskUserQuestion` 停下問使用者（依全域偏好：有建議的選項排第一 + label 加「（建議）」）。

## Phase 4：收尾 Redteam Review

全部自主執行完成後，呼叫 Agent tool 派**獨立審核 subagent（`model: opus`）**，沿用 `/pm-review` Step 2 的骨架：

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
5. spec 一致性（僅當提供 specs/<slug>.md）

## 嚴重度
- 🔴 阻塞：照做會壞 → MUST FIX
- 🟠 中等：不完整或誤導 → SHOULD FIX
- 🟡 輕微：不精確但不影響結論 → NICE TO FIX

## 報告
附加進 reviews/YYYY-MM-DD-HH-MM-pmauto.md，包含總評（🚫 REJECT / ⚠️ REVISE / ✅ PASS）+ 發現清單（依嚴重度分組，含位置/問題/裁決）。
```

附上 Phase 3 執行結果（改了哪些檔、git diff）作為審核素材。

### 處理審核結果

- **🔴 阻塞 / 🟠 中等** → **自動修正**，不再問（呼應「事後 review 完再完成修正」的原始需求）
- **🟡 輕微** → 列在最終報告，不自動動手（避免過度擴權）
- 修正完後跑一次驗證（有對應 test 就跑，無則跳過，比照 Coding Discipline），**不做第二輪無限迴圈重審**
- 若審核 subagent 判定嚴重到 **🚫 REJECT** 且自動修正解決不了 → 視同 Phase 3 的 (b) 情況，升級問使用者

## Phase 5：結尾摘要

```
🤖 PM Auto 完成

✅ 完成項目：<列點>
🧭 仲裁次數：N（詳見 log）
🔧 review 後自動修正：N 項（🔴 N / 🟠 N）
🟡 待人工評估：N 項
⚠️ 升級詢問：N 次（原因：<簡述>）
📋 Log：reviews/YYYY-MM-DD-HH-MM-pmauto.md
```

---

## 注意事項

- 所有輸出使用繁體中文
- 仲裁 / 審核 subagent 一律 `model: opus`，不可用 haiku
- **破壞性操作永遠不可仲裁**，這是硬性安全線，不因本指令鬆動
- `/pm-auto` 是 opt-in 單次模式，一般任務仍走 global 預設 Plan-Execute Workflow
