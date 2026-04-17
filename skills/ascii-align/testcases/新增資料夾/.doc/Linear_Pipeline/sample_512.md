## Sample 512

**Source**: `Reporter_v1\WORKSPACE\a05\TM_UR_COMPLETED_SUMMARY_elk.md` L319

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

