## Sample 455

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L573

```
現在（兩條 Bridge，直接 push Server，無斷線保護）：

  ROS topics ──→ prometheus_bridge ──→ Server Prometheus
             ──→ influxdb_bridge  ──→ Server InfluxDB

合併後（一條 Bridge，本地 buffer，統一 push）：

  ROS topics ─┐
  CSV 來源 ───┼→ amr_bridge ──→ Edge SQLite ──batch push──→ Server InfluxDB
  E84 log ────┘                     ↑
                              Tiny Agent 斷線時讀取
```

---

