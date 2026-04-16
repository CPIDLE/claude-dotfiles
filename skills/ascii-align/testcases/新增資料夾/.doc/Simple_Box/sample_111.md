## Sample 111

**Source**: `D455_LidarScan\FLOW.md` L7

```
Lines    Module
──────   ──────────────────────────────
1-8      Module docstring
10-19    Imports (standard library)
21-23    Imports (pyrealsense2, numpy, opencv)
25-37    Optional imports (rclpy, rerun, onnxruntime)
40-99    LIDAR_MODELS dict (5 presets)
101      D455_HFOV_DEG = 86.0
104-112  LaserScan dataclass
116-151  UDPOutput class
153-186  ROS2Output class
188-238  GravityEstimator class
240-380  NeuralStereoEstimator class (CREStereo ONNX)
382-413  D455LidarScanner.__init__() + start()
415-520  D455LidarScanner.start() (pipeline, sensor config, neural stereo, filters)
522-527  D455LidarScanner._build_pixel_grid()
529-532  D455LidarScanner.stop()
534-588  D455LidarScanner._get_frames()
589-608  D455LidarScanner._depth_to_points()
610-624  D455LidarScanner._depth_to_points_from_array()
626-651  D455LidarScanner._estimate_camera_height()
653-671  D455LidarScanner._fill_depth_gaps()
673-757  D455LidarScanner._points_to_scan()
759-814  D455LidarScanner._points_to_ground_lines()
816-900  D455LidarScanner.process_frame()
902-972  draw_scan() -- OpenCV 2D visualization
974-1069 RerunLogger class
1072-1341 main() -- CLI args + main loop
```

