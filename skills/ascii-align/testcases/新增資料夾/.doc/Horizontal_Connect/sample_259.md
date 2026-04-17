## Sample 259

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L130

```
var_read_RTDE ≔ read_input_integer_register(0)
    │
    ├─ 30001：初始化歸位（開夾 → 依位置回 Home_L 或 Home_R）
    ├─ 30000：移動到啟動位（p_for_startup）
    ├─ 30002：開夾 → 回 Home_R
    ├─ 30009：Fork 感測器檢查
    └─ 其他 ：進入自動作業模式
```

---

