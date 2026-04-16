## Sample 573

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L69

```
  ┌────────────────────────────────────────────────────────────────────┐
  │                    兩套工具鏈（各 80% 完成）                       │
  │                                                                    │
  │   TM 工具鏈 (8 模組 .  4,003 行)    UR 工具鏈 (11 模組 .  3,629 行)│
  │                                                                   │
  │   .flow XML ───> Parser ───> Analyzer ───> Doc Generator          │
  │       ^                                       │                   │
  │       └──── Editor (MutableFlowDocument) <────┘                   │
  │              Simplifier (重複偵測)                                │
  │              Kinematics (FK/IK)                                   │
  │                                                                   │
  │   .script ───> Parser ───> Loader ───> Analyzer ───> Doc Gen      │
  │       ^                                            │              │
  │       └──── Editor (ScriptEditor) <────────────────┘              │
  │              Simplifier (跨檔重複)                                │
  │              Kinematics (FK/IK)                                   │
  └───────────────────────────────────────────────────────────────────┘

  已自動產出：50+ 份 TM 分析文件 ｜ 81+ 份 UR 分析文件
  測試覆蓋：  34 tests (TM)      ｜ 46 tests (UR)
  FK/IK：    TM12 DH 驗證通過    ｜ UR30 DH 驗證通過
```

