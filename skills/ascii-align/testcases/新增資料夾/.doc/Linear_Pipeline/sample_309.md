## Sample 309

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L217

```
Browser (Chat UI from v1) ──> docker-compose
                                │
                                ├── FastAPI + Auth ──> API Gateway
                                │                     ├── /api/search
                                │                     ├── /api/deep-query
                                │                     └── OAuth / API Key
                                │
                                ├── Qdrant HA ───────> 向量搜尋 + 自動備份
                                ├── Ollama bge-m3 ──> 本地 Embedding
                                ├── PostgreSQL ─────> State DB (取代 SQLite)
                                │
                                └── Shared Volume (NTFS)
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
        CI/CD                    Monitoring               Knowledge Graph
        ├── GitHub Actions       ├── Prometheus            ├── Entity Extraction
        ├── pytest + coverage    ├── Grafana               └── Graph DB
        └── auto deploy          └── RAG Eval (F1)
```

