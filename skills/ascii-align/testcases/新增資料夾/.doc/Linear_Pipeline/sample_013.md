## Sample 013

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L222

```
gyro/
├── launch/             # Launch 檔案
│   ├── robots/         # 各車型專屬 launch
│   └── mir/            # MiR 相容 launch
├── scripts/            # Python 腳本（ROS 節點）
├── src/gyro/           # C++ 原始碼
│   └── arduino/        # Arduino 韌體
├── config/             # 車型設定（50+ 車型）
│   ├── ase-AMR-A-04L4/ # 日月光
│   ├── spil-AMR-A-04L4-SG/ # 矽品
│   ├── nxcp-AMR-A-04L4-NC/ # 日月光中壢
│   ├── pti-AMR-A-04L4/ # PTI
│   └── ...             # 更多客戶車型
├── map/                # 地圖（40+ 場域）
│   ├── ASE_0708/       # 日月光
│   ├── SPIL_1F_CP/     # 矽品
│   ├── UMC/            # 聯電
│   └── ...
├── msg/                # 自訂 ROS 訊息
├── cfg/                # dynamic_reconfigure 定義
├── urdf/               # 機器人 URDF 模型
├── meshes/             # 3D 模型
├── sound/              # 音效檔
├── bag/                # ROS bag 錄製資料
├── install/            # 安裝腳本
├── include/gyro/       # C++ header
└── stage/              # Stage simulator 設定
```

---

