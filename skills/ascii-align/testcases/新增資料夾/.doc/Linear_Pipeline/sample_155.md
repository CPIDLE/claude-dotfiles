## Sample 155

**Source**: `Line_bot_v0\README.md` L135

```
.
├── docker-compose.yml          # Docker 服務（n8n + nginx + ngrok）
├── nginx/
│   └── default.conf            # nginx 反向代理 + 靜態檔案
├── workflows/
│   ├── line-bot-gemini.json    # n8n workflow
│   └── ai-smart-handler-fc.js  # AI Smart Handler 原始碼（Function Calling 版）
├── images/                     # AI 生成圖片（runtime，git ignored）
├── n8n-data/                   # n8n 持久化資料（git ignored）
│   ├── chat-log/               # 訊息記錄 JSON + MD（runtime，保留 3 天）
│   ├── chat-history/           # 對話記憶（per-user，30 分鐘過期）
│   ├── pending/                # 等待中結果（pending mechanism，5 分鐘過期）
│   └── daily-summaries/        # 每日摘要存檔（4AM 自動生成）
├── .env.example                # 環境變數範本
├── CHANGELOG.md                # 修改紀錄
└── README.md
```

