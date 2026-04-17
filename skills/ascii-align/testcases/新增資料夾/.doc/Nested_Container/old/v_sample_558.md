## Sample 558

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L9

```
                        MainFlow (113 節點)
                             │
          ┌──────────┬───────┴───────┬───────────┐
          │          │               │           │
    37 SubFlow   5 MultiThread  68 Vision   244 變數
          │          │               Job    370 點位
          │          │
  ┌───────┴───────┐  ├─ CHECK_ALL_SENSOR_WHEN_CAR_MOVING
  │ MR_PORT_PLACE │  ├─ CHECK_ENCODER
  │  (423 節點)   │  ├─ CHECK_GRIP
  │               │  ├─ Pause_handle
  │ HT_9046LS_    │  └─ Pub_RS485IO
  │ TMMARK_NORMAL │
  │  (259 節點)   │
  └───────────────┘

  設計哲學：模組化 .  數據驅動 .  主人模式（主動 Modbus 監聽自主決策）
```

---

