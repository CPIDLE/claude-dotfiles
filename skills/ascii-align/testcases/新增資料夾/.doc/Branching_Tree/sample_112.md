## Sample 112

**Source**: `D455_LidarScan\FLOW.md` L40

```
main()
 │
 ├── Parse CLI args (argparse)
 ├── Init network outputs (UDP/ROS2)
 ├── Init RerunLogger (optional)
 ├── Create D455LidarScanner(args)
 │    ├── pipeline = rs.pipeline()
 │    ├── GravityEstimator(alpha=0.98)
 │    └── Post-processing filters (decimation, spatial, temporal, threshold)
 │
 ├── scanner.start()
 │    ├── config.enable_stream(depth, 1280x720, z16, 30fps)
 │    ├── config.enable_stream(color, 1280x720, rgb8, 30fps)
 │    ├── (if --neural-stereo) config.enable_stream(infrared 1 & 2, y8)
 │    ├── config.enable_stream(accel)
 │    ├── config.enable_stream(gyro)
 │    ├── pipeline.start(config)
 │    ├── Configure sensor (emitter, preset)
 │    ├── (if --neural-stereo) force emitter OFF
 │    ├── (if --neural-stereo) read IR intrinsics + stereo baseline
 │    ├── (if --neural-stereo) init NeuralStereoEstimator (ONNX background thread)
 │    ├── Configure filters (decimation, spatial, temporal, threshold)
 │    ├── Get depth intrinsics (fx, fy, ppx, ppy)
 │    └── Precompute pixel grid (_u_grid, _v_grid)
 │
 └── Main loop:
      │
      ├── scanner.process_frame()
      │    │
      │    ├── _get_frames()
      │    │    ├── pipeline.wait_for_frames()
      │    │    ├── get_depth_frame()
      │    │    ├── Apply filters: decimation → threshold → spatial → temporal
      │    │    ├── Update intrinsics if decimation changed resolution
      │    │    ├── Extract color frame → _last_color_image
      │    │    ├── (if neural stereo) Extract IR left/right → _last_ir_left/right
      │    │    └── Extract IMU: accel_data, gyro_data
      │    │
      │    ├── gravity_estimator.update(accel)
      │    │    └── Low-pass filter: g = α*g + (1-α)*accel
      │    │
      │    ├── gravity_estimator.get_rotation_matrix()
      │    │    ├── Normalize gravity → Y_up axis
      │    │    ├── Project camera forward → Z_forward axis
      │    │    ├── Cross product → X_right axis
      │    │    └── Return R = [X; Y; Z] rotation matrix
      │    │
      │    ├── _depth_to_points(depth_frame) → real_points
      │    │    ├── depth_image * depth_scale → z (meters)
      │    │    ├── x = (u - ppx) * z / fx  (vectorized)
      │    │    ├── y = (v - ppy) * z / fy  (vectorized)
      │    │    └── Return Nx3 points [x, y, z] in camera frame
      │    │
      │    ├── (if auto height) _estimate_camera_height(real_points)
      │    │    ├── aligned = R @ points.T → ground-aligned frame
      │    │    ├── Select nearby points (0.5m < h_dist < 4.0m)
      │    │    ├── ground_y = percentile(Y, 15th)
      │    │    └── EMA smooth: h = 0.05*new + 0.95*old
      │    │
      │    ├── (if --neural-stereo) Depth Fusion:
      │    │    ├── push IR pair to NeuralStereoEstimator (non-blocking)
      │    │    ├── get_latest_depth() → neural_depth, neural_ms
      │    │    ├── if neural_depth available:
      │    │    │    ├── stereo_depth = depth_frame → float32 meters
      │    │    │    ├── fused = stereo_depth.copy()
      │    │    │    ├── gap = ~stereo_valid
      │    │    │    ├── fill_neural = gap & neural_valid
      │    │    │    ├── fused[fill_neural] = neural_depth[fill_neural]
      │    │    │    ├── (if not --no-fill-depth) _fill_depth_gaps(fused)
      │    │    │    │    ├── Diamond dilation [3,5,7,11,15,23]
      │    │    │    │    └── Bilateral filter (preserve edges)
      │    │    │    └── points = _depth_to_points_from_array(fused)
      │    │    └── else: points = real_points (first few frames)
      │    │
      │    ├── _points_to_scan(points, rotation) → LaserScan
      │    │    ├── aligned = R @ points.T → [X_right, Y_up, Z_forward]
      │    │    ├── Height filter: height_min ≤ (camera_height + Y) ≤ height_max
      │    │    ├── Polar: angles = atan2(X, Z), ranges = √(X²+Z²)
      │    │    ├── Range filter: range_min ≤ r ≤ range_max
      │    │    ├── Bin: indices = (angle - angle_min) / angle_increment
      │    │    └── np.minimum.at(scan_ranges, indices, ranges)
      │    │
      │    └── (if --ground-scan) _points_to_ground_lines(points, rotation)
      │         ├── aligned = R @ points.T
      │         ├── vert_angles = degrees(atan2(-Y, h_dist))
      │         ├── For each line (α, α+Δ):
      │         │    ├── mask = |vert_angle - target| ≤ tolerance
      │         │    ├── horiz_angles = atan2(X, Z)
      │         │    ├── slant_ranges = √(X² + Y² + Z²)
      │         │    └── np.minimum.at(scan_ranges, indices, slant_ranges)
      │         └── Return (LaserScan_line0, LaserScan_line1)
      │
      ├── net_output.send(scan)              # UDP/ROS2
      ├── ground_outputs[0/1].send(lines)    # if ground scanner
      ├── rerun_logger.log_frame(...)        # if --rerun
      │
      ├── (if --no-viz) print status line
      └── (else) draw_scan() → cv2.imshow()
           ├── Range circles (1m, 2m, ...)
           ├── LiDAR model FOV lines (dark blue)
           ├── D455 FOV wedge (yellow)
           ├── Camera position (yellow dot)
           └── Scan points (green dots)
```

---
