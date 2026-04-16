## Sample 480

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L98

```
LINE 使用者
    │
    v 
ngrok HTTPS tunnel
    │
    v 
n8n:5678 webhook
    ├─ Log Handler --> chat-log (JSON, 3 天)
    ├─ AI Smart Handler (Gemini Function Calling)
    │   ├─ search_documents
    │   ├─ search_images
    │   ├─ generate_image_context
    │   └─ generate_image (use_kb param)
    └─ Summary Handler (@SUM / @SUMD)
        └─ Gemini 2.5 Flash thinking mode

nginx:80 --> /images/* (AI 生成圖片靜態服務)
```

