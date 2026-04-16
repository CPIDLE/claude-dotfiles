## Sample 308

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L123

```
資料源 (14,975 files + 31,990 emails)
  │
  ├─ Phase 1: Vault ──> SHA256 dedup --> MANIFEST.csv
  │
  ├─ Phase 2: Embed ──> Extractors (7 formats + Email + Video)
  │                     ├── Gemini 2.5-flash (Vision)
  │                     ├── Gemini embedding-2 (3072d)
  │                     └── Ollama bge-m3 (1024d)
  │                              │
  │                     Qdrant Docker (6 collections, 1.95M vectors)
  │                     on_disk=True | RAM 380MB | D:/PKB_db/
  │
  ├─ Phase 3: Synth ──> GYRO_context.md + 14 類報告範本
  │
  └─ Phase 4: API ────> FastAPI :8000
                        ├── /api/search (語意搜尋)
                        ├── /api/deep-query (Agentic RAG + SSE)
                        └── /api/stats (使用統計)
```

