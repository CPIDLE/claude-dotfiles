## Sample 588

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L258

```
initial_prog.script (12,241 行 / 1,341 moves)
  │
  ├─ 常駐載入 Helper Scripts ───────────────────────────────────────┐
  │    tc100_gripper_open / close     夾爪開關                      │
  │    gripeer_cover_open / close     蓋子開關                      │
  │    fork_sensor_check              叉子感測器驗證（4 sensors）   │
  │    payload.script                 計算載重                      │
  │    initial_modbus_tcp             Modbus 初始化                 │
  │    get_command_*                  解析外部指令                  │
  │    rs485io_read                   讀取 IO Box                   │
  │    set_alarm_and_stop             報警停機                      │
  │    Loop / Loop_initial            迴圈控制                      │
  │                                                                 │
  ├─ Body ────────────────────────────────────────────────────────  │
  │    Body_take_put (4,145 行 / 405 moves)                         │
  │      呼叫: fork_sensor_check, payload, tc100_*                  │
  │                                                                 │
  ├─ EQ2600 ──────────────────────────────────────────────────────  │
  │    port1_load / port2_unload / port3_load / port4_unload        │
  │      呼叫: fork_sensor_check, payload, tc100_*                  │
  │                                                                 │
  ├─ EQ2800 ──────────────────────────────────────────────────────  │
  │    port1_unload / port2_load / port3_unload / port4_load        │
  │    port14_swap（交換模式）                                      │
  │    EQ2800P02_* 變體                                             │
  │      呼叫: fork_sensor_check, payload, set_alarm_and_stop       │
  │                                                                 │
  ├─ EQ2845 ─── port1_load_unload                                   │
  ├─ EQ3670 ─── port1/port2_load_unload + backup                    │
  ├─ EQ3800 ─── port1_load_unload                                   │
  │                                                                 │
  └─ Erack ───────────────────────────────────────────────────────  │
       Erack_load_unload (1,195 行 / 73 moves)                      │
       Erack_teach / Erack_teach123（教導模式）                     │
         呼叫: fork_sensor_check, payload, tc100_*, gripeer_cover   │
```

---

