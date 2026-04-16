## Sample 162

**Source**: `LineBot_Reporter_v1\docs\unified-aws-migration.md` L129

```
┌─────────────────────────────────────┐
│  EC2 (t3.medium, Ubuntu)            │
│                                     │
│  Docker Compose:                    │
│  ├── Caddy (HTTPS, 取代 ngrok+nginx)│
│  ├── n8n (LINE Bot)                 │
│  │                                  │
│  Host:                              │
│  ├── Reporter_v0 腳本               │
│  ├── .doc/ 知識庫 (~55MB)           │
│  ├── Claude Code CLI                │
│  └── Chrome (PDF 輸出)              │
└─────────────────────────────────────┘
```

