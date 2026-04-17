## Sample 015

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L441

```
┌──────────────┐    /motor_cmd      ┌───────────────┐
│              │ ─────────────────> │               │
│  gyro-ros    │    /motor_actual   │  ethercat /   │
│  (主系統)    │ <───────────────── │  canopen      │
│              │    /motorAlarm     │  (馬達控制)   │
│              │ <───────────────── │               │
└──────┬───────┘                    └───────────────┘
       │
       │  rosbridge (port 9090)
       │
┌──────┴──────┐
│   agvweb    │
│   (Web UI)  │
└─────────────┘
```

---

