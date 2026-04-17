## Sample 099

**Source**: `D435i_LidarScan\README.md` L307

```
Side view (camera tilted ~10-20° down):

           Camera ──── horizontal (0°) ────────────────
             ╲  ╲
        line0 ╲  ╲ line1
     (α=30°)   ╲  ╲ (α+Δ=32°)
                 ╲  ╲
    ──────────────P0──P1────────────────── flat ground
                 │    │
                 d0   d1  ← ground hit distances

Geometry:
    d = camera_height / tan(α)
    P0 is farther from camera than P1 (shallower angle = farther)
    Spacing between P0 and P1 on ground = d0 - d1
```

---

