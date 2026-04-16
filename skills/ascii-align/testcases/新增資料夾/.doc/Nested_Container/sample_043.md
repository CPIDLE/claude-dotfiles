## Sample 043

**Source**: `Chat_bot_v1\aws-migration-discussion.md` L109

```
┌───────────┐    ┌──────────────────┐    ┌─────┐
│ API GW    │ -->│ ECS/Fargate      │ <---->   │ S3  │
│           │    │ Docker 容器      │    │     │
└───────────┘    │ FastAPI          │    └─────┘
                 │ Python 腳本      │
                 │                  │    ┌────────────────┐
                 │  gemini client ──│───>│ Google Gemini  │
                 │                  │    │ - Embedding API│
                 └──────────────────┘    │ - Chat/Gen API │
                                         └────────────────┘
```

