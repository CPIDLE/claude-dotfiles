## Sample 456

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L57

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  v 
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  v 
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       v 
  ├--> AGVC ───> AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├--> eRackC ──> E-Rack（TCP/IP）
  ├--> StockerC --> Stocker（Socket IO）
  └--> Sorter
```

