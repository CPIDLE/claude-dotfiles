## Sample 526

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書.md` L223

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

