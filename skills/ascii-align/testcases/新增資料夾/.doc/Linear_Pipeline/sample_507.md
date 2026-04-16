## Sample 507

**Source**: `Reporter_v1\WORKSPACE\a04\07_Reporter_v0.md` L29

```
_build_vectors.py (一次性)      _search_vectors.py (查詢時)
    │                           │
    v                               v 
讀取 _index.json           語意搜尋 (cosine)
    │                      + 關鍵字搜尋 (FTS5 BM25)
    v                       + RRF 混合排序
讀取 5,636 個 .txt              │
    │                          v 
    v                     候選文件清單
分段 (chunk)            (含分數+路徑+摘要)
    │
    v 
Gemini embedding-001
(768-dim, batch 100)
    │
    v 
_vectors.db (SQLite BLOB)
```

