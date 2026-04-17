## Sample 092

**Source**: `D435i_LidarScan\FLOW.md` L510

```
Input: points[N, 3], rotation R[3, 3]
Config: ground_angle (a), ground_angle_delta (d), ground_angle_tol (tol)

Step A: Transform to ground-aligned frame
    aligned = R @ points.T  →  [N, 3]  (Y=up, XZ=ground)
    x, y, z = aligned columns

Step B: Compute vertical angle below horizontal for each point
    h_dist = sqrt(x² + z²)             ← horizontal distance
    vert_angle = atan2(-y, h_dist)      ← angle below horizontal (deg)
                                           positive = downward

    Side view (ground-aligned frame):
        Camera ──── horizontal (0°) ──────
          ╲  ╲
     line0 ╲  ╲ line1
     (a°)   ╲  ╲ (a+d°)
              ╲  ╲
    ───────────P0─P1────── ground
               │   │
               d0  d1   ground hit distances: d = h / tan(angle)

Step C: Select points for each line (2 lines)
    Line 0: |vert_angle - a| ≤ tol        (e.g., 30° ± 0.3°)
    Line 1: |vert_angle - (a+d)| ≤ tol    (e.g., 32° ± 0.3°)

Step D: For each line, bin into horizontal angular bins
    HFOV = D435i native ~87°
    horiz_angle = atan2(x, z)
    slant_range = sqrt(x² + y² + z²)     ← 3D distance (not horizontal!)

    bin_index = (horiz_angle - angle_min) / angle_increment
    For each bin: keep MINIMUM range (closest)

Output: (LaserScan_line0, LaserScan_line1)
    Each with:
    ├── angle_min = -43.5°, angle_max = +43.5°  (D435i HFOV)
    ├── angle_increment = 0.25° (default)
    ├── ranges[n_bins]           (slant distance, meters)
    └── model_name               (e.g., "ground_line0_30.0deg")
```

---

