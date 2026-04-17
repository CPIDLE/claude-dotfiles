## Sample 219

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\結案報告_AMR2_CPU分析.md` L69

```
Host OS (Ubuntu 20.04)
├── Chrome kiosk（觸控面板 UI，連 agvweb）
├── update-manager、gnome-shell、rqt 等桌面程式
└── Docker 容器 ×5
    ├── gyro-docker-debugging  ← 主要 ROS 運行環境（115 ROS 節點）
    ├── ethercat_control       ← EtherCAT 馬達控制
    ├── agvweb                 ← Web UI 前端
    ├── mqtt                   ← MQTT Broker
    └── canopen_control        ← CANopen 通訊
```

---

