## Sample 641

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L41

```
                    ┌──────────────────┐
    RTDE (reg 0-2)  │   PLC / MES      │
  <────────────────>│  (外部控制器)    │
                    └──────────────────┘
                            │
                    ┌───────┴───────┐
                    │    UR30       │
                    │ (Polyscope)   │
                    └──┬───┬───┬────┘
          Modbus TCP   │   │   │  RS485
       ┌───────────────┘   │   └──────────────┐
       v                   v                  v 
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ PLC/IO 模組  │  │  SensoPart   │  │ TC100 Gripper    │
│ 192.168.1.1  │  │  VISOR       │  │ + RS485 IO Box   │
│ Modbus TCP   │  │  XML-RPC     │  │ Tool Modbus      │
│ port 502     │  │  port 46527  │  │ addr 1,2         │
└──────────────┘  └──────────────┘  └──────────────────┘
```

