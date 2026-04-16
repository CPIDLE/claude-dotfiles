## Sample 039

**Source**: `Chat_bot_v1\architecture.md` L21

```
使用者（@gyro.com.tw）
    │ HTTPS POST + JWT
    v 
Google Chat 平台 ─────────────────────────── 公司 GCP
    │
    v 
Cloud Run (asia-east1, FastAPI) ────────── 個人 GCP
    │ HTTPS + API Key
    v 
ngrok tunnel (free static domain) ─────── 個人 ngrok
    │
    v 
本機 RAG backend (port 8001, FastAPI)
    │
    ├───> Ollama bge-m3 (embedding, 本機) ── 個人
    ├───> Gemini API (LLM) ──────────────── 個人 API key
    └───> Qdrant localhost:6333 ─────────── 本機 Docker
```

