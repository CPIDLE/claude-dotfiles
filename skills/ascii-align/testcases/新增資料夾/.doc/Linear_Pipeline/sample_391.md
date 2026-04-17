## Sample 391

**Source**: `Reporter_v1\WORKSPACE\a01\17_WebCamToLidarScan.md` L55

```
├── prototype/
│   ├── run_demo.py                # CLI 入口（synthetic/image/webcam/video）
│   ├── depth_to_scan.py           # 核心：LUT 轉換 + RANSAC 地面校正 + ScanPipeline
│   ├── depth_source.py            # 深度來源（Synthetic/ONNX/Webcam/Image/Video/D435i）
│   ├── temporal_filter.py         # EMA 時序濾波（adaptive/asymmetric/IMU-aware）
│   ├── egomotion_fuser.py         # 多幀拼接（2D rigid transform）
│   ├── d435i_source.py            # D435i 統一 Pipeline（RGB+Depth+IMU 單管線）
│   ├── d435i_imu_source.py        # D435i IMU 源（舊版 3-pipeline，已被統一版取代）
│   ├── imu_tilt_estimator.py      # IMU roll/pitch/yaw 估計
│   ├── d435i_depth_validator.py   # D435i 深度驗證（玻璃/鏡面/金屬網偵測）+ 校正器
│   ├── requirements.txt
│   ├── tests/
│   │   ├── test_phase1_integration.py   # Phase 1 硬體整合測試
│   │   ├── test_webcam_scan.py          # Webcam 掃描測試
│   │   ├── test_d435i_rgb.py            # D435i RGB 測試
│   │   ├── diagnose_webcam.py           # Webcam 診斷
│   │   └── manual_test_imu_effect.py    # IMU 效果手動測試
│   └── models/onnx/                     # ONNX 模型（gitignored）
├── docs/
│   ├── TECHNICAL.md                     # 技術文件（690 行）
│   ├── REQUIREMENTS.md                  # 需求規格（含 C++ 偽碼 + CUDA kernel 設計）
│   └── COMPARISON_TESLA_US20250282344.md # Tesla 專利比較分析
└── README.md
```

---

