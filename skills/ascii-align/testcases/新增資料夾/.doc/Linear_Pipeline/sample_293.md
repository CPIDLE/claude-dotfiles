## Sample 293

**Source**: `personal-rag_v2\PKB\workspace\test_08\timeline_detail.md` L345

```
[觸發] 12:48:30 Technician 按 Stick Start 重啟 Project
                                    │
                                    ▼
[正常] 12:48:34~35 Init → gripper_init（自檢：閉→開）
             ├─ CST 在 slot4（FoupLock 固定），不在夾爪中
             └─ gripper_init 結束在「開」= 正常起始狀態
                                    │
                                    ▼
[EtherCAT Direct] 正常操作開始 pick → 此次 pick 走 EtherCAT Direct 模式（DO 由 cyclic PDO 維持）
             ├─ pick 成功（CCTV 推定，DI0=T 未被 modbus 記錄）
             └─ DO 由 PDO 週期更新驅動（非 CMD61 硬體鎖存）
                                    │
                                    ▼
[⚠️ PDO Watchdog — 假說，未驗證] 12:48:42 Lidar Pause #1 → CMDE3,0 暫停 EtherCAT → PDO 停止更新
             ├─ End Module PDO watchdog 逾時（通常 <1s，遠小於 ~15s Pause）
             ├─ **DO 歸零 = 夾爪短暫鬆開**（CST 在無夾持力下靠重力偏移）
             └─ ~15s後 CMDE3,1 恢復 → PDO 重啟 → 夾爪重新夾回，但 CST 已偏移
                                    │
                                    ▼
[鬆動] 12:49:09 DI0=F — CST 偏移到 sensor 失去接觸（夾回但位置不正）
                                    │
                                    ▼
[掉落] ~12:49:1x CST 靠重力從靜止的手臂滑落（CCTV 確認手臂沒動）
                                    │
                                    ▼
[人員反應] 12:49:18 TB1000 — 人員踢 bumper（emergencystop, Driver Board）
             └─ 12:49:19 TS9907 手臂急停
```

---

