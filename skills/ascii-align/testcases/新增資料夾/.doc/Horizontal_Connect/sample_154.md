## Sample 154

**Source**: `Line_bot_v0\README.md` L48

```
LINE 使用者
     |
ngrok (HTTPS tunnel, docker-compose 內建)
     |
n8n:5678 (webhook 直連)
     |
n8n workflow
  Log Message  → 所有文字訊息寫入 chat-log (JSON + MD)
  @?           → LINE Reply Help
  @ai          → AI Smart Handler (Gemini Function Calling)
               │  General 模式：聊天 + generate_image
               │  KB 模式(/k)：search_documents / search_images /
               │                generate_image_context / generate_image
               └→ 最多 3+1 輪 FC loop + post-check retry
  @KD/@KI/@KGI → 知識庫直接搜尋 (Loop Handler 支援連續搜尋)
  @img         → Gemini Image Generation → 存檔 → Reply/Push 圖片
  @SUM         → 讀取 2hr chat-log → Gemini 摘要 → Reply
  Daily 4AM    → 讀取 24hr chat-log → Gemini 每日摘要 → 存檔

nginx:80
  /images/*    → 靜態圖片（供 @img 結果顯示）
```

---

