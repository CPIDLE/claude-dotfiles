## Sample 529

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書_elk.md` L26

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

