## Sample 559

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L31

```
            initial_prog.script (12,241 行 / 1,341 moves)
                              │
       ┌──────────┬───────────┼───────────┬───────────────┐
       │          │           │           │               │
   73 程式     719 點位    Modbus TCP   SensoPart   RS485
   64,503 行  (unique 321)  /RTU        VISOR

   ┌──────────────────────────────────────────────────────┐
   │ 設備群組程式分佈                                     │
   ├──────────┬───────┬───────────────────────────────────┤
   │ Body     │  3 支 │ Body_take_put (4,145行/405 moves) │
   │ EQ2600   │  7 支 │ port load/unload                  │
   │ EQ2800   │ 14 支 │ port swap                         │
   │ EQ3670   │  4 支 │ 最大 6,870行/651 moves            │
   │ Erack    │  7 支 │ load/unload                       │
   │ Gyro_util│ 20 支 │ initial_prog 主控                 │
   └──────────┴───────┴───────────────────────────────────┘

  設計哲學：巨石腳本 · 指令驅動 · 僕人模式（被動等 PLC RTDE 指令）
```

