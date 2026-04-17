## Sample 040

**Source**: `Chat_bot_v1\architecture.md` L86

```
使用者 /kb 電源設計
  │
  ▼ [公司 GCP]       Google Chat → Cloud Run
  ▼ [個人 GCP]       JWT 驗證 → 解析 slash command
  ▼ [本機 Ollama]    bge-m3 embedding("電源設計") → vector
  ▼ [本機]           Qdrant 並行搜尋 3 collections top-10，組裝 context
  ▼ [個人 Gemini]    Gemini 2.5 Flash 推理 → 繁中回答 + 建議關鍵字
  ▼ [個人 GCP]       格式化回應
  ▼                  Google Chat 顯示 RAG 回答
```

---

