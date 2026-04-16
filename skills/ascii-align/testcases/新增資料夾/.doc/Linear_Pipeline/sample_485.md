## Sample 485

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L328

```
_build_vectors.py (一次性建置)
    │
    v 
讀取 _index.json + 5,636 個 .txt
    │
    v 
分段 (chunk_size=1500, overlap=300)
    │
    v 
Gemini embedding-001 (768 維, batch=100)
    │
    v 
_vectors.db (SQLite BLOB)
    │
    v  <-- 查詢時
_search_vectors.py
    ├─ 語意搜尋 (cosine)
    ├─ 關鍵字搜尋 (SQLite FTS5 BM25)
    └─ RRF (Reciprocal Rank Fusion)
        │
        v 
候選文件清單（含分數+路徑+摘要）
```

