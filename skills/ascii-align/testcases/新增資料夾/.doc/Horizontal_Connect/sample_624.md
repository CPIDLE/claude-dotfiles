## Sample 624

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L93

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") != true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") != true
  ├─ [條件成立] --> Port 是空的 --> 繼續放置
  └─ [條件不成立] --> Port 上有東西
       ├─ [var_PSPL_check < 3] --> 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] --> 超過重試次數
            --> Log: ERROR_CODE
            --> SET: ERROR_CODE_MODBUS = 1311
            --> STOP（停機）
```

