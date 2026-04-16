## Sample 595

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L156

```
Input [batch, 5, 30]
  │
  ├─ Feature Attention Gate: Linear(30,30) --> sigmoid 逐特徵加權
  ├─ Projection: Linear(30, 64)
  ├─ Learnable Positional Embedding(5, 64)
  ├─ TransformerEncoder x  2 (ffn=256, GELU)
  ├─ Attention Pooling: Linear(64,1) --> softmax 加權聚合
  └─ Classification Head (with residual)
       ├─ LayerNorm(64) --> Linear(64,64) --> GELU --> Dropout
       └─ Linear(64, 3) + residual
```

