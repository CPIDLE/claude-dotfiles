## Sample 389

**Source**: `Reporter_v1\WORKSPACE\a01\16_D435i_LidarScan_v2.md` L45

```
├── src/
│   ├── camera.py              # D435i 相機（含 depth-->color alignment）
│   ├── stage1.py ~ stage6.py  # 6-Stage Pipeline
│   ├── scene_segmentor.py     # SegFormer-B0 + FP16 + 牆面分割
│   ├── yolo_detector.py       # YOLO 物體偵測
│   ├── nlspn/                 # NLSPN 深度補全模型
│   │   ├── nlspn_model.py
│   │   ├── propagation.py
│   │   └── common.py
│   ├── nlspn_completer.py
│   ├── cuda_buffer.py         # GPU 加速
│   ├── preprocessing.py       # 資料預處理
│   ├── ransac_completion.py   # RANSAC 平面
│   ├── output.py              # 輸出（含 label --> voxel downsample）
│   ├── rerun_logger.py        # Rerun 視覺化
│   └── gate.py                # Gate 控制
├── config/gate_config.yaml    # 延遲閾值 + 相機外參
├── CHANGELOG.md
├── CLAUDE.md
└── requirements.txt
```

