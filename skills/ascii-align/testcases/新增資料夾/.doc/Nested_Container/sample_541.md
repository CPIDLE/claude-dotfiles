## Sample 541

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_Architecture.md` L56

```
┌──────────────────────────────────────────────────────────────┐
│                    Unified Web / HMI UI                      │
│   (React/Vue)  設定 .  操作 .  監控 .  教導 .  模擬              │
├──────────────────────────────────────────────────────────────┤
│                  gRPC Gateway (Proto3)                       │
│   統一 API 層 -- 平台無關的操作語意                          │
├──────────────────────┬───────────────────────────────────────┤
│   Module A          │   Module B                           │
│   GYRO 解析層       │   硬體即時通訊層                     │
│   (離線 / 設定)     │   (線上 / 操控)                      │
│                     │                                      │
│   ┌─ DSL Engine ────┐│   ┌─ Protocol Adapters ─────────────┐│
│   │ GYRO-DSL        ││   │ UR:  RTDE + Modbus TCP          ││
│   │ GYRO-Compiler   ││   │ TM:  Modbus TCP + EtherCAT      ││
│   └─────────────────┘│   │ AMR: ROS2 Action/Topic          ││
│                     ││ 人型: ROS2 + MoveIt2 + MCP      │   │
│   ┌─ Platform ──────┐│   └─────────────────────────────────┘│
│   │ Parsers         ││                                     │
│   │ TM: flow_parser ││   ┌─ Safety Layer ──────────────────┐│
│   │ UR: script_     ││   │ 碰撞偵測 .  力矩限制 .  E-Stop  ││
│   │     parser      │││ 安全區域 .  速度限制           │   │
│   │ Editors         ││   └─────────────────────────────────┘│
│   │ Kinematics      ││                                     │
│   └─────────────────┘│                                     │
├──────────────────────┴───────────────────────────────────────┤
│              Data Layer (Git + DB)                         │
│   task.gyro.yaml (唯一真實來源) .  SQLite logs .  Prometheus│
└────────────────────────────────────────────────────────────┘
```

