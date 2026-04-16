## Sample 303

**Source**: `personal-rag_v2\README.md` L212

```
SQLite: db/phase2_state.db
  ├── progress 表: sha256(PK), status(pending/processing/done/error)
  └── run_log 表:  event(start/crash/complete/email_sent), timestamp

重啟時：
  1. status=processing --> 重設為 pending
  2. 偵測上次未完成 --> 寄重啟通知
  3. 跳過 status=done 的檔案
```

