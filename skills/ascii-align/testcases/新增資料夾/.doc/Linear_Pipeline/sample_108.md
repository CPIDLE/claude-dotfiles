## Sample 108

**Source**: `D435I_LidarScan_v1\D435i_DepthCompletion_CLAUDE.md` L86

```
d435i_depth_completion/
├── README.md
├── requirements.txt
├── config/
│   ├── camera_config.yaml        # D435i 串流參數設定
│   └── pipeline_config.yaml      # 各 stage 開關與參數
├── src/
│   ├── camera/
│   │   ├── realsense_node.py     # D435i 擷取，IR emitter OFF
│   │   └── postprocess.py        # Stage 1: librealsense filters
│   ├── completion/
│   │   ├── base_completer.py     # 抽象介面
│   │   ├── sparsedc_completer.py # Stage 2: SparseDC wrapper
│   │   ├── nlspn_completer.py    # Stage 2: NLSPN wrapper（備選）
│   │   └── mde_fallback.py       # Stage 3: Depth Anything V2
│   ├── fusion/
│   │   └── depth_fusion.py       # Stage 2+3 結果融合
│   ├── pipeline.py               # 主 Pipeline 整合
│   └── visualizer.py             # 開發用視覺化工具
├── tools/
│   ├── record_bag.py             # 錄製測試資料（rosbag 或 .bag）
│   ├── evaluate.py               # 離線評估（RMSE / MAE）
│   └── export_trt.py             # TensorRT 轉換腳本（Jetson 部署用）
├── models/                       # 預訓練權重存放（.gitignore）
├── data/                         # 測試資料集（.gitignore）
└── tests/
    ├── test_camera.py
    ├── test_completion.py
    └── test_pipeline_fps.py      # FPS 基準測試
```

---

