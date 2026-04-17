## Sample 500

**Source**: `Reporter_v1\WORKSPACE\a04\03_LineBot_Reporter_v1.md` L59

```
LineBot_Reporter_v1/
├── docker-compose.yml          # 三服務定義 (caddy + n8n + reporter-api)
├── Caddyfile                   # Caddy 反向代理配置
├── .env.example                # 環境變數模板
├── docs/
│   ├── phase0-report.md        # Phase 0 完成報告
│   ├── unified-aws-migration.md # AWS 遷移規劃
│   ├── aws-migration-discussion.md
│   └── line-bot-aws-migration.md
├── reporter/                   # FastAPI 知識庫應用
├── workflows/                  # n8n workflow JSON
├── knowledge-base/             # 知識庫檔案掛載點
├── images/                     # n8n 生成圖片
└── n8n-data/                   # n8n 持久化資料
```

---

