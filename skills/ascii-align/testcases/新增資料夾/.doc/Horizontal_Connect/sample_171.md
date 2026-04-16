## Sample 171

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L36

```
Need storage?
├─ Key-value (config, sessions, cache) --> kv/
├─ Relational SQL --> d1/ (SQLite) or hyperdrive/ (existing Postgres/MySQL)
├─ Object/file storage (S3-compatible) --> r2/
├─ Message queue (async processing) --> queues/
├─ Vector embeddings (AI/semantic search) --> vectorize/
├─ Strongly-consistent per-entity state --> durable-objects/ (DO storage)
├─ Secrets management --> secrets-store/
├─ Streaming ETL to R2 --> pipelines/
└─ Persistent cache (long-term retention) --> cache-reserve/
```

