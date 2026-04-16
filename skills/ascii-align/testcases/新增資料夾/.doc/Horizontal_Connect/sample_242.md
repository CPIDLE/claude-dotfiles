## Sample 242

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\MR_PORT_PLACE_ANALYSIS.md` L109

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") == true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") == true
  ├─ [條件成立] --> Tray 確認在位 --> 後退離開
  └─ [條件不成立] --> Tray 不在位
       ├─ [var_PSPL_check < 3] --> 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] --> 超過重試次數
            --> Log: ERROR_CODE
            --> SET: ERROR_CODE_MODBUS = 1311
            --> STOP（停機）
```

