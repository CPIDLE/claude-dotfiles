## Sample 283

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L43

```
┌─────────────────────────────────┐
│ IPC: BOXER-6639 / 6640          │
│                                 │
│ ├─ USB 3.0 x 2, USB 2.0         │
│ ├─ LAN x 3                      │
│ │   ├─ T-01 --> TP-LINK LAN HUB │
│ │   ├─ T-03 --> TM 手臂主機     │ <─── TM Modbus / ROS 通訊
│ │   └─ T-04 --> 外部擴充面板    │
│ │                               │
│ ├─ 擴充面板                     │
│ │   ├─ COM1~COM5 (RS485/232)    │
│ │   ├─ HDMI x 2 ──────────> 觸控螢幕（直接接，非樹莓派）
│ │   ├─ VGA                      │
│ │   └─ 觸控 USB ─────────> 觸控螢幕
│ │                               │
│ ├─ Docker 容器                  │
│ │   ├─ AGVWeb (Flask)           │ <─── Web UI + TM STOP 按鈕
│ │   ├─ rosbridge_websocket :9090│ <─── browser JS <-> ROS
│ │   └─ ROS master               │
│ │                               │
│ └─ LAN HUB-A / HUB-B            │
│     ├─ sensor 網路              │
│     └─ 外部擴充                 │
└─────────────────────────────────┘
```

