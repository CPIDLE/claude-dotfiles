# PM Auto — 自主執行 + 紅隊仲裁收尾

opt-in 的**單次任務**自主模式：卡點不停下來問使用者，改派獨立仲裁 subagent 頂替判斷；只有真正的安全紅線才停下問使用者本人。全部做完後再送一次紅隊 review，把發現的問題自動修正掉。

> **不是常駐行為**：一般任務仍走 global `Plan-Execute Workflow` 預設（會照常在 STOP 條件停下問使用者）。只有使用者明確打 `/pm-auto` 這次任務才套用本流程。

## 觸發

- `/pm-auto <任務描述>` —— 全新任務，走完整 Phase 1～5
- `/pm-auto`（不帶任務描述，且對話中已有進行中的任務）—— **中途啟用**，見下方「中途啟用」小節

---

## Phase 1：Plan

沿用既有 `EnterPlanMode`：列 Goal / Steps（含檔案路徑）/ Scope boundary / 權限 / 影響。`ExitPlanMode` 等使用者核准。

**這是整個流程唯一一次事前確認關卡**——核准之後直到任務結束都不會再為了「該怎麼做」停下來問使用者，只有 Phase 3 的硬停條件例外。

### 中途啟用（任務已在執行中）

適用情境：目前有個任務已經在正常 Plan-Execute Workflow 下跑（可能原本就核准過一次 Plan），使用者中途不帶任務描述直接打 `/pm-auto`，意思是「接下來剩下的部分改自主模式，卡點別再問我」。

- **不是開新任務**：已經執行完的步驟不受影響，不追溯套用仲裁或 Phase 4 自動修正
- **Phase 1 精簡處理**：不重新走完整 `EnterPlanMode`/`ExitPlanMode`，沿用原任務已核准的 Goal/Scope，只印一段精簡確認：

  ```
  --- 中途啟用確認 ---
  沿用原任務 Goal：<原任務目標>
  剩餘範圍：<列出還沒做的步驟>
  確認把剩餘部分切換為 pm-auto 自主模式？
  ```

  等使用者一次輕量核准（簡短同意即可，不必是完整 Plan 核准儀式）
- 核准後直接進入 Phase 2 Permission Summary，之後比照全新任務走 Phase 3～5
- log 開頭加一行註記：`本次為中途啟用，原任務於 HH:MM 開始，於 HH:MM 切換為 pm-auto 自主模式`，方便事後追溯這次執行不是從頭到尾都自主

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

## 使用範例

> 以下純屬示意（walkthrough），不是真的對某個外部 repo 動手，用來說明五個 Phase 實際跑起來的樣子。

**觸發**：

```
/pm-auto 幫這個 Node.js 專案的 .gitignore 加一條規則，忽略 build/ 產出目錄
```

**Phase 1：Plan**

```
Goal：.gitignore 新增一條忽略 build/ 的規則
Steps：
  1. Read .gitignore 確認現有規則與換行慣例
  2. Edit .gitignore 加入規則
  3. Write reviews/*.md（仲裁記錄 + 收尾 review 共用同一份）
Scope boundary：只改 .gitignore；不刪改任何既有規則
權限：Read、Edit、Write（reviews/ log）、Agent（仲裁 subagent）、Agent（收尾審核 subagent）
影響：低風險，純設定檔異動，不改動既有規則內容
```

使用者核准（呼叫 `ExitPlanMode`）。

**Phase 2：Permission Summary**

```
--- Permission Summary ---
- Read：.gitignore
- Edit：.gitignore
- Write：reviews/YYYY-MM-DD-HH-MM-pmauto.md（示意檔名，非真實存在的檔案；時戳取本次執行第一次寫入 log 的時間，之後同一次執行都 append 進同一份，不會改變）
- Agent：仲裁 subagent（model: opus）
- Agent：收尾審核 subagent（model: opus）
```

**Phase 3：Autonomous Execution — 仲裁分流範例**

執行 Edit 時，`.gitignore` 混雜 CRLF/LF 換行且檔尾沒有換行字元，直接在檔尾附加新行的嘗試連續失敗兩次（精確字串比對不到預期的行尾）。這是「步驟失敗無法自修」——可仲裁範圍，派仲裁 subagent：

```
決策：(a) 改用讀取原始位元組偵測檔案主要換行慣例，在檔尾補上一個換行字元後插入新規則；不改動任何既有行的內容或順序
理由：純粹修正插入方式本身，不觸碰既有規則，風險低
信心程度：高
```

寫入仲裁記錄：

```markdown
## 仲裁記錄

| 時間 | 卡點描述 | 仲裁決策 | 理由 |
|---|---|---|---|
| 14:32 | .gitignore 換行不一致，附加新行連續失敗 | (a) 偵測換行慣例後插入，不動既有行 | 只改插入方式，不觸碰既有規則，風險低 |
```

> 這次只走到分支 (a)。若卡點的性質是「這其實已經超出原本 Plan 核准的範圍」（例如發現 `.gitignore` 其實是由另一個工具自動生成、手動改了下次會被覆蓋）→ 仲裁會選 (b)，回報建議升級問使用者，不會自己硬做決定。而如果這一步原本是「刪掉舊的 build/ 目錄」這類破壞性操作，不管仲裁怎麼判斷都不會走到這裡——那是硬停條件，直接停下問使用者，跳過仲裁。

**Phase 4：收尾 Redteam Review**

獨立審核 subagent 檢查這次 `.gitignore` 異動，發現：

```
編號：F-001
位置：.gitignore 新增行
嚴重度：🟠 中等
問題：新規則寫成 build/（沒有開頭 /），會遞迴比對到專案任何層級、名為 build 的目錄；若該目錄底下未來新增檔案，會被 git 自動忽略而不會出現在 git status/git add 的結果中，即使該目錄不是建置產物
裁決：SHOULD FIX
```

總評：⚠️ REVISE（附加進同一份 `reviews/YYYY-MM-DD-HH-MM-pmauto.md`）

🟠 屬於自動修正範圍 → 把規則錨定成 `/build/`（限定在專案根目錄）。非 test 型變更，改跑 `git ls-files | grep -E '(^|/)build(/|$)'` 確認目前沒有已追蹤的路徑落在某個名為 build 的目錄下。

> Phase 4 本體沒有定義「修正後重新出總評」的機制（不做第二輪重審）：修正完成後，這次執行的總評仍是審核 subagent 當下給的 ⚠️ REVISE，不會被主 agent 自行改判成 ✅ PASS。

**Phase 5：結尾摘要**

```
🤖 PM Auto 完成

✅ 完成項目：.gitignore 新增 /build/ 規則（含換行慣例修正 + 錨定修正）
🧭 仲裁次數：1（詳見 log）
🔧 review 後自動修正：1 項（🔴 0 / 🟠 1）
🟡 待人工評估：0 項
⚠️ 升級詢問：0 次（無）
📋 Log：reviews/YYYY-MM-DD-HH-MM-pmauto.md（示意，非本 repo 實際檔案）
```

---

## 注意事項

- 所有輸出使用繁體中文
- 仲裁 / 審核 subagent 一律 `model: opus`，不可用 haiku
- **破壞性操作永遠不可仲裁**，這是硬性安全線，不因本指令鬆動
- `/pm-auto` 是 opt-in 單次模式，一般任務仍走 global 預設 Plan-Execute Workflow
- 中途啟用（不帶任務描述）只切換**剩餘部分**，已執行完的步驟不追溯套用仲裁/自動修正
