## Sample 021

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L284

```
AMR01 端 MQTT 通訊路徑中斷（整個 session 21 次獨立事件）
  ├─ 非 WiFi（wlp1s0 全天未連線、car ip 100% up）
  ├─ TCP unicast 正常（但 mqtt_client Docker 網路堆疊獨立）
  ├─ 非 CPU（離線時 avg 61.9% vs 基線 61.0%）
  ├─ 直接證據：MQTT error [-12] 緩衝溢出（06:00、08:55）
  ├─ 48% 同步離線 --> AMR01 接收端 mqtt_client 斷連
  └─ 52% 獨自離線 --> 對方發送端 mqtt_client 獨立故障
     v 
costmap 5 秒 timeout + ignore_offline:true --> 其他車障礙物被移除
     v 
碰撞時恰好在離線窗口 + AMR01 正在橫移會車
     v  同時
W1/W2 已觸發（13:42:26）但：
  ├─ 安全開啟時未停車（原因不明）
  └─ 隨後安全功能被 macro 關閉（13:42:28~35，7 秒窗口）
     v  同時
CPU 過載（AprilTag 107% + log_update 92%）+ motor jitter（持續 6.4 次/分）
     v 
碰撞 --> pointcloud_stop（13:43:15）--> Alarm + Manual（13:43:48）
```

