## Sample 497

**Source**: `Reporter_v1\WORKSPACE\a04\02_Line_bot_v0.md` L28

```
LINE 使用者 → ngrok HTTPS tunnel → n8n:5678 webhook
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         │                                                       │
    Log Handler → chat-log (JSON)                    AI Smart Handler
    @?/@ai/@KD/@img (Function Calling)               │
    @SUM/@SUMD (聊天摘要)                            ├─ search_documents
                                                     ├─ search_images
                                                     ├─ generate_image_context
                                                     └─ generate_image (use_kb param)

    nginx:80 → /images/* (AI 生成圖片靜態服務)
```

---

