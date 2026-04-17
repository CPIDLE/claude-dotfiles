## Sample 252

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\VISION_ARCHITECTURE.md` L246

```
experiments/baseline/        ← TM Flow 匯出的最簡 Vision Job
experiments/exp_NN_<name>/   ← 改一項設定後的快照
        │
        ▼
scripts/vision_schema_diff.py
        │
        ▼
docs/findings/exp_NN_*.md    ← 自動 diff 報表
        │
        ▼
docs/VISION_SCHEMA_FINDINGS.md  ← 累積知識庫
```

---

