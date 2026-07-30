# PM Auto — 自主執行 + 紅隊仲裁收尾

opt-in 的**單次任務**自主模式：卡點不停下來問使用者，改派獨立仲裁 subagent 頂替判斷；只有安全紅線才停下問使用者本人。做完再送一次紅隊 review，發現的問題自動修正。

> **不是常駐行為**：一般任務仍走 global `Plan-Execute Workflow`。只有這次明確打 `/pm-auto` 才套用。

## 觸發

- `/pm-auto <任務描述>` — 全新任務，走 Phase 1～5
- `/pm-auto`（不帶描述，對話中已有進行中任務）— **中途啟用**，見下

---

## Phase 1：Plan

沿用 `EnterPlanMode`：列 Goal / Steps（含檔案路徑）/ Scope boundary / 權限 / 影響，`ExitPlanMode` 等核准。

**這是唯一一次事前確認關卡**——核准後不再為「該怎麼做」停下問使用者，只有 Phase 3 硬停條件例外。

### 中途啟用

原任務已在正常流程跑，使用者中途打 `/pm-auto` = 「剩下的別再問我」。

- **不是開新任務**：已執行完的步驟不追溯套用仲裁
- **但 Phase 4 審全工作樹**：baseline 切不開切換前後（切換前未 commit 的改動照樣在 `git diff` 裡），硬要分只會漏審。審多不審少
- 不重跑完整 plan mode，沿用原 Goal/Scope，只印精簡確認等一次輕量同意：

  ```
  --- 中途啟用確認 ---
  沿用原任務 Goal：<原任務目標>
  剩餘範圍：<還沒做的步驟>
  確認把剩餘部分切換為 pm-auto 自主模式？
  ```

- 核准後進 Phase 2，之後比照全新任務
- log 開頭註記：`本次為中途啟用，原任務於 HH:MM 開始，HH:MM 切換為自主模式`

## Phase 2：Permission Summary + 審核基準點

印 `--- Permission Summary ---`（列需要的工具權限），僅通知不等確認。同時記錄基準點：

```bash
git rev-parse HEAD    # 記為 <baseline>
```

只在 Phase 2 取一次，Phase 3 期間有 commit 也不更新。非 git repo → 改記錄執行前的檔案清單。

## Phase 3：Autonomous Execution — 仲裁分流

沿用 global CLAUDE.md 的 4 個 STOP 條件：

| STOP 條件 | 處理 |
|---|---|
| 未核准的破壞性操作 | **硬停，不可仲裁**，這條紅線不因 `/pm-auto` 鬆動 |
| 超出 scope（邊界模糊）/ 步驟失敗無法自修 / 需修改計畫 | **可仲裁** — 派仲裁 subagent 決策，不問使用者 |

### 硬停清單（不可仲裁）

「破壞性」不靠臨場感覺認定——判定者是正在趕進度的主 agent 本人。以下明列即硬停（Phase 1 已逐項核准的除外）：

| 類別 | 動作 |
|---|---|
| 刪除 / 覆寫 | `rm`、刪目錄、整檔覆寫、`git clean` |
| Git | `git reset --hard`、`git push`（含 `--force`）、`git rebase`、砍 branch/tag |
| 資料層 | DB migration、schema 變更、批次 UPDATE/DELETE |
| **不可逆對外動作** | 寄信、webhook、POST 外部 API、發佈/部署、Artifact 發佈、開 PR / 留言 |
| 環境 | 改 `~/.claude/` 部署檔、系統設定、排程（Task Scheduler / cron） |

> **判不出來 → 當作破壞性，硬停**。「應該還好吧」不是繼續的理由。
> 對外動作單獨列，是因為它們不「破壞」什麼、最容易被當成安全，但送出去收不回來。

### 仲裁 subagent

**一律 `model: opus`**（頂替使用者判斷，不可用 haiku）。Prompt：

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

每次決定 append 進 `reviews/YYYY-MM-DD-HH-MM-pmauto.md`（同一次執行共用一份，時戳取第一次寫入時間）：

```markdown
## 仲裁記錄

| 時間 | 卡點描述 | 仲裁決策 | 理由 |
|---|---|---|---|
```

判斷 (b) → 用 `AskUserQuestion` 問使用者（建議選項排第一 + label 加「（建議）」）。

### 仲裁上限（強制升級）

命中任一條就停止仲裁、升級問使用者，並附完整仲裁歷程（試過什麼、為何都不成立）：

- 同一步驟連續仲裁 **2 次**仍卡 → 再派也一樣
- 本次累計仲裁 **5 次** → 卡點密度這麼高代表 Plan 本身有問題

## Phase 4：收尾 Redteam Review

**直接跑 `/pm-review` deep 全流程**（Step 0 事實基礎 → Step 1 收集 → Step 1.5 CodeRabbit → Step 2 審核），不自訂精簡版紅隊：人盯得最少的模式不該配最弱的審核，而且複製的 prompt 一定會 drift。單一事實來源在 `/pm-review`。

### 審核素材

用 `<baseline>` 界定範圍，**四項都要給**——裸 `git diff` 看不到 untracked 新檔，以產生新檔為主的任務只給它等於讓紅隊審空 diff 然後回 ✅ PASS：

```bash
git diff <baseline>...HEAD    # 1. 已 commit
git diff                      # 2. 未 commit
git status --short            # 3. 列出 untracked
```

4. **untracked 檔逐一 `Read` 附全文**（排除自己的 log）：`git status --short` 只給檔名，紅隊知道「有這個檔」卻看不到內容。**不要用 `git add -N` 代替**——那會動 index，等於在自主模式下製造未核准的狀態變更。

非 git repo → 用 Phase 2 記的檔案清單做前後比對，新增/修改的檔一律 Read 附全文。

外加 Phase 3 的**仲裁記錄**：這次執行中沒有人類把關的決策點，最該被盯。

### 套用 `/pm-review` 的四處覆寫

| 原行為 | pm-auto 覆寫 |
|---|---|
| Step 0 掃到 cc 衍生檔（regex 含 `reviews/`）→ 跑 `/rt-fact` | **排除本次自己產的 `reviews/*-pmauto.md`**，否則必然命中自己的 log，每次白燒一輪 |
| Step 0 事實基礎 ⚠️/❌ → 暫停詢問 | **視同 (b) 升級問使用者**：事實層污染時，自動修正只會把錯誤修得更整齊 |
| Step 3 🚫 REJECT → 詢問是否修正 | 走下方自動修正流程 |
| Step 2 報告寫入 `reviews/YYYY-MM-DD-HH-MM.md` | **改 append 進 `-pmauto.md` 那份**（與仲裁記錄同檔）。不覆寫會產生兩份報告，Step 3 的「讀最新報告」撈到哪份看時戳運氣 |

### 處理審核結果

- **🔴 / 🟠** → **自動修正**，不再問
- **🟡** → 只列報告，不動手

自動修正的兩條界線：

1. **不得越過 Phase 1 的 Scope boundary**。🟠「缺少錯誤處理」照字面修下去會寫出從沒核准的新程式碼路徑——修正權是收尾用的，不是拿來擴張任務。超出 → 不修，降級 🟡 並註記「超出 scope 未修」。**判不出來算不算超出 → 當作超出**（判定者同樣是想把事做完的主 agent，比照硬停清單從嚴）。
2. **修正動作命中硬停清單 → 硬停**，不因為「review 要求的」放行。

### 限定範圍複驗（上限 1 輪）

無 🔴/🟠 發現（沒東西要修）→ **整節跳過**，直接 Phase 5。

有修正時：跑驗證（有 test 就跑，無則跳過），再派 subagent（`model: opus`）複驗：

```
以下是紅隊發現的 N 項問題，以及針對每項所做的修正 diff。
逐項判定：已解決 / 未解決 / 修正本身引入新問題。
只看這 N 項，不要擴大範圍重審整份變更。
```

- 全部已解決 → Phase 5
- 任一未解決 / 引入新問題 → **視同 (b) 升級問使用者**，附複驗結果
- **只跑 1 輪**，不遞迴重審

> 沒有這輪的話，「若修正解決不了就升級」缺乏判定依據，🔴 阻塞的修正等於零驗證出貨。

**總評不自行改判**：總評永遠是紅隊 subagent 當下給的那個，主 agent 不得因為「我修好了」改成 ✅ PASS。

## Phase 5：結尾摘要

```
🤖 PM Auto 完成

📊 總評：<🚫 REJECT / ⚠️ REVISE / ✅ PASS>（紅隊原始裁決，未因修正改判）
✅ 完成項目：<列點>
⏭️ 跳過步驟：N（仲裁判 (c)，逐項列出理由）
🧭 仲裁次數：N（詳見 log）
🔧 自動修正：N 項（🔴 N / 🟠 N）
🔁 複驗：N 已解決 / N 未解決
🟡 待人工評估：N 項（含超出 scope 未修：N）
⚠️ 升級詢問：N 次（原因：<簡述>）
📋 Log：reviews/YYYY-MM-DD-HH-MM-pmauto.md
```

---

## 使用範例（示意）

`/pm-auto 幫這個 Node.js 專案的 .gitignore 加一條規則，忽略 build/ 產出目錄`

**P1** Goal 為新增一條忽略 build/ 的規則；Scope boundary：只改 `.gitignore`、不刪改既有規則。使用者核准。

**P2** 印 Permission Summary（Read/Edit `.gitignore`、Write log、Bash git、Agent ×3），記 `<baseline> = a1b2c3d`。

**P3** `.gitignore` 混雜 CRLF/LF 且檔尾無換行，附加新行連續失敗兩次 → 「步驟失敗無法自修」，可仲裁：

```
決策：(a) 偵測檔案主要換行慣例，補上檔尾換行後插入新規則，不動既有行
理由：只改插入方式，不觸碰既有規則，風險低
信心程度：高
```

> 若卡點性質是「`.gitignore` 其實由工具自動生成、手改會被覆蓋」→ 仲裁選 (b) 升級。若這步是「刪掉舊的 build/ 目錄」→ 硬停，根本不會走到仲裁。

**P4** 跑 `/pm-review` deep，素材為 `git diff a1b2c3d...HEAD` + `git diff` + `git status --short` + 仲裁記錄；排除自己的 log 所以沒誤觸發 `/rt-fact`，純設定檔變更跳過 CodeRabbit。發現：

```
F-001｜.gitignore 新增行｜🟠 中等｜SHOULD FIX
規則寫成 build/（無開頭 /）會遞迴比對任何層級名為 build 的目錄，
底下未來新增的檔案會被靜默忽略、不出現在 git status
```

總評 ⚠️ REVISE。🟠 過界線檢查（仍在 Scope boundary 內、非硬停動作）→ 錨定成 `/build/`，跑 `git ls-files | grep -E '(^|/)build(/|$)'` 確認沒有已追蹤路徑受影響。複驗回報「已解決，未引入新問題」。

> 對照組：若紅隊開的是「應該連 `dist/`、`coverage/` 一起忽略」→ 超出 Scope boundary，**不自動修**，降級 🟡。

**P5** 總評 ⚠️ REVISE（不改判）｜跳過 0｜仲裁 1 次｜自動修正 1 項（🟠 1）｜複驗 1 已解決｜升級 0 次。

---

## 注意事項

- 所有輸出使用繁體中文
- 仲裁 / 審核 / 複驗 subagent 一律 `model: opus`，不可用 haiku
- **破壞性操作永遠不可仲裁**，判不出來一律從嚴
- opt-in 單次模式，一般任務仍走 global 預設
- 中途啟用只切換剩餘部分，不追溯
