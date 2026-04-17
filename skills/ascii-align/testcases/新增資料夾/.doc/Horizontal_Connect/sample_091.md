## Sample 091

**Source**: `D435i_LidarScan\FLOW.md` L454

```
Input: points[N, 3], rotation R[3, 3], LiDAR model specs

Step A: Load scan parameters from LiDAR model
    Model selected  → use model's FOV, resolution, range, n_steps
    Custom mode     → use CLI args, D435i native FOV (~87°)

Step B: Transform to ground-aligned frame
    aligned = R @ points.T  →  [N, 3]  (Y=up, XZ=ground)

Step C: Height filtering
    heights = aligned[:, 1]  (Y axis = height)
    keep where: height_min ≤ height ≤ height_max

    Example: 0.1m ≤ height ≤ 1.8m
    ┌─────────────┐ 1.8m  ← max
    │ /////////// │
    │ // KEEP /// │  ← obstacles in this height band
    │ /////////// │
    ├─────────────┤ 0.1m  ← min
    │  (ground)   │ 0.0m
    └─────────────┘

Step D: Project to 2D ground plane (XZ)
    x = filtered[:, 0]   (X axis)
    z = filtered[:, 2]   (Z axis = forward)

Step E: Convert to polar coordinates
    range = sqrt(x² + z²)
    angle = atan2(x, z)     ← angle from forward (Z), positive = right

Step F: Range filtering (using model specs)
    keep where: range_min ≤ range ≤ range_max

Step G: Discretize into angular bins (using model specs)
    Example (Hokuyo UST-10LX):
        angle_min = -135°, angle_max = +135°  (270° FOV)
        angle_increment = 0.25°
        n_bins = 1081

    bin_index = (angle - angle_min) / angle_increment
    For each bin: keep MINIMUM range (closest obstacle)

    D435i coverage: ~87° centered → fills ~348 of 1081 bins
    Remaining bins = inf (no data)

Output: LaserScan
    ├── angle_min, angle_max     (from model FOV)
    ├── angle_increment          (from model resolution)
    ├── range_min, range_max     (from model specs)
    ├── ranges[n_steps]          (meters, inf = no obstacle)
    └── model_name               (e.g., "Hokuyo UST-10LX")
```

---

