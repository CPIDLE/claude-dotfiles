## Sample 659

**Source**: `WebCamToLidarScan\README.md` L75

```
WebCamToLidarScan/
├── README.md
├── docs/
│   ├── REQUIREMENTS.md                    # 完整技術規格書（含 CUDA 設計與驗證報告）
│   └── COMPARISON_TESLA_US20250282344.md  # Tesla SDF 專利比較分析
├── prototype/                             # Python 原型驗證
│   ├── depth_to_scan.py                   # DepthToScan + ScanPipeline
│   ├── depth_source.py                    # ONNX 深度推論 (Metric/Relative)
│   ├── temporal_filter.py                 # EMA (連續自適應) / Median 濾波器
│   ├── run_demo.py                        # Webcam 即時 demo + overlay
│   ├── diagnose_webcam.py                 # 深度映射診斷工具
│   ├── test_webcam_scan.py                # 非互動 webcam 測試
│   └── requirements.txt
└── ros2_ws/                               # ROS 2 C++ 正式實作
    └── src/
        └── depth_to_virtual_lidar/
            ├── CMakeLists.txt
            ├── package.xml
            ├── launch/
            ├── include/
            ├── src/
            │   ├── virtual_lidar_node.cpp
            │   ├── cpu_processor.cpp
            │   ├── lut_generator.cpp
            │   ├── temporal_filter.cpp    # 時間融合
            │   ├── egomotion_fuser.cpp    # Ego-motion 補償
            │   └── kernels/               # CUDA (可選)
            └── config/
```

