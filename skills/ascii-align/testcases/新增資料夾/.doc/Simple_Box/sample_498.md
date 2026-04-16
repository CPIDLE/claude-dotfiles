## Sample 498

**Source**: `Reporter_v1\WORKSPACE\a04\02_Line_bot_v0.md` L58

```
Line_bot_v0/
├── docker-compose.yml           # 三服務編排 (n8n + nginx + ngrok)
├── README.md                    # 文檔及指令說明
├── changelog.md                 # 30+ 項特性與修復紀錄
├── .env.example                 # 環境變數模板
├── nginx/
│   └── default.conf            # 反向代理 + 靜態檔案配置
├── workflows/
│   ├── line-bot-gemini.json    # n8n workflow JSON
│   └── ai-smart-handler-fc.js  # Function Calling 實現
├── images/                      # AI 生成圖片 (runtime)
└── n8n-data/
    ├── chat-log/               # 訊息記錄 (JSON + MD, 保留 3 天)
    ├── chat-history/           # 對話記憶 (per-user, 30 min TTL)
    ├── pending/                # 待辦結果 (5 min TTL)
    └── daily-summaries/        # 每日摘要存檔 (4AM 自動生成)
```

