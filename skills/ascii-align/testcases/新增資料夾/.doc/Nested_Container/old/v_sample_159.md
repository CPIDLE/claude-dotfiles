## Sample 159

**Source**: `LineBot_Reporter_v1\docs\aws-migration-discussion.md` L176

```
┌──────────┐     ┌──────────────────────┐     ┌─────┐
│ API GW   │ --> │ Fargate Container    │ <-> │ S3  │
│ or Web   │     │                      │     │ .txt files
└──────────┘     │ FastAPI              │     │ templates
                 │ ├── /report (生成)   │     └─────┘
                 │ ├── /search (搜尋)   │
                 │ ├── /calc   (計算)   │         ┌──────────┐
                 │ └── gemini_client ───│───────> │ Gemini   │
                 │                      │         │ 2.5 Pro  │
                 │ _calc_throughput.py  │         └──────────┘
                 │ gyro-report gen      │
                 └──────────────────────┘
```

---

