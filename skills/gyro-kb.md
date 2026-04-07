---
name: gyro-kb
description: GYRO PKB v2 統一工具 — 搜尋 / 客戶關聯 / 工程計算 / 完整報告 / 快速草稿，自動依輸入智慧路由（ChromaDB + raw_phase3）
arguments: 客戶需求、關鍵字、客戶名稱、JSON路徑等（自動判斷模式）
user_invocable: true
---

## 兩大 Skill 關係

```
/gyro-kb ── 負責「內容產出」── 知識庫搜尋 + 計算 + 報告撰寫
  │
  │  產出 .md 報告
  ▼
/report-gyro ── 負責「排版呈現」── MD → HTML 簡報 + PDF + Excel 驗算
```

> **典型工作流**: `/gyro-kb <客戶需求>` → 產出 `.md` → `/report-gyro <.md> <.html>` → 產出簡報
> `/gyro-kb` 只寫內容不做排版。`/report-gyro` 只做排版不寫內容。

---

## 第 0 步：讀取公司知識（每次必做）

**任何模式開始前，先讀取 `E:/github/personal-rag_v2/PKB/GYRO_context.md`**。
此檔案包含公司概述、產品線、客戶清單、核心技術、報價慣例、圖片資源等摘要。

---

## 智慧路由

根據 `$ARGUMENTS` 內容自動判斷執行模式，**不需要子命令**：

| # | 判斷條件 | 模式 | 執行內容 |
|---|---------|------|---------|
| 2 | 只有 1-3 個搜尋詞（如「Stocker AMR」「FOUP 規格」） | **Search** | ChromaDB 語義+metadata 搜尋 |
| 3 | 含客戶名稱 + 「歷史」「關聯」或單純客戶名 | **Related** | ChromaDB + raw_phase3 客戶歸納 |
| 4 | 含 JSON 路徑、`--demo`、數值參數、「計算」「試算」 | **Calc** | 內嵌 Python 工程計算 |
| 5 | 含客戶需求描述、PDF/文件路徑、「報告」「report」 | **Report** | 完整報告流程（基本版或深度版） |
| 6 | 含「草稿」「draft」，或簡短需求描述（一句話） | **Draft** | ChromaDB 快速搜尋 + 6 節草稿 |

**判斷優先順序**: Report > Draft > Calc > Related > Search（預設）

> Mode 1 Ingest 已移除 — v2 使用 `scripts/phase1~3` 管線處理，不由 skill 觸發。

如果無法確定模式，詢問使用者意圖。

---

## 共用設定

### PKB 位置

```
E:/github/personal-rag_v2/PKB/
├── GYRO_context.md          ← 公司知識摘要（必讀）
├── MANIFEST.csv             ← 文件追蹤清單
├── db/chroma/               ← ChromaDB 持久化
│   ├── pkb_docs             ← 文件 collection
│   └── pkb_images           ← 圖片 collection
├── vault/                   ← 原始文件庫
│   ├── docs/
│   ├── images/
│   ├── videos/
│   └── embedded_images/
├── raw_phase3/              ← Phase 3 歸納（唯讀）
│   ├── customers/batch_01~24.md
│   └── products/*.md
├── templates/               ← 報告模板（18+ 模板）
│   └── 00_報告產生流程/     ← 報告工作流定義
└── workspace/CASE##/        ← 報告輸出工作區
```

### ChromaDB Collections

| Collection | Embedding | 維度 | 用途 |
|---|---|---|---|
| `pkb_docs` | Gemini `gemini-embedding-2-preview` | 3072 | 文件（主要） |
| `pkb_images` | Gemini `gemini-embedding-2-preview` | 3072 | 圖片（主要） |
| `pkb_docs_ollama` | Ollama `bge-m3` | 1024 | 文件（備用，本地） |
| `pkb_images_ollama` | Ollama `bge-m3` | 1024 | 圖片（備用，本地） |

### ChromaDB 連接 + 語義搜尋片段（所有模式共用）

**重要**：`query_texts` 無法使用（embedding function 不匹配）。必須**手動 embed query** 再用 `query_embeddings`。

```python
import chromadb
from google import genai
from dotenv import load_dotenv
import os

# 載入 API key
load_dotenv("E:/github/personal-rag_v2/PKB/.env")

# Gemini embedding（主要，3072 維，品質較高）
g_client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def gemini_embed(text: str) -> list[float]:
    result = g_client.models.embed_content(
        model="gemini-embedding-2-preview",
        contents=text
    )
    return result.embeddings[0].values

# ChromaDB
client = chromadb.PersistentClient(path="E:/github/personal-rag_v2/PKB/db/chroma/")
pkb_docs = client.get_collection(name="pkb_docs")
pkb_images = client.get_collection(name="pkb_images")

# 語義搜尋
query_emb = gemini_embed("搜尋文字")
results = pkb_docs.query(
    query_embeddings=[query_emb],
    n_results=20,
    where={"subtype": {"$ne": "image_ref"}}
)
```

**備用方案（Ollama，離線/免費）**：當 Gemini API 不可用時

```python
import requests

def ollama_embed(text: str) -> list[float]:
    r = requests.post("http://localhost:11434/api/embed",
                      json={"model": "bge-m3", "input": text})
    return r.json()["embeddings"][0]

pkb_docs_ollama = client.get_collection(name="pkb_docs_ollama")
query_emb = ollama_embed("搜尋文字")
results = pkb_docs_ollama.query(query_embeddings=[query_emb], n_results=20)
```

### pkb_docs metadata 欄位

`type`, `subtype`, `source_file`, `page_or_slide`, `chunk_index`, `date`, `scene`, `objects`, `usage`, `client`, `path`, `filename`

### 客戶產業對照

| 產業 | 客戶 |
|---|---|
| 封測 | 矽品, ASE, 日月光, KYEC, 京元電, 南茂, 力成, TOPPAN, 頎邦, 矽格, Chipbond |
| 晶圓代工 | 聯電, UMC, TSMC, 力積電, 世界先進, 台勝科, 環球晶 |
| 記憶體 | Intel, Hynix, TI, Micron, 美光, Renesas, 南亞科 |
| 面板光電 | AUO, 友達, Eink, 錼創, 欣興 |
| 系統整合 | 盟立, 東捷, 大福, 沃亞 |

### 同義詞展開表

| 原始詞 | 同時搜尋 |
|---|---|
| Stocker | STK, 儲位, Buffer, eRack, E-Rack, 站前緩衝, MiniStocker |
| AMR | AGV, 自動搬運, AMRA04, AMRW, AMRL, AMRAX, 無人搬運, Gyrobot |
| FOUP | SMIF, CST, FUOP, 載具, 晶圓盒, carrier |
| 充電 | 充電樁, 充電座, 機會充電 |
| Sorter | 分流, 分揀, 合流, 路由 |
| MCS | TSC, AMHS, RTD, EAP, 物料控制, AGVC |
| 軟體 | TSC, MCS lite, E-RACKC, SECS, E84 |

---

## Mode 2: Search（搜尋）

**何時觸發**: 只有 1-3 個關鍵字，想快速查找知識庫文件。

### 執行

**Step 1: 展開同義詞**（參照上方展開表）

**Step 2: ChromaDB 語義搜尋**（手動 embed query）

```python
query_emb = gemini_embed("<原始關鍵字 + 同義詞組合>")
results = pkb_docs.query(
    query_embeddings=[query_emb],
    n_results=20,
    where={"subtype": {"$ne": "image_ref"}}
)
```

**Step 3: ChromaDB metadata 搜尋**（補充精確匹配）

```python
# 按 client / type / source_file 等精確搜尋
results = pkb_docs.get(
    where={"client": "<客戶名>"},
    limit=20
)
```

### 後續

搜尋結果含 `source_file` 路徑。用 Read 工具讀取感興趣的原始文件（在 `vault/docs/` 下）。

---

## Mode 3: Related（客戶關聯）

**何時觸發**: 提供客戶名稱，想查該客戶歷史或同產業案例。

### 執行

**Step 1: ChromaDB 客戶專屬文件**

```python
results = pkb_docs.get(
    where={"client": "<客戶名>", "subtype": {"$ne": "image_ref"}},
    limit=30
)
```

**Step 2: raw_phase3 客戶歸納**

讀取 `raw_phase3/customers/batch_*.md`（共 24 批），搜尋目標客戶的歸納段落。
每個 batch 檔案包含多個客戶的整合歸納，包括：
- 案件歷史
- 軟體整合層級（full_tsc_mcs / partial_tsc / third_party_mcs / no_software）
- 硬體配置
- 時間線

**Step 3: 同產業案例**

根據客戶產業對照表，找出同產業客戶，再用 ChromaDB 搜尋類似案例。

**Step 4: 相關產品規格**

讀取 `raw_phase3/products/*.md`，找出該客戶使用或可能需要的產品資料。

### 搜尋結果四大類

1. **同客戶歷史文件** — 該客戶過去所有案例（ChromaDB + batch 歸納）
2. **同產業類比案例** — 同產業其他客戶案例
3. **相關產品規格** — AMR 車型、搬運方案、STK、軟體文件
4. **報價參考** — 歷史報價單（內部機密，參考 `raw_phase3/products/a_報價單.md`）

---

## Mode 4: Calc（工程計算）

**何時觸發**: 有數值參數或 JSON、想做瓶頸/流量/設備估算。不需要知識庫。

### 執行

直接用 Python 內嵌計算（v2 無獨立計算腳本）。

**方式 1: 使用者提供 JSON**

```python
import json

with open("<path_to_json>", "r", encoding="utf-8") as f:
    data = json.load(f)
# 執行計算...
```

**方式 2: 從對話組裝 JSON**

```python
data = {
    "project": "專案名稱",
    "pieces_per_carrier": 25,
    "wip_total_pieces": 1000,
    "stations": [
        {"name": "A1", "machines": 10, "pt_per_piece": 8},
        {"name": "P",  "machines": 7,  "pt_per_piece": 90}
    ],
    "flows": [
        {
            "name": "流程1",
            "path": ["TS", "Sorter", "STK", "A1", "Sorter", "TS"],
            "cycle_time_min": 48,
            "wip_ratio": 0.25,
            "repeat": 1
        }
    ],
    "charge_strategy": "opportunity",
    "peak_factor": 1.5
}
```

### 計算內容

1. **瓶頸分析** — 各站產能排序，標記瓶頸站
2. **搬運流量** — EQ→EQ 中轉規則修正，各流程 moves/hr
3. **設備估算** — AMR 數量、STK 座數、Tower Stocker 容量、充電座

### 關鍵公式

- 站區產能 = (60 / Pt_carrier) × machines [FOUPs/hr]
- 中轉規則: EQ→EQ 必須經 STK 中轉
- AMR = ceil(peak_moves / (capacity × availability))
  - capacity ≈ 12 moves/hr/台
  - availability = 95%（機會充電）或 75%（定點充電）

---

## Mode 5: Report（完整報告）

**何時觸發**: 有客戶需求描述或需求文件，要產出完整技術討論報告。

**這是最常用的模式**，內部會自動呼叫 Search + Related + Calc。

### 選擇工作流版本

| 情境 | 使用工作流 | 檔案 |
|------|-----------|------|
| 單一客戶提案、規格書、一般報告 | 基本版（6 階段） | `templates/00_報告產生流程/report_workflow.md` |
| 跨多客戶/多產品/多時間軸、系統性研究 | 深度研究版（Phase A→B→C） | `templates/00_報告產生流程/report_workflow_v1.md` |

> **先讀取對應的 workflow 檔案**，嚴格依照其定義的流程執行。

### 基本版流程（report_workflow.md）

```
輸入 → 理解 → 確認 → 計算/分析 → 撰寫 → 排版
```

| 階段 | 做什麼 | 產出 |
|------|--------|------|
| **輸入** | 收集客戶/專案資料 | 原始檔案 + `.images/` |
| **理解** | 提取結構化資訊、查 ChromaDB | `input_data.json` |
| **確認** | 逐項確認參數、釐清疑問 | `params.json` 定案 |
| **計算** | 數值分析（Python，非 AI） | `results.json` |
| **撰寫** | 套模板 + AI 生成文案 | `.md` 定稿 |
| **排版** | `/report-gyro` 轉 HTML | `.html` |

### 深度研究版流程（report_workflow_v1.md）

```
Phase A：大量撈取 → Phase B：統整+圖片 → Phase C：報告產出
```

- **A1**: ChromaDB 20~30 關鍵字擴大搜尋
- **A2**: `raw_phase3/customers/` 全部批次全文讀取
- **A3**: `raw_phase3/products/` 全部檔案讀取
- **A4**: Top 15~20 核心文件完整撈取
- **B1~B3**: 功能統整 / 客戶矩陣 / 報價分析
- **IA1~IC1**: 圖片搜尋 / 安全篩選 / 複製
- **C1~C4**: 完整版 / 精簡版 / 對外版 / 排版

### 知識庫搜尋策略

**語義搜尋（主要，手動 embed）**
```python
query_emb = gemini_embed("<客戶名> <關鍵字1> <關鍵字2>")
results = pkb_docs.query(
    query_embeddings=[query_emb],
    n_results=30,
    where={"subtype": {"$ne": "image_ref"}}
)
```

**客戶專屬文件**
```python
results = pkb_docs.get(
    where={"client": "<客戶名>", "subtype": {"$ne": "image_ref"}},
    limit=30
)
```

**raw_phase3 歸納讀取**
- `raw_phase3/customers/batch_*.md` — 客戶歸納（24 批次）
- `raw_phase3/products/*.md` — 產品歸納

### 報告模板

從 `templates/` 選擇對應類型的模板：

| 類型 | 模板路徑 |
|------|----------|
| 客戶提案 | `templates/01_客戶提案/customer_proposal_template.md` |
| 系統擴充 | `templates/01_客戶提案/system_expansion_proposal_template.md` |
| 系統升級 | `templates/01_客戶提案/system_upgrade_proposal_template.md` |
| 技術方案 | `templates/01_客戶提案/technical_solution_template.md` |
| 需求分析 | `templates/01_客戶提案/requirement_analysis_template.md` |
| PoC 計畫 | `templates/01_客戶提案/poc_plan_template.md` |
| 標準報價 | `templates/01_客戶提案/standard_quotation_template.md` |
| 專案執行計畫 | `templates/01_客戶提案/project_execution_plan_template.md` |
| 系統導入提案 | `templates/01_客戶提案/system_implementation_proposal_template.md` |
| AGV 規劃 | `templates/18_AGV規劃/agv_planning_template.md` |
| 測試報告 | `templates/04_測試報告/test_report_template.md` |
| 市場分析 | `templates/08_市場分析報告/market_analysis_template.md` |
| 設計文件 | `templates/09_設計文件/design_document_template.md` |

### 工作區結構

```
workspace/CASE##/
├── [原始檔案]                        ← 輸入
├── input_data.json                   ← 理解（結構化提取）
├── params.json                       ← 確認（單一真相來源）
├── results.json                      ← 計算
├── 01_requirements_review.md/.html   ← 需求確認
├── 02_analysis_report.md/.html       ← 分析報告
├── 03_[文件類型].md/.html            ← 最終產出
└── .images/
    ├── client/                       ← 客戶提供
    ├── db/                           ← ChromaDB 搜尋
    └── generated/                    ← Mermaid 渲染
```

### 圖片工作流

**搜尋圖片**
```python
# 語義搜尋（手動 embed）
query_emb = gemini_embed("<搜尋主題>")
results = pkb_images.query(
    query_embeddings=[query_emb],
    n_results=10
)
# 或按 metadata 篩選
results = pkb_images.get(
    where={"objects": {"$contains": "AMR"}},
    limit=10
)
```

**安全篩選規則（對外文件）**

| 排除條件 | 原因 |
|----------|------|
| usage = internal | 內部文件 |
| 手機截圖/email/聊天 | 含人員資訊 |
| caption/objects 含其他客戶名稱 | 客戶隱私 |
| 報價單（含金額） | 商業機密 |

### 撰寫原則

1. **數據有來源** — 引用知識庫文件路徑
2. **假設要標記** — 客戶未提供的用 **粗體** 標記「估算」或「假設」
3. **計算要透明** — 列出公式和中間步驟
4. **表格化呈現** — 比較數據用表格
5. **待確認必完整** — 所有缺失資訊列入待確認事項
6. **附錄要分離** — 機密資訊放附錄
7. **單位統一** — mm / min / hr / pcs / FOUPs
8. **瓶頸要醒目** — 粗體+箭頭標記
9. **params.json 為唯一數據來源** — 所有數字從此取
10. **MD 定稿後才排版** — HTML 只生成一次

### 客戶隱私規則

對外文件中，非目標客戶名稱必須匿名化：
- 保留第一個字，其餘用 `X` 替代
- 範例：`矽品` → `矽X`、`台積電` → `台XX`、`Micron` → `MiXXXX`、`ASE` → `AXX`
- 內部文件不受此限制

### 輸出規範

- **格式**: Markdown (.md)
- **位置**: `workspace/CASE##/`
- **版本**: Header 標注 V0.1

---

## Mode 6: Draft（快速草稿）

**何時觸發**: 含「草稿」「draft」關鍵字，或簡短一句話需求（不需要完整報告精度）。

**與 Report 模式的差異**:
- 不執行工程計算
- 不使用模板骨架
- 簡化為 6 節輸出（不含附錄）
- 用 ChromaDB 快速查詢，不做深度研究

### 執行流程

1. ChromaDB 語義搜尋，找出最相關的文件

```python
query_emb = gemini_embed("<需求描述>")
results = pkb_docs.query(
    query_embeddings=[query_emb],
    n_results=10,
    where={"subtype": {"$ne": "image_ref"}}
)
```

2. 讀取最相關的 3-5 筆結果的原始文件
3. 參考歷史文件的格式、用語與技術細節，產出草稿

### 草稿結構（6 節）

```
# {客戶名稱} 需求對應草稿

## 專案概述
客戶名稱、產業、需求摘要

## 車型建議
根據搬運物品與環境推薦適合的 AMR 車型

## 系統架構
軟硬體整合方案、路線規劃

## 搬運方案
動線設計、站點配置、產能估算

## 報價參考
參考歷史案例的報價範圍（如有）

## 參考文件
列出引用的歷史文件路徑
```

### 撰寫原則

- 使用繁體中文
- 技術術語與歷史文件保持一致
- 如果搜尋結果不足，明確說明哪些部分需要補充資訊
