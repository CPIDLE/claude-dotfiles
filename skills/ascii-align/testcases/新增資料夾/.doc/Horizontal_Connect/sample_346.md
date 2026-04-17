## Sample 346

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L530

```
_search_index.py → 候選文件清單 (--json)
_find_related.py → 分類關聯文件 (--json)
_calc_throughput.py → 工程計算結果 (--json) ─┐
                                               ├→ _report_init.py → 報告骨架 (.md)
                   客戶需求 JSON ───────────────┘
```

---

