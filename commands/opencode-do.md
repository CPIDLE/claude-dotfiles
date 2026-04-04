# opencode-do — 委派任務給 opencode

Claude Code 產 spec，opencode 執行。用 `$ARGUMENTS` 接收參數。

## 子指令

| 指令 | 說明 |
|---|---|
| `/opencode-do <任務>` | 產出 spec（手動模式） |
| `/opencode-do auto <任務>` | 產 spec + 自動執行 + 自動審核 |
| `/opencode-do agents` | 列出所有 agent 狀態 |
| `/opencode-do review` | 審核交付結果（手動模式） |
| `/opencode-do review <id>` | 審核指定 agent |
| `/opencode-do review all` | 批次審核所有已完成未審核的 agent |
| `/opencode-do status` | 查看等級與歷史 |
| `/opencode-do set-level <1-3>` | 手動設定等級 |

---

## 狀態檔

在當前專案 memory 目錄下：
- `opencode_level.md` — 一個數字（1/2/3），不存在預設 1
- `opencode_history.md` — markdown 表格紀錄


Spec 檔（opencode 可直接讀取）：
- **專案根目錄** `.opencode-task.md` — 當前待執行的 spec

命名規則：
- 第一次：`.opencode-task.md`
- 產新 spec 時：若 `.opencode-task.md` 已存在，先改名為 `.opencode-task-<N>.md`（N 為下一個流水號），再寫入新的 `.opencode-task.md`
- 這樣 `.opencode-task.md` 永遠是最新任務，歷史任務保留為 `.opencode-task-1.md`、`.opencode-task-2.md`...

---

## 主流程：`/opencode-do <任務>`

1. 讀 `opencode_level.md` 取等級，不存在視為 L1
2. **紅線檢查**：任務涉及架構決策、AGENTS.md/CLAUDE.md 修改、安全敏感、跨系統整合、release → 拒絕，印 `🚫 不適合委派：<原因>`
3. 掃描相關程式碼，確認涉及的檔案
4. 依等級產 spec（整段放在 code block 內方便複製）
5. 若 `.opencode-task.md` 已存在 → 改名為 `.opencode-task-<N>.md`（下一個流水號），再將新 spec 寫入 `.opencode-task.md`
6. 結尾印：
   ```
   📋 完成後：/opencode-do review
   💡 或使用 /opencode-do auto <任務> 全自動執行
   ```

### L1 Spec（新模組）

只准新增檔案。

```
# Task: <標題>
## Level: L1

## 目標
<做什麼>

## 新增檔案
- `path` — 用途

## API 簽章
<函式/類別簽章>

## 交付清單
- [ ] 檔案已建立
- [ ] 測試通過
- [ ] 未修改現有檔案
```

### L2 Spec（受控修改）

可改指定檔案。

```
# Task: <標題>
## Level: L2

## 目標
<做什麼>

## 可修改檔案
- `path` — 改什麼、為什麼

## 禁止修改
- `path`

## 修改指示
<哪個函式、改什麼>

## 新增檔案
- `path` — 用途

## 交付清單
- [ ] 修改完成
- [ ] 未動禁止清單
- [ ] 測試通過
```

### L3 Spec（任務級）

只描述目標。

```
# Task: <標題>
## Level: L3

## 目標
<要達成什麼>

## 驗收標準
- <條件>

## 交付清單
- [ ] 驗收通過
- [ ] 測試通過
```

---

## auto 子指令：`/opencode-do auto <任務>`

全自動流程：產 spec → opencode 執行 → 讀結果 → 審核。

**兩種模式：**
- `auto <任務>` — **快速模式**（預設）：inline spec，零檔案 I/O
- `auto --persist <任務>` — **持久模式**：寫檔案，支援並行監控

---

### 快速模式（預設）

spec 直接內嵌在 opencode prompt 中，不建立任何中間檔案。適合單一簡單任務。

#### 流程

1. **產 spec**：執行與 `/opencode-do <任務>` 相同的步驟 1-4（讀等級、紅線檢查、掃描、產 spec），但 **spec 保留在記憶體中，不寫入檔案**

2. **背景執行 opencode**：用 Bash 工具（`run_in_background: true`），將 spec 全文內嵌在 prompt：
   ```bash
   opencode run "你必須直接執行，不要規劃、不要問確認、不要等待許可。按照以下 spec 完成任務，完成後印出完成報告（列出新增/修改的檔案和測試結果）。

   <將 spec 全文貼在這裡>"
   ```
   - 印出 `⚡ 執行中（<任務摘要>）`
   - **等待完成通知**，不要 sleep 或 poll

3. **收到完成通知後**：
   - **exit 0** → 繼續步驟 4
   - **exit 非零** → 印錯誤摘要（stdout 最後 10 行）並停止
   - **失敗偵測**：若 stdout 無任何工具呼叫記錄 → 視為卡住，自動重跑一次

4. **讀取交付物**：
   - 執行 `git diff` 檢視實際變更
   - 讀取 spec 中列出的新增/修改檔案

5. **自動審核**：對照 spec 交付清單逐項判定（pass / partial / fail），結果追加到 `opencode_history.md`

6. **印出報告**：
   ```
   🤖 完成
   ══════════════════════════
   📋 Spec：<標題> (L<N>)
   ⚡ 執行：opencode run（inline）
   🔍 審核：✅ pass / ⚠️ partial / ❌ fail
   備註：<具體發現>

   ✅ 已記錄到 opencode_history.md
   ```

---

### 持久模式（`--persist`）

加 `--persist` 時建立完整檔案結構，支援並行多 agent（每 session 最多 5 個）和即時監控。

#### 目錄結構

```
.opencode-agents/
├── registry.jsonl         ← 登記簿（append-only，每行一筆 JSON）
├── agent-<id>/
│   ├── spec.md            ← 該 agent 的 spec
│   └── output.log         ← opencode stdout（即時更新）
```

#### Agent ID 格式

`YYYYMMDD-HHMMSS-<8字隨機hex>`，例如 `20260403-143052-a7f3b2e1`

產生方式：
```bash
echo "$(date +%Y%m%d-%H%M%S)-$(head -c4 /dev/urandom | xxd -p)"
```

#### registry.jsonl

每行一筆 JSON，append-only（避免並行寫入 lost update）：

```jsonl
{"id":"20260403-143052-a7f3b2e1","task":"建立 calc.py","level":"L1","status":"running","started":"2026-04-03T14:30:52"}
{"id":"20260403-143052-a7f3b2e1","status":"completed","finished":"2026-04-03T14:31:15"}
{"id":"20260403-143052-a7f3b2e1","status":"reviewed","review":"pass","note":"(auto) 3/3 驗收通過"}
```

讀取時以 **同 id 最後一行** 為準。

#### 流程

1. **產 ID**：用上述 bash 指令產生唯一 ID

2. **限額檢查**：讀 `registry.jsonl`，解析每個 agent 最新狀態：
   - 計算 status=running 的數量
   - started 超過 10 分鐘且 status=running → 視為 stale，append 一行 `{"id":"...","status":"stale"}`
   - running 數量 ≥ 5 → 拒絕：
     ```
     ⚠️ 已達上限（5/5 agents 執行中）。等待完成或用 /opencode-do agents 查看狀態。
     ```

3. **產 spec**：執行與 `/opencode-do <任務>` 相同的步驟 1-4。Spec 寫入 `.opencode-agents/agent-<id>/spec.md`

4. **登記**：append 一行到 `registry.jsonl`，status=running

5. **背景執行 opencode**：用 Bash 工具（`run_in_background: true`）：
   ```bash
   opencode run "你必須直接執行，不要規劃、不要問確認、不要等待許可。讀取 .opencode-agents/agent-<id>/spec.md 並立即按照 spec 完成任務。完成後印出完成報告，列出新增/修改的檔案和測試結果。" > .opencode-agents/agent-<id>/output.log 2>&1
   ```
   - 印出 `⚡ Agent <id> 執行中（<任務摘要>）`
   - **等待完成通知**，不要 sleep 或 poll
   - **失敗偵測**：完成後讀 log，若無任何工具呼叫記錄 → 視為卡住，自動重跑一次

6. **收到完成通知後，讀取結果**：
   - 讀 `.opencode-agents/agent-<id>/output.log` 全文
   - **exit 0** → append `{"id":"...","status":"completed","finished":"..."}` → 繼續步驟 7
   - **exit 非零** → append `{"id":"...","status":"failed"}` → 印錯誤摘要並停止

7. **讀取交付物**：`git diff` + 讀取 spec 列出的檔案

8. **自動審核**：對照交付清單判定，結果 append 到 registry + `opencode_history.md`

9. **印出報告**（同快速模式格式，但包含 Agent ID）

#### 注意事項

- opencode run 會自動 approve 所有工具呼叫，無需人工介入
- 執行中可隨時 Read `.opencode-agents/agent-<id>/output.log` 監控進度
- 如果 opencode 輸出不完整，仍進行審核，以 git diff 為準
- 多個 auto --persist 可同時啟動，各自獨立 ID + 目錄

---

## agents 子指令：`/opencode-do agents`

列出所有 agent 狀態。

### 流程

1. 讀 `.opencode-agents/registry.jsonl`，不存在 → `📭 沒有 agent 紀錄。`
2. 解析每個 agent 最新狀態（同 id 取最後一行）
3. started 超過 10 分鐘且 status=running → 標記為 stale（append 到 registry）
4. 印出表格：

```
🤖 opencode agents
═══════════════════
ID                         | 任務           | 狀態           | 審核
20260403-143052-a7f3b2e1   | calc.py        | ✅ completed   | ✅ pass
20260403-143055-b2e1c3d4   | counter.py     | ⚡ running     | —
20260403-143100-e5f67890   | greet.py       | ⏳ stale       | —
─────��──────────────
執行中：1/5
```

---

## review 子指令

審核 opencode 的交付成果。三種用法：

| 用法 | 說明 |
|---|---|
| `/opencode-do review` | 手動模式：讀 `.opencode-task.md`（向後相容） |
| `/opencode-do review <id>` | 審核指定 agent |
| `/opencode-do review all` | 批次審核所有已完成未審核的 agent |

### 審核流程（通用）

1. **取得 spec**：
   - 無參數 → 讀 `.opencode-task.md`
   - 有 id → 讀 `.opencode-agents/agent-<id>/spec.md`
   - `all` → 從 registry 找 status=completed 且無 review 的 agent，逐一執行以下步驟
2. 讀取 git diff 或掃描 spec 中列出的檔案，確認交付物
3. 跑測試（如有）
4. 對照 spec 交付清單逐項判定
5. 自動判定結果：
   - **pass** — 交付清單全部完成、測試通過、未違反限制
   - **partial** — 大致完成但有缺漏（如少了 edge case、部分測試未過）
   - **fail** — 未達標、破壞現有功能、違反禁止事項
6. 記錄：
   - 追加到 `opencode_history.md`（auto 模式備註欄加 `(auto)` 前綴）
   - 如果是 agent 模式 → 寫 `.opencode-agents/agent-<id>/result.json` + append registry

```markdown
| 日期 | Level | 任務 | 結果 | 備註 |
|------|-------|------|------|------|
| 2026-04-03 | L1 | 模組開發 | pass | 46 tests 全過 |
```

7. 印出審核摘要：

```
🔍 opencode 交付審核
════════════════════
任務：<標題>
等級：L<N>
結果：✅ pass / ⚠️ partial / ❌ fail
備註：<具體發現>

✅ 已記錄到 opencode_history.md
```

---

## status 子指令

讀兩個檔案，印：

```
目前等級：L1
歷史：L1 ✅3 ⚠️1 ❌0 | L2 ✅1
```

---

## set-level 子指令

寫入數字到 `opencode_level.md`，印 `✅ 已設為 L<N>`

---

## 輸出語言

繁體中文。技術術語保持英文。
