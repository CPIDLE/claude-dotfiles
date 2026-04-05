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

### gemini 引擎

```bash
python -c "
import sys, os
from google import genai
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
model = os.environ.get('DO_MODEL_EASY', 'gemini-3.1-flash-lite-preview')  # easy 用 lite; deep 用 DO_MODEL_DEEP
spec = sys.stdin.read()
prompt = '<系統提示>\n\n' + spec
r = client.models.generate_content(model=model, contents=prompt)
print(r.text)
" <<'SPEC_EOF'
<spec 全文>
SPEC_EOF
```

### ollama 引擎

```bash
python -c "
import sys, os, json, urllib.request
url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
model = os.environ.get('DO_MODEL_EASY', 'qwen3:8b')  # easy 用此; deep 用 DO_MODEL_DEEP
spec = sys.stdin.read()
prompt = '<系統提示>\n\n' + spec
data = json.dumps({'model': model, 'prompt': prompt, 'stream': False}).encode()
req = urllib.request.Request(f'{url}/api/generate', data=data, headers={'Content-Type': 'application/json'})
resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
print(resp['response'])
" <<'SPEC_EOF'
<spec 全文>
SPEC_EOF
```

> ollama 引擎使用 `urllib.request`，零額外依賴。

### opencode 引擎

```bash
echo '<指令前綴 + spec 全文>' | opencode run --format json 2>&1
```

解析 JSONL 輸出，提取 `{"type":"text","part":{"text":"..."}}` 事件。

---

## 引擎前置檢查

執行前自動檢查引擎是否可用：

| 引擎 | 檢查方式 | 失敗訊息 |
|---|---|---|
| gemini | `python -c "from google import genai"` + `GEMINI_API_KEY` 存在 | `⚠️ 缺少 google-genai 或 GEMINI_API_KEY` |
| ollama | `curl -s <OLLAMA_URL>/api/tags` 回應包含 model 名稱 | `⚠️ Ollama 未啟動或 model 未下載` |
| opencode | `which opencode` 成功 | `⚠️ opencode CLI 未安裝` |

失敗時印訊息並停止，不 fallback 到其他引擎。

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

### 系統提示

```
你是資深軟體工程師。直接執行以下任務，只輸出交付物（程式碼或文件）。不要包裝在 markdown code fence 中（除非交付物本身就是 markdown）。
```

### 流程

1. **Spec 產出**（共用步驟 1-4），spec 保留在記憶體中

2. **呼叫引擎**：依 `DO_ENGINE` 選擇對應實作，將系統提示 + spec 送入
   - 印出 `⚡ <引擎名稱> 執行中（<任務摘要>）`
   - 設定 `timeout: 120000`（2 分鐘）

3. **處理結果**：
   - 成功 → 從回應中提取程式碼/文件
   - 如果是程式碼任務：
     - 用 Write tool 寫入 spec 指定的檔案
     - 簡單驗證：`python -c "import ast; ast.parse(open('<file>').read())"` 檢查語法
   - 如果是文件任務：
     - 用 Write tool 寫入指定檔案
   - 失敗（timeout / API error）→ 印錯誤並停止

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

2. **Round 1 — 生成**：

   系統提示（比 easy 更詳細）：
   ```
   你是資深軟體工程師。按照以下 spec 完成任務。

   要求：
   - 完整實作所有功能
   - 包含錯誤處理和邊界條件
   - 程式碼須包含 type hints 和 docstrings
   - 確保可直接執行，無需修改

   只輸出交付物，不要解釋。
   ```

   - 印出 `⚡ Round 1: <引擎> 生成中...`
   - 設定 `timeout: 180000`（3 分鐘）

3. **寫入檔案**：將產出寫入 spec 指定的檔案路徑

4. **Round 2 — 審核**：用同一個引擎（同 model）審核 Round 1 的產出

   審核提示：
   ```
   你是嚴格的 code reviewer。審核以下程式碼/文件是否符合 spec。

   回應格式（JSON）：
   {
     "verdict": "pass" | "fail",
     "issues": [
       {"severity": "high|medium|low", "line": N, "description": "..."}
     ],
     "fix_instructions": "如果 fail，描述如何修正（供下一輪 LLM 使用）"
   }

   只輸出 JSON，不要其他文字。
   ```

   輸入：spec 全文 + Round 1 產出

   - 印出 `🔍 Round 2: <引擎> 審核中...`
   - 設定 `timeout: 120000`

5. **解析審核結果**：
   - `verdict: "pass"` → 跳到步驟 7
   - `verdict: "fail"` → 繼續步驟 6
   - JSON 解析失敗 → 視為 pass（容錯）

6. **Round 3 — 修正**（最多 1 次）：

   將原始 spec + Round 1 產出 + 審核 issues + fix_instructions 送回引擎修正：

   ```
   你是資深軟體工程師。以下程式碼有問題，請根據審核意見修正。

   輸出完整的修正後程式碼/文件，不要只輸出 diff。不要解釋。
   ```

   - 印出 `🔧 Round 3: 修正中...`
   - 修正後更新檔案

7. **執行測試**（如果是程式碼任務）：
   - 語法檢查：`python -c "import ast; ast.parse(open('<file>').read())"`
   - 如果 spec 有測試指示 → 執行測試
   - 如果專案有 pytest/jest → 跑相關測試

8. **紅線驗證**（rule-based，不用 LLM）：
   - L1：確認沒有修改現有檔案（`git diff --name-only` 只有新增）
   - L2：確認只改了 spec 允許的檔案
   - CLAUDE.md / AGENTS.md 未被修改

9. **記錄 + 報告**：

   ```
   🤖 完成（deep）
   ══════════════════════════
   📋 Spec：<標題> (L<N>)
   ⚡ 引擎：<engine> (<model>)
   🔄 輪次：<N> rounds（生成 → 審核 → 修正）
   🔍 審核：✅ pass / ⚠️ partial / ❌ fail
   📊 Issues：🔴 N | 🟠 N | 🟡 N
   備註：<具體發現>

   ✅ 已記錄到 do_history.md
   ```

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
