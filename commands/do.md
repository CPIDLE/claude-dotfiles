# do — 委派任務給外部 LLM

Claude Code 產 spec，外部 LLM 引擎執行。用 `$ARGUMENTS` 接收參數。

> 取代 `/opencode-do` 和 `/gemini-do`。引擎由 `DO_ENGINE` 環境變數決定。

## 子指令

| 指令 | 說明 |
|---|---|
| `/do easy <任務>` | 單次呼叫，快速產出 |
| `/do deep <任務>` | 多輪（生成→驗證→修正），高品質產出 |
| `/do status` | 查看等級與歷史 |
| `/do set-level <1-3>` | 手動設定等級 |

---

## 引擎設定

環境變數 `DO_ENGINE` 決定使用哪個引擎（預設 `gemini`）：

| `DO_ENGINE` | 執行方式 | 必要條件 |
|---|---|---|
| `gemini`（預設） | `google.genai` Python SDK | `pip install google-genai` + `GEMINI_API_KEY` |
| `ollama` | Ollama REST API（local） | Ollama 已啟動 + model 已下載 |
| `opencode` | `opencode run --format json` | opencode CLI 已安裝 |

### Model 設定

| 環境變數 | 用途 | gemini 預設 | ollama 預設 | opencode 預設 |
|---|---|---|---|---|
| `DO_MODEL_EASY` | easy 模式 | `gemini-3.1-flash-lite-preview` | `qwen3:8b` | `gemini-3-flash-preview` |
| `DO_MODEL_DEEP` | deep 模式全部輪次 | `gemini-3-flash-preview` | `qwen3:8b` | `gemini-3-flash-preview` |
| `OLLAMA_URL` | Ollama 端點 | — | `http://localhost:11434` | — |

> Benchmark 驗證：flash-lite 品質 4.85/5.0（-0.15），速度 3.7x，價格 -50%。easy 用 lite 夠用，deep 維持 flash。

---

## 引擎呼叫實作

所有引擎統一透過 `do_helper.py` 呼叫，單一進程內完成所有 API 呼叫（含 deep 多輪）：

```bash
# helper 路徑（install script 會複製到此）
DO_HELPER="$HOME/.claude/skills/do/scripts/do_helper.py"

# easy — 單次呼叫（系���提示已內嵌，只傳 spec）
PYTHONIOENCODING=utf-8 python "$DO_HELPER" easy --engine "${DO_ENGINE:-gemini}" <<'SPEC_EOF'
<spec 全文>
SPEC_EOF

# deep — 多輪在同一進程完成，輸出 JSON-lines
PYTHONIOENCODING=utf-8 python "$DO_HELPER" deep --engine "${DO_ENGINE:-gemini}" <<'SPEC_EOF'
<spec 全文>
SPEC_EOF
```

### 輸出格式（JSON-lines）

easy 輸出一行：
```json
{"status":"ok","result":"<程式碼或文件>"}
```

deep 輸出多行（每輪一行 + 最終結果）：
```jsonl
{"round":1,"status":"done","result":"<R1 產出>"}
{"round":2,"status":"done","result":"<R2 審核 JSON>"}
{"final":"<最終程式碼>","rounds":2,"verdict":"pass","issues":[]}
```

Claude Code 解析最後一行取 `final`（程式碼）、`rounds`（輪數）、`verdict`（pass/fixed）、`issues`、`advisory_notes`（R2 觀察到 spec 外的潛在問題，永遠取自 R2，即使 R3 觸發）。

> 優勢：deep 模式省去多次 Python 啟動 + Claude Code round-trip，加速約 4-8 秒。

---

## 引擎前置檢查

執行前用 `do_helper.py check` 檢查引擎是否可用：

```bash
PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/do/scripts/do_helper.py" check --engine "${DO_ENGINE:-gemini}"
```

輸出 `{"ok":true}` 表示可用，`{"ok":false,"error":"..."}` 表示失敗。
失敗時印 `⚠️ 引擎不可用：<error>`，停止，不 fallback 到其他引擎。

---

## 狀態檔

在當前專案 memory 目錄下：
- `do_level.md` — 一個數字（1/2/3），不存在預設 1
- `do_history.md` — markdown 表格紀錄

> 向後相容：如果 `do_level.md` 不存在但 `opencode_level.md` 存在 → 讀取 `opencode_level.md`。
> 如果 `do_history.md` 不存在但 `opencode_history.md` 存在 → 讀取 `opencode_history.md`。
> 新紀錄一律寫入 `do_history.md`。

---

## 共用：Spec 產出流程

easy 和 deep 共用前 4 步：

1. 讀 `do_level.md` 取等級，不存在視為 L1
2. **紅線檢查**：任務涉及架構決策、AGENTS.md/CLAUDE.md 修改、安全敏感、跨系統整合、release → 拒絕，印 `🚫 不適合委派：<原因>`
3. 掃描相關程式碼，確認涉及的檔案
4. 依等級產 spec（L1/L2/L3 格式見下方）

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

## easy 模式：`/do easy <任務>`

單次 LLM 呼叫，適合簡單程式碼或文件產出。不做驗證、不重試。

### 流程

1. **Spec 產出**（共用步驟 1-4），spec 保留在記憶體中

2. **呼叫 do_helper.py easy**：
   - 印出 `⚡ <引擎名稱> 執行中（<任務摘要>）`
   - 執行：
     ```bash
     PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/do/scripts/do_helper.py" easy --engine "${DO_ENGINE:-gemini}" <<'SPEC_EOF'
     <spec 全文>
     SPEC_EOF
     ```
   - 設定 `timeout: 120000`（2 分鐘）
   - 系統提示已內嵌在 do_helper.py 中

3. **處理結果**：
   - 解析 JSON 輸出：`{"status":"ok","result":"..."}`
   - 從 `result` 欄位提取程式碼/文件
   - 如果是程式碼任務：
     - 用 Write tool 寫入 spec 指定的檔案
     - 簡單驗證：`python -c "import ast; ast.parse(open('<file>').read())"` 檢查語法
   - 如果是文件任務：
     - 用 Write tool 寫入指定檔案
   - `status: "error"` 或 timeout → 印錯誤並停止

4. **快速審核**：
   - 檢查交付清單（檔案是否存在、語法是否正確）
   - 自動判定：pass / partial / fail

5. **記錄 + 報告**：
   ```
   🤖 完成（easy）
   ══════════════════════════
   📋 Spec：<標題> (L<N>)
   ⚡ 引擎：<engine> (<model>)
   🔍 審核：✅ pass / ⚠️ partial / ❌ fail
   備註：<具體發現>

   ✅ 已記錄到 do_history.md
   ```

   追加到 `do_history.md`：
   ```markdown
   | 日期 | Level | 任務 | 引擎 | 結果 | 備註 |
   | 2026-04-05 | L1 | units.py | gemini | pass | 語法通過 |
   ```

---

## deep 模式：`/do deep <任務>`

多輪 LLM 呼叫：生成 → 驗證 → 修正（最多 3 輪），適合複雜任務。

### 流程

1. **Spec 產出**（共用步驟 1-4），spec 保留在記憶體中

2. **呼叫 do_helper.py deep**（所有 rounds 在單一進程內完成）：
   - 印出 `⚡ deep: <引擎> 執行中（<任務摘要>）`
   - 執行：
     ```bash
     PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/do/scripts/do_helper.py" deep --engine "${DO_ENGINE:-gemini}" <<'SPEC_EOF'
     <spec 全文>
     SPEC_EOF
     ```
   - 設定 `timeout: 300000`（5 分鐘，涵蓋最多 3 輪）
   - 系統提示（R1 生成 / R2 審核 / R3 修正）已內嵌在 do_helper.py 中
   - do_helper.py 內部自動處理：R1→R2→判定 pass/fail→R3（如需）

3. **解析結果**：
   - 輸出為 JSON-lines，取最後一行：
     ```json
     {"final":"<最終程式碼>","rounds":N,"verdict":"pass|fixed","issues":[...]}
     ```
   - `final` = 最終程式碼（R2 pass 時為 R1 產出，R3 修正時為 R3 產出）
   - `rounds` = 實際輪數（2 或 3）
   - `verdict` = `"pass"`（R2 通過）或 `"fixed"`（R3 修正後）
   - `issues` = R2 發現的問題列表

4. **寫入檔案**：用 Write tool 將 `final` 寫入 spec 指定的檔案路徑

5. **執行測試**（如果是程式碼任務）：
   - 語法檢查：`python -c "import ast; ast.parse(open('<file>').read())"`
   - 如果 spec 有測試指示 → 執行測試
   - 如果專案有 pytest/jest → 跑相關測試

6. **紅線驗證**（rule-based，不用 LLM）：
   - L1：確認沒有修改現有檔案（`git diff --name-only` 只有新增）
   - L2：確認只改了 spec 允許的檔案
   - CLAUDE.md / AGENTS.md 未被修改

7. **記錄 + 報告**：

   ```
   🤖 完成（deep）
   ══════════════════════════
   📋 Spec：<標題> (L<N>)
   ⚡ 引擎：<engine> (<model>)
   🔄 輪次：<N> rounds（生成 → 審核 → 修正）
   🔍 審核：✅ pass / ⚠️ partial / ❌ fail
   📊 Issues：🔴 N | 🟠 N | 🟡 N
   💡 Advisory：N notes（若 advisory_notes 非空則列出，否則省略此行）
   備註：<具體發現>

   ✅ 已記錄到 do_history.md
   ```

   > **Advisory 顯示**：若 final JSON 的 `advisory_notes` 非空則顯示此行並列出每條。這是 R2 觀察到 spec 外的潛在問題（不影響 verdict），best effort 顯示，唯一保證是 JSON-lines 內有資料。

   追加到 `do_history.md`：
   ```markdown
   | 日期 | Level | 任務 | 引擎 | 結果 | 備註 |
   | 2026-04-05 | L2 | filesync.py | gemini-deep | pass | 3 rounds, 2 issues fixed |
   ```

---

## status 子指令

讀取 `do_level.md` + `do_history.md`，印：

```
目前等級：L1
引擎：gemini（DO_ENGINE）
歷史：
  gemini:    L1 ✅3 ⚠️1 ❌0 | L2 ✅1
  ollama:    L1 ✅2 ⚠️0 ❌0
  opencode:  L1 ✅1 ⚠️0 ❌0
```

---

## set-level 子指令

寫入數字到 `do_level.md`，印 `✅ 已設為 L<N>`

---

## easy vs deep 選擇指引

| 條件 | 建議 |
|---|---|
| L1 新檔案、單一模組 | easy |
| 簡單文件（README, CHANGELOG） | easy |
| L2 修改現有程式碼 | deep |
| 複雜邏輯（多函式、threading、async） | deep |
| L3 任務級 | deep |
| 不確定 | deep（多花 30 秒審核，品質更穩） |

---

## 注意事項

- 所有輸出使用繁體中文。技術術語保持英文。
- deep 模式最多 3 輪（生成 + 審核 + 修正），不會無限迴圈
- 產出的程式碼由 Claude Code 用 Write tool 寫入，不是外部引擎直接寫磁碟
- 引擎檢查失敗時直接停止，不自動 fallback（避免意外行為）
- deep 模式 3 輪全部使用同一個 model（生成 + 審核 + 修正）
- 所有引擎呼叫透過 `do_helper.py`（`skills/do/scripts/do_helper.py`），單一進程內完成，避免重複啟動 Python + 建立連線
- System prompts 內嵌在 `do_helper.py` 中，do.md 不需包含完整提示文字
