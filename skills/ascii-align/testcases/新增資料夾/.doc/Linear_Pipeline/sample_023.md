## Sample 023

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L461

```
IPC <-> Slave 1（前輪轉向）實體連線問題
  ├─ 100% Slave 1 先 lost（26/26 次）
  ├─ 降速改善 5.5 倍（震動 --> 線路搖晃）
  ├─ 19:48~19:57 密集叢集（10 分鐘 11 次 = 間歇性接觸不良）
  └─ 軟體一致但只有 AMR03 頻繁發生
     v 
Slave 1 lost --> daisy chain 下游全部失聯 (M1+M2+M3+M4 3804)
     v 
Sync Manager Watchdog (0x001b) --> 4 馬達同時報錯
     v 
恢復與錯誤每秒震盪 75 秒
     v 
Docking 機構超時 --> DockNG x  2
```

