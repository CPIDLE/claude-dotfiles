## Sample 338

**Source**: `Reporter_v0\plan.md` L12

```
_build_vectors.py              _search_vectors.py
(一次性建置)                    (搜尋時使用)
     │                              │
     ▼                              ▼
讀取 _index.json            語意搜尋 (cosine)
     │                      + 關鍵字搜尋 (FTS5)
     ▼                      + RRF 混合排序
讀取 5,636 個 .txt                  │
     │                              ▼
     ▼                        候選文件清單
分段 (chunk)                  (含分數+路徑+摘要)
     │
     ▼
Gemini embedding-001
(768-dim, batch 100)
     │
     ▼
_vectors.db (SQLite)
```

---

