# OpenCode 使用場景紀錄

2026-04-02 實際操作案例。

---

## 成功場景

### 1. 專案 README 撰寫

- **工作區**：Claude_code_leak_v0
- **模型**：google/gemini-3.1-pro-preview
- **任務**：掃描 src/ 目錄結構，撰寫 README.md（架構分析、技術棧、目錄說明）
- **結果**：一次成功，產出品質高
- **原因**：文件產生是 LLM 的強項，不涉及程式修改

### 2. Code Review（Calculator）

- **工作區**：UR_Program_Analysis_v0
- **模型**：google/gemini-3.1-pro-preview
- **任務**：review test_code.md 中的 Python Calculator 程式碼
- **結果**：成功找出潛在問題（chain 方法的 args 索引問題、statistics mode 邏輯）
- **原因**：唯讀分析，不需修改程式碼

### 3. Git 操作輔助

- **工作區**：Claude_code_leak_v0
- **模型**：任意
- **任務**：git add、commit、status、log
- **結果**：穩定可靠
- **原因**：固定格式指令，不需推理

---

## 失敗場景

### 4. 多檔案重構（ur_script_parser.py）

- **工作區**：UR_Program_Analysis_v0
- **模型**：google/gemini-3.1-pro-preview
- **任務**：在 ur_script_parser.py 新增 Statement dataclass 和 statements property
- **失敗原因**：
  1. **IndentationError** — 空 class body 沒有 `pass`
  2. **import 位置錯誤** — `from itertools import chain` 放在 dataclass 內部
  3. **幻覺 class** — 新增了不存在的 `URScriptParser` class，破壞所有 import
  4. **佔位註解** — 用 `# ... (原有內容)` 取代真實程式碼，導致截斷
- **修復成本**：撰寫 187 行逐步修復指示（review.md），7 個 step 各含驗證指令
- **教訓**：複雜重構不適合交給 OpenCode

### 5. Ollama 本地模型 Coding

- **工作區**：Claude_code_leak_v0
- **模型**：qwen2.5-coder:14b（本地）
- **任務**：分析 TypeScript 程式碼結構
- **結果**：回應品質明顯低於雲端模型
- **原因**：14B 參數量在複雜程式碼分析上推理能力不足
- **適用場景**：簡單問答、格式轉換、基本 code completion

---

## 場景適用性矩陣

| 場景 | 推薦工具 | 原因 |
|---|---|---|
| 文件產生（README、changelog） | OpenCode (Gemini) | 強項，一次成功率高 |
| Code Review（唯讀） | OpenCode (Gemini) | 不修改程式碼，風險低 |
| Git 操作 | OpenCode（任意） | 固定指令，穩定 |
| 簡單 bug fix（單檔） | OpenCode (Gemini) | 可行，但需明確指示 |
| 多檔案重構 | Claude Code | OpenCode 容易改壞 |
| 架構設計 | Claude Code | 需要深度推理 |
| 複雜 debug | Claude Code | 需要追蹤多層 call stack |
| 本地離線工作 | OpenCode (Ollama) | 唯一選項，品質打折 |
| Claude Code 限流備案 | OpenCode (Gemini) | 簡單任務可替代 |
