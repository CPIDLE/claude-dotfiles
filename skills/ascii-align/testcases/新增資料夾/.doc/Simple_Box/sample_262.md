## Sample 262

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L361

```
initial_prog (主程式)
├── Body_take_put
├── Erack_load_unload
├── EQ2600_port1_load / port2_unload / port3_load / port4_unload
├── EQ2800_port{1-4}_{load/unload/swap}
├── EQ2800P02_port{1-4}_{load/unload/swap}
├── EQ2845_port1_load_unload
├── EQ3670_port{1-2}_load_unload
├── EQ3800_port1_load_unload
└── [helpers]
    ├── tc100_gripper_open / close
    ├── gripeer_cover_open / close / open_180
    ├── fork_sensor_check
    ├── payload
    ├── set_alarm_and_stop
    ├── initial_modbus_tcp
    ├── get_command_extra_info / portname
    ├── rs485io_read
    └── Loop_initial / Loop
```

---

