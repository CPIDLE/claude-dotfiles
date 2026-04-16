## Sample 607

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L115

```
Day:  0 ────── 500 ── 560 ── 620 ── ... ── N
      │ Fold 1 train │ val1  │
      │         Fold 2 train │ val2 │
      │              Fold 3 train   │ val3 │

窗口: train=expanding, val=sliding 60 days, step=60 days
```

