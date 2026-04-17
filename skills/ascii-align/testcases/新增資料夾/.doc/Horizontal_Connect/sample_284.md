## Sample 284

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L74

```
┌──────────────────────────────────────┐
│ TM 手臂主機                          │
│                                       │
│ 安全回路（左側）                       │
│ ├─ STO-1, STO-2    → 安全扭力關閉     │
│ ├─ SAFE1~SAFE4     → 安全功能         │
│ ├─ SI1-1, SI1-2    → Safety Input    │
│ ├─ DI_9, DI_10, DI_12, DI_13        │
│ └─ Power +24V, DI_COM               │
│                                       │
│ I/O 面板（右側） → 100PIN 連接器       │
│ ├─ DO/MFP, DO/MFF                    │
│ ├─ ST.D/DI-1                         │
│ ├─ R1~R5 (CB00, RB02, 1X_17, etc.) │
│ ├─ B1~B4 (SB00, SB01, 1X_19, CK11) │
│ ├─ SAFE-1~SAFE-5, SAFE-Y            │
│ ├─ E/ESTOP                           │
│ └─ RT/EDIM-1                         │
│                                       │
│ End Module (Multi-IO, slot 7)        │
│ ├─ EtherCAT 內部通訊                  │
│ └─ → Tool Port 8-pin + 5-pin        │
└──────────────────────────────────────┘
```

---

