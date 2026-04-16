## Sample 247

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L33

```
+----------------------------+       +-----------------------------------------+
|  外接 HID 裝置              |       |  統一 UI (Electron / Web)                |
|  ├─ 雙類比搖桿              |       |  ├─ 教點面板 (Teach Panel Widget)        |
|  ├─ 3Dconnexion SpaceMouse  |       |  ├─ 點位瀏覽器 (Point Browser)           |
|  ├─ 腳踏開關 (deadman)      |       |  ├─ 位姿即時顯示 (Live Pose Readout)     |
|  └─ 自製按鍵面板 (HID-bt)   |       |  ├─ HID 對應設定 UI                      |
+-------------+--------------+       |  └─ GYRO YAML 編輯器 (Source of Truth)   |
              |                      +--------------------+--------------------+
              | USB / Bluetooth HID                       |
              v                                            |
+-------------+-----------------------+                    |
|  hid_input/ (Python, 跨平台)         |                    |
|  ├─ pygame / inputs / evdev 後端    |                    |
|  ├─ HID 事件 --> 抽象 intent 事件     |---------------------+
|  │   (JogIntent / SaveIntent /      |   intent events
|  │    FreeDriveIntent / ...)        |
|  └─ profile 檔 (YAML) 定義按鍵對應  |
+-------------+-----------------------+
              |
              | 統一 UI 內部 event bus
              v
+-------------+-----------------------+
|  tmflow_domain_client/ (Python)      |
|  ├─ 自動從 .proto 產生 stub          |
|  ├─ Connection Manager (KeepAlive)   |
|  ├─ TeachSession context manager     |
|  │    (OpenProject / EnterJogMode /  |
|  │     ExitJogMode / CloseProject)   |
|  └─ High-level helpers (Jog / Save)  |
+--------------------+-----------------+
                     |
                     | gRPC (TmDomainService.proto)
                     v
+--------------------+-----------------+
|  TMflow Controller (Manual Mode)     |
|  DomainAPI + Jog RPCs (S.4 待 TM 實作)|
+--------------------------------------+
```

