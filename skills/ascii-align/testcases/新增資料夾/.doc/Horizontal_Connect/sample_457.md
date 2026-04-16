## Sample 457

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L311

```
1  設備即時資料
   ROS topics / API poll ───> Bridge ───> Edge SQLite (synced=0)

2  正常同步
   Bridge 背景執行緒 --> SELECT synced=0 LIMIT 1000 --> push Server InfluxDB --> UPDATE synced=1

3  斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

4  重連
   背景執行緒掃 synced=0 --> batch push 回補 --> Server 時間軸完整

5  現場除錯（臨時）
   NB 同步小工具 <─── Edge SQLite --> NB InfluxDB + Grafana
```

