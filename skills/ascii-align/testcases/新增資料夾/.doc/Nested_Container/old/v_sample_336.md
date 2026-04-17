## Sample 336

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L109

```
┌───────────┐    ┌──────────────────┐    ┌─────┐
│ API GW    │ >  │ ECS/Fargate      │ <> │ S3  │
│           │    │ Docker 容器      │    │     │
└───────────┘    │ FastAPI          │    └─────┘
                 │ Python 腳本      │
                 │                  │    ┌────────────────┐
                 │  gemini client ──│──> │ Google Gemini  │
                 │                  │    │ - Embedding API│
                 └──────────────────┘    │ - Chat/Gen API │
                                         └────────────────┘
```

---

