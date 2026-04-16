## Sample 149

**Source**: `HaloScan_v0\docs\10_Mid360_POE配線方案.md` L75

```
AMR 24V 電源軌 --> Moxa EDS-G205A-4PoE（120W POE budget）
  ├── Port 1 --> 網路線 --> POE Splitter --> 12V DC + RJ45 --> Mid-360 FL
  ├── Port 2 --> 網路線 --> POE Splitter --> 12V DC + RJ45 --> Mid-360 FR
  ├── Port 3 --> 網路線 --> POE Splitter --> 12V DC + RJ45 --> Mid-360 RL
  ├── Port 4 --> 網路線 --> POE Splitter --> 12V DC + RJ45 --> Mid-360 RR
  └── Port 5 --> RPi 5（需另外 5V/5A 供電，或用 POE HAT）
```

