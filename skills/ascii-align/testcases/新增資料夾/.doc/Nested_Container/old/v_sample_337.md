## Sample 337

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L176

<!-- aa: flow -->
```
┌──────────┐    ┌─────────────────────┐    ┌─────────┐
│ API GW   │    │ Fargate Container   │    │ S3      │
│ or Web   │ -->│                     │<-->│ .txt    │
└──────────┘    │ FastAPI             │    │ files   │
                │ ├── /report (生成)  │    │templates│
                │ ├── /search (搜尋)  │    └─────────┘
                │ ├── /calc   (計算)  │
                │ └── gemini_client ──│───────> ┌──────────┐
                │                     │         │ Gemini   │
                │ _calc_throughput.py │         │ 2.5 Pro  │
                │ gyro-report gen     │         └──────────┘
                └─────────────────────┘
```

---

