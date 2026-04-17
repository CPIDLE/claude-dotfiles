## Sample 050

**Source**: `Chat_bot_v1\README.md` L90

```
Google Chat (@gyro.com.tw)  ─┐
LINE Bot                     ├→ Cloud Run thin proxy (JWT 驗證, 個人 GCP)
                             │     → ngrok tunnel → 本機 RAG backend (API key + rate limit)
                             │         → Ollama bge-m3 (embedding) + Gemini API (LLM)
                             │         → 本機 Qdrant (向量搜尋, 並行 3 collections)
                             │
LINE Webhook ────────────────┘  → /webhook/line-webhook (signature 驗證)
                                → /line/push (主動推送)
```

---

