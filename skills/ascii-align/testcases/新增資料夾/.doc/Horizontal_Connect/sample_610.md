## Sample 610

**Source**: `TM_Program_Analysis_v0\docs\ERROR_CODE_REFERENCE.md` L137

```
夾爪應該夾緊 (grip_close=true)，正常期望 RS485IO = {1,0,1,1,1,*,0,1}
  ├─ RS485IO[0]==0 & [1]==1?  → YES → Error 1119（近接感測器反向）
  ├─ RS485IO[2]==0?           → YES → Error 1120（壓力感測器無信號）
  ├─ RS485IO[3]==0?
  │   ├─ RS485IO[4]==0?       → YES → Error 1122（位置感測器也無信號）
  │   ├─ RS485IO[6]==1?       → YES → Error 1124（異常偵測觸發）
  │   └─ RS485IO[7]==0?       → YES → Error 1125（重量感測器無信號）
  ├─ RS485IO[3]==1? (Tray 在位)
  │   ├─ RS485IO[4]==0?       → YES → Error 1122
  │   ├─ RS485IO[6]==1?       → YES → Error 1124
  │   └─ RS485IO[7]==0?       → YES → Error 1125
  └─ 都正常 → I/O 記錄 → Error 1121（狀態不一致）
```

---

