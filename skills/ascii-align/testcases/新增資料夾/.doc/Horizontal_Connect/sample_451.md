## Sample 451

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L237

```
ROS topics ──┐
CSV 來源 ────┤── Bridge process ───> SQLite（本地）
E84 log ─────┘       │
                     │ 背景執行緒（每 5-10 秒）
                     │ SELECT * FROM <table> WHERE synced = 0 LIMIT 1000
                     │ --> influxdb_client.write_points(rows)
                     │ --> UPDATE SET synced = 1
                     v 
              Server InfluxDB
```

