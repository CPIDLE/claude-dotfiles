## Sample 305

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_external.md` L107

```
資料源（文件/圖片/影片/Email）
        |
   Phase 1: 備份去重
        |
   Phase 2: 萃取 + Embedding（Gemini 3072d / Ollama bge-m3 1024d）
        |
   Qdrant Docker（6 collections, ~1.95M vectors, on_disk）
        |
   Phase 3: 知識合成 ──> 公司知識庫 + 報告範本
        |
   FastAPI API Server（語意搜尋 / 深度查詢 / 統計）
```

