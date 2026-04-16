## Sample 654

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L631

```
depth_to_virtual_lidar/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── virtual_lidar.launch.py
├── include/
│   └── depth_to_virtual_lidar/
│       ├── virtual_lidar_node.hpp
│       ├── cpu_processor.hpp        # CPU 路徑
│       ├── cuda_processor.hpp       # CUDA 路徑介面
│       └── lut_generator.hpp        # LUT 預計算（CPU/CUDA 共用邏輯）
├── src/
│   ├── virtual_lidar_node.cpp       # ROS 2 lifecycle 節點主體
│   ├── cpu_processor.cpp            # CPU 單次遍歷實作
│   ├── lut_generator.cpp            # LUT 預計算
│   └── kernels/                     # CUDA kernels（可選編譯）
│       ├── depth_to_scan.cu         # 核心 kernel
│       └── reset_scan.cu            # scan bin 重置
└── config/
    └── default_params.yaml
```

