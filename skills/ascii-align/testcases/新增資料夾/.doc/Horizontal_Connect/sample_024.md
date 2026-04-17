## Sample 024

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L637

```
IPC (enp5s0, SOEM Master)
  │
  ╞══ Slave 1: 前輪轉向 (Position mode) ← 100% 先 lost
  ╞══ Slave 2: 前輪驅動 (Speed mode)
  ╞══ Slave 3: 後輪轉向 (Position mode)
  ╘══ Slave 4: 後輪驅動 (Speed mode)

Daisy chain 拓撲：斷在 Slave 1 → 下游 2/3/4 全部連帶失聯
驅動器之間無 IPC 連線（純串接）
SM Watchdog: 硬編碼 5000 (motor_control.cpp L213)
Cycle time: 2ms, DC sync: 62.5µs shift
```

---

