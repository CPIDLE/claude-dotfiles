# opencode-do → Gemini/Ollama API 遷移計畫

> 日期：2026-04-05
> 目標：將 `/opencode-do auto` 從 opencode CLI 遷移到直接 LLM API 呼叫

---

## 1. 為什麼遷移

| | opencode（現狀） | 直接 API（目標） |
|---|---|---|
| 依賴 | opencode CLI + Gemini/Ollama | 只需 `google-generativeai` 或 `requests` |
| 程式碼 | 黑盒，控制力有限 | **1 個 script，完全掌控** |
| 切換 model | 改 opencode.json | **改 URL + model 名** |
| 試驗→上線 | 試驗用 opencode，上線要重寫 | **同一份 script，只換 endpoint** |
| 除錯 | opencode 內部行為不透明 | 直接看 API request/response |

---

## 2. 遷移範圍

### 保留不動

- Claude Code 主導設計 + 審核
- Spec 格式（L1/L2/L3）
- Level 分層邏輯
- 紅線規則
- opencode_history.md 格式

### 替換

| 現狀 | 目標 |
|---|---|
| `echo spec \| opencode run --format json` | `python llm-do.py --spec spec.md` |
| opencode 內部 LLM 呼叫 | 直接 Gemini API / Ollama REST API |
| opencode bash/read/write 工具 | script 內 subprocess + file I/O |
| `.opencode-agents/registry.jsonl` | `.llm-agents/registry.jsonl`（格式不變） |

### 廢棄

| 項目 | 處理 |
|---|---|
| `commands/opencode-do.md` | 新建 `commands/llm-do.md` 取代 |
| `commands-opencode/do.md` | 不需要，直接被 Claude Code 呼叫 |
| `opencode-config/` | 保留作離線備援 |

---

## 3. 核心 script：llm-do.py

單一檔案，約 100 行：

```python
#!/usr/bin/env python3
"""Claude Code 委派執行器：直接呼叫 Gemini API 或 Ollama REST API"""

import os, sys, json, subprocess, requests

# --- LLM Provider ---

def call_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    resp = genai.GenerativeModel(model).generate_content(prompt)
    return resp.text

def call_ollama(prompt: str, model: str = "qwen3:8b") -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    resp = requests.post(f"{url}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False
    })
    return resp.json()["response"]

def call_llm(prompt: str, mode: str = "fast") -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini")
    if provider == "gemini":
        model = "gemini-2.5-flash" if mode == "fast" else "gemini-2.5-pro"
        return call_gemini(prompt, model)
    else:
        model = "qwen3:8b" if mode == "fast" else "qwen3:72b"
        return call_ollama(prompt, model)

# --- 執行 ---

SYSTEM_PREFIX = (
    "你是程式碼執行者。直接按照 spec 完成任務，不要規劃、不要問確認。"
    "完成後列出：1) 新增/修改的檔案 2) 測試結果。"
    "輸出格式：先輸出所有程式碼（每個檔案用 ```path/to/file 標記），最後輸出完成報告。"
)

def run_task(spec: str) -> dict:
    prompt = f"{SYSTEM_PREFIX}\n\n{spec}"
    response = call_llm(prompt, mode="fast")

    # 解析回應中的檔案區塊並寫入
    files_written = parse_and_write_files(response)

    # 跑測試
    test_result = run_tests()

    return {
        "response": response,
        "files_written": files_written,
        "test_result": test_result,
    }

def parse_and_write_files(response: str) -> list:
    """解析 LLM 回應中的 ```path/to/file 區塊，寫入檔案"""
    files = []
    lines = response.split("\n")
    current_file = None
    content = []

    for line in lines:
        if line.startswith("```") and "/" in line and current_file is None:
            current_file = line.strip("`").strip()
            content = []
        elif line.strip() == "```" and current_file:
            os.makedirs(os.path.dirname(current_file) or ".", exist_ok=True)
            with open(current_file, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
            files.append(current_file)
            current_file = None
            content = []
        elif current_file is not None:
            content.append(line)

    return files

def run_tests() -> str:
    """偵測並執行測試框架"""
    for cmd in ["pytest", "npm test", "go test ./...", "cargo test"]:
        try:
            r = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            return f"{cmd}: {'PASS' if r.returncode == 0 else 'FAIL'}\n{r.stdout[-500:]}"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return "no test framework detected"

# --- CLI ---

if __name__ == "__main__":
    if "--spec" in sys.argv:
        with open(sys.argv[sys.argv.index("--spec") + 1], encoding="utf-8") as f:
            spec = f.read()
    else:
        spec = sys.stdin.read()

    result = run_task(spec)
    print(json.dumps({
        "files": result["files_written"],
        "tests": result["test_result"],
    }, ensure_ascii=False, indent=2))
```

---

## 4. Claude Code 整合

### 指令對照

| 現狀 | 新版 |
|---|---|
| `/opencode-do auto <task>` | `/llm-do auto <task>` |
| `/opencode-do auto --persist <task>` | `/llm-do auto --persist <task>` |
| `/opencode-do review` | `/llm-do review` |
| `/opencode-do agents` | `/llm-do agents` |
| `/opencode-do status` | `/llm-do status` |

### 快速模式呼叫

```bash
# 原本
echo '<spec>' | opencode run --format json 2>&1

# 新版
echo '<spec>' | python llm-do.py 2>&1
```

### 持久模式呼叫

```bash
# 原本
opencode run --format json "<prompt>" > .opencode-agents/agent-<id>/output.log 2>&1

# 新版
python llm-do.py --spec .llm-agents/agent-<id>/spec.md > .llm-agents/agent-<id>/output.log 2>&1
```

---

## 5. 環境設定

```bash
# 試驗階段（Gemini API）
pip install google-generativeai requests
export GEMINI_API_KEY=<your-key>
export LLM_PROVIDER=gemini

# Production（本地 Ollama）
export LLM_PROVIDER=ollama
export OLLAMA_URL=http://localhost:11434
# 不需要額外 pip install（只用 requests）
```

---

## 6. 實施步驟

| Step | 內容 | 預估 |
|---|---|---|
| 1 | 建立 `llm-do.py`，實作 Gemini API 呼叫 + 檔案解析 | 1 session |
| 2 | 用 `dual-engine/examples/` 的 8 個案例測試 | 同 session |
| 3 | 建立 `commands/llm-do.md`（Claude Code command） | 1 session |
| 4 | 平行驗證：同一任務跑 opencode 和 llm-do，比較結果 | 1 週 |
| 5 | 通過後 `/opencode-do` 標記 deprecated | -- |

**合計：2 sessions + 1 週驗證**（比 LangGraph 版省一半以上）

---

## 7. 完成標準

- [ ] `llm-do.py` 可處理 L1/L2/L3 三種 spec
- [ ] `dual-engine/examples/` 8 個案例全部通過
- [ ] `/llm-do auto` 快速模式端對端成功
- [ ] `/llm-do auto --persist` 持久模式端對端成功
- [ ] Gemini API → Ollama 切換只改環境變數
- [ ] 平行驗證 1 週，品質 >= opencode

---

## 8. LangGraph 定位調整

LangGraph 不再用於開發工具，保留給 AMHS 產線 Phase 2+ 評估：

| 場景 | 方案 |
|---|---|
| 開發工具（取代 opencode-do） | **直接 API（本文件）** |
| AMHS Phase 1（輔助工具） | **直接 API**（同上，查詢類） |
| AMHS Phase 2（提供建議） | 評估 LangGraph（多步 Skill workflow 開始有需求） |
| AMHS Phase 3（主動決策） | 可能需要 LangGraph（複雜 workflow + state persistence） |

**原則：用最簡單的方案解決當前問題。LangGraph 等到真正需要時再引入。**
