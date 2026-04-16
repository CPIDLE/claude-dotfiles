## Sample 594

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L26

```
yfinance / FinMind API
        │
        v 
┌──────────────────┐    ┌────────────────────┐
│   US Market      │    │   TW Market        │
│   Fetcher        │    │   Fetcher          │
│  (20+ symbols)   │    │  (法人/期貨/融資)  │
└────────┬─────────┘    └────────┬───────────┘
         │                       │
         v                       v 
    ┌────────────────────────────────┐
    │       daily_features (SQLite)  │
    │   25 global + 8 TAIEX 技術指標 │
    └──────────────┬─────────────────┘
                   │
         ┌─────────┴─────────┐
         v                   v 
  FeatureBuilder [5, 30]   GMP FeatureEngineer
         │                   │
    ┌────┴────┐         LightGBM
    v         v          (週/月報酬)
Transformer  RL PPO
 (分類)     (交易)
    │         │
    v         v 
 prediction_log ───> Daily Email
```

