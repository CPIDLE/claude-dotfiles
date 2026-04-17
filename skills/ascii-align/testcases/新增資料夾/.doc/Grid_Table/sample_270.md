## Sample 270

**Source**: `personal-rag_v2\PKB\workspace\test_02\01_mcs_lite_study.md` L99

```
┌─────────────────────────────────────────────────────────┐
│                    客戶 MES / MCS                        │
│              (WEB API / MSMQ / E82/E88)                  │
└──────────────────────┬──────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │    ACS Gateway        │  (Windows 10 Pro)
           │  - MSMQ Bridge        │
           │  - Web UI             │
           └───────────┬───────────┘
                       │ (ACS 專用網域)
           ┌───────────┴───────────┐
           │    TSC + MCS lite     │  (Linux RedHat / Windows Server)
           │  ┌─────────────────┐  │
           │  │    MCS lite     │  │  - 物料管理 / 搬運指令
           │  │  (BYPASS/RTD)   │  │  - SECS E82/E82+/E88
           │  └────────┬────────┘  │
           │           │           │
           │  ┌────────┼────────┐  │
           │  │        │        │  │
           │ AGVC   E-RACKC  STKC │  - 派車交管 / 貨架管理 / 倉儲管理
           │  │        │        │  │
           └──┼────────┼────────┼──┘
              │        │        │
     ┌────────┴─┐  ┌───┴───┐  ┌┴────────┐
     │ AMR 車輛  │  │E-Rack │  │ Stocker │
     │(Prop.    │  │(TCP/IP│  │(E84/    │
     │ Protocol)│  │ JSON) │  │ SECS)   │
     └──────────┘  └───────┘  └─────────┘
         │
    ┌────┴────┐
    │EQ Load  │  (E84 / Virtual E84)
    │Port     │
    └─────────┘
```

---

