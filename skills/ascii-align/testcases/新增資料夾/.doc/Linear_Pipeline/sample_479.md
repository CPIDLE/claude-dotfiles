## Sample 479

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L50

```
Google Chat (@gyro.com.tw)
        │
        ▼
GCP Cloud Run thin proxy (asia-east1)
  ├─ JWT (OIDC) 驗證
  ├─ Rate limiting
  └─ 轉發 → ngrok tunnel
        │
        ▼
本機 Backend (FastAPI + Uvicorn)
  ├─ API key 驗證
  ├─ rag.py（async embedding）
  ├─ Ollama bge-m3（本機 embedding）
  ├─ Gemini 2.5 Flash（LLM 推理）
  └─ Qdrant Docker（並行 3 collections 搜尋）
```

---

