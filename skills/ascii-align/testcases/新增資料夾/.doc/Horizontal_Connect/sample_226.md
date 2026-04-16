## Sample 226

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\ERROR_CODE_REFERENCE.md` L113

```
夾爪應該夾緊，但 DI[2]&DI[5] 無信號
  ├─ DI[0] 有信號?  --> YES --> Error 1115（DI0 異常觸發）
  ├─ DI[1]&DI[2] 有信號? --> YES --> Error 1116（DI1+DI2 組合異常）
  ├─ DI[3] 有信號?  --> YES --> Error 1117（DI3 異常觸發）
  └─ 都沒有 --> WaitFor 重試
```

