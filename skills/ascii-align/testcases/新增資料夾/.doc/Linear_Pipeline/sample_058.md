## Sample 058

**Source**: `Claude-Code-Agent-Monitor\server\README.md` L130

```
server/
├── index.js               # Express app + server bootstrap
├── db.js                  # SQLite connection + prepared statements
├── websocket.js           # WebSocket server + broadcast
├── compat-sqlite.js       # Fallback for node:sqlite (Node 22.5+)
│
├── routes/
│   ├── hooks.js           # Hook ingestion endpoints
│   ├── sessions.js        # Session CRUD API
│   ├── agents.js          # Agent CRUD API
│   └── pricing.js         # Pricing rules API
│
└── __tests__/
    └── api.test.js        # Integration tests
```

---

