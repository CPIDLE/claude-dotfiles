## Sample 094

**Source**: `D435i_LidarScan\FLOW.md` L591

```
Binary protocol over UDP (default port 7777):

┌───────────────────────────────────────────┐
│ Header (40 bytes, little-endian)          │
├────────────┬──────────────────────────────┤
│ magic      │ "LS2D" (4 bytes)             │
│ timestamp  │ float64, Unix time (8 bytes) │
│ n_steps    │ uint32 (4 bytes)             │
│ angle_min  │ float32, radians (4 bytes)   │
│ angle_max  │ float32, radians (4 bytes)   │
│ angle_inc  │ float32, radians (4 bytes)   │
│ range_min  │ float32, meters (4 bytes)    │
│ range_max  │ float32, meters (4 bytes)    │
├────────────┴──────────────────────────────┤
│ Data                                      │
├───────────────────────────────────────────┤
│ ranges     │ float32[] (n_steps x  4 bytes)│
│            │ meters, range_max+1 = no data│
└───────────────────────────────────────────┘

Flow: LaserScan --> pack header --> replace inf --> sendto(broadcast)
```

