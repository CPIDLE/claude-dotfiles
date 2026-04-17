## Sample 472

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L258

```
Google Chat (@gyro.com.tw)
        ↓
GCP Cloud Run thin proxy (asia-east1)
  ├─ JWT (OIDC) 驗證
  ├─ Rate limiting
  └─ 轉發 → ngrok tunnel
        ↓
本機 Backend (FastAPI)
  ├─ API key 驗證
  ├─ rag.py (async embedding)
  ├─ Ollama bge-m3 (本機 embedding)
  ├─ Gemini 2.5 Flash (LLM)
  └─ Qdrant Docker (並行 3 collections)
```

---

