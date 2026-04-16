## Sample 120

**Source**: `D455_LidarScan\README_temp.md` L305

```
Side view (camera tilted ~10-20° down):

           Camera ──── horizontal (0°) ────────────────
             ╲  ╲
        line0 ╲  ╲ line1
     (a =30°)   ╲  ╲ (a +D =32°)
                 ╲  ╲
    ──────────────P0──P1────────────────── flat ground
                 │    │
                 d0   d1  <-- ground hit distances

Geometry:
    d = camera_height / tan(a )
    P0 is farther from camera than P1 (shallower angle = farther)
    Spacing between P0 and P1 on ground = d0 - d1
```

