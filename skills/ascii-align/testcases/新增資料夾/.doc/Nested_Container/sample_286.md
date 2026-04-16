## Sample 286

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L135

```
垂直電路板                          水平電路板
┌───────────┐                     ┌───────────┐
│ V-PL01 ───┐│                      │ H-PL01 ─┐│
│ V-PL02 ─┤ │                       │ H-PL02 ─┤│
│ V-PL03 ─┼──> AND (U8)───┐         │ H-PL03 ─┼──> AND (U8)─┐
│ V-PL04 ───┘│            │         │ H-PL04 ─┘│            │
│           │            v          │         │            v 
│ BUMP(L) ───>─ OR ───> DI_2        │ BUMP(R) ───>─ OR ───> DI_2
└───────────┘     ^                └──────────┘     ^ 
                  │                                  │
           PS group AND ───> DI_0              PS group AND ───> DI_0
           PL group AND ───> DI_1              PL group AND ───> DI_1
```

