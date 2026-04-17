## Sample 505

**Source**: `Reporter_v1\WORKSPACE\a04\06_personal-rag_v2.md` L29

```
來源目錄 (F:\機器人專案\06_AGV)
    │
    ▼ Phase 1
PKB/vault/ (SHA256 去重) → MANIFEST.csv
    │
    ▼ Phase 2 (orchestrator)
├─ phase2_extractors.py (PPTX/PDF/DOCX 轉文本/影像)
├─ phase2_gemini.py (Vision 分析 + embedding 呼叫)
├─ phase2_qdrant.py (Qdrant Docker 索引)
├─ reembed_ollama_qdrant.py (Ollama bge-m3 re-embed)
└─ phase2_notify.py (Email 進度)
    │
    ▼ Phase 3
├─ phase3_batch_api.py (API server + 批次 pipeline)
├─ phase3_synthesize.py (報告生成)
└─ PKB_db/ (Qdrant Docker)
```

---

