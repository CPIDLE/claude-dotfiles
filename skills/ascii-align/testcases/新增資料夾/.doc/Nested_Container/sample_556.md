## Sample 556

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L273

```
  Phase 3                    Phase 4                     Phase 5
  單臂                       多臂 + 移動平台              全身

  ┌──────────────────────────────────────────────┐          ┌─────────────────┐         ┌───────────────┐
  │ TM                                           │         │  DualArm         │         │ Humanoid      │
  │ Adapter                                      │─────┐        │  ├ left: TM      │         │ ├ left_arm    │
  └──────────────────────────────────────────────┘│        │  ├ right: TM    │         │ ├ right_arm   │
             ├──共用-->                        │  └ coordinator │──共用──>│ ├ legs        │
  ┌────────────────────────────────────────────────┐│  介面  ├──────────────────┤  介面   │ ├ torso          │
  │ UR                                             │─────┘        │  AMR             │         │ └ AI policy   │
  │ Adapter                                        │         │  └ ROS2 nav2     │         └─────────────────────┘
  └────────────────────────────────────────────────┘          └─────────────────┘
                       TriArm
                       ├ arm1: TM
                       ├ arm2: TM
                       └ arm3: UR

  關鍵：手臂的 Adapter 介面從 Phase 3 到 Phase 5 完全複用
```

