## Sample 093

**Source**: `D435i_LidarScan\FLOW.md` L555

```
This system outputs raw scan data. Detection logic runs on AGV side.

─── How two lines reveal ground anomalies ───

Flat ground:                      Pit (hole):
    line0: ──────────────             line0: ──────╲    ╱──────
    line1: ──────────────             line1: ────────╲╱────────
    drange ~= constant                 line0 range jumps (sees into pit)
                                      drange >> baseline

Bump (raised obstacle):           Slope / ramp:
    line0: ─────╱╲───────            line0: ──────────╲╲╲╲
    line1: ───╱╲─────────            line1: ──────────╲╲╲╲
    line1 hits bump first             both shift together
    drange << baseline                drange ~= constant (not anomaly)

─── FOV constraint ───

D435i VFOV ~= 58° (+-29° from optical axis)
Camera tilt T° down --> max ground_angle reachable = T + 29°

    tilt  0° --> ground_angle max = 29°
    tilt 10° --> ground_angle max = 39°    <-- recommended
    tilt 20° --> ground_angle max = 49°    <-- horizontal LiDAR FOV narrows

For ground_angle = 30°, d = 2°:  need tilt >= 3° (easy)
For ground_angle = 45°, d = 2°:  need tilt >= 18° (significant)
```

