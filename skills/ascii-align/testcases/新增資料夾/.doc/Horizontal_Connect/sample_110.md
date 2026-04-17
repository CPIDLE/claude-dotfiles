## Sample 110

**Source**: `D435i_LidarScan_v3a\README.md` L53

```
src/
├── camera.py          # D435i 相機控制（RGB + depth + IMU）
├── calibration.py     # RANSAC 地面平面校正
├── bev/               # BEV 投影引擎
│   ├── config.py      # 設定參數
│   ├── lift.py        # 像素→3D 世界座標
│   ├── splat.py       # 3D→BEV 網格（Z-buffer）
│   ├── renderer.py    # 視覺化渲染
│   └── pipeline.py    # 整合 pipeline
└── depth/             # 深度估測模組
    ├── da_inference.py    # Depth Anything v2 推論
    ├── da_finetune.py     # Fine-tune 訓練
    └── depth_scaler.py    # 深度校準

tools/
├── live_occupancy.py  # 即時佔用網格預覽
├── live_bev.py        # 即時 BEV 預覽
├── collect_data.py    # 資料收集工具
├── validate_bev.py    # BEV 離線驗證
└── train_da.py        # DA 訓練腳本
```

---

