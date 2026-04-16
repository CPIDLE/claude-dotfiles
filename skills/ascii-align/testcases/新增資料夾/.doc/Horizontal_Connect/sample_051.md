## Sample 051

**Source**: `Chat_bot_v1\使用指引.md` L7

```
Google Chat (@gyro.com.tw)
    │ HTTPS POST + JWT
    v 
Cloud Run thin proxy (asia-east1, FastAPI)  ── 個人 GCP
    │ HTTPS + API Key
    v 
ngrok tunnel --> 本機 RAG backend (port 8001)
    │
    ├───> Ollama bge-m3 (embedding, 本機)
    ├───> Qdrant (localhost:6333, 向量搜尋)
    └───> Gemini 2.5 Flash API (LLM 推理)
```

