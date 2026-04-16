## Sample 481

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L141

```
Internet :80 / :443
            │
    ┌───┴───┐
    │ Caddy │  反向代理 + HTTPS 自動憑證
    └───┬───┘
            │
   ┌────┼───┐
/webhook  /api  /images
   │        │      │
 [n8n]  [reporter-api]  [static]
 :5678    :8000          /srv/images/
   │        │
LINE Bot  FastAPI 知識庫
Gemini    + ChromaDB + Gemini embedding
```

