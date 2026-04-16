## Sample 454

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L526

```
ROS topics ───> prometheus_bridge.py (port 9200) ───> Prometheus (port 80) ───> Grafana
           ───> influxdb_bridge.py               ───> InfluxDB (port 8181) ───> Grafana
```

