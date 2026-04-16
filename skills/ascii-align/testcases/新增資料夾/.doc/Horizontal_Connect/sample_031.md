## Sample 031

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6a.md` L143

```
停車層（stuckstate = True）：
  ├─ P1/P2 = Lidar 保護區 --> 立即停車
  ├─ IRCollisionProt = IR 碰撞保護 --> 立即停車
  └─ pointcloud_stop = 3D 點雲 --> 最後防線

減速層（playslowdown = True）：
  ├─ W1/W2 = Lidar 警告區 --> 播音減速（不停車）
  └─ LidarSurround_Det2/4 --> 播音減速

來源：sys_indicator.py L1680-1733、safety_monitor.py（純 log 記錄器）
```

