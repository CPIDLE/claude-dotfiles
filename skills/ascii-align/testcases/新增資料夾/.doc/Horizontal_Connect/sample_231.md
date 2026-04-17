## Sample 231

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L88

```
IF: var_camera_once_eq_flag==true & g_camera_once==true?
  ├─ [YES] 已經拍過照，跳過 Vision FAR
  │    IF: var_runing > 0?
  │      ├─ [YES] → 直接到 Port 分派（Phase 5）
  │      └─ [NO]  → 移動到 P110 → Phase 5
  │
  └─ [NO] 未拍過照，執行 Vision FAR（Phase 3）
```

---

