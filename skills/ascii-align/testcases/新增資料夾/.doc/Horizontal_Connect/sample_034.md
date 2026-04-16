## Sample 034

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L158

```
log_update.py（主程式）
├── runningLog.__init__()
│   ├── loggingCarWork:        0.01s（預設，車上未設定）<-- 100Hz！
│   ├── loggingMaintenanceTime: 3600s（車上設定）
│   └── loggingStatisticTime:  1s（預設，車上未設定）
├── _runningLog()
│   ├── _runningperiodiclog(0.01, log_work)           <-- 每 0.01 秒
│   ├── _runningperiodiclog(3600, log_componentlife)   <-- 每 1 小時
│   └── _runningperiodiclog(1, log_consumption)        <-- 每 1 秒
└── sched.scheduler.run()  <-- 事件迴圈

子模組（每個都是獨立 class）：
├── log_work_update.py    --> log_work()        <-- 100Hz 呼叫！
├── log_pscmd_update.py   --> subscriber callback
├── log_consumption_update.py --> log_consumption()  <-- 每秒呼叫
├── log_maintenance_update.py --> log_maintain_update()
├── log_componentlife_update.py --> log_componentlife()
└── log_folder_check.py   --> log_folder_check()
```

