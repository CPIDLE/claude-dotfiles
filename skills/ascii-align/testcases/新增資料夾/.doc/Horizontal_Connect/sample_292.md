## Sample 292

**Source**: `personal-rag_v2\PKB\workspace\test_08\LOG_Investigation_AMR04_20260328.md` L333

```
時間（CST）  TMflow                 E84 State            carwork / Slot
─────────── ────────────────────── ──────────────────── ─────────────────────────
12:44:27    STOP Project                                 AMR at STK
            (軟體層，arm 未停)
12:44:29                           CMD 31,1,6 (load)    STK, DoorOK2, TM Moving
12:45:14                           succeeded ✓           TM Moving OK 21203
12:46:46                           CMD 2,1,6 (unload)   STK
12:47:28                                                 PS4=True (cassette in)
12:47:32                                                 CST_ID: WP0800222
12:47:34                           succeeded ✓           TM Moving OK -21403
12:47:40                                                 Moving → TEL57
12:48:31                                                 Docking at 7TEL57
12:48:34    ██ Run Project ██                            DockOK at 7TEL57
            (Init → Modbus                               Slot4: WP0800222
             open gripper!)
12:48:36                           CMD 32,0,6 (unload)  Loadunload, PioStart
12:48:39                                                 DoorOK2, TM Moving
12:49:17                           EQ unload goods ack
12:49:18    rapid pause/resume                           ██ TB1000 ██
12:49:18                                                 TB1000;RM1089
12:49:19                                                 ██ TM Moving NG ██
12:49:19                                                 Standby (stopped)
12:51:17                           ██ State1: error ██   EC103B added
                                   EC 103B (TP4 timeout)
12:53:16                           force reset ×2
13:08:59    SafetyIO Pause                               CD0006 (CstDoor err)
```

---

