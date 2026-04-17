## Sample 150

**Source**: `HaloScan_v0\README.md` L23

```
HaloScan_v0/
├── CLAUDE.md                    # 專案指引（架構、約束、感測器規格）
├── README.md
├── docs/                        # 技術文件（會議計畫、感測器提案、配線方案）
├── refs/                        # 參考資料（規格書、通訊協定、設定指南）
└── cameras/                     # 攝影機侵入偵測模組
    ├── CAMERAS.md               # 7 台攝影機清單 + 連線資訊
    ├── cameras_inventory.json   # 結構化設備資料
    ├── captures/                # 攝影機截圖
    ├── calibrate.py             # 多攝影機共同點校正 + BEV 拼接
    ├── segment.py               # YOLOv8x-seg 語意分割
    ├── intrusion.py             # Zone 比對 + 嚴重度判定
    ├── realtime.py              # 7 路 RTSP 即時偵測（grid 模式）
    ├── path_editor.py           # 走道標註 + 偵測 + BEV 並排
    ├── floor_intrusion.py       # 地板遮蔽偵測（毫秒級，不需 YOLO）
    ├── zone_editor.py           # Zone Map 互動編輯器
    ├── site_calibration.py      # 現場校正（棋盤格→內參→位姿→統一 BEV）
    └── checkerboard_A2.png      # A2 棋盤格（列印用）
```

---

