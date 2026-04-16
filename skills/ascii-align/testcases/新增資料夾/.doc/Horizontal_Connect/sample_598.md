## Sample 598

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L270

```
Observation [150]
  ├─ Policy Net: Linear(150,64) --> Tanh --> Linear(64,64) --> Tanh
  │    └─ Action Net: Linear(64, 3) --> Categorical Distribution
  └─ Value Net:  Linear(150,64) --> Tanh --> Linear(64,64) --> Tanh
       └─ Linear(64, 1) --> V(s)
```

