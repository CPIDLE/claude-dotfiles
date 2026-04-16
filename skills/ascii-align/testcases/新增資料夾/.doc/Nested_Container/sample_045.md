## Sample 045

**Source**: `Chat_bot_v1\google-chat-bot-aws.md` L47

```
Google Chat                        AWS EC2
┌──────────┐    HTTPS POST     ┌────────────────────────────┐
│ 使用者   │ ────────────────> │ Caddy (reverse proxy)      │
│ @kb ...  │                   │   ├── /chat/event --> FastAPI│
│          │ <──────────────── │   └── /api/* --> FastAPI   │
│ 回應卡片 │    JSON response  │                            │
└──────────┘                   │ FastAPI (api_server.py)    │
                               │   ├── /chat/event (新增)   │
                               │   │   ├── 解析 Chat event  │
                               │   │   ├── 路由 fast/deep   │
                               │   │   └── 格式化回應卡片   │
                               │   ├── /api/search (既有)   │
                               │   └── /api/deep-query(既有)│
                               │                            │
                               │ Qdrant Docker (port 6333)  │
                               │   ├── pkb_docs             │
                               │   ├── pkb_images           │
                               │   └── pkb_mail             │
                               └──────────┬─────────────────┘
                                          │
                                          v 
                               ┌──────────────────┐
                               │ Google Gemini API│
                               │ - Embedding      │
                               │ - 2.5 Flash (RAG)│
                               └──────────────────┘
```

