## Sample 542

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_Architecture.md` L224

```
RobotAdapter
├── URAdapter          (單臂 — UR30)
├── TMAdapter          (單臂 — TM12/TM14M)
├── AMRAdapter         (移動平台 — AMRA04/AMRW)
│   └── nav2_client    (ROS2 Action)
├── DualArmAdapter     (雙臂組合)
│   ├── left: TMAdapter
│   ├── right: TMAdapter
│   └── coordinator: DualArmCoordinator
└── TriArmAdapter      (三臂組合)
    ├── arms: [TMAdapter, TMAdapter, URAdapter]
    └── coordinator: TriArmCoordinator
```

---

