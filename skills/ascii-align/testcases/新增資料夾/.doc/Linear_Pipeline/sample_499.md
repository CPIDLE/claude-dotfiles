## Sample 499

**Source**: `Reporter_v1\WORKSPACE\a04\03_LineBot_Reporter_v1.md` L28

```
Internet:80/443
        │
    [ Caddy ]  (反向代理 + HTTPS)
    /   |   \
   /    |    \
/webhook/* /api/* /images/*
  │         │        │
[n8n]  [reporter-api]  [static]
:5678      :8000        /srv/images/
  │         │
LINE Bot  知識庫搜尋 (FastAPI)
Gemini    + ChromaDB vector DB
         + Gemini embedding
```

