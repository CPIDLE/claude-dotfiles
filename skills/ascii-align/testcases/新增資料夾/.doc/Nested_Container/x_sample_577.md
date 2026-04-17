## Sample 577

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L163

```
  task.gyro.yaml (平台無關)
  ┌───────────────────────────────────────────────────────────────────────┐
  │ waypoints:              │                                             │
  │   pick_pos: [x,y,z,r]   │       GYRO-Compiler                         │
  │ sequences:              │      ┌──────────────┐                       │
  │   pick_and_place:       │────-->│ --target=tm  │──--> .flow (TM 原生) │
  │     - move_linear: pick │      │ --target=ur  │──--> .script (UR 原生)│
  │     - gripper: close    │      └──────────────┘                       │
  │     - move_linear: place│                                             │
  │     - gripper: open     │  Git 版控 . 可 diff . 可 review             │
  └───────────────────────────────────────────────────────────────────────┘
```

---
