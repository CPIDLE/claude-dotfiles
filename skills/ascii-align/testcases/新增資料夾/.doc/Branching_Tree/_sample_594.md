## Sample 594

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L26

```
yfinance / FinMind API
        │
        ▼
┌─────────────────┐     ┌───────────────────┐
│   US Market      │     │   TW Market        │
│   Fetcher        │     │   Fetcher          │
│  (20+ symbols)   │     │  (法人/期貨/融資)  │
└────────┬────────┘     └────────┬──────────┘
         │                       │
         ▼                       ▼
    ┌────────────────────────────────┐
    │       daily_features (SQLite)  │
    │   25 global + 8 TAIEX 技術指標 │
    └──────────────┬─────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  FeatureBuilder [5, 30]   GMP FeatureEngineer
         │                   │
    ┌────┴────┐         LightGBM
    ▼         ▼         (週/月報酬)
Transformer  RL PPO
 (分類)     (交易)
    │         │
    ▼         ▼
 prediction_log ──► Daily Email
```

---
