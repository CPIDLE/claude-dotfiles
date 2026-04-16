## Sample 302

**Source**: `personal-rag_v2\README.md` L169

```
ThreadPoolExecutor
  ├── images/docs: 4 workers
  └── videos: 1 worker (大檔上傳避免衝突)

Gemini API 速率限制
  ├── deque 追蹤最近 25 次請求時間戳 (thread-safe)
  ├── 超過 25 req/sec --> sleep
  └── 429 / RESOURCE_EXHAUSTED --> 指數退避 (2^n * 2s, max 120s)

LibreOffice
  └── threading.Lock 全域鎖（不支援 concurrent instances）
```

