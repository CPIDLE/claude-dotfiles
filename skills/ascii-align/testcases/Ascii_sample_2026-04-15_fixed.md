# ASCII Box-Drawing Samples

Auto-collected from `E:\github` on 2026-04-15.
Total: **659** code blocks from **322** files.

---

## Sample 001

**Source**: `ai-sdk-fix\AGENTS.md` L34

```
ai ─────────────────┬──▶ @ai-sdk/provider-utils ──▶ @ai-sdk/provider
                    │
@ai-sdk/<provider> ─┴──▶ @ai-sdk/provider-utils ──▶ @ai-sdk/provider
```

---

## Sample 002

**Source**: `ai-sdk-fix\architecture\stream-text-loop-control.md` L60

````
┌────────────────────────────────────────────────────────────┐
│           FUNNEL IN: N STEP STREAMS                        │
│          (sequential, not parallel)                        │
└────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐            ┌──────────────┐
│   Step 0     │  │   Step 1     │            │   Step N     │
│   model.do   │  │   model.do   │            │   model.do   │
│   Stream()   │  │   Stream()   │    ···     │   Stream()   │
└──────┬───────┘  └──────┬───────┘            └──────┬───────┘
       │                 │                           │
 tool callbacks    tool callbacks              tool callbacks
       │                 │                           │
 tool execution    tool execution              tool execution
       │                 │                           │
 step metadata     step metadata               step metadata
 + start/finish    + start/finish              + start/finish
       │                 │                           │
       ▼                 ▼                           ▼
┌────────────────────────────────────────────────────────────┐
│        addStream()    addStream()         addStream()      │
│                                                            │
│                   STITCHABLE STREAM                        │
│     (sequential queue — consumes one at a time,           │
│      next step added on recursion from flush)              │
└─────────────────────────┬──────────────────────────────────┘
                          │
══════════════════════════╪═══════════════════════════════════
                          │
             ┌────────────┴────────────────────────┐
             │         MIDDLE PIPELINE             │
             │    (single linear transform chain)  │
             └────────────┬────────────────────────┘
                          │
                          ▼
                  resilient stream
             (abort handling + start event)
                          │
                          ▼
                      stop gate
                 (stopStream() support)
                          │
                          ▼
                   user transforms
               (experimental_transform[])
                          │
                          ▼
                   output transform
               (enrich w/ partialOutput)
                          │
                          ▼
                   event processor
                 (onChunk, onStepFinish,
                  accumulate content,
                 resolve delayed promises)
                          │
══════════════════════════╪═══════════════════════════════════
                          │
        ┌─────────────────┴─────────────────────┐
        │      FUNNEL OUT: ON-DEMAND .tee()     │
        │                                       │
        │             BASE STREAM               │
        │    (each .tee() splits into two:      │
        │     one for consumer, one remains     │
        │     as baseStream for next tee)       │
        │                                       │
        │   each can be called multiple times   │
        └──┬─────┬──────┬────┬──────┬────┬──────┘
           │     │      │    │      │    │
           ▼     ▼      ▼    ▼      ▼    ▼
         text  full  partial elem   UI  consume
        Stream Stream Output Stream Msg  Stream
                      Stream       Stream
        (text  (all  (json (output (maps (drains
        deltas parts) parse) spec) to UI) stream,
        only)                             resolves
                                          promises)
````

---

## Sample 003

**Source**: `ai-sdk-fix\skills\add-provider-package\SKILL.md` L36

```
packages/<provider>/
├── src/
│   ├── index.ts                  # Main exports
│   ├── version.ts                # Package version
│   ├── <provider>-provider.ts    # Provider implementation
│   ├── <provider>-provider.test.ts
│   ├── <provider>-*-options.ts   # Model-specific options
│   └── <provider>-*-model.ts     # Model implementations (e.g., language, embedding, image)
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── tsup.config.ts
├── turbo.json
├── vitest.node.config.js
├── vitest.edge.config.js
└── README.md
```

---

## Sample 004

**Source**: `AMRCoolDown_v0\AMR_CPU_RAM_體檢報告.md` L435

```
syswork.launch (root)
├── alarm_warn_code_gathering.launch
│   ├── alarmcode_gathering
│   └── warncode_gathering
├── MapLocationservice.launch
│   └── maplocation_server
├── CameraLocationservice.launch
│   └── cameralocation_server
├── syschecker.launch
│   └── syschecker (10 Hz)
├── sysindicator.launch
│   └── sysindicator (10 Hz, 125KB)
├── logs_update.launch
│   └── logs_update
├── syncrobotstate.launch
│   └── syncrobotstate (10 Hz)
├── monitor.launch
│   ├── batt_monitor.launch → battery_monitor (1 Hz)
│   ├── relative_monitor.launch → move_relative_monitor
│   ├── modbus_monitor.launch → modbus_monitor (0.5 Hz) + tm_arm_status_check
│   ├── safety_monitor.launch → safety_monitor (0.5 Hz)
│   ├── carvel_monitor.launch → carvel_monitor (10 Hz)
│   ├── camera_monitor.launch → camera_monitor (0.1 Hz)
│   ├── dashcam_monitor.launch → dashcam_monitor (0.5 Hz)
│   ├── slot_monitor.launch → slot_monitor (20 Hz ⚠️)
│   ├── path_log.launch → path_log
│   ├── tag_log.launch → TagLog
│   ├── network_monitor.launch → network_monitor (5+ threads)
│   ├── wirelesscharger_monitor.launch → wirelesscharger_monitor
│   ├── get_imu_log.launch → get_imu_log
│   ├── rosparam_monitor.launch → rosparam_monitor (60s)
│   ├── system_info_monitor.launch → system_info_monitor (0.5 Hz)
│   ├── cpu_monitor.launch → cpu_monitor_new (0.2 Hz + threads)
│   ├── disk_health_monitor.launch → disk_health_monitor (0.001 Hz ⚠️)
│   ├── automode_action_control.launch → automode_action_control
│   └── mqtt_bridge.launch → mqtt_bridge (1 Hz)
├── logclear.launch
│   └── log_clear (0.004 Hz)
├── loggathering.launch
│   └── loggathering (0.05 Hz, sync ⚠️)
└── griptmEMO.launch
    └── griptmEMO (10 Hz)

routemap.launch (separate)
├── armdooraction
├── processjson_server
├── routemap (10 Hz, 343KB ⚠️)
└── Tag_position_recovery (10 Hz)

ethercat SOEM_m.launch (container 2)
└── motor_control (C++, sudo, 50~1000 Hz)

canopen_control.launch (container 3)
├── canopen_controller (100 Hz ⚠️)
├── canopen_log (10 Hz)
└── canopen_motor_data_logger
```

---

## Sample 005

**Source**: `AMRCoolDown_v0\AMR_CPU優化計畫_v1.md` L23

```
Phase 1 ─ 緊急修復（團隊）     省 ~28%(sys) + 防止 +8.7% 復發
Phase 2 ─ 程式碼優化            省 ~4%(sys)
Phase 3 ─ 運維調整（免改碼）    省 ~4%(sys) + 回收 RAM
Phase 4 ─ 進階優化（可選）      省 ~3%(sys)
                                ─────────────
                          合計目標：82% → ~35-40%(sys)
```

---

## Sample 006

**Source**: `AMRCoolDown_v0\AMR_撞機事件根因分析.md` L168

```
                    正常狀態                         雪崩狀態
              ┌─────────────────┐            ┌─────────────────┐
              │  loggingCarWork │            │  loggingCarWork  │
              │    = 0.01s      │            │    = 0.01s       │
              │  (100Hz 排程)    │            │  (100Hz 排程)   │
              └────────┬────────┘            └────────┬─────────┘
                       ↓                              ↓
              ┌─────────────────┐            ┌──────────────────┐
              │  log_work() 執行 │            │  log_work() 執行  │
              │  耗時 5ms < 10ms │            │  耗時 15ms > 10ms │
              │  → sleep 5ms    │            │  → 跳過 sleep    │
              │  → 下一次排程    │            │  → 立即排下一次 │
              └─────────────────┘            │  → 堆積 → 連續執行 │
                                             │  → CPU 100%       │
              CPU: 69%                       └──────────────────┘
                                             CPU: 95~100%
```

---

## Sample 007

**Source**: `AMRCoolDown_v0\AMR_撞機事件根因分析.md` L262

```
每日磁碟消耗估算：
├── 4 台相機錄影（streamfile.py）
│   └── 15 fps × 4 cam × 86400 sec × ~50KB/frame = ~250 GB/天（未壓縮）
│       （壓縮後估 ~5-25 GB/天，取決於 codec）
├── ROS log（output="screen" × 38 節點）
│   └── 估 ~500 MB ~ 2 GB/天
├── CSV 日誌（syswork 各 monitor）
│   └── 估 ~100~500 MB/天
└── 合計：數 GB ~ 數十 GB/天

Day 3: 磁碟接近滿 → write() 阻塞
       → 所有含 file I/O 的節點卡住
       → loggathering.py 的 os.system("sync") 阻塞 10+ 秒
       → 系統凍結 → 導航中斷
```

---

## Sample 008

**Source**: `AMRCoolDown_v0\AMR_撞機事件根因分析.md` L353

```
Hour 0 ─────────────────────────────────────────────────────
  系統啟動
  CPU: ~45% (全核)    RAM: ~2.0 GB    Disk: 60%
  log_update: 69% (單核)    log_work() 耗時: 5ms < 10ms ✓
  導航延遲: <50ms ✓

Hour 12 ────────────────────────────────────────────────────
  CSV 累積 ~200MB    ROS log 累積 ~500MB
  CPU: ~48%    RAM: ~2.5 GB    Disk: 65%
  log_work() 耗時: 7ms < 10ms ✓（I/O 稍慢）
  導航延遲: <50ms ✓

Hour 24 ────────────────────────────────────────────────────
  CSV 累積 ~500MB    ROS log 累積 ~1.5GB    錄影累積 ~10GB
  CPU: ~52%    RAM: ~3.2 GB    Disk: 72%
  log_work() 耗時: 9ms < 10ms ✓（接近臨界）
  無界 queue 開始微量堆積
  導航延遲: <60ms ✓

Hour 36 ────────────────────────────────────────────────────
  CSV 累積 ~800MB（寫入變慢）
  CPU: ~58%    RAM: ~4.0 GB    Disk: 78%
  log_work() 耗時: 11ms > 10ms ⚠️ 開始排隊
  log_update CPU: 69% → 75%
  導航延遲: ~80ms ⚠️

Hour 48 ────────────────────────────────────────────────────
  CSV > 1GB    磁碟 I/O 延遲上升
  CPU: ~68%    RAM: ~5.5 GB    Disk: 85%
  log_work() 耗時: 15ms >> 10ms ⚠️ 排隊加速
  log_update CPU: 85~90%
  部分 ping timeout → 執行緒累積
  導航延遲: ~150ms ⚠️

Hour 60 ─────────────── ⚡ 臨界點 ──────────────────────────
  RAM: ~7.0 GB（接近 7.7GB 上限）
  Disk: 92%（sync 開始阻塞數秒）
  CPU: ~85%（全核）

  ┌─ 觸發鏈 ──────────────────────────────────┐
  │ log_update scheduler 完全雪崩 → CPU 100%   │
  │ + RAM 接近 OOM → swap thrashing            │
  │ + sync 阻塞 → I/O 凍結                     │
  │ + 執行緒累積 → context switch 200K+/s      │
  │                                             │
  │ = move_base 被搶光 CPU                      │
  │ = amcl 定位更新延遲 > 500ms                 │
  │ = costmap 來不及更新障礙物                  │
  │ = 安全煞車計算超時                          │
  └─────────────────────────────────────────────┘
                       ↓
              ❌ 導航延遲 → 撞擊機台

Hour 60+ ───────────────────────────────────────────────────
  系統可能自行部分恢復（OOM killer 殺掉某些節點）
  但傷害已經造成
```

---

## Sample 009

**Source**: `AMRCoolDown_v0\AMR_撞機事件根因分析.md` L416

```
                    ┌──────────────┐
                    │  時間累積    │
                    │  （數天運行） │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ CSV 檔案增長  │ │ ROS queue    │ │ 錄影+ROS log │
    │ (log_update) │ │ 堆積         │ │ 持續寫入     │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
           ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ I/O 變慢     │ │ RAM 增長     │ │ 磁碟空間減少 │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
           ↓               │               ↓
    ┌──────────────┐       │        ┌──────────────┐
    │ scheduler    │       │        │ sync 阻塞    │
    │ 排隊雪崩     │       │        │ write 阻塞   │
    └──────┬───────┘       │        └──────┬───────┘
           │               │               │
           └───────────────┼───────────────┘
                           ↓
                    ┌──────────────┐
                    │  CPU 飆高    │
                    │  RAM 耗盡    │
                    │  I/O 凍結    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ move_base    │
                    │ amcl         │
                    │ 計算延遲     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ ❌ 導航失控  │
                    │ ❌ 撞擊機台  │
                    └──────────────┘
```

---

## Sample 010

**Source**: `AMRCoolDown_v0\AMR_整合分析報告_v2.md` L129

```
CPU%  Load
 82 ┤                                          ████████████
 78 ┤                                     █████
 74 ┤
 70 ┤
 66 ┤
 62 ┤
 58 ┤
 54 ┤              ████████████████████████
 50 ┤         █████
 46 ┤    █████
 42 ┤████
     3/17  18   19   20   21   22   23   24   25   26   27   28
                                          ↑
                                       轉折點
```

---

## Sample 011

**Source**: `AMRCoolDown_v0\AMR_整合分析報告_精簡_v2.md` L51

```
CPU%(sys)
 82 ┤                                          ████████████
 78 ┤                                     █████
 54 ┤              ████████████████████████
 44 ┤████████████
     3/17  18   19   20   21   22   23   24   25   26   27   28
                                          ↑
                                    AprilTag mux 忘關
```

---

## Sample 012

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L15

```
┌─────────────────────────────────────────────────────────────────┐
│                     Host OS (Ubuntu 20.04)                      │
│                   Intel i7-7700T / 7.7GB RAM                    │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│ Docker 1 │ Docker 2 │ Docker 3 │ Docker 4 │     Docker 5        │
│ gyro-ros │ ethercat │ canopen  │ agvweb   │     mqtt            │
│ :8022    │ :8024    │ :8023    │ :80/:5000│                     │
│          │          │          │          │                     │
│ ROS      │ EtherCAT │ CANopen  │ Flask    │ MQTT Bridge         │
│ Kinetic  │ Noetic   │ Noetic   │ ExtJS    │                     │
│ 50+ pkg  │ 7 pkg    │ 3 pkg    │ 152+ API │                     │
├──────────┴──────────┴──────────┴──────────┴─────────────────────┤
│                  ROS Master (port 11311)                        │
│              rosbridge (port 9090, WebSocket)                   │
├─────────────────────────────────────────────────────────────────┤
│  Hardware: USB2CAN / EtherCAT NIC / RS485 / RealSense / LIDAR   │
└─────────────────────────────────────────────────────────────────┘
```

---

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

## Sample 014

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L417

```
/static/dbfolder/
├── car_info/json/          # 設定檔
│   ├── processcontrol.json # 流程狀態機（54KB）
│   ├── processjsonmacro.json # 巨集庫（38KB）
│   ├── routemap.json       # 路線資料（237KB）
│   ├── allalarm.json       # 警報定義（100KB）
│   └── itemConf.json, ledConf.json, limit_group_default.json
├── car_setting/            # 車型設定（C4, D2, L4, L12 等）
├── warn_err/               # 錯誤/警告碼
├── errorcode/              # 延伸錯誤資訊
├── map/                    # 路線地圖
├── zip/                    # 日誌壓縮檔
└── tm_image/               # 達明手臂圖片
```

---

## Sample 015

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L441

```
┌─────────────┐    /motor_cmd     ┌──────────────┐
│             │ ────────────────→ │             │
│  gyro-ros   │    /motor_actual  │  ethercat /  │
│  (主系統)    │ ←──────────────── │  canopen   │
│             │    /motorAlarm    │  (馬達控制)  │
│             │ ←──────────────── │             │
└──────┬──────┘                   └──────────────┘
       │
       │  rosbridge (port 9090)
       ↕
┌──────┴──────┐
│   agvweb    │
│   (Web UI)  │
└─────────────┘
```

---

## Sample 016

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L494

```
package/
└── param/
    ├── L8N-BCnn-BLMR-FS54/   # 車型 A 設定
    ├── L4-LFUF-OBLV-FS54/    # 車型 B 設定
    └── default/               # 預設設定
```

---

## Sample 017

**Source**: `AMRCoolDown_v0\AMR_程式架構分析_v2.md` L674

```
~/maintain_work_logs/
├── ros/$DATE/          # ROS 日誌（每日目錄）
├── syswork/            # 系統監控日誌
├── e84/                # E84 通訊日誌
├── tcpbridge/          # TCP Bridge 日誌
├── TM_Export/          # 達明手臂日誌
├── TM_modbus/          # 達明 Modbus 日誌
├── maintain/           # 維護日誌
├── lidarscan/          # LIDAR 掃描日誌
├── job/                # 任務執行日誌
└── user/               # 使用者操作日誌
```

---

## Sample 018

**Source**: `AMRCoolDown_v0\AMR_網路頻寬分析.md` L197

```
RealSense D435 × 4
  ↓ USB 3.0（每台 ~30 MB/s）
  ↓
ROS Driver（realsense-ros）
  ↓ 發布 /d435_*/color/image_raw（30 Hz, 921 KB/frame）
  ↓
┌─────────────────────────────────┐
│ Subscriber 1: camera_monitor    │ ← 接收 4 台 = 110 MB/s
│ Subscriber 2: processjsonservice│ ← 接收 4 台 = 110 MB/s（視覺定位時）
│ Subscriber 3: video_record      │ ← 接收 4 台 = 110 MB/s（錄影時）
│ Subscriber 4: web_video_server  │ ← 接收 4 台 = 110 MB/s（串流時）
└─────────────────────────────────┘
                                    最壞情況：4 subscriber × 110 MB/s = 440 MB/s
                                    = CPU 必須每秒複製/序列化 440 MB 的 image data
```

---

## Sample 019

**Source**: `AMRCoolDown_v0\case01\mqtt分析.md` L175

```
斷線期間：
  ├─ Client 端：buffer 10 條 → 5 秒溢出 → 後續全部 error [-12] 丟棄
  ├─ Broker 端：clean_session=true → 不保留離線訊息
  └─ 協議層：QoS=0 → 不重試

重連後：
  ├─ buffer 清空 → 之前的都丟了
  ├─ broker 無保留 → 不補發
  └─ 新訊息才開始收到 → 但 GyrobotLayer 5 秒後才算恢復
```

---

## Sample 020

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v1.md` L143

```
停車層（stuckstate = True）：
  ├─ P1/P2 = Lidar 保護區 → 立即停車
  ├─ IRCollisionProt = IR 碰撞保護 → 立即停車
  └─ pointcloud_stop = 3D 點雲 → 最後防線

減速層（playslowdown = True）：
  ├─ W1/W2 = Lidar 警告區 → 播音減速（不停車）
  └─ LidarSurround_Det2/4 → 播音減速

來源：sys_indicator.py L1680-1733、safety_monitor.py（純 log 記錄器）
```

---

## Sample 021

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L284

```
AMR01 端 MQTT 通訊路徑中斷（整個 session 21 次獨立事件）
  ├─ 非 WiFi（wlp1s0 全天未連線、car ip 100% up）
  ├─ TCP unicast 正常（但 mqtt_client Docker 網路堆疊獨立）
  ├─ 非 CPU（離線時 avg 61.9% vs 基線 61.0%）
  ├─ 直接證據：MQTT error [-12] 緩衝溢出（06:00、08:55）
  ├─ 48% 同步離線 → AMR01 接收端 mqtt_client 斷連
  └─ 52% 獨自離線 → 對方發送端 mqtt_client 獨立故障
     ↓
costmap 5 秒 timeout + ignore_offline:true → 其他車障礙物被移除
     ↓
碰撞時恰好在離線窗口 + AMR01 正在橫移會車
     ↓ 同時
W1/W2 已觸發（13:42:26）但：
  ├─ 安全開啟時未停車（原因不明）
  └─ 隨後安全功能被 macro 關閉（13:42:28~35，7 秒窗口）
     ↓ 同時
CPU 過載（AprilTag 107% + log_update 92%）+ motor jitter（持續 6.4 次/分）
     ↓
碰撞 → pointcloud_stop（13:43:15）→ Alarm + Manual（13:43:48）
```

---

## Sample 022

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L357

```
IPC (enp5s0, EtherCAT Master / SOEM)
  │
  ╞══════════ Slave 1: 前輪轉向 (Position mode)  ← 100% 先 lost
  │              Alarm: M1xxxx
  │
  ╞══════════ Slave 2: 前輪驅動 (Speed mode)
  │              Alarm: M2xxxx
  │
  ╞══════════ Slave 3: 後輪轉向 (Position mode)
  │              Alarm: M3xxxx
  │
  ╘══════════ Slave 4: 後輪驅動 (Speed mode)
                 Alarm: M4xxxx
```

---

## Sample 023

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L461

```
IPC ↔ Slave 1（前輪轉向）實體連線問題
  ├─ 100% Slave 1 先 lost（26/26 次）
  ├─ 降速改善 5.5 倍（震動 → 線路搖晃）
  ├─ 19:48~19:57 密集叢集（10 分鐘 11 次 = 間歇性接觸不良）
  └─ 軟體一致但只有 AMR03 頻繁發生
     ↓
Slave 1 lost → daisy chain 下游全部失聯 (M1+M2+M3+M4 3804)
     ↓
Sync Manager Watchdog (0x001b) → 4 馬達同時報錯
     ↓
恢復與錯誤每秒震盪 75 秒
     ↓
Docking 機構超時 → DockNG × 2
```

---

## Sample 024

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L637

```
IPC (enp5s0, SOEM Master)
  │
  ╞══ Slave 1: 前輪轉向 (Position mode) ← 100% 先 lost
  ╞══ Slave 2: 前輪驅動 (Speed mode)
  ╞══ Slave 3: 後輪轉向 (Position mode)
  ╘══ Slave 4: 後輪驅動 (Speed mode)

Daisy chain 拓撲：斷在 Slave 1 → 下游 2/3/4 全部連帶失聯
驅動器之間無 IPC 連線（純串接）
SM Watchdog: 硬編碼 5000 (motor_control.cpp L213)
Cycle time: 2ms, DC sync: 62.5µs shift
```

---

## Sample 025

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v5.md` L653

```
        ┌─────────────────────────────────────────────┐
        │              AP Mesh 網路                   │
        │  (各車自建 AP: ASEK-AMRA04STR-L4K3-xxx)     │
        │  wlp1s0 未使用，car ip 走其他介面           │
        └─────────────┬───────────────────────────────┘
                      │
    ┌─────────────────┼──────────────────┐
    │                 │                  │
  AMR01             AMR02             AMR03
    │                 │                  │
    │  ┌──────────────┴──────────────┐   │
    │  │     MQTT Broker             │   │
    │  │  (車對車位置廣播)           │   │
    │  └──────────────┬──────────────┘   │
    │                 │                  │
    │  inter_robot_comm → ROS topic → GyrobotLayer
    │  (5 秒 timeout → "Treating it as offline")
    │
    │  ┌──────────────────────────────┐
    │  │     TCP Bridge (TSC)         │
    │  │  (指令/狀態，~1.1s 週期)     │
    │  └──────────────────────────────┘
    │
    │  ┌──────────────────────────────┐
    │  │     mqtt_bridge.py (TSC)     │
    │  │  (TSC↔AMR 指令，非車對車)   │
    │  └──────────────────────────────┘
```

---

## Sample 026

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6.md` L310

```
AMR01 端 MQTT 通訊路徑中斷（整個 session 21 次獨立事件）
  ├─ 非 WiFi（wlp1s0 全天未連線、car ip 100% up）
  ├─ TCP unicast 正常（但 mqtt_client Docker 網路堆疊獨立）
  ├─ 非 CPU（離線時 avg 61.9% vs 基線 61.0%）
  ├─ 直接證據：MQTT error [-12] 緩衝溢出（06:00、08:55）
  ├─ 48% 同步離線 → AMR01 接收端 mqtt_client 斷連
  └─ 52% 獨自離線 → 對方發送端 mqtt_client 獨立故障
     ↓
costmap 5 秒 timeout + ignore_offline:true → 其他車障礙物被移除
     ↓
碰撞時恰好在離線窗口 + AMR01 正在橫移會車
     ↓ 同時
W1/W2 已觸發（13:42:26）但：
  ├─ 安全開啟時未停車（原因不明）
  └─ 隨後安全功能被 macro 關閉（13:42:28~35，7 秒窗口）
     ↓ 同時
CPU 過載（AprilTag 107% + log_update 92%）+ motor jitter（持續 6.4 次/分）
     ↓
碰撞 → pointcloud_stop（13:43:15）→ Alarm + Manual（13:43:48）
```

---

## Sample 027

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6.md` L394

```
IPC (enp5s0, EtherCAT Master / SOEM)
  │
  ╞══════════ Slave 1: 前輪轉向 (Position mode)  ← 100% 先 lost
  │              Alarm: M1xxxx
  │
  ╞══════════ Slave 2: 前輪驅動 (Speed mode)
  │              Alarm: M2xxxx
  │
  ╞══════════ Slave 3: 後輪轉向 (Position mode)
  │              Alarm: M3xxxx
  │
  ╘══════════ Slave 4: 後輪驅動 (Speed mode)
                 Alarm: M4xxxx
```

---

## Sample 028

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6.md` L498

```
IPC ↔ Slave 1（前輪轉向）實體連線問題
  ├─ 100% Slave 1 先 lost（26/26 次）
  ├─ 降速改善 5.5 倍（震動 → 線路搖晃）
  ├─ 19:48~19:57 密集叢集（10 分鐘 11 次 = 間歇性接觸不良）
  └─ 軟體一致但只有 AMR03 頻繁發生
     ↓
Slave 1 lost → daisy chain 下游全部失聯 (M1+M2+M3+M4 3804)
     ↓
Sync Manager Watchdog (0x001b) → 4 馬達同時報錯
     ↓
恢復與錯誤每秒震盪 75 秒
     ↓
Docking 機構超時 → DockNG × 2
```

---

## Sample 029

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6.md` L675

```
IPC (enp5s0, SOEM Master)
  │
  ╞══ Slave 1: 前輪轉向 (Position mode) ← 100% 先 lost
  ╞══ Slave 2: 前輪驅動 (Speed mode)
  ╞══ Slave 3: 後輪轉向 (Position mode)
  ╘══ Slave 4: 後輪驅動 (Speed mode)

Daisy chain 拓撲：斷在 Slave 1 → 下游 2/3/4 全部連帶失聯
驅動器之間無 IPC 連線（純串接）
SM Watchdog: 硬編碼 5000 (motor_control.cpp L213)
Cycle time: 2ms, DC sync: 62.5µs shift
```

---

## Sample 030

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6.md` L691

```
        ┌─────────────────────────────────────────────┐
        │              AP Mesh 網路                   │
        │  (各車自建 AP: ASEK-AMRA04STR-L4K3-xxx)     │
        │  wlp1s0 未使用，car ip 走其他介面           │
        └─────────────┬───────────────────────────────┘
                      │
    ┌─────────────────┼──────────────────┐
    │                 │                  │
  AMR01             AMR02             AMR03
    │                 │                  │
    │  ┌──────────────┴──────────────┐   │
    │  │     MQTT Broker             │   │
    │  │  (車對車位置廣播)           │   │
    │  └──────────────┬──────────────┘   │
    │                 │                  │
    │  inter_robot_comm → ROS topic → GyrobotLayer
    │  (5 秒 timeout → "Treating it as offline")
    │
    │  ┌──────────────────────────────┐
    │  │     TCP Bridge (TSC)         │
    │  │  (指令/狀態，~1.1s 週期)     │
    │  └──────────────────────────────┘
    │
    │  ┌──────────────────────────────┐
    │  │     mqtt_bridge.py (TSC)     │
    │  │  (TSC↔AMR 指令，非車對車)   │
    │  └──────────────────────────────┘
```

---

## Sample 031

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6a.md` L143

```
停車層（stuckstate = True）：
  ├─ P1/P2 = Lidar 保護區 → 立即停車
  ├─ IRCollisionProt = IR 碰撞保護 → 立即停車
  └─ pointcloud_stop = 3D 點雲 → 最後防線

減速層（playslowdown = True）：
  ├─ W1/W2 = Lidar 警告區 → 播音減速（不停車）
  └─ LidarSurround_Det2/4 → 播音減速

來源：sys_indicator.py L1680-1733、safety_monitor.py（純 log 記錄器）
```

---

## Sample 032

**Source**: `AMRCoolDown_v0\case01\事件分析報告_v6b.md` L143

```
停車層（stuckstate = True）：
  ├─ P1/P2 = Lidar 保護區 → 立即停車
  ├─ IRCollisionProt = IR 碰撞保護 → 立即停車
  └─ pointcloud_stop = 3D 點雲 → 最後防線

減速層（playslowdown = True）：
  ├─ W1/W2 = Lidar 警告區 → 播音減速（不停車）
  └─ LidarSurround_Det2/4 → 播音減速

來源：sys_indicator.py L1680-1733、safety_monitor.py（純 log 記錄器）
```

---

## Sample 033

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L39

```
usserver.py
├── __init__()
│   ├── sensor_model: "UB350"（ROS param，實際值 UB350）
│   ├── rate: frame_rate（ROS param，實際值 8Hz）
│   ├── sensor_number: 8 個超音波感測器
│   ├── uslimit[]: 各感測器距離門檻
│   └── Publisher: /usserial (Int16MultiArray)
├── NormalProcess()  ← 主迴圈，threading 運行
│   └── while KeepRunning:
│       ├── usmod.dislimitArray_get()  ← 讀取感測器
│       ├── usserialpub.publish()      ← 發布到 ROS topic
│       └── time.sleep(resttime) 或 busy wait
└── vrstart()  ← 啟動 daemon thread

usmodule_UB350.py（感測器驅動）
├── __init__()
│   ├── baudrate: 115200
│   └── comport: /dev/ttyS0（serial port）
├── start()  ← 開啟 serial port
└── dislimitArray_get()  ← 核心讀取函式
    ├── while True: serial.read(1) 逐 byte 搜尋 header "UT"
    ├── serial.read(13) 讀取剩餘資料
    ├── XOR checksum 驗證
    └── 判斷 8 個感測器距離是否超過門檻
```

---

## Sample 034

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L158

```
log_update.py（主程式）
├── runningLog.__init__()
│   ├── loggingCarWork:        0.01s（預設，車上未設定）← 100Hz！
│   ├── loggingMaintenanceTime: 3600s（車上設定）
│   └── loggingStatisticTime:  1s（預設，車上未設定）
├── _runningLog()
│   ├── _runningperiodiclog(0.01, log_work)           ← 每 0.01 秒
│   ├── _runningperiodiclog(3600, log_componentlife)   ← 每 1 小時
│   └── _runningperiodiclog(1, log_consumption)        ← 每 1 秒
└── sched.scheduler.run()  ← 事件迴圈

子模組（每個都是獨立 class）：
├── log_work_update.py    → log_work()        ← 100Hz 呼叫！
├── log_pscmd_update.py   → subscriber callback
├── log_consumption_update.py → log_consumption()  ← 每秒呼叫
├── log_maintenance_update.py → log_maintain_update()
├── log_componentlife_update.py → log_componentlife()
└── log_folder_check.py   → log_folder_check()
```

---

## Sample 035

**Source**: `AMRCoolDown_v0\Phase2_原始碼分析報告.md` L183

```
Step 1: 從 12 個 ROS Subscriber 讀取最新狀態
       ├── /carmovestate (routeprogress) → 車輛移動狀態
       ├── /battery_level (Float32)      → 電池電量
       ├── /robot_pose (Pose)            → 機器人位姿
       ├── /sysindicator/error (syserr)  → 警報代碼
       ├── /sysindicator/warn (syswarn)  → 警告代碼
       ├── /rfiderack (String)           → RFID 讀取
       ├── /rfiderack_UHF (String)       → UHF RFID
       ├── /cansns (cansns1)             → CAN 感測器 1
       ├── /cansns4 (cansns4)            → CAN 感測器 4
       ├── /cansns2 (cansns2)            → CAN 感測器 2
       ├── /docking_pose (Float32MultiArray) → 對接位姿
       └── listener class 封裝每個 subscriber

Step 2: 比較 20+ 個 field 的 new vs old 值
       ├── work_status, docking_status, next_point...
       ├── arm_status, battery_level, e84State...
       ├── lotStatus, chargeStationState, alarmcode...
       └── 任一欄位變化 → 觸發寫入

Step 3: 如果有變化
       ├── check_file()       → 驗證 CSV 檔案完整性（讀取整個檔案！）
       ├── 讀取 CSV 最後一行  → 與新資料再次比較
       └── 寫入 CSV            → append 一行（25 個欄位）

Step 4: 更新 old = new（15 個 field）
```

---

## Sample 036

**Source**: `AMRCoolDown_v0\README.md` L23

```
AMRCoolDown_v0/
├── syswork/          # ROS 系統監控套件 (v2.16.1, GPLv2)
│   ├── scripts/      # 55+ Python 監控腳本
│   ├── launch/       # 45 ROS launch 檔
│   ├── msg/srv/      # 自定義 ROS 訊息與服務
│   └── errorcode/    # 多語系警報定義
├── routemap/         # ROS 路徑規劃套件 (v1.25.8, GPLv2)
│   ├── scripts/      # 15 Python 核心腳本
│   ├── src/          # C++ 插件 + Python 模組
│   └── launch/       # 8 launch 檔
├── AGVWeb/           # Flask Web 管理介面
│   ├── agvweb/       # Flask 應用套件
│   ├── templates/    # 網頁模板
│   └── Dockerfile    # Docker 部署設定
├── Phase1_*.md       # 環境探索報告
├── Phase2_*.md       # 原始碼分析報告
├── Phase3_*.md       # 程式優化建議報告
├── 結案報告_*.md      # 結案報告
├── 調查方法手冊.md    # 診斷方法論
└── ssh_cmd.py        # SSH 遠端指令工具
```

---

## Sample 037

**Source**: `AMRCoolDown_v0\結案報告_AMR2_CPU分析.md` L69

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

## Sample 038

**Source**: `AMRCoolDown_v0\調查方法手冊.md` L462

```
Phase 1：環境探索（SSH 指令為主）
  ├── 系統資訊 → lscpu, free, uptime, df
  ├── CPU 概覽 → vmstat, top batch
  ├── 記憶體概覽 → free, ps --sort=-%mem
  ├── Docker 容器 → docker ps, docker stats
  ├── ROS 環境 → rosnode list, rosversion
  └── 輸出：Phase1_環境探索報告.md

Phase 2：原始碼深度分析（SSH + Git + /proc）
  ├── 從 CodeCommit clone repo（syswork, routemap, AGVWeb）
  ├── 從 /proc/<PID>/root/ 撈取非 repo 的原始碼（canbus）
  ├── rosparam get 驗證車上實際參數 vs 程式碼預設
  ├── rostopic hz 驗證 topic 發布頻率
  ├── 5 次 top batch 取樣取中位數
  ├── grep -r 搜尋程式碼中的關鍵 pattern
  └── 輸出：Phase2_原始碼分析報告.md

Phase 3：優化建議整理（本地分析為主）
  ├── 對照原始碼 + 即時數據，產出修改建議
  ├── 安全影響分析（最壞情況評估）
  ├── Bug 報告（程式碼品質問題）
  └── 輸出：Phase3_程式優化建議報告.md

審核：多輪交叉驗證
  ├── 獨立審核 agent 進行紅隊式否定審查
  ├── 每輪審核產出補充驗證指令
  ├── 執行補充指令後更新報告
  └── 輸出：Phase1_2_審核報告.md（初審 → 二審 → 三審）
```

---

## Sample 039

**Source**: `Chat_bot_v1\architecture.md` L21

```
使用者（@gyro.com.tw）
    │ HTTPS POST + JWT
    ▼
Google Chat 平台 ─────────────────────────── 公司 GCP
    │
    ▼
Cloud Run (asia-east1, FastAPI) ────────── 個人 GCP
    │ HTTPS + API Key
    ▼
ngrok tunnel (free static domain) ─────── 個人 ngrok
    │
    ▼
本機 RAG backend (port 8001, FastAPI)
    │
    ├──→ Ollama bge-m3 (embedding, 本機) ── 個人
    ├──→ Gemini API (LLM) ──────────────── 個人 API key
    └──→ Qdrant localhost:6333 ─────────── 本機 Docker
```

---

## Sample 040

**Source**: `Chat_bot_v1\architecture.md` L86

```
使用者 /kb 電源設計
  │
  ▼ [公司 GCP]       Google Chat → Cloud Run
  ▼ [個人 GCP]       JWT 驗證 → 解析 slash command
  ▼ [本機 Ollama]    bge-m3 embedding("電源設計") → vector
  ▼ [本機]           Qdrant 並行搜尋 3 collections top-10，組裝 context
  ▼ [個人 Gemini]    Gemini 2.5 Flash 推理 → 繁中回答 + 建議關鍵字
  ▼ [個人 GCP]       格式化回應
  ▼                  Google Chat 顯示 RAG 回答
```

---

## Sample 041

**Source**: `Chat_bot_v1\aws-migration-discussion.md` L74

```
┌─────────────────────────────┐
│  EC2 (t3.medium, Ubuntu)    │
│                             │
│  ├── Python 3.8+            │
│  ├── Reporter_v0 腳本       │
│  ├── .doc/ 知識庫 (~55MB)   │
│  ├── Claude Code CLI        │
│  └── Chrome (PDF 輸出)      │
└─────────────────────────────┘
```

---

## Sample 042

**Source**: `Chat_bot_v1\aws-migration-discussion.md` L93

```
┌──────────────────┐     ┌──────────────┐
│  EC2 (運算)       │ ←→  │  S3 (儲存) │
│  Python 腳本      │     │  .doc/ 知識庫 │
│  FastAPI (可選)   │     │  報告輸出   │
│  Claude API      │     │  _index.json │
└──────────────────┘     └──────────────┘
```

---

## Sample 043

**Source**: `Chat_bot_v1\aws-migration-discussion.md` L109

```
┌───────────┐    ┌──────────────────┐    ┌─────┐
│ API GW    │ →  │ ECS/Fargate      │ ←→ │ S3 │
│           │    │ Docker 容器       │    │    │
└───────────┘    │ FastAPI          │    └─────┘
                 │ Python 腳本      │
                 │                  │    ┌────────────────┐
                 │  gemini client ──│──→ │ Google Gemini │
                 │                  │    │ - Embedding API │
                 └──────────────────┘    │ - Chat/Gen API │
                                         └────────────────┘
```

---

## Sample 044

**Source**: `Chat_bot_v1\aws-migration-discussion.md` L176

```
┌──────────┐    ┌─────────────────────┐    ┌─────┐
│ API GW   │ →  │ Fargate Container   │ ←→ │ S3 │
│ or Web   │    │                     │    │ .txt files
└──────────┘    │ FastAPI             │    │ templates
                │ ├── /report (生成)   │    └─────┘
                │ ├── /search (搜尋)   │
                │ ├── /calc   (計算)   │        ┌──────────┐
                │ └── gemini_client ───│──────→ │ Gemini │
                │                     │        │ 2.5 Pro │
                │ _calc_throughput.py  │        └──────────┘
                │ gyro-report gen     │
                └─────────────────────┘
```

---

## Sample 045

**Source**: `Chat_bot_v1\google-chat-bot-aws.md` L47

```
Google Chat                        AWS EC2
┌──────────┐    HTTPS POST     ┌──────────────────────────┐
│ 使用者    │ ───────────────→ │ Caddy (reverse proxy)      │
│ @kb ...  │                   │   ├── /chat/event → FastAPI│
│          │ ←─────────────── │   └── /api/* → FastAPI     │
│ 回應卡片  │    JSON response  │                            │
└──────────┘                   │ FastAPI (api_server.py)     │
                               │   ├── /chat/event (新增)   │
                               │   │   ├── 解析 Chat event  │
                               │   │   ├── 路由 fast/deep   │
                               │   │   └── 格式化回應卡片   │
                               │   ├── /api/search (既有)   │
                               │   └── /api/deep-query(既有) │
                               │                            │
                               │ Qdrant Docker (port 6333)  │
                               │   ├── pkb_docs             │
                               │   ├── pkb_images           │
                               │   └── pkb_mail             │
                               └──────────┬─────────────────┘
                                          │
                                          ▼
                               ┌──────────────────┐
                               │ Google Gemini API │
                               │ - Embedding       │
                               │ - 2.5 Flash (RAG) │
                               └──────────────────┘
```

---

## Sample 046

**Source**: `Chat_bot_v1\google-chat-bot-aws.md` L153

```
EC2 t3.medium           ~$30/月
EBS 100 GB gp3          ~$8/月
Elastic IP              免費（綁定運行中 instance）
Gemini API              ~$1-5/月（依用量）
域名                    ~$1/月（Route 53）
────────────────────────────────
總計                    ~$40-45/月
```

---

## Sample 047

**Source**: `Chat_bot_v1\google-workspace-setup.md` L13

```
/pm sync
  ├── curl POST ──────────────────→ Google Chat Space (Webhook)
  └── curl GET (Base64 payload) ──→ Apps Script Web App
                                          └── Google Sheet (Dashboard)
```

---

## Sample 048

**Source**: `Chat_bot_v1\PKB_專案說明_v2_0327.md` L54

```
personal-rag_v2\PKB\
├── .env                    GEMINI_API_KEY / GOOGLE_API_KEY
├── CLAUDE.md               Claude Code 規則 + 草圖引擎邏輯
├── GYRO_context.md         產品規格 / 客戶 / 公式（≤150 行）
├── MANIFEST.csv            Phase 1 處理清單（SHA256 去重）
├── SKIPPED_ARCHIVES.csv    跳過的壓縮檔清單（302 個）
├── images_index.csv        圖片精確標籤
├── image_embed_state.db    Phase 3 圖片/影片 embedding 進度
├── vault\                  原始資料備份（唯讀，SHA256 去重）
│   ├── docs\               技術文件（PPTX/PDF/DOCX）
│   ├── images\             圖片
│   ├── videos\             影片
│   └── embedded_images\    文件內嵌圖片
├── templates\              報告模板 Markdown（14 類）
│   ├── 00_報告產生流程\    Marp 使用指南 + 範例
│   ├── 01_客戶提案\        含 8 種子模板
│   ├── 04_測試報告\  05_進度報告\  06_會議記錄\
│   ├── 08_市場分析\  09_設計文件\  10_操作手冊\
│   ├── 12_工作管制表\  13_圖紙\  14_不良分析報告\
│   ├── 16_內部研究\  17_介紹信\  18_AGV規劃\
├── raw_phase3\             Phase 3 歸納中間產出（僅供參考）
│   ├── customers\          客戶分析（24 batches）
│   ├── products\           產品線分析
│   └── templates\          模板原型（18 種）
├── scripts\                所有執行腳本（見下方）
├── sketch\                 草圖 SVG 輸出
├── workspace\              每次任務工作資料夾
├── logs\                   執行日誌
└── db\chroma\              ChromaDB legacy（唯讀，待清除）
```

---

## Sample 049

**Source**: `Chat_bot_v1\README.md` L66

```
Chat_bot_v1/
├── app.py                 # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py             # RAG backend（本機, API key 驗證 + LINE webhook/push）
├── rag.py                 # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── rate_limit.py           # Sliding window per-IP rate limiter
├── conv_logger.py         # （已停用）本地 JSONL 對話記錄
├── drive_logger.py        # （已停用）Google Drive 記錄同步
├── drive_sync.py          # （已停用）JSONL → Drive 增量同步
├── start-backend.sh       # Backend 啟動腳本（Windows/Linux）
├── stop-backend.sh        # Backend 停止腳本
├── Dockerfile             # Cloud Run thin proxy 映像
├── docker-compose.yml     # 本機開發用（Qdrant）
├── requirements.txt       # Python 依賴
├── pyproject.toml         # Ruff / pytest 設定
├── requirements-dev.txt   # 開發依賴（pytest, ruff）
├── tests/                 # Unit tests（33 cases）
├── architecture.md        # 架構與帳號歸屬文件
├── .env.example           # 環境變數範本
└── reviews/               # 程式碼審核報告
```

---

## Sample 050

**Source**: `Chat_bot_v1\README.md` L90

```
Google Chat (@gyro.com.tw)  ─┐
LINE Bot                     ├→ Cloud Run thin proxy (JWT 驗證, 個人 GCP)
                             │     → ngrok tunnel → 本機 RAG backend (API key + rate limit)
                             │         → Ollama bge-m3 (embedding) + Gemini API (LLM)
                             │         → 本機 Qdrant (向量搜尋, 並行 3 collections)
                             │
LINE Webhook ────────────────┘  → /webhook/line-webhook (signature 驗證)
                                → /line/push (主動推送)
```

---

## Sample 051

**Source**: `Chat_bot_v1\使用指引.md` L7

```
Google Chat (@gyro.com.tw)
    │ HTTPS POST + JWT
    ▼
Cloud Run thin proxy (asia-east1, FastAPI)  ── 個人 GCP
    │ HTTPS + API Key
    ▼
ngrok tunnel → 本機 RAG backend (port 8001)
    │
    ├──→ Ollama bge-m3 (embedding, 本機)
    ├──→ Qdrant (localhost:6333, 向量搜尋)
    └──→ Gemini 2.5 Flash API (LLM 推理)
```

---

## Sample 052

**Source**: `Chat_bot_v1\使用指引.md` L121

```
Chat_bot_v1/
├── app.py                 # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py             # RAG backend（本機, API key 驗證）
├── rag.py                 # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── Dockerfile             # Cloud Run thin proxy 映像
├── docker-compose.yml     # 本機開發用（Qdrant）
├── start-backend.sh       # Backend + ngrok 啟動腳本
├── stop-backend.sh        # Backend + ngrok 停止腳本
├── requirements.txt       # Proxy 依賴
├── requirements-backend.txt # Backend 依賴
├── .env.example           # 環境變數範本
├── architecture.md        # 架構與帳號歸屬文件
├── conv_logger.py         # （已停用）本地 JSONL 對話記錄
├── drive_logger.py        # （已停用）Google Drive 記錄同步
├── drive_sync.py          # （已停用）JSONL → Drive 增量同步
└── reviews/               # 程式碼審核報告
```

---

## Sample 053

**Source**: `Claude-Code-Agent-Monitor\.superpowers\README.md` L27

```
.superpowers/
├── brainstorm/        # Design explorations and refined specs
├── plans/             # Task breakdowns and execution plans
├── reviews/           # Code review outputs and feedback
├── runs/              # Execution logs or agent traces
└── README.md          # This file
```

---

## Sample 054

**Source**: `Claude-Code-Agent-Monitor\client\README.md` L147

```
client/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── __tests__/      # Component tests
│   │   ├── AgentCard.tsx
│   │   ├── SessionCard.tsx
│   │   ├── ToolCard.tsx
│   │   ├── EventTimeline.tsx
│   │   ├── NotificationBadge.tsx
│   │   └── Layout.tsx
│   │
│   ├── pages/              # Route pages
│   │   ├── SessionsPage.tsx
│   │   ├── SessionDetailPage.tsx
│   │   ├── AgentDetailPage.tsx
│   │   ├── SettingsPage.tsx
│   │   └── PricingPage.tsx
│   │
│   ├── lib/                # Core utilities & business logic
│   │   ├── __tests__/      # Utility tests
│   │   ├── api.ts          # REST API client
│   │   ├── websocket.ts    # WebSocket manager
│   │   ├── eventBus.ts     # Event pub/sub
│   │   ├── notifications.ts # Browser notifications
│   │   ├── format.ts       # Formatters (fmt, fmtCost, timeAgo)
│   │   ├── types.ts        # TypeScript type definitions
│   │   └── constants.ts    # App-wide constants
│   │
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles (Tailwind imports)
│
├── public/                 # Static assets
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
├── vitest.config.ts        # Test configuration
├── tailwind.config.js      # Tailwind CSS config
├── tsconfig.json           # TypeScript config
└── package.json
```

---

## Sample 055

**Source**: `Claude-Code-Agent-Monitor\client\README.md` L577

```
┌────────────────────────────────────────┐
│ 🟢 Session Title         $0.45         │
│ claude-sonnet-4                        │
│ Started: 2 hours ago                   │
│ Agents: 3 | Tools: 12                  │
└────────────────────────────────────────┘
```

---

## Sample 056

**Source**: `Claude-Code-Agent-Monitor\client\README.md` L732

```
client/src/
├── components/__tests__/
│   ├── AgentCard.test.tsx
│   ├── SessionCard.test.tsx
│   └── EventTimeline.test.tsx
│
└── lib/__tests__/
    ├── format.test.ts
    ├── eventBus.test.ts
    └── api.test.ts
```

---

## Sample 057

**Source**: `Claude-Code-Agent-Monitor\docs\MCP.md` L147

```
mcp/
├── src/
│   ├── index.ts              # MCP server entry point
│   ├── config/
│   │   └── app-config.ts     # Configuration + validation
│   ├── tools/
│   │   ├── sessions.ts       # Session-related tools
│   │   ├── agents.ts         # Agent-related tools
│   │   ├── pricing.ts        # Pricing management tools
│   │   └── stats.ts          # Statistics tools
│   └── types.ts              # TypeScript type definitions
│
├── dist/                     # Compiled JavaScript (gitignored)
├── package.json
├── tsconfig.json
└── README.md
```

---

## Sample 058

**Source**: `Claude-Code-Agent-Monitor\server\README.md` L130

```
server/
├── index.js               # Express app + server bootstrap
├── db.js                  # SQLite connection + prepared statements
├── websocket.js           # WebSocket server + broadcast
├── compat-sqlite.js       # Fallback for node:sqlite (Node 22.5+)
│
├── routes/
│   ├── hooks.js           # Hook ingestion endpoints
│   ├── sessions.js        # Session CRUD API
│   ├── agents.js          # Agent CRUD API
│   └── pricing.js         # Pricing rules API
│
└── __tests__/
    └── api.test.js        # Integration tests
```

---

## Sample 059

**Source**: `claude-dotfiles\benchmark-results\outputs-claude\4a-ADR-claude.md` L29

```
classify → execute → validate → report
              ↑          |
              └── retry ──┘ (max 1)
```

---

## Sample 060

**Source**: `claude-dotfiles\commands\pm-sync.md` L16

```
📊 目前狀態
├─ Tasks: N/M completed
├─ Git: X modified, Y untracked
├─ 上次同步：<時間 或「—」>
└─ Dashboard: <已同步 / 未同步>
```

---

## Sample 061

**Source**: `claude-dotfiles\docs\env-setup.md` L140

```
專案根目錄/
├── opencode.json          # 主設定檔（provider、model、agent、permission、mcp）
├── AGENTS.md              # Agent 系統指示（OpenCode 版的 CLAUDE.md）
├── package.json           # npm 依賴
└── .opencode/             # OpenCode 客製化目錄
    ├── plugins/           # 自訂 plugin
    └── skills/            # 自訂 skill
```

---

## Sample 062

**Source**: `claude-dotfiles\docs\google-workspace-setup.md` L13

```
/pm sync
  ├── curl POST ──────────────────→ Google Chat Space (Webhook)
  └── curl GET (Base64 payload) ──→ Apps Script Web App
                                          └── Google Sheet (Dashboard)
```

---

## Sample 063

**Source**: `claude-dotfiles\docs\opencode-vs-claude-code.md` L71

```
Claude Code（主力）
├── 複雜任務：多檔重構、架構設計、深度 debug
├── 品質要求高：production code、PR review
└── 需要工具整合：IDE、memory、plan mode

OpenCode（輔助）
├── 簡單任務：文件產生、格式轉換、git 操作
├── Claude Code 限流時：備案（Gemini 雲端）
├── 離線工作：Ollama 本地模型
└── 省錢：免費額度內的日常小任務
```

---

## Sample 064

**Source**: `claude-dotfiles\dual-engine\README.md` L51

```
DuelEngineSOP_v0/
├── README.md                       # 本文件
├── dual-engine-sop.md              # SOP 完整規格
├── commands/
│   ├── claude-code/
│   │   └── opencode-do.md          # Claude Code /opencode-do 指令
│   └── opencode/
│       └── do.md                   # opencode /do 指令
```

---

## Sample 065

**Source**: `claude-dotfiles\opencode-config\AGENTS.md` L176

```
.opencode/              # OpenCode 工作目錄設定
├── plugins/            # TypeScript plugins（hook 系統）
│   └── git-attribution.ts
├── skills/             # Skill definitions
│   └── project-status/
│       └── SKILL.md
└── package.json

opencode-config/        # 可分發的設定套件
├── AGENTS.md          # 主要的 agent 指示
├── AGENTS-ur.md       # UR_Program_Analysis 專用指示
├── opencode.json      # 模型、agent、permission、MCP 設定
└── .opencode/         # 副本（plugins/skills）
```

---

## Sample 066

**Source**: `claude-dotfiles\pm-v2-design.md` L37

```
/pm ──────→ 開工（判斷首次/正常模式）
/pm sync ──→ 選單：同步 | 審核 | 調整計畫
/pm bye ───→ 自動：回顧 → easy 審核 → smart-commit → push? → sync → retro → 告別
/pm review → easy（主 agent）或 deep（獨立 subagent 紅隊）
```

---

## Sample 067

**Source**: `claude-dotfiles\pm-v2-design.md` L46

```
progress.md ──→ Google Doc（單向同步：本地→Doc）
                ↓
            Google Chat Space（摘要通知，防洗版）
                ↓
            Dashboard Google Doc（各專案區段）
```

---

## Sample 068

**Source**: `claude-dotfiles\pm-v2-design.md` L172

```
~/.claude/
├── commands/
│   ├── pm.md          ← v2 主指令（~660 行）
│   ├── hello.md       ← legacy（已 deprecated）
│   ├── sc.md          ← legacy（已 deprecated）
│   └── bye.md         ← legacy（已 deprecated）
├── statusline.js      ← status line 渲染
├── statusline.sh      ← status line 入口
├── pm-update.sh       ← status line 狀態更新
├── pm-last.txt        ← status line 狀態檔（runtime）
└── settings.json      ← hooks（SessionStart reset、Stop beep、PreToolUse beep）

GitHub Repo: CPIDLE/claude-dotfiles
├── commands/pm.md     ← 主指令源碼
├── reviews/           ← deep 審核報告
├── pm-v2-design.md    ← 本文件
├── install.ps1        ← Windows 安裝腳本
└── install.sh         ← Linux/Mac 安裝腳本
```

---

## Sample 069

**Source**: `claude-dotfiles\README.md` L24

```
claude-dotfiles │ master │ pm▸sync▸bye     Opus 4.6 │ ctx:6% 5h:2%▸03:00 7d:78%▸4/3
```

---

## Sample 070

**Source**: `claude-dotfiles\README.md` L75

```
/pm                          # 開工
  ↓
  工作
  ├─ 完成功能 → /smart-commit
  ├─ 簡單任務 → /do easy <任務>
  ├─ 複雜任務 → /do deep <任務>
  ├─ ctx ≈ 60% → /pm-bye → /clear → /pm
  ↓
/pm-bye                      # 收工
```

---

## Sample 071

**Source**: `claude-dotfiles\README.md` L106

```
├── global-claude.md         # 全域指令（→ ~/.claude/CLAUDE.md）
├── settings.json            # Hooks、plugins、statusline
├── mcp.json                 # MCP server config（→ ~/.claude/.mcp.json）
├── statusline.sh / .js      # Status Line 腳本
├── pm-update.sh             # /pm 狀態更新
├── commands/                # Claude Code slash commands
├── skills/                  # Custom skills（8 個）
├── benchmark.py             # Gemini API 品質評測
├── benchmark-results/       # 評測結果 + 產出檔案
├── langgraph-migration.md   # LangGraph 遷移計畫（參考）
├── dual-engine/             # Dual Engine SOP + 範例
├── docs/                    # 設定指南
│   ├── google-workspace-setup.md
│   ├── plugins.md
│   ├── mcp-setup.md
│   └── ...
├── install.ps1              # Windows 安裝
└── install.sh               # macOS/Linux 安裝
```

---

## Sample 072

**Source**: `claude-dotfiles\skills\agent-browser\references\snapshot-refs.md` L140

```
@e1 [tag type="value"] "text content" placeholder="hint"
│    │   │             │               │
│    │   │             │               └─ Additional attributes
│    │   │             └─ Visible text
│    │   └─ Key attributes shown
│    └─ HTML tag name
└─ Unique ref ID
```

---

## Sample 073

**Source**: `claude-dotfiles\skills\ascii-align\SKILL.md` L98

```
Font: Sarasa Mono TC.
Display width: box-drawing (─│├┐┘┤┌┬┴┼) = 1 col,
arrows (▼▲→←) = 2 cols, geometric (●○■□◆) = 2 cols.

Rules:
- Every line in a box group must have identical display width
- Only adjust spacing. Never change text content.
- ▼/→ must start at same column as │ above it
- Junction (┬┴┼) must align vertically with │ in content lines
```

---

## Sample 074

**Source**: `claude-dotfiles\skills\gyro-kb.md` L10

```
/gyro-kb ── 負責「內容產出」── 知識庫搜尋 + 計算 + 報告撰寫
  │
  │  產出 .md 報告
  ▼
/report-gyro ── 負責「排版呈現」── MD → HTML 簡報 + PDF + Excel 驗算
```

---

## Sample 075

**Source**: `claude-dotfiles\skills\gyro-kb.md` L54

```
E:/github/personal-rag_v2/PKB/
├── GYRO_context.md          ← 公司知識摘要（必讀）
├── MANIFEST.csv             ← 文件追蹤清單
├── db/chroma/               ← ChromaDB 持久化
│   ├── pkb_docs             ← 文件 collection
│   └── pkb_images           ← 圖片 collection
├── vault/                   ← 原始文件庫
│   ├── docs/
│   ├── images/
│   ├── videos/
│   └── embedded_images/
├── raw_phase3/              ← Phase 3 歸納（唯讀）
│   ├── customers/batch_01~24.md
│   └── products/*.md
├── templates/               ← 報告模板（18+ 模板）
│   └── 00_報告產生流程/     ← 報告工作流定義
└── workspace/CASE##/        ← 報告輸出工作區
```

---

## Sample 076

**Source**: `claude-dotfiles\skills\gyro-kb.md` L388

```
workspace/CASE##/
├── [原始檔案]                        ← 輸入
├── input_data.json                   ← 理解（結構化提取）
├── params.json                       ← 確認（單一真相來源）
├── results.json                      ← 計算
├── 01_requirements_review.md/.html   ← 需求確認
├── 02_analysis_report.md/.html       ← 分析報告
├── 03_[文件類型].md/.html            ← 最終產出
└── .images/
    ├── client/                       ← 客戶提供
    ├── db/                           ← ChromaDB 搜尋
    └── generated/                    ← Mermaid 渲染
```

---

## Sample 077

**Source**: `claude-dotfiles\skills\report-easy\SKILL.md` L18

```
source.md (純文字)
   │
   │  Stage 1: 圖表化（D2/ELK 為主，Mermaid 為輔）
   ▼
source_elk.md  +  ./assets/*.d2  +  ./assets/*_elk.png
   │
   │  Stage 2: 套白皮書 HTML 模板（直 + 橫）
   ▼
source_elk_直.html (A4 portrait)
source_elk_橫.html (A4 landscape)
```

---

## Sample 078

**Source**: `claude-dotfiles\skills\report-easy\SKILL.md` L108

```
skills/report-easy/
├── SKILL.md                  ← 本檔案
├── assets/
│   ├── template_直.html      ← A4 portrait 模板（含 {{TITLE}} / {{MARKDOWN_CONTENT}} 占位）
│   ├── template_橫.html      ← A4 landscape 模板
│   └── d2_common.d2          ← 共用 D2 樣式 classes
└── scripts/
    └── build_html.py         ← 一鍵產生 直/橫 HTML
```

---

## Sample 079

**Source**: `claude-dotfiles\skills\report-gyro\README_載入SOP.md` L7

```
.claude/skills/report-gyro/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   └── gyro-marp-theme.css               ← Marp theme
└── scripts/
    └── gen_verification.py               ← Excel 驗算產生器
```

---

## Sample 080

**Source**: `claude-dotfiles\skills\report-gyro\SKILL.md` L17

```
/gyro-kb ── 負責「內容產出」── 知識庫搜尋 + 報告撰寫
  │
  │  產出 .md 報告
  ▼
/report-gyro ── 負責「排版呈現」── 三條路線
                 ↑ 你在這裡
```

---

## Sample 081

**Source**: `claude-dotfiles\skills\report-gyro\SKILL.md` L151

```
skills/report-gyro/
├── SKILL.md                          ← 本檔案
├── README_載入SOP.md
├── assets/
│   └── gyro-marp-theme.css           ← Marp 唯一 theme
└── scripts/
    └── gen_verification.py           ← Excel 驗算產生器
```

---

## Sample 082

**Source**: `Claude_code_leak_v0\README.md` L55

```text
src/
├── main.tsx                 # Entrypoint orchestration (Commander.js-based CLI path)
├── commands.ts              # Command registry
├── tools.ts                 # Tool registry
├── Tool.ts                  # Tool type definitions
├── QueryEngine.ts           # LLM query engine
├── context.ts               # System/user context collection
├── cost-tracker.ts          # Token cost tracking
│
├── commands/                # Slash command implementations (~50)
├── tools/                   # Agent tool implementations (~40)
├── components/              # Ink UI components (~140)
├── hooks/                   # React hooks
├── services/                # External service integrations
├── screens/                 # Full-screen UIs (Doctor, REPL, Resume)
├── types/                   # TypeScript type definitions
├── utils/                   # Utility functions
│
├── bridge/                  # IDE and remote-control bridge
├── coordinator/             # Multi-agent coordinator
├── plugins/                 # Plugin system
├── skills/                  # Skill system
├── keybindings/             # Keybinding configuration
├── vim/                     # Vim mode
├── voice/                   # Voice input
├── remote/                  # Remote sessions
├── server/                  # Server mode
├── memdir/                  # Persistent memory directory
├── tasks/                   # Task management
├── state/                   # State management
├── migrations/              # Config migrations
├── schemas/                 # Config schemas (Zod)
├── entrypoints/             # Initialization logic
├── ink/                     # Ink renderer wrapper
├── buddy/                   # Companion sprite
├── native-ts/               # Native TypeScript utilities
├── outputStyles/            # Output styling
├── query/                   # Query pipeline
└── upstreamproxy/           # Proxy configuration
```

---

## Sample 083

**Source**: `D435i_LidarScan\FLOW.md` L5

```
D435i Camera (emitter BLINK/OFF) ► Depth Frame ──► 3D Point Cloud ──► Ground-Aligned
                  IMU Frame  ──► Gravity Vector ──► Rotation Matrix ──┘
               Color Frame  ──► Depth Anything V2 (mono) ──┐         │
           IR Left + Right  ──► CREStereo (stereo ONNX) ──┤          │
                            ──► Texture Map (IR variance)──┤         │
                                                     │                │
                                           ┌─────────┴───────────────┴──┐
                                           ▼                            ▼
                                  [LiDAR 1: Horizontal]       [LiDAR 2: Ground]
                                   Height Filter → 2D Scan     Vertical Angle Filter
                                           │                   → 2 × LaserScan
                                   ┌───────┤                         │
                                   ▼       ▼                   ┌─────┴─────┐
                                 UDP:7777  ROS2:/scan          ▼           ▼
                                 OpenCV                     UDP:7778    UDP:7779
                                                            line0       line1
```

---

## Sample 084

**Source**: `D435i_LidarScan\FLOW.md` L69

```
Available presets (--lidar-model):
┌──────────────┬─────────────────┬───────┬───────────┬───────────────┬───────┐
│ Key          │ Name            │ FOV   │ Res (deg) │ Range (m)     │ Steps │
├──────────────┼─────────────────┼───────┼───────────┼───────────────┼───────┤
│ hokuyo_urg   │ Hokuyo URG-04LX │ 240°  │ 0.36      │ 0.02 - 5.6   │ 683    │
│ hokuyo_utm   │ Hokuyo UTM-30LX │ 270°  │ 0.25      │ 0.1  - 30.0  │ 1081   │
│ hokuyo_ust   │ Hokuyo UST-10LX │ 270°  │ 0.25      │ 0.06 - 10.0  │ 1081   │
│ rplidar_a2   │ RPLIDAR A2      │ 360°  │ 0.45      │ 0.15 - 12.0  │ 800    │
│ sick_tim561  │ SICK TiM561     │ 270°  │ 0.33      │ 0.05 - 10.0  │ 811    │
│ custom       │ (user-defined)  │ 87°*  │ user      │ user          │ user  │
└──────────────┴─────────────────┴───────┴───────────┴───────────────┴───────┘
* custom mode uses D435i's native ~87° FOV

Note: D435i has ~87° HFOV. Only that angular portion has real data.
      Bins outside D435i coverage = inf (no data).
```

---

## Sample 085

**Source**: `D435i_LidarScan\FLOW.md` L88

```
D435iLidarScanner
├── rs.pipeline()              ← RealSense pipeline
├── GravityEstimator(alpha=0.98)  ← IMU low-pass filter
├── NeuralStereoEstimator      ← (optional, when --neural-stereo)
│   └── CREStereo ONNX + background thread
├── MonoDepthEstimator         ← (optional, when --mono-depth)
│   └── Depth Anything V2 ONNX + background thread
└── Post-processing filters
    ├── rs.decimation_filter()
    ├── rs.spatial_filter()
    ├── rs.temporal_filter()
    └── rs.threshold_filter()
```

---

## Sample 086

**Source**: `D435i_LidarScan\FLOW.md` L104

```
┌─────────────────────────────────────────────┐
│ 1. Enable streams                           │
│    ├── depth (1280x720, z16, 15fps)         │
│    ├── color (1280x720, rgb8, 15fps)        │
│    ├── infrared 1 (1280x720, y8, 15fps) *   │
│    ├── infrared 2 (1280x720, y8, 15fps) *   │
│    ├── accel (accelerometer)                │
│    └── gyro  (gyroscope)                    │
│    (* IR when --neural-stereo or --mono-depth) │
│                                             │
│ 2. Configure sensor                         │
│    ├── Emitter: BLINK mode or OFF           │
│    ├── Set visual preset (high_accuracy)    │
│    └── Get depth_scale                      │
│                                             │
│ 3. Neural stereo setup (if enabled)         │
│    ├── Get IR intrinsics (fx for depth)     │
│    ├── Get stereo baseline from extrinsics  │
│    └── Create NeuralStereoEstimator         │
│                                             │
│ 4. Configure post-processing filters        │
│    ├── Decimation: magnitude = 2            │
│    │   (1280x720 → 640x360)                │
│    ├── Spatial: alpha=0.5, delta=20         │
│    ├── Temporal: alpha=0.2, delta=50        │
│    └── Threshold: range_min ~ range_max     │
│                                             │
│ 5. Get depth intrinsics (fx, fy, cx, cy)    │
│                                             │
│ 6. Precompute pixel coordinate grid         │
│    u_grid[H,W], v_grid[H,W]                 │
└─────────────────────────────────────────────┘
```

---

## Sample 087

**Source**: `D435i_LidarScan\FLOW.md` L157

```
while True:
    ┌──────────────────────────────────────────────────┐
    │              process_frame()                    │
    │                    │                            │
    │         ┌──────── ▼ ────────┐                  │
    │         │   _get_frames()    │                  │
    │         └────────────────────┘                  │
    │                   │                             │
    │      ┌────────┬───┼────────┬──────┐             │
    │      ▼        ▼   ▼        ▼      ▼        │
    │    depth   accel gyro   IR_L    IR_R            │
    │    frame   [xyz] [xyz]  (Y8)    (Y8)            │
    │      │        │                  │              │
    │      │        ▼                  │             │
    │      │  GravityEstimator.update()│              │
    │      │        │                  │              │
    │      │        ▼                  │             │
    │      │  get_rotation_matrix()→R  │             │
    │      ▼                           ▼            │
    │    ┌── neural_stereo ON? ─────────────────┐     │
    │    │ YES                         NO       │     │
    │    │                                      │     │
    │    │ real_points (stereo, ~11%)           │     │
    │    │   (for camera height only)           │     │
    │    │ push IR pair → bg thread            │     │
    │    │ get_latest_depth → neural depth     │     │
    │    │ fuse(stereo + neural) → ~100%       │     │
    │    │ → fused_points [N,3]                │     │
    │    │                    _depth_to_points  │     │
    │    │                    + ground_synth    │     │
    │    │                    → points [N,3]   │     │
    │    └──────────────────────────────────────┘     │
    │                 │                               │
    │          ├───────────────────────┐              │
    │          ▼                       ▼            │
    │  _points_to_scan(R)    _points_to_ground_lines(R) │
    │  [LiDAR 1: horizontal]  [LiDAR 2: ground]       │
    │          │                  │                   │
    │          ▼                  ▼                 │
    │     LaserScan        (LaserScan, LaserScan)     │
    │                      line0        line1         │
    └─────┬────────────────────┬─────────────────────┘
          │                    │
    ┌─────┼─────┐        ┌────┼────┐
    ▼     ▼     ▼        ▼         ▼
  draw  net_out Rerun   ground_out ground_out
  scan  .send() 3D viz  [0].send() [1].send()
```

---

## Sample 088

**Source**: `D435i_LidarScan\FLOW.md` L211

```
When --emitter is enabled, IR emitter runs in blink cycle:

    ┌─────────────────────────────────────────────────────────────┐
    │  3.0s OFF          │ 3 frames ON (~0.2s) │  3.0s OFF  ...   │
    │  emitter=0         │ emitter=1           │  emitter=0       │
    │                    │                     │                  │
    │  Neural stereo ✓   │ Neural stereo ✗     │  Neural stereo ✓ │
    │  Mono depth    ✓   │ Mono depth    ✗     │  Mono depth    ✓ │
    │  Fusion        ✓   │ Fusion: skip        │  Fusion        ✓ │
    │  Apply corr maps   │ Update corr maps    │  Apply corr maps │
    │  → corrected fused │ → real_points only  │  → corrected  │
    └─────────────────────────────────────────────────────────────┘

Emitter ON frames:
  - Built-in stereo has high coverage (~62%) from IR dot pattern
  - Neural stereo/mono push skipped (IR dots corrupt input)
  - Capture stereo depth as reference (ground truth)
  - Compare reference vs stale neural/mono results → update correction maps
  - No fusion — use real_points directly

Emitter OFF frames (majority):
  - Normal fusion pipeline: stereo + CREStereo + mono depth
  - Neural depth × neural_correction_map → corrected neural depth
  - Mono relative depth × mono_correction_map → corrected mono (before scale_map)
  - Correction maps fix systematic model bias, not scene geometry

Correction map computation:
  - Per-block (20×20) median of ref_depth / pred_depth
  - EMA blend α=0.7 new + 0.3 old across blink cycles
  - Clamped to [0.5, 2.0] range
  - Requires >30% emitter-ON coverage, >500 overlap pixels

Compatible with: --neural-stereo, --mono-depth, standalone
```

---

## Sample 089

**Source**: `D435i_LidarScan\FLOW.md` L253

```
pipeline.wait_for_frames()
         │
         ├──► depth_frame
         │         │
         │         ▼  Post-processing pipeline
         │    ┌─────────────┐
         │    │ Decimation   │  1280x720 → 640x360 (mag=2)
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Threshold    │  Remove < range_min or > range_max
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Spatial      │  Edge-preserving spatial smoothing
         │    └──────┬──────┘
         │    ┌──────▼──────┐
         │    │ Temporal     │  Cross-frame temporal smoothing
         │    └──────┬──────┘
         │           ▼
         │    filtered depth_frame
         │    (+ update intrinsics if resolution changed)
         │
         ├──► color_frame → RGB8 image (1280x720)
         │    (stored for ground synthesis + visualization)
         │
         ├──► infrared_frame(1) → Left IR (1280x720 Y8)  *
         ├──► infrared_frame(2) → Right IR (1280x720 Y8) *
         │    (* when --neural-stereo enabled)
         │
         ├──► accel_frame → [ax, ay, az]  (m/s²)
         │
         └──► gyro_frame  → [gx, gy, gz]  (rad/s)
```

---

## Sample 090

**Source**: `D435i_LidarScan\FLOW.md` L410

```
Purpose: combine all depth sources for optimal coverage + quality.
Active when --neural-stereo and/or --mono-depth enabled.

Per-frame mono scale correction:
    mono_rel = 1.0 / inv_depth
    scale = median(stereo[overlap] / mono_rel[overlap])  (IQR robust)
    scale_ema = 0.1 * scale + 0.9 * scale_ema
    mono_metric = mono_rel * scale_ema

Texture map from IR:
    local_var = blur(IR²) - blur(IR)²     (7×7 kernel)
    low_texture = local_var < threshold    (default: 50)

3-level fusion:
    ┌──────────────────────────────────────────────────────┐
    │  1. stereo valid?         → built-in stereo (32mm)   │
    │  2. gap + low texture?    → mono metric   (smooth)   │
    │  3. gap + high texture?   → CREStereo     (metric)   │
    │  4. gap + fallback?       → whichever available      │
    └──────────────────────────────────────────────────────┘

Backward compatibility:
    --neural-stereo only        → CREStereo fills all gaps (v3 behavior)
    --mono-depth only           → mono fills all gaps
    --neural-stereo --mono-depth → texture-adaptive fusion
```

---

## Sample 091

**Source**: `D435i_LidarScan\FLOW.md` L454

```
Input: points[N, 3], rotation R[3, 3], LiDAR model specs

Step A: Load scan parameters from LiDAR model
    Model selected  → use model's FOV, resolution, range, n_steps
    Custom mode     → use CLI args, D435i native FOV (~87°)

Step B: Transform to ground-aligned frame
    aligned = R @ points.T  →  [N, 3]  (Y=up, XZ=ground)

Step C: Height filtering
    heights = aligned[:, 1]  (Y axis = height)
    keep where: height_min ≤ height ≤ height_max

    Example: 0.1m ≤ height ≤ 1.8m
    ┌─────────────┐ 1.8m  ← max
    │ /////////// │
    │ // KEEP /// │  ← obstacles in this height band
    │ /////////// │
    ├─────────────┤ 0.1m  ← min
    │  (ground)   │ 0.0m
    └─────────────┘

Step D: Project to 2D ground plane (XZ)
    x = filtered[:, 0]   (X axis)
    z = filtered[:, 2]   (Z axis = forward)

Step E: Convert to polar coordinates
    range = sqrt(x² + z²)
    angle = atan2(x, z)     ← angle from forward (Z), positive = right

Step F: Range filtering (using model specs)
    keep where: range_min ≤ range ≤ range_max

Step G: Discretize into angular bins (using model specs)
    Example (Hokuyo UST-10LX):
        angle_min = -135°, angle_max = +135°  (270° FOV)
        angle_increment = 0.25°
        n_bins = 1081

    bin_index = (angle - angle_min) / angle_increment
    For each bin: keep MINIMUM range (closest obstacle)

    D435i coverage: ~87° centered → fills ~348 of 1081 bins
    Remaining bins = inf (no data)

Output: LaserScan
    ├── angle_min, angle_max     (from model FOV)
    ├── angle_increment          (from model resolution)
    ├── range_min, range_max     (from model specs)
    ├── ranges[n_steps]          (meters, inf = no obstacle)
    └── model_name               (e.g., "Hokuyo UST-10LX")
```

---

## Sample 092

**Source**: `D435i_LidarScan\FLOW.md` L510

```
Input: points[N, 3], rotation R[3, 3]
Config: ground_angle (a), ground_angle_delta (d), ground_angle_tol (tol)

Step A: Transform to ground-aligned frame
    aligned = R @ points.T  →  [N, 3]  (Y=up, XZ=ground)
    x, y, z = aligned columns

Step B: Compute vertical angle below horizontal for each point
    h_dist = sqrt(x² + z²)             ← horizontal distance
    vert_angle = atan2(-y, h_dist)      ← angle below horizontal (deg)
                                           positive = downward

    Side view (ground-aligned frame):
        Camera ──── horizontal (0°) ──────
          ╲  ╲
     line0 ╲  ╲ line1
     (a°)   ╲  ╲ (a+d°)
              ╲  ╲
    ───────────P0─P1────── ground
               │   │
               d0  d1   ground hit distances: d = h / tan(angle)

Step C: Select points for each line (2 lines)
    Line 0: |vert_angle - a| ≤ tol        (e.g., 30° ± 0.3°)
    Line 1: |vert_angle - (a+d)| ≤ tol    (e.g., 32° ± 0.3°)

Step D: For each line, bin into horizontal angular bins
    HFOV = D435i native ~87°
    horiz_angle = atan2(x, z)
    slant_range = sqrt(x² + y² + z²)     ← 3D distance (not horizontal!)

    bin_index = (horiz_angle - angle_min) / angle_increment
    For each bin: keep MINIMUM range (closest)

Output: (LaserScan_line0, LaserScan_line1)
    Each with:
    ├── angle_min = -43.5°, angle_max = +43.5°  (D435i HFOV)
    ├── angle_increment = 0.25° (default)
    ├── ranges[n_bins]           (slant distance, meters)
    └── model_name               (e.g., "ground_line0_30.0deg")
```

---

## Sample 093

**Source**: `D435i_LidarScan\FLOW.md` L555

```
This system outputs raw scan data. Detection logic runs on AGV side.

─── How two lines reveal ground anomalies ───

Flat ground:                      Pit (hole):
    line0: ──────────────             line0: ──────╲    ╱──────
    line1: ──────────────             line1: ────────╲╱────────
    drange ≈ constant                 line0 range jumps (sees into pit)
                                      drange >> baseline

Bump (raised obstacle):           Slope / ramp:
    line0: ─────╱╲───────            line0: ──────────╲╲╲╲
    line1: ───╱╲─────────            line1: ──────────╲╲╲╲
    line1 hits bump first             both shift together
    drange << baseline                drange ≈ constant (not anomaly)

─── FOV constraint ───

D435i VFOV ≈ 58° (±29° from optical axis)
Camera tilt T° down → max ground_angle reachable = T + 29°

    tilt  0° → ground_angle max = 29°
    tilt 10° → ground_angle max = 39°    ← recommended
    tilt 20° → ground_angle max = 49°    ← horizontal LiDAR FOV narrows

For ground_angle = 30°, d = 2°:  need tilt ≥ 3° (easy)
For ground_angle = 45°, d = 2°:  need tilt ≥ 18° (significant)
```

---

## Sample 094

**Source**: `D435i_LidarScan\FLOW.md` L591

```
Binary protocol over UDP (default port 7777):

┌───────────────────────────────────────────┐
│ Header (40 bytes, little-endian)          │
├────────────┬──────────────────────────────┤
│ magic      │ "LS2D" (4 bytes)             │
│ timestamp  │ float64, Unix time (8 bytes) │
│ n_steps    │ uint32 (4 bytes)             │
│ angle_min  │ float32, radians (4 bytes)   │
│ angle_max  │ float32, radians (4 bytes)   │
│ angle_inc  │ float32, radians (4 bytes)   │
│ range_min  │ float32, meters (4 bytes)    │
│ range_max  │ float32, meters (4 bytes)    │
├────────────┴──────────────────────────────┤
│ Data                                      │
├───────────────────────────────────────────┤
│ ranges     │ float32[] (n_steps × 4 bytes)│
│            │ meters, range_max+1 = no data│
└───────────────────────────────────────────┘

Flow: LaserScan → pack header → replace inf → sendto(broadcast)
```

---

## Sample 095

**Source**: `D435i_LidarScan\FLOW.md` L649

```
600x600 black image, camera at center (300, 300)

┌──────────────────────────────────┐
│  FPS: 14.0  NS: 70ms             │
│  Model: Hokuyo UST-10LX          │
│  Height: 0.1m ~ 1.8m             │
│  Points: 87/1081                 │
│  Min range: 0.45m                │
│  Ground: 45/348 | 42/348        │  ← (when --ground-scan)
│       ╱╱                         │
│      ╱╱  D435i FOV (yellow)      │
│     ╱╱                           │
│   ╱  · ·                         │
│  ╱ ·     ·   ← green dots       │
│ ╱  · · · ·     (obstacles)       │
│╱     ◉  ← camera (yellow dot)  │
│╲                                 │
│ ╲                                │
│  ╲   LiDAR FOV (dark blue)       │
│     ○───○───○  range circles  │
│    1m  2m  3m                    │
│                                  │
│  D435i FOV  LiDAR FOV            │
│  D435i -> Hokuyo UST-10LX        │
└──────────────────────────────────┘

NS: neural stereo inference latency (shown when --neural-stereo)
```

---

## Sample 096

**Source**: `D435i_LidarScan\FLOW.md` L702

```
D435i USB 3.0
    │
    ├── Depth Stream (1280×720 @ 15fps)
    │       │
    │       ▼
    │   [Decimation] → [Threshold] → [Spatial] → [Temporal]
    │       │
    │       ▼
    │   depth_image (640x360 float32, meters)
    │       │
    │       ├──── [--neural-stereo/--mono-depth ON] ──────── ┐
    │       │     stereo_depth (numpy, ~11% coverage) │
    │       │         │ │
    │       │         ▼ │
    │       │     3-source texture-adaptive fusion: │
    │       │     ├── stereo valid → stereo    (32mm MAE) │
    │       │     ├── gap+smooth  → mono      (scaled) │
    │       │     └── gap+textured → CREStereo (metric) │
    │       │         │ │
    │       │         ▼ │
    │       │     fused_depth → _depth_to_points_from_array │
    │       │     → points [N, 3]  (~100% coverage) │
    │       │ │
    │       ├──── [--neural-stereo OFF] ────────────────┐ │
    │       │     Vectorized deprojection               │ │
    │       │     → real_points [N, 3]                  │ │
    │       │         │                                 │ │
    │       │         ├── [Emitter OFF] Ground synthesis │ │
    │       │         │   Color seg + plane eq           │ │
    │       │         │   → points = concat(real, synth) │ │
    │       │         │                                 │ │
    │       │         └── [Emitter ON] points = real     │ │
    │       │                                           │ │
    │       ├─── Camera height: stereo-only points (EMA)┘ │
    │       │ │
    │       ▼ │
    │   3D point cloud [N, 3] ◄───────────────────────────── ┘
    │       │
    │       ├────────────────────── ┐
    │       ▼                      ▼
    │   [LiDAR 1: Horizontal]  [LiDAR 2: Ground]
    │       │                      │
    │       ▼                      ▼
    │   Height filter          Vertical angle filter
    │   (0.1m ~ 1.8m)         (a° ± tol, (a+d)° ± tol)
    │       │                      │
    │       ▼                      ▼
    │   2D projection          Horizontal angular binning
    │   (XZ plane)             (slant range)
    │       │                      │
    │       ▼                      ▼
    │   Polar + binning        (LaserScan_0, LaserScan_1)
    │   (model specs)              │
    │       │                      ├──► UDP :7778 (line0)
    │       ▼                      └──► UDP :7779 (line1)
    │   LaserScan                  └──► ROS2 /ground_scan/*
    │       │
    │       ├──► OpenCV visualization
    │       ├──► UDP :7777 (broadcast)
    │       ├──► ROS2 /scan
    │       └──► Rerun 3D viewer
    │
    ├── Color Stream (1280×720 @ 15fps, RGB8)
    │       │
    │       ├── [--mono-depth] → MonoDepthEstimator.push_rgb()
    │       │       → background thread
    │       │       → resize → ImageNet norm → [1,3,210,364]
    │       │       → Depth Anything V2 ONNX (~77ms)
    │       │       → inverse depth (for fusion on next frame)
    │       │
    │       ├── [emitter OFF, no neural/mono] → ground point synthesis
    │       │
    │       └── Rerun camera image
    │
    ├── IR Left Stream (1280×720 @ 15fps, Y8)  *
    ├── IR Right Stream (1280×720 @ 15fps, Y8) *
    │       │  (* when --neural-stereo or --mono-depth)
    │       │
    │       ├── [--neural-stereo] NeuralStereoEstimator.push_ir_pair()
    │       │       → background thread
    │       │       → resize 1280×720 → 640×360
    │       │       → CREStereo ONNX inference (~70ms)
    │       │       → disparity → depth (baseline × fx / disp)
    │       │       → _latest_depth (for fusion on next frame)
    │       │
    │       └── [--mono-depth] → texture map (IR local variance)
    │
    ├── Accel Stream (63/250 Hz)
    │       │
    │       ▼
    │   GravityEstimator (low-pass alpha=0.98)
    │       │
    │       ▼
    │   Rotation matrix R [3×3] ──────────────────────────────
    │
    └── Gyro Stream (200/400 Hz)
            │
            └── (reserved for future complementary filter)
```

---

## Sample 097

**Source**: `D435i_LidarScan\README.md` L41

```
D435i Camera (emitter OFF)
    │
    ├── IR Left + Right ──► CREStereo ONNX (bg thread, ~70ms)
    │                       → metric depth (textured surfaces)
    │
    ├── Color RGB ────────► Depth Anything V2 ONNX (bg thread, ~77ms)
    │                       → relative inverse depth (smooth surfaces)
    │                       → per-frame scale correction from stereo overlap
    │
    ├── IR Left ──────────► Texture map (local variance)
    │                       low variance = smooth → use mono
    │                       high variance = textured → use CREStereo
    │
    ├── Built-in Stereo ──► Priority 1: stereo (32mm MAE, ~11%)
    │   (640x360)           Priority 2: mono on smooth gaps
    │                       Priority 3: CREStereo on textured gaps
    │                       Fallback: whichever available
    │                         │
    │                         ▼
    │                fused depth (640x360, ~100% coverage)
    │                         │
    └── IMU ──► Gravity ──► _depth_to_points → 3D point cloud
```

---

## Sample 098

**Source**: `D435i_LidarScan\README.md` L88

```
Side view:
    Camera ──── horizontal ────
      ╲  ╲
  line0 ╲  ╲ line1        Flat ground: both lines stable, Δrange ≈ constant
   (α°)  ╲  ╲ (α+Δ°)     Pit:  line0 range jumps → Δrange spikes
          ╲  ╲             Bump: line1 range drops → Δrange dips
───────────╲──╲──── ground
```

---

## Sample 099

**Source**: `D435i_LidarScan\README.md` L307

```
Side view (camera tilted ~10-20° down):

           Camera ──── horizontal (0°) ────────────────
             ╲  ╲
        line0 ╲  ╲ line1
     (α=30°)   ╲  ╲ (α+Δ=32°)
                 ╲  ╲
    ──────────────P0──P1────────────────── flat ground
                 │    │
                 d0   d1  ← ground hit distances

Geometry:
    d = camera_height / tan(α)
    P0 is farther from camera than P1 (shallower angle = farther)
    Spacing between P0 and P1 on ground = d0 - d1
```

---

## Sample 100

**Source**: `D435i_LidarScan\README.md` L331

```
Flat ground:                    Pit encountered:

line0: ─────────────────        line0: ────────╲    ╱──────
line1: ─────────────────        line1: ──────────╲╱────────
       (both stable,                   (line0 sees into pit first,
        Δrange ≈ constant)              Δrange spikes)

Bump encountered:               Slope / ramp:

line0: ─────╱╲──────────        line0: ──────────────╲╲╲
line1: ───╱╲────────────        line1: ──────────────╲╲╲
       (line1 hits bump first,         (both shift together,
        Δrange drops)                   Δrange ≈ constant)
```

---

## Sample 101

**Source**: `D435i_LidarScan\README.md` L422

```
D435i (single camera)
    │
    ├──► LiDAR 1: Horizontal 2D LiDAR
    │    ├── Simulates Hokuyo / RPLIDAR / SICK
    │    ├── Height range 0.1~1.8m compressed to single scan plane
    │    ├── For: obstacle avoidance, SLAM, navigation
    │    └── Output: UDP :7777 or ROS2 /scan
    │
    └──► LiDAR 2: Dual-Line Ground Scanner
         ├── Two scan lines at α° and (α+Δ)° below horizontal
         ├── Slant range (3D distance) per bin
         ├── For: AGV ground inspection (pit/bump detection)
         └── Output: UDP :7778/:7779 or ROS2 /ground_scan/line0, line1
```

---

## Sample 102

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L79

```
Color Frame (1280x720 RGB)
    │
    ▼
Resize → (364x210 或其他解析度)
    │
    ▼
ImageNet 正規化
  mean=[0.485, 0.456, 0.406]
  std =[0.229, 0.224, 0.225]
    │
    ▼
ONNX Inference (DmlExecutionProvider / CPU)
  Model: depth_anything_v2_small.onnx (INT8, ~27MB)
  Input: pixel_values [1, 3, H, W] float32
    │
    ▼
Output: predicted_depth [1, H, W]
  → 相對反向深度（relative inverse depth / disparity）
  → 非公制深度！需要 scale 校正
    │
    ▼
Resize to depth frame resolution
    │
    ▼
自動偵測反向深度 (correlation < 0 → 取倒數)
    │
    ▼
Scale / Affine 校正 (median ratio with stereo)
    │
    ▼
融合：stereo 有值用 stereo，無值用 mono
```

---

## Sample 103

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L233

```
D435i Camera (emitter OFF)
    │
    ├── IR Left (1280x720 Y8)
    ├── IR Right (1280x720 Y8)
    │         │
    │         ▼
    │   Resize 1280x720 → 640x360
    │   Gray → 3-channel [B, 3, H, W] float32
    │         │
    │   ┌─────┴─────┐
    │   │ CREStereo  │  ← ONNX, background thread
    │   │ iter2      │     ~70ms per inference
    │   │ 360x640    │     DirectML GPU / CPU fallback
    │   └─────┬─────┘
    │         │
    │   Output: flow [2, 360, 640]
    │   → take x-flow → abs() → disparity
    │         │
    │   Depth = baseline × fx / (disparity × scale_x)
    │     baseline ≈ 50.0mm (factory calibrated)
    │     fx ≈ 649.9px (at 1280x720)
    │     scale_x = 1280/640 = 2.0
    │         │
    │         ▼
    │   Neural depth map (640x360, float32, meters)
    │
    ├── Built-in Stereo (emitter OFF)
    │   → depth_frame → decimation → spatial → temporal
    │   → stereo depth (640x360, ~11% coverage, 32mm MAE)
    │         │
    │         ▼
    │   ┌─────────────────────────────────────────┐
    │   │ Fusion:                                 │
    │   │   fused[stereo > 0] = stereo  ← 優先   │
    │   │   fused[stereo = 0] = neural  ← 填補   │
    │   └─────────────────────────────────────────┘
    │         │
    │         ▼
    │   Fused depth map (640x360, ~100% coverage)
    │         │
    │   _depth_to_points_from_array()
    │   → 3D point cloud [N, 3]
    │
    └── IMU → Gravity → Rotation R
              → Ground-aligned coordinates
```

---

## Sample 104

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L285

```
┌─────────────────────────────────────────────────┐
│  Main Thread            Background Thread       │
│                                                 │
│  push_ir_pair(L, R)                             │
│       │                                         │
│       ▼                                        │
│  _pending_pair ──event──► _worker()            │
│                              │                  │
│                         Resize IR               │
│                         1280×720 → 640×360     │
│                         Gray → 3ch [B,3,H,W]   │
│                              │                  │
│                         ONNX inference          │
│                         (DML GPU or CPU)        │
│                              │                  │
│                         raw[0] → disparity     │
│                         (abs of x-flow)         │
│                              │                  │
│                         depth = baseline×fx/disp│
│                         → _latest_depth        │
│                              │                  │
│  get_latest_depth() ◄────────┘                 │
│       │                                         │
│  thread-safe (Lock)                             │
└─────────────────────────────────────────────────┘
```

---

## Sample 105

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L430

```
D435i Camera (emitter OFF) ──► Depth Frame ──► 3D Point Cloud ──► Ground-Aligned
                  IMU Frame  ──► Gravity Vector ──► Rotation Matrix ──┘
               Color Frame  ──► Floor Segmentation ──┐              │
           IR Left + Right  ──► CREStereo (ONNX) ───┤               │
                                                     │               │
                                           ┌─────────┴───────────────┴──┐
                                           ▼                            ▼
                                  [LiDAR 1: Horizontal]       [LiDAR 2: Ground]
                                   Height Filter → 2D Scan     Vertical Angle Filter
                                           │                   → 2 × LaserScan
                                   ┌───────┤                         │
                                   ▼       ▼                   ┌─────┴─────┐
                                 UDP:7777  ROS2:/scan          ▼           ▼
                                 OpenCV                     UDP:7778    UDP:7779
                                                            line0       line1
```

---

## Sample 106

**Source**: `D435i_LidarScan\REPORT_v3_depth_compensation.md` L450

```
┌────────────────────────────────────────────────────────────────────┐
│ Depth Source Priority                                              │
│                                                                    │
│ 1. --neural-stereo 啟用？                                          │
│    YES → Built-in stereo (priority) + CREStereo (fill)            │
│          → ~100% coverage                                         │
│          → emitter 強制 OFF                                       │
│          → 地面點合成停用                                         │
│                                                                    │
│ 2. --emitter OFF？                                                 │
│    YES → Built-in stereo (~11%) + 地面點合成 (color segmentation) │
│          → 有色地板區域補點                                       │
│                                                                    │
│ 3. --emitter ON                                                    │
│    → Built-in stereo (~62%) 直接使用                              │
│    → 最簡單，但半導體廠不可用                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Sample 107

**Source**: `D435I_LidarScan_v1\D435i_DepthCompletion_CLAUDE.md` L45

```
D435i（IR Emitter OFF）
    │
    ├─ RGB stream (color)
    ├─ Left IR stream  (emitter off → passive texture only)
    ├─ Right IR stream
    └─ Stereo Depth stream (sparse + holes in featureless regions)
         │
         ▼
  [Stage 1] librealsense Post-processing Filters
  Spatial filter + Temporal filter + Hole-filling filter
  → 快速修補小孔洞，零 AI 成本
         │
         ▼
  [Stage 2] AI Depth Completion
  Input:  RGB image  +  sparse depth (from Stage 1)
  Model:  SparseDC 或 NLSPN（依速度需求選擇）
  Output: Dense depth map
         │
         ▼  （Stage 2 仍有大片 invalid 時的 fallback）
  [Stage 3] Monocular Depth Estimation（選配）
  Input:  RGB image only
  Model:  Depth Anything V2 Small（metric depth）
  用途:   補全 Stage 2 剩餘孔洞，scale 對齊後融合
         │
         ▼
  最終 Dense Depth Map → 障礙物偵測 / Costmap
```

---

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

## Sample 109

**Source**: `D435i_LidarScan_v2\CLAUDE.md` L15

```
D435i (Emitter OFF, manual exposure for metal reflections)
  │
  ├─ RGB + Depth (Z16 → CUDA Float32 Tensor)
  │
  ▼
[Stage 1] Foundation — Rerun streaming (RGB, Depth, Time-sequence), CUDA buffer init
  ▼
[Stage 2] SDK Pre-processing — Decimation → Spatial → Temporal → Hole Filling filters
  ▼
[Stage 3] YOLO Semantic Detection (TensorRT) — BBox + Mask for walls/floors/steel equipment
  ▼
[Stage 4] Geometric Completion — CUDA RANSAC plane fitting within YOLO regions, fill zeros with plane equation
  ▼
[Stage 5] Neural Refinement — NLSPN or Depth Anything V2 Small, RGB+sparse depth fusion, weighted residual correction
  ▼
[Stage 6] Output — Camera→Base Link transform, Voxel Grid downsampling, .pcd or ROS2 PointCloud2 broadcast
```

---

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

## Sample 111

**Source**: `D455_LidarScan\FLOW.md` L7

```
Lines    Module
──────   ──────────────────────────────
1-8      Module docstring
10-19    Imports (standard library)
21-23    Imports (pyrealsense2, numpy, opencv)
25-37    Optional imports (rclpy, rerun, onnxruntime)
40-99    LIDAR_MODELS dict (5 presets)
101      D455_HFOV_DEG = 86.0
104-112  LaserScan dataclass
116-151  UDPOutput class
153-186  ROS2Output class
188-238  GravityEstimator class
240-380  NeuralStereoEstimator class (CREStereo ONNX)
382-413  D455LidarScanner.__init__() + start()
415-520  D455LidarScanner.start() (pipeline, sensor config, neural stereo, filters)
522-527  D455LidarScanner._build_pixel_grid()
529-532  D455LidarScanner.stop()
534-588  D455LidarScanner._get_frames()
589-608  D455LidarScanner._depth_to_points()
610-624  D455LidarScanner._depth_to_points_from_array()
626-651  D455LidarScanner._estimate_camera_height()
653-671  D455LidarScanner._fill_depth_gaps()
673-757  D455LidarScanner._points_to_scan()
759-814  D455LidarScanner._points_to_ground_lines()
816-900  D455LidarScanner.process_frame()
902-972  draw_scan() — OpenCV 2D visualization
974-1069 RerunLogger class
1072-1341 main() — CLI args + main loop
```

---

## Sample 112

**Source**: `D455_LidarScan\FLOW.md` L40

```
main()
 │
 ├── Parse CLI args (argparse)
 ├── Init network outputs (UDP/ROS2)
 ├── Init RerunLogger (optional)
 ├── Create D455LidarScanner(args)
 │    ├── pipeline = rs.pipeline()
 │    ├── GravityEstimator(alpha=0.98)
 │    └── Post-processing filters (decimation, spatial, temporal, threshold)
 │
 ├── scanner.start()
 │    ├── config.enable_stream(depth, 1280x720, z16, 30fps)
 │    ├── config.enable_stream(color, 1280x720, rgb8, 30fps)
 │    ├── (if --neural-stereo) config.enable_stream(infrared 1 & 2, y8)
 │    ├── config.enable_stream(accel)
 │    ├── config.enable_stream(gyro)
 │    ├── pipeline.start(config)
 │    ├── Configure sensor (emitter, preset)
 │    ├── (if --neural-stereo) force emitter OFF
 │    ├── (if --neural-stereo) read IR intrinsics + stereo baseline
 │    ├── (if --neural-stereo) init NeuralStereoEstimator (ONNX background thread)
 │    ├── Configure filters (decimation, spatial, temporal, threshold)
 │    ├── Get depth intrinsics (fx, fy, ppx, ppy)
 │    └── Precompute pixel grid (_u_grid, _v_grid)
 │
 └── Main loop:
      │
      ├── scanner.process_frame()
      │    │
      │    ├── _get_frames()
      │    │    ├── pipeline.wait_for_frames()
      │    │    ├── get_depth_frame()
      │    │    ├── Apply filters: decimation → threshold → spatial → temporal
      │    │    ├── Update intrinsics if decimation changed resolution
      │    │    ├── Extract color frame → _last_color_image
      │    │    ├── (if neural stereo) Extract IR left/right → _last_ir_left/right
      │    │    └── Extract IMU: accel_data, gyro_data
      │    │
      │    ├── gravity_estimator.update(accel)
      │    │    └── Low-pass filter: g = α*g + (1-α)*accel
      │    │
      │    ├── gravity_estimator.get_rotation_matrix()
      │    │    ├── Normalize gravity → Y_up axis
      │    │    ├── Project camera forward → Z_forward axis
      │    │    ├── Cross product → X_right axis
      │    │    └── Return R = [X; Y; Z] rotation matrix
      │    │
      │    ├── _depth_to_points(depth_frame) → real_points
      │    │    ├── depth_image * depth_scale → z (meters)
      │    │    ├── x = (u - ppx) * z / fx  (vectorized)
      │    │    ├── y = (v - ppy) * z / fy  (vectorized)
      │    │    └── Return Nx3 points [x, y, z] in camera frame
      │    │
      │    ├── (if auto height) _estimate_camera_height(real_points)
      │    │    ├── aligned = R @ points.T → ground-aligned frame
      │    │    ├── Select nearby points (0.5m < h_dist < 4.0m)
      │    │    ├── ground_y = percentile(Y, 15th)
      │    │    └── EMA smooth: h = 0.05*new + 0.95*old
      │    │
      │    ├── (if --neural-stereo) Depth Fusion:
      │    │    ├── push IR pair to NeuralStereoEstimator (non-blocking)
      │    │    ├── get_latest_depth() → neural_depth, neural_ms
      │    │    ├── if neural_depth available:
      │    │    │    ├── stereo_depth = depth_frame → float32 meters
      │    │    │    ├── fused = stereo_depth.copy()
      │    │    │    ├── gap = ~stereo_valid
      │    │    │    ├── fill_neural = gap & neural_valid
      │    │    │    ├── fused[fill_neural] = neural_depth[fill_neural]
      │    │    │    ├── (if not --no-fill-depth) _fill_depth_gaps(fused)
      │    │    │    │    ├── Diamond dilation [3,5,7,11,15,23]
      │    │    │    │    └── Bilateral filter (preserve edges)
      │    │    │    └── points = _depth_to_points_from_array(fused)
      │    │    └── else: points = real_points (first few frames)
      │    │
      │    ├── _points_to_scan(points, rotation) → LaserScan
      │    │    ├── aligned = R @ points.T → [X_right, Y_up, Z_forward]
      │    │    ├── Height filter: height_min ≤ (camera_height + Y) ≤ height_max
      │    │    ├── Polar: angles = atan2(X, Z), ranges = √(X²+Z²)
      │    │    ├── Range filter: range_min ≤ r ≤ range_max
      │    │    ├── Bin: indices = (angle - angle_min) / angle_increment
      │    │    └── np.minimum.at(scan_ranges, indices, ranges)
      │    │
      │    └── (if --ground-scan) _points_to_ground_lines(points, rotation)
      │         ├── aligned = R @ points.T
      │         ├── vert_angles = degrees(atan2(-Y, h_dist))
      │         ├── For each line (α, α+Δ):
      │         │    ├── mask = |vert_angle - target| ≤ tolerance
      │         │    ├── horiz_angles = atan2(X, Z)
      │         │    ├── slant_ranges = √(X² + Y² + Z²)
      │         │    └── np.minimum.at(scan_ranges, indices, slant_ranges)
      │         └── Return (LaserScan_line0, LaserScan_line1)
      │
      ├── net_output.send(scan)              # UDP/ROS2
      ├── ground_outputs[0/1].send(lines)    # if ground scanner
      ├── rerun_logger.log_frame(...)        # if --rerun
      │
      ├── (if --no-viz) print status line
      └── (else) draw_scan() → cv2.imshow()
           ├── Range circles (1m, 2m, ...)
           ├── LiDAR model FOV lines (dark blue)
           ├── D455 FOV wedge (yellow)
           ├── Camera position (yellow dot)
           └── Scan points (green dots)
```

---

## Sample 113

**Source**: `D455_LidarScan\FLOW.md` L160

```
D455 Camera
    │
    ├── Depth (z16, 1280x720 @ 30fps)
    │    ├── Decimation (÷2 → 640x360)
    │    ├── Threshold (0.6-6.0m)
    │    ├── Spatial (edge-preserving smooth)
    │    ├── Temporal (inter-frame smooth)
    │    └── Vectorized deprojection → Nx3 point cloud
    │
    ├── IR Left/Right (y8, 1280x720 @ 30fps) [if --neural-stereo]
    │    └── CREStereo ONNX (background thread)
    │         ├── Resize to model resolution (640x360)
    │         ├── Disparity bias correction (ratio LUT)
    │         ├── Disparity → metric depth (baseline * fx / disp)
    │         └── Fusion: stereo base + neural fills gaps
    │              └── IP-Basic gap filling (dilation + bilateral)
    │
    ├── Color (rgb8, 1280x720 @ 30fps) → Rerun camera image
    │
    ├── Accelerometer → GravityEstimator → Rotation Matrix
    │
    └── Point cloud + Rotation
         │
         ├── Auto camera height (EMA, 15th percentile)
         │
         ├──► LiDAR 1: Height filter → 2D polar → LaserScan
         │    └── Output: OpenCV / Rerun / UDP / ROS2
         │
         └──► LiDAR 2: Vertical angle filter → Dual LaserScan
              └── Output: Rerun / UDP / ROS2
```

---

## Sample 114

**Source**: `D455_LidarScan\plan.md` L46

```
D455_LidarScan/
├── d455_lidar_scan.py      # 主程式 (single-file)
├── requirements.txt        # 依賴套件
├── README.md               # 使用者文件
├── CLAUDE.md               # 專案架構/慣例
├── FLOW.md                 # 程式流程 (code 完成後)
└── .gitignore
```

---

## Sample 115

**Source**: `D455_LidarScan\README.md` L29

```
Side view:
    Camera ──── horizontal ────
      ╲  ╲
  line0 ╲  ╲ line1        Flat ground: both lines stable, Δrange ≈ constant
   (α°)  ╲  ╲ (α+Δ°)     Pit:  line0 range jumps → Δrange spikes
          ╲  ╲             Bump: line1 range drops → Δrange dips
───────────╲──╲──── ground
```

---

## Sample 116

**Source**: `D455_LidarScan\README.md` L250

```
Flat ground:                    Pit encountered:

line0: ─────────────────        line0: ────────╲    ╱──────
line1: ─────────────────        line1: ──────────╲╱────────
       (both stable,                   (line0 sees into pit first,
        Δrange ≈ constant)              Δrange spikes)

Bump encountered:               Slope / ramp:

line0: ─────╱╲──────────        line0: ──────────────╲╲╲
line1: ───╱╲────────────        line1: ──────────────╲╲╲
       (line1 hits bump first,         (both shift together,
        Δrange drops)                   Δrange ≈ constant)
```

---

## Sample 117

**Source**: `D455_LidarScan\README.md` L278

```
D455 (single camera)
    │
    ├──► LiDAR 1: Horizontal 2D LiDAR
    │    ├── Simulates Hokuyo / RPLIDAR / SICK
    │    ├── Height range 0.1~1.8m compressed to single scan plane
    │    ├── For: obstacle avoidance, SLAM, navigation
    │    └── Output: UDP :7777 or ROS2 /scan
    │
    └──► LiDAR 2: Dual-Line Ground Scanner
         ├── Two scan lines at α° and (α+Δ)° below horizontal
         ├── Slant range (3D distance) per bin
         ├── For: AGV ground inspection (pit/bump detection)
         └── Output: UDP :7778/:7779 or ROS2 /ground_scan/line0, line1
```

---

## Sample 118

**Source**: `D455_LidarScan\README_temp.md` L41

```
D435i Camera (emitter OFF)
    │
    ├── IR Left + Right ──► CREStereo ONNX (bg thread, ~70ms)
    │                       → metric depth (textured surfaces)
    │
    ├── Color RGB ────────► Depth Anything V2 ONNX (bg thread, ~77ms)
    │                       → relative inverse depth (smooth surfaces)
    │                       → per-frame scale correction from stereo overlap
    │
    ├── IR Left ──────────► Texture map (local variance)
    │                       low variance = smooth → use mono
    │                       high variance = textured → use CREStereo
    │
    ├── Built-in Stereo ──► Priority 1: stereo (32mm MAE, ~11%)
    │   (640x360)           Priority 2: mono on smooth gaps
    │                       Priority 3: CREStereo on textured gaps
    │                       Fallback: whichever available
    │                         │
    │                         ▼
    │                fused depth (640x360, ~100% coverage)
    │                         │
    └── IMU ──► Gravity ──► _depth_to_points → 3D point cloud
```

---

## Sample 119

**Source**: `D455_LidarScan\README_temp.md` L87

```
Side view:
    Camera ──── horizontal ────
      ╲  ╲
  line0 ╲  ╲ line1        Flat ground: both lines stable, Δrange ≈ constant
   (α°)  ╲  ╲ (α+Δ°)     Pit:  line0 range jumps → Δrange spikes
          ╲  ╲             Bump: line1 range drops → Δrange dips
───────────╲──╲──── ground
```

---

## Sample 120

**Source**: `D455_LidarScan\README_temp.md` L305

```
Side view (camera tilted ~10-20° down):

           Camera ──── horizontal (0°) ────────────────
             ╲  ╲
        line0 ╲  ╲ line1
     (α=30°)   ╲  ╲ (α+Δ=32°)
                 ╲  ╲
    ──────────────P0──P1────────────────── flat ground
                 │    │
                 d0   d1  ← ground hit distances

Geometry:
    d = camera_height / tan(α)
    P0 is farther from camera than P1 (shallower angle = farther)
    Spacing between P0 and P1 on ground = d0 - d1
```

---

## Sample 121

**Source**: `D455_LidarScan\README_temp.md` L329

```
Flat ground:                    Pit encountered:

line0: ─────────────────        line0: ────────╲    ╱──────
line1: ─────────────────        line1: ──────────╲╱────────
       (both stable,                   (line0 sees into pit first,
        Δrange ≈ constant)              Δrange spikes)

Bump encountered:               Slope / ramp:

line0: ─────╱╲──────────        line0: ──────────────╲╲╲
line1: ───╱╲────────────        line1: ──────────────╲╲╲
       (line1 hits bump first,         (both shift together,
        Δrange drops)                   Δrange ≈ constant)
```

---

## Sample 122

**Source**: `D455_LidarScan\README_temp.md` L420

```
D435i (single camera)
    │
    ├──► LiDAR 1: Horizontal 2D LiDAR
    │    ├── Simulates Hokuyo / RPLIDAR / SICK
    │    ├── Height range 0.1~1.8m compressed to single scan plane
    │    ├── For: obstacle avoidance, SLAM, navigation
    │    └── Output: UDP :7777 or ROS2 /scan
    │
    └──► LiDAR 2: Dual-Line Ground Scanner
         ├── Two scan lines at α° and (α+Δ)° below horizontal
         ├── Slant range (3D distance) per bin
         ├── For: AGV ground inspection (pit/bump detection)
         └── Output: UDP :7778/:7779 or ROS2 /ground_scan/line0, line1
```

---

## Sample 123

**Source**: `draft-draw\SESSION_NOTES.md` L18

```
C:\Users\benth\Documents\GitHub\draft-draw\
├── generate_images.py          # Gemini Imagen API image generation script
├── generate_prompts.py         # Gemini Vision API batch prompt generation script
├── filter_by_date.py           # Date filter: .images_full → .images_main
├── SESSION_NOTES.md            # This file
├── .generate_prompts_checkpoint.json  # Prompt generation checkpoint/resume
├── .generate_prompts.log       # Prompt generation log file
├── .images_full/               # Original 188,431 images (READ-ONLY source)
│   ├── 00_其他/
│   ├── 01_產品介紹/
│   ├── 02_工程圖面/
│   ├── 03_技術規格/
│   ├── 04_認證標準/
│   ├── 05_電池充電/
│   ├── 06_系統軟體/
│   ├── 07_客戶提案/
│   ├── 08_安全規範/
│   ├── 09_操作手冊/
│   ├── 10_報告分析/
│   └── skipped_files.txt
├── .images_sample/             # 50 sample images + 50 .md prompts + 38 generated images
│   └── (same subdirectory structure)
├── detect_text_images.py        # Text/blank image detection and removal
├── .images_main/               # Filtered working directory: 73,058 visual images (2021+, text removed)
│   └── (same subdirectory structure)
├── .images_main_scan_results.csv  # Full scan classification results
├── .images_main_deleted.log       # Log of deleted file paths
└── .claude/
    └── settings.local.json
```

---

## Sample 124

**Source**: `draft-forge\DOC_image_extraction_and_classification.md` L26

```
D:\benth\Documents\機器人專案\06_AGV     .images_full/
  7,433 個文件                             188,431 張圖片
  (pptx, pdf, docx, ppt, doc)              ├── 01_產品介紹/  18,557
                                            ├── 02_工程圖面/  14,809
  ┌─────────┐   ┌──────────┐   ┌────────┐  ├── 03_技術規格/  24,071
  │ sample  │──>│ extract  │──>│classify│  ├── 04_認證標準/  22,359
  │ _files  │   │ _images  │   │_images │  ├── 05_電池充電/   8,004
  └─────────┘   └──────────┘   └────┬───┘  ├── 06_系統軟體/  27,569
   50 個取樣     多進程擷取      關鍵字  │  ├── 07_客戶提案/  13,906
                                 分類   │  ├── 08_安全規範/   3,136
                               ┌────────┘  ├── 09_操作手冊/  24,019
                               │           ├── 10_報告分析/  29,932
                          ┌────┴───┐       └── 00_其他/       2,069
                          │  ai    │
                          │classify│
                          └────────┘
                          Gemini Vision
                          再分類 00_其他
```

---

## Sample 125

**Source**: `draft-forge\DOC_image_extraction_and_classification.md` L291

```
.images_full/
├── 01_產品介紹/     (18,557 files)  產品型錄、公司簡介
├── 02_工程圖面/     (14,809 files)  CAD 圖面、3D 模型、機構設計
├── 03_技術規格/     (24,071 files)  規格書、Datasheet
├── 04_認證標準/     (22,359 files)  SEMI/CE/RoHS/IEC/ISO 認證文件
├── 05_電池充電/      (8,004 files)  電池、充電系統
├── 06_系統軟體/     (27,569 files)  TSC/MCS/導航/派車軟體
├── 07_客戶提案/     (13,906 files)  提案、報價、會議記錄
├── 08_安全規範/      (3,136 files)  安全規範、風險評估
├── 09_操作手冊/     (24,019 files)  操作手冊、訓練教材
├── 10_報告分析/     (29,932 files)  報告、分析、測試
└── 00_其他/          (2,069 files)  無法歸類的圖片
```

---

## Sample 126

**Source**: `hacker_v0\cameras\CAMERAS.md` L79

```
cameras/captures/
├── cam_192_168_200_75.png      # 主串流截圖
├── cam_192_168_200_77.png
├── cam_192_168_200_78.png
├── cam_192_168_200_79.png
├── cam_192_168_200_80.png
├── cam_192_168_200_81.png
├── cam_192_168_200_82.png
├── cam_192_168_200_75_sub.png  # 副串流截圖
├── cam_192_168_200_77_sub.png
├── cam_192_168_200_78_sub.png
├── cam_192_168_200_79_sub.png
├── cam_192_168_200_80_sub.png
├── cam_192_168_200_81_sub.png
└── cam_192_168_200_82_sub.png
```

---

## Sample 127

**Source**: `hacker_v0\README.md` L20

```
scanners/
├── network_scan.py      # 網段存活主機 & 開放 Port 偵測
├── default_creds.py     # 常見設備預設帳密檢測
├── smb_check.py         # SMB 弱點 & 匿名存取檢查
├── arp_monitor.py       # ARP 異常偵測（spoofing）
├── rogue_dhcp.py        # 偽冒 DHCP Server 偵測
└── ot_protocol_check.py # Modbus/OPC UA 暴露檢測
```

---

## Sample 128

**Source**: `hacker_v0\reports\scan_2026-04-10.md` L175

```
Internet
  │
  ├─ 192.168.4.2~5 (4x UniFi Dream Machine SE)
  │   ├─ 192.168.230.0/24  Wi-Fi（辦公 + IoT）
  │   ├─ 192.168.40.0/24   AMR 專網 B
  │   ├─ 192.168.50.0/24   AMR 專網 A
  │   ├─ 192.168.60.0/24   AMR 專網 C
  │   ├─ 192.168.200.0/24  監控網段（7 台 Hipcam + Synology Router）
  │   ├─ 192.168.2.0/24    管理用
  │   └─ 192.168.20.0/24   管理用
  │
  └─ ZeroTier VPN (10.63.138.0/24) — overlay，各設備自行加入
```

---

## Sample 129

**Source**: `HaloScan_v0\cameras\CAMERAS.md` L79

```
cameras/captures/
├── cam_192_168_200_75.png      # 主串流截圖
├── cam_192_168_200_77.png
├── cam_192_168_200_78.png
├── cam_192_168_200_79.png
├── cam_192_168_200_80.png
├── cam_192_168_200_81.png
├── cam_192_168_200_82.png
├── cam_192_168_200_75_sub.png  # 副串流截圖
├── cam_192_168_200_77_sub.png
├── cam_192_168_200_78_sub.png
├── cam_192_168_200_79_sub.png
├── cam_192_168_200_80_sub.png
├── cam_192_168_200_81_sub.png
└── cam_192_168_200_82_sub.png
```

---

## Sample 130

**Source**: `HaloScan_v0\docs\01_會議計畫書_v0.md` L17

```
4× Livox Mid-360 (各 200K pts/s，合計 ~800K pts/s)
│
├─── 路徑 A：安全區偵測（本專案核心）
│    │
│    TF transform（sensor frame → /base_link，含 pitch offset）
│    │
│    C++ 安全區判定（PCL CropBox / 手寫座標閾值）
│    ├── 4 核心各處理 1 顆 LiDAR（std::thread / OpenMP）
│    ├── 定義 3D Bounding Box：停止區、減速區、懸崖區
│    └── 點落在危險區 → 計數超過雜訊閾值 → 觸發狀態
│    │
│    統整 4 顆結果 → 發佈 std_msgs/Int8
│    │        0 = 安全 ／ 1 = 減速 ／ 2 = 停止
│    │
│    RPi 5 ──(ROS Topic via Switch)──→ IPC (ROS Master 訂閱)
│                                       └─ 0.5s watchdog timeout
│                                          未收到 → 強制停車
│
└─── 路徑 B：導航避障（沿用既有導航架構）
     │
     TF transform → PassThrough filter (z: 0.00~1.80m)
     │
     ConcatenatePointCloud（合併 4 組）
     │
     pointcloud_to_laserscan（最近距離投影 → 2D）
     │
     /scan（sensor_msgs/LaserScan，10 Hz，360°）
     │
     Nav2 Costmap ／ 導航軟體消費
```

---

## Sample 131

**Source**: `HaloScan_v0\docs\01_會議計畫書_v0.md` L101

```
         前方 FRONT
              ↑
    [FL]──────────[FR]
  +45°│            │-45°
      │   車體中心  │
      │      +      │
 +135°│            │-135°
    [RL]──────────[RR]

  * 每顆同時向下傾斜 15～25°
```

---

## Sample 132

**Source**: `HaloScan_v0\docs\01_會議計畫書_v0.md` L149

```
        側視圖（車體右前角）

        機械手臂活動範圍
        ┊
┌───────┴───────────────┐
│    白色設備櫃         │
│                       │
├───────────────────────┤ ← 底盤與櫃體交界
│ 底盤台階突出區 ●       │ ← ● Mid-360 候選位置
│               ■       │ ← ■ 現有安全 LiDAR
└───────────────────────┘
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  地面
```

---

## Sample 133

**Source**: `HaloScan_v0\docs\01_會議計畫書_v0.md` L183

```
Mid-360 FL ─── 192.168.1.101 ──┐
Mid-360 FR ─── 192.168.1.102 ──┤
Mid-360 RL ─── 192.168.1.103 ──├── Unmanaged GbE 5-port Switch
Mid-360 RR ─── 192.168.1.104 ──┤
RPi 5 ──────── 192.168.1.10  ──┘
```

---

## Sample 134

**Source**: `HaloScan_v0\docs\02_會議計畫書_v1.md` L18

```
4× Livox Mid-360 (各 200K pts/s，合計 ~800K pts/s)
│
├─── 路徑 A：安全區偵測（本專案核心）
│    │
│    TF transform（sensor frame → /base_link，含 pitch offset）
│    │
│    C++ 安全區判定（PCL CropBox / 手寫座標閾值）
│    ├── 4 核心各處理 1 顆 LiDAR（std::thread / OpenMP）
│    ├── 定義 3D Bounding Box：停止區、減速區、懸崖區
│    └── 點落在危險區 → 計數超過雜訊閾值 → 觸發狀態
│    │
│    統整 4 顆結果 → 發佈 std_msgs/Int8
│    │        0 = 安全 ／ 1 = 減速 ／ 2 = 停止
│    │
│    RPi 5 ──(ROS Topic via Switch)──→ IPC (ROS Master 訂閱)
│                                       └─ 0.5s watchdog timeout
│                                          未收到 → 強制停車
│
└─── 路徑 B：導航避障（沿用既有導航架構）
     │
     TF transform → PassThrough filter (z: 0.00~1.80m)
     │
     ConcatenatePointCloud（合併 4 組）
     │
     pointcloud_to_laserscan（最近距離投影 → 2D）
     │
     /scan（sensor_msgs/LaserScan，10 Hz，360°）
     │
     Nav2 Costmap ／ 導航軟體消費
```

---

## Sample 135

**Source**: `HaloScan_v0\docs\02_會議計畫書_v1.md` L102

```
         前方 FRONT
              ↑
    [FL]──────────[FR]
  +45°│            │-45°
      │   車體中心  │
      │      +      │
 +135°│            │-135°
    [RL]──────────[RR]

  * 每顆同時向下傾斜 15～25°
```

---

## Sample 136

**Source**: `HaloScan_v0\docs\02_會議計畫書_v1.md` L152

```
        側視圖（車體右前角）

        機械手臂活動範圍
        ┊
┌───────┴───────────────┐
│    白色設備櫃         │
│                       │
├───────────────────────┤ ← 底盤與櫃體交界
│ 底盤台階突出區 ●       │ ← ● Mid-360 候選位置
│               ■       │ ← ■ 現有安全 LiDAR
└───────────────────────┘
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  地面
```

---

## Sample 137

**Source**: `HaloScan_v0\docs\02_會議計畫書_v1.md` L187

```
Mid-360 FL ─── 192.168.1.101 ──┐
Mid-360 FR ─── 192.168.1.102 ──┤
Mid-360 RL ─── 192.168.1.103 ──├── Unmanaged GbE 5-port Switch
Mid-360 RR ─── 192.168.1.104 ──┤
RPi 5 ──────── 192.168.1.10  ──┘
```

---

## Sample 138

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L41

```
                    前方 FRONT
                         ↑
           [FL]────[📷 Front]────[FR]
          +45° ●                  ● -45°
               │                  │
         [📷]  │    車體中心       │  [📷]
         Left  │       +          │  Right
               │                  │
         +135° ●                  ● -135°
           [RL]────[📷 Rear]─────[RR]
                    
   ● = Livox Mid-360 LiDAR（角落，斜 45° 朝外，向下傾斜 20°）
   📷 = 魚眼相機（面中央，水平朝外，微向下 5-10°）
```

---

## Sample 139

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L72

```
俯視圖 — 覆蓋示意

              Front 魚眼 FOV (>185°)
                 ╱ ─ ─ ─ ╲
           FL ● ╱           ╲ ● FR
              ╲ LiDAR FOV 重疊區 ╱
               ╲      ↑      ╱
     Left 魚眼 ←│  車體中心  │→ Right 魚眼
               ╱      ↓      ╲
              ╱  LiDAR FOV 重疊區╲
           RL ● ╲           ╱ ● RR
                 ╲ ─ ─ ─ ╱
              Rear 魚眼 FOV (>185°)
```

---

## Sample 140

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L139

```
┌─────────────────────────────────────────────────────┐
│                    IPC（工業電腦）                  │
│  ┌──────────────┐ ┌──────────────┐  ┌─────────────┐ │
│  │ Nav2 Costmap │  │  決策引擎     │  │ 影像記錄/HMI │ │
│  └──────────────┘ └──────┬───────┘  └─────────────┘ │
│         │  /scan         │ 安全碼 + 語意標籤        │
└─────────┼────────────────┼──────────────────────────┘
          │                │
  ┌───────┴────────┐  ┌───┴───────────────────────┐
  │   RPi 5        │  │   Jetson Orin（新增） │
  │ ┌─────────────┐ │  │ ┌────────────────────────┐ │
  │ │路徑 A 安全  │ │  │ │路徑 C 視覺感知         │ │
  │ │CropBox      │ │  │ │魚眼語意分割 + 融合     │ │
  │ │4x LiDAR     │ │  │ │4x 魚眼相機             │ │
  │ └─────────────┘ │  │ └────────────────────────┘ │
  │       │Int8    │  │            │語意標籤 │
  └───────┼────────┘  └────────────┼───────────────┘
          │                        │
          ▼                        ▼
    IPC Watchdog              導航/決策參考
   （0.5s timeout）          （非 safety-critical）
```

---

## Sample 141

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L187

```
4x 魚眼相機（USB3）
│
├─ 魚眼影像前處理（去畸變 / 等距投影正規化）
│
├─ 語意分割推論（YOLOv8-seg / ERFNet）
│  輸出：每個 pixel 的類別標籤
│  類別：人員 / AGV / 台車 / 物料 / FOUP / 地板 / 牆壁 / 未知
│
├─ 3D 投影匹配
│  LiDAR 點雲 → 座標轉換 → 投影至魚眼影像平面
│  每個 3D 點獲得對應的語意標籤
│
├─ 標記融合
│  將語意標記的 3D 點雲與 CropBox 安全區交叉比對
│  輸出：安全區內物件的類別資訊
│
└─ 發佈 ROS Topic
   /perception/labeled_objects  (custom msg: 類別 + 位置 + 信心度)
   /perception/fisheye_images   (sensor_msgs/CompressedImage, 事件觸發時記錄)
```

---

## Sample 142

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L226

```
RPi 5                          Jetson Orin
┌──────────┐                   ┌──────────────┐
│ LiDAR ×4 │──(PointCloud2)──→│ 3D 投影匹配  │
│          │                   │              │
│ CropBox  │──(Int8 安全碼)──→ │ 融合標記    │
│ 判定     │                   │              │
└──────────┘                   │ 魚眼 ×4      │
                               │ 語意分割      │
                               └──────┬───────┘
                                      │
                               (labeled_objects)
                                      │
                                      ▼
                               ┌──────────────┐
                               │     IPC      │
                               │ 決策引擎     │
                               │ 影像記錄     │
                               └──────────────┘
```

---

## Sample 143

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L404

```
                    4× Livox Mid-360（角落安裝）
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌──────────┐
│路徑 A   │    │路徑 B     │    │路徑 C  │
│安全偵測  │    │導航避障   │    │視覺感知   │ ← 本提案新增
│         │    │          │    │          │
│CropBox  │    │LaserScan │    │語意分割  │
│C++ / RPi│    │ROS2 / RPi│    │DNN/Jetson│
│         │    │          │    │          │
│Int8     │    │/scan     │    │labeled   │
│安全碼    │    │Nav2      │    │objects  │
└────┬────┘    └────┬─────┘    └────┬─────┘
     │              │               │
     ▼              ▼               ▼
┌─────────────────────────────────────────┐
│              IPC（工業電腦）            │
│                                         │
│  安全碼 → Watchdog → 停車/減速控制    │
│  /scan  → Nav2 Costmap → 路徑規劃     │
│  語意   → 決策引擎 → 差異化安全策略（未來） │
│  影像   → 事件記錄 → 事後分析         │
└─────────────────────────────────────────┘
```

---

## Sample 144

**Source**: `HaloScan_v0\docs\04_Mid360_技術計畫_初版.md` L122

```
         前方 FRONT
              ↑
    [FL]──────────[FR]
  +45°│            │-45°
      │   車體中心  │
      │      +      │
 +135°│            │-135°
    [RL]──────────[RR]

* 每顆感測器同時向下傾斜 15～25°（側視方向）
```

---

## Sample 145

**Source**: `HaloScan_v0\docs\04_Mid360_技術計畫_初版.md` L150

```
livox_ros_driver2（× 4，各感測器獨立 topic）
      │
TF transform（sensor frame → /base_link，含 pitch offset）
      │
PassThrough filter：z: 0.00 m ～ 1.80 m
      │
ConcatenatePointCloud（合併 4 組點雲）
      │
pointcloud_to_laserscan（最近距離投影 → 2D）
      │
/scan（sensor_msgs/LaserScan，10 Hz，360°）
      │
Nav2 Costmap  ／  安全停機層
```

---

## Sample 146

**Source**: `HaloScan_v0\docs\05_楷浚討論筆記.md` L18

```
LiDAR Point Cloud (4× MID-360, 共約 80 萬點/秒)
    ├── 安全區偵測 → 狀態碼（0=安全, 1=減速, 2=停止）→ 直接停車/減速
    └── 避障用途 → 匯入 costmap → 導航軟體消費
```

---

## Sample 147

**Source**: `HaloScan_v0\docs\07_UAM-05LP_設定檔解析.md` L30

```
<?xml version="1.0" encoding="UTF-8"?>
<UAMProjectDesigner>
  └── <Areas>
        ├── <Area Type="NormalArea|ReferenceArea" Id="1">
        │     ├── <AreaComment>        — 區域備註（最大 64 字元）
        │     ├── <ScanSkipCount>      — 掃描跳過次數（0~3，0 = 每圈都檢查）
        │     └── <Regions>
        │           ├── <Region Type="Warning1">      — 外層警告區
        │           │     ├── <Points>   — 1081 個徑向距離值（mm）
        │           │     └── <Vertices> — 多邊形控制點索引
        │           ├── <Region Type="Warning2">      — 內層警告區
        │           │     ├── <Points>
        │           │     └── <Vertices>
        │           └── <Region Type="Protection1">   — 保護區（急停）
        │                 ├── <OnDelay>  — 觸發延遲（掃描次數，1次=30ms）
        │                 ├── <OffDelay> — 解除延遲（掃描次數，1次=30ms）
        │                 ├── <MinDetectionWidth> — 最小偵測寬度（僅新韌體）
        │                 ├── <Points>
        │                 └── <Vertices>
        ├── <Area Type="NormalArea" Id="2">
        │     └── （同上結構）
        └── <Area Type="NormalArea" Id="4">
              └── （同上結構）
```

---

## Sample 148

**Source**: `HaloScan_v0\docs\07_UAM-05LP_設定檔解析.md` L86

```
┌───────────────────────────────────┐
│         Warning1（外層）           │  → 第一級預警：減速準備
│   ┌────────────────────────────┐  │
│   │      Warning2（中間）      │   │  → 第二級警告：主動減速
│   │   ┌───────────────────┐    │  │
│   │                            │ Protection1（內層）│   │   │  → 保護區：急停
│   │                            │ │   │ │
│   │                            │ [感測器]        │   │ │
│   │   └───────────────────┘    │  │
│   └────────────────────────────┘  │
└───────────────────────────────────┘
```

---

## Sample 149

**Source**: `HaloScan_v0\docs\10_Mid360_POE配線方案.md` L75

```
AMR 24V 電源軌 → Moxa EDS-G205A-4PoE（120W POE budget）
  ├── Port 1 → 網路線 → POE Splitter → 12V DC + RJ45 → Mid-360 FL
  ├── Port 2 → 網路線 → POE Splitter → 12V DC + RJ45 → Mid-360 FR
  ├── Port 3 → 網路線 → POE Splitter → 12V DC + RJ45 → Mid-360 RL
  ├── Port 4 → 網路線 → POE Splitter → 12V DC + RJ45 → Mid-360 RR
  └── Port 5 → RPi 5（需另外 5V/5A 供電，或用 POE HAT）
```

---

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

## Sample 151

**Source**: `HaloScan_v0\refs\mid360\03_livox_ros_driver2_設定指南.md` L70

```
livox_ros_driver2/
├── launch_ROS2/
│   ├── msg_MID360_launch.py      # Mid-360 ROS2 launch 檔
│   └── rviz_MID360_launch.py     # 含 RViz 視覺化
├── config/
│   └── MID360_config.json        # 裝置設定檔
└── ...
```

---

## Sample 152

**Source**: `HaloScan_v0\refs\mid360\04_PTP_時間同步設定.md` L13

```
RPi 5（PTP Master / Grandmaster）
    │
    │  PTP Sync / Follow_Up / Delay_Req / Delay_Resp
    │
    ├── Mid-360 FL（PTP Slave）
    ├── Mid-360 FR（PTP Slave）
    ├── Mid-360 RL（PTP Slave）
    └── Mid-360 RR（PTP Slave）
```

---

## Sample 153

**Source**: `Line_bot_v0\changelog.md` L153

```
📋 指令列表 Commands
────────────────
🤖
@ai [問題] <AI 回應文字或圖片>
@ai -sum <近2小時對話摘要>
@ai -sumd [日期] <查詢每日摘要>
@ai /k [關鍵字] <資料庫搜尋>
@ai /k -g [關鍵字] <圖片生成>
@ai /k -i [關鍵字] <指定搜圖>
────────────────
📝 所有訊息自動記錄（保留 3 天）
```

---

## Sample 154

**Source**: `Line_bot_v0\README.md` L48

```
LINE 使用者
     |
ngrok (HTTPS tunnel, docker-compose 內建)
     |
n8n:5678 (webhook 直連)
     |
n8n workflow
  Log Message  → 所有文字訊息寫入 chat-log (JSON + MD)
  @?           → LINE Reply Help
  @ai          → AI Smart Handler (Gemini Function Calling)
               │  General 模式：聊天 + generate_image
               │  KB 模式(/k)：search_documents / search_images /
               │                generate_image_context / generate_image
               └→ 最多 3+1 輪 FC loop + post-check retry
  @KD/@KI/@KGI → 知識庫直接搜尋 (Loop Handler 支援連續搜尋)
  @img         → Gemini Image Generation → 存檔 → Reply/Push 圖片
  @SUM         → 讀取 2hr chat-log → Gemini 摘要 → Reply
  Daily 4AM    → 讀取 24hr chat-log → Gemini 每日摘要 → 存檔

nginx:80
  /images/*    → 靜態圖片（供 @img 結果顯示）
```

---

## Sample 155

**Source**: `Line_bot_v0\README.md` L135

```
.
├── docker-compose.yml          # Docker 服務（n8n + nginx + ngrok）
├── nginx/
│   └── default.conf            # nginx 反向代理 + 靜態檔案
├── workflows/
│   ├── line-bot-gemini.json    # n8n workflow
│   └── ai-smart-handler-fc.js  # AI Smart Handler 原始碼（Function Calling 版）
├── images/                     # AI 生成圖片（runtime，git ignored）
├── n8n-data/                   # n8n 持久化資料（git ignored）
│   ├── chat-log/               # 訊息記錄 JSON + MD（runtime，保留 3 天）
│   ├── chat-history/           # 對話記憶（per-user，30 分鐘過期）
│   ├── pending/                # 等待中結果（pending mechanism，5 分鐘過期）
│   └── daily-summaries/        # 每日摘要存檔（4AM 自動生成）
├── .env.example                # 環境變數範本
├── CHANGELOG.md                # 修改紀錄
└── README.md
```

---

## Sample 156

**Source**: `LineBot_Reporter_v1\docs\aws-migration-discussion.md` L74

```
┌─────────────────────────────┐
│  EC2 (t3.medium, Ubuntu)    │
│                             │
│  ├── Python 3.8+            │
│  ├── Reporter_v0 腳本       │
│  ├── .doc/ 知識庫 (~55MB)   │
│  ├── Claude Code CLI        │
│  └── Chrome (PDF 輸出)      │
└─────────────────────────────┘
```

---

## Sample 157

**Source**: `LineBot_Reporter_v1\docs\aws-migration-discussion.md` L93

```
┌──────────────────┐     ┌──────────────┐
│  EC2 (運算)       │ ←→  │  S3 (儲存) │
│  Python 腳本      │     │  .doc/ 知識庫 │
│  FastAPI (可選)   │     │  報告輸出   │
│  Claude API      │     │  _index.json │
└──────────────────┘     └──────────────┘
```

---

## Sample 158

**Source**: `LineBot_Reporter_v1\docs\aws-migration-discussion.md` L109

```
┌───────────┐    ┌──────────────────┐    ┌─────┐
│ API GW    │ →  │ ECS/Fargate      │ ←→ │ S3 │
│           │    │ Docker 容器       │    │    │
└───────────┘    │ FastAPI          │    └─────┘
                 │ Python 腳本      │
                 │                  │    ┌────────────────┐
                 │  gemini client ──│──→ │ Google Gemini │
                 │                  │    │ - Embedding API │
                 └──────────────────┘    │ - Chat/Gen API │
                                         └────────────────┘
```

---

## Sample 159

**Source**: `LineBot_Reporter_v1\docs\aws-migration-discussion.md` L176

```
┌──────────┐    ┌─────────────────────┐    ┌─────┐
│ API GW   │ →  │ Fargate Container   │ ←→ │ S3 │
│ or Web   │    │                     │    │ .txt files
└──────────┘    │ FastAPI             │    │ templates
                │ ├── /report (生成)   │    └─────┘
                │ ├── /search (搜尋)   │
                │ ├── /calc   (計算)   │        ┌──────────┐
                │ └── gemini_client ───│──────→ │ Gemini │
                │                     │        │ 2.5 Pro │
                │ _calc_throughput.py  │        └──────────┘
                │ gyro-report gen     │
                └─────────────────────┘
```

---

## Sample 160

**Source**: `LineBot_Reporter_v1\docs\phase0-report.md` L56

```
LineBot_Reporter_v1/
├── docker-compose.yml          # 三服務架構
├── Caddyfile                   # 反向代理設定
├── .env.example                # 環境變數範本
├── .gitignore
├── reporter/                   # Reporter API 服務
│   ├── Dockerfile
│   ├── requirements.txt        # fastapi, uvicorn, pdfplumber, python-pptx, python-docx
│   ├── main.py                 # FastAPI：5 個 endpoint
│   ├── config.py               # 路徑/環境變數集中管理
│   ├── scripts/                # 13 個 Python 腳本（已參數化路徑）
│   │   ├── _build_index.py     # 索引建置
│   │   ├── _extract.py         # 文字萃取主控
│   │   ├── _extract_batch.py   # 批次萃取引擎
│   │   ├── _extract_one.py     # 單檔萃取
│   │   ├── _search_index.py    # 索引搜尋（同義詞展開+評分）
│   │   ├── _find_related.py    # 關聯文件搜尋
│   │   ├── _calc_throughput.py # 工程計算（瓶頸/流量/設備）
│   │   ├── _report_init.py     # 報告骨架產出
│   │   ├── _classify_rules.py  # 分類規則引擎
│   │   ├── _copy_files.py      # 檔案複製
│   │   ├── _scan.py            # 來源掃描
│   │   ├── _quality_report.py  # 品質報告
│   │   └── _setup.py           # 工具包安裝
│   └── templates/              # 10 個報告模板
├── workflows/                  # n8n workflow JSON
│   └── line-bot-gemini.json
├── images/                     # 靜態圖片（23 張）
├── n8n-data/                   # n8n 持久化資料
├── knowledge-base/             # 知識庫掛載點
└── docs/                       # 規劃文件
```

---

## Sample 161

**Source**: `LineBot_Reporter_v1\docs\unified-aws-migration.md` L100

```
本機 Windows

┌─────────────────────────────────────────────────┐
│  Docker Compose                                 │
│  ┌──────────┐ ┌───────────┐  ┌───────────────┐  │
│  │  ngrok   │ → │  n8n      │               │ nginx        │ │
│  │  (HTTPS) │  │  (5678)   │  │  (80, 圖片)   │ │
│  └──────────┘ └─────┬─────┘  └───────────────┘  │
│                     │                           │
│              LINE webhook                       │
│              @ai, @kb, @img...                  │
└─────────────────┬───────────────────────────────┘
                  │ volume mount (知識庫)
┌─────────────────▼───────────────────────────────┐
│  Reporter_v0                                     │
│  ├── .doc/  知識庫（55MB, 63,752 檔案）          │
│  ├── _index.json（7,338 筆）                     │
│  ├── 14 個 Python 腳本                           │
│  └── 6 個 Claude Code Skills                     │
└─────────────────────────────────────────────────┘
```

---

## Sample 162

**Source**: `LineBot_Reporter_v1\docs\unified-aws-migration.md` L129

```
┌─────────────────────────────────────┐
│  EC2 (t3.medium, Ubuntu)            │
│                                     │
│  Docker Compose:                    │
│  ├── Caddy (HTTPS, 取代 ngrok+nginx)│
│  ├── n8n (LINE Bot)                 │
│  │                                  │
│  Host:                              │
│  ├── Reporter_v0 腳本               │
│  ├── .doc/ 知識庫 (~55MB)           │
│  ├── Claude Code CLI                │
│  └── Chrome (PDF 輸出)              │
└─────────────────────────────────────┘
```

---

## Sample 163

**Source**: `LineBot_Reporter_v1\docs\unified-aws-migration.md` L152

```
┌──────────────────┐     ┌──────────────┐
│  EC2 (運算)       │ ←→  │  S3 (儲存) │
│  Docker: Caddy+n8n│     │  .doc/ 知識庫 │
│  Python 腳本      │     │  報告輸出   │
│  Claude/Gemini API│     │  _index.json │
└──────────────────┘     └──────────────┘
```

---

## Sample 164

**Source**: `LineBot_Reporter_v1\docs\unified-aws-migration.md` L168

```
┌─────────────────────────────────────────────────────┐
│  EC2 (t3.medium+)                                   │
│                                                     │
│  ┌───────────┐   ┌──────────────┐   ┌────────────┐  │
│  │  Caddy    │ → │  n8n         │   │ Reporter   │ │
│  │  (HTTPS)  │   │  (LINE Bot)  │ → │ API        │ │
│  │  :80/:443 │   │  :5678       │   │ (FastAPI)  │  │
│  └───────────┘   └──────────────┘   │ :8000      │  │
│        │                             │            │ │
│        │ /images/* → 靜態檔案        │ /report    │ │
│        │                             │ /search    │ │
│        │                             │ /calc      │ │
│        │                             └──────┬─────┘ │
│        │                                    │       │
│  ┌─────▼────────────────────────────────────▼─────┐ │
│  │  .doc/ 知識庫（共用 volume）                     │ │
│  │  55MB, 7,338 索引, 5,636 txt                     │ │
│  └──────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Google      │
                    │ Gemini API  │
                    │ - 2.5 Pro   │
                    │ - Embedding │
                    └─────────────┘
```

---

## Sample 165

**Source**: `LineBot_Reporter_v1\reporter\templates\10_技術文件.md` L195

```
{根目錄}/
├── {子目錄 1}/
│   ├── {檔案}
│   └── {檔案}
├── {子目錄 2}/
│   └── {檔案}
├── {設定檔}
└── {主程式}
```

---

## Sample 166

**Source**: `Mail_Checker_v0\README.md` L82

```
extracted_attachments/
├── 2023-04/
│   ├── 報價單.pdf
│   └── 專案規格.docx
├── 2023-05/
│   ├── 月報.xlsx
│   └── 會議簡報.pptx
└── _attachment_index.csv
```

---

## Sample 167

**Source**: `Mail_Checker_v0\README.md` L94

```
extracted_attachments/
├── john.wang/
├── mary.chen/
└── _attachment_index.csv
```

---

## Sample 168

**Source**: `Mail_Checker_v0\README.md` L102

```
extracted_attachments/
├── 報價單.pdf
├── 專案規格.docx
└── _attachment_index.csv
```

---

## Sample 169

**Source**: `opencode\packages\app\e2e\AGENTS.md` L32

```
e2e/
├── fixtures.ts       # Test fixtures (test, expect, gotoSession, sdk)
├── actions.ts        # Reusable action helpers
├── selectors.ts      # DOM selectors
├── utils.ts          # Utilities (serverUrl, modKey, path helpers)
└── [feature]/
    └── *.spec.ts     # Test files
```

---

## Sample 170

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L20

```
Need to run code?
├─ Serverless functions at the edge → workers/
├─ Full-stack web app with Git deploys → pages/
├─ Stateful coordination/real-time → durable-objects/
├─ Long-running multi-step jobs → workflows/
├─ Run containers → containers/
├─ Multi-tenant (customers deploy code) → workers-for-platforms/
├─ Scheduled tasks (cron) → cron-triggers/
├─ Lightweight edge logic (modify HTTP) → snippets/
├─ Process Worker execution events (logs/observability) → tail-workers/
└─ Optimize latency to backend infrastructure → smart-placement/
```

---

## Sample 171

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L36

```
Need storage?
├─ Key-value (config, sessions, cache) → kv/
├─ Relational SQL → d1/ (SQLite) or hyperdrive/ (existing Postgres/MySQL)
├─ Object/file storage (S3-compatible) → r2/
├─ Message queue (async processing) → queues/
├─ Vector embeddings (AI/semantic search) → vectorize/
├─ Strongly-consistent per-entity state → durable-objects/ (DO storage)
├─ Secrets management → secrets-store/
├─ Streaming ETL to R2 → pipelines/
└─ Persistent cache (long-term retention) → cache-reserve/
```

---

## Sample 172

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L51

```
Need AI?
├─ Run inference (LLMs, embeddings, images) → workers-ai/
├─ Vector database for RAG/search → vectorize/
├─ Build stateful AI agents → agents-sdk/
├─ Gateway for any AI provider (caching, routing) → ai-gateway/
└─ AI-powered search widget → ai-search/
```

---

## Sample 173

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L62

```
Need networking?
├─ Expose local service to internet → tunnel/
├─ TCP/UDP proxy (non-HTTP) → spectrum/
├─ WebRTC TURN server → turn/
├─ Private network connectivity → network-interconnect/
├─ Optimize routing → argo-smart-routing/
├─ Optimize latency to backend (not user) → smart-placement/
└─ Real-time video/audio → realtimekit/ or realtime-sfu/
```

---

## Sample 174

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L75

```
Need security?
├─ Web Application Firewall → waf/
├─ DDoS protection → ddos/
├─ Bot detection/management → bot-management/
├─ API protection → api-shield/
├─ CAPTCHA alternative → turnstile/
└─ Credential leak detection → waf/ (managed ruleset)
```

---

## Sample 175

**Source**: `opencode\packages\opencode\test\fixture\skills\cloudflare\SKILL.md` L87

```
Need media?
├─ Image optimization/transformation → images/
├─ Video streaming/encoding → stream/
├─ Browser automation/screenshots → browser-rendering/
└─ Third-party script management → zaraz/
```

---

## Sample 176

**Source**: `opencode\packages\web\README.md` L20

```
.
├── public/
├── src/
│   ├── assets/
│   ├── content/
│   │   ├── docs/
│   └── content.config.ts
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

---

## Sample 177

**Source**: `opencode-bench\4090-2026-04-08\RESULTS.md` L83

```
dgx-spark-qwen-gemma-2026-04-08/  # 原名 4090-2026-04-08（誤）
├── opencode.json            # LiteLLM provider 設定
├── run_bench.sh             # 執行腳本
├── run_bench.log            # 時間摘要
├── RESULTS.md               # 本文件
├── gemma4/                  { T1_log, T2_log, wc_lite.py }
├── qwen25-coder-14b/        { T1_log, T2_log }            ← 無檔案產物
├── qwen3-coder-30b/         { T1_log, T2_log, wc_lite.py }
└── qwen3-coder-next/        { T1_log, T2_log, wc_lite.py, test_wc_lite.py }
```

---

## Sample 178

**Source**: `opencode-bench\4090-DEPLOYMENT.md` L93

```
開發者電腦（VS Code / 終端機）
    │
    ▼
opencode CLI 或 Cline（VS Code 插件）
    │
    ▼
4090 伺服器 :4001（OpenAI-compatible API）
    │  Ollama + LiteLLM + fix-proxy
    ▼
qwen3-coder:30b（開源模型，18GB）
```

---

## Sample 179

**Source**: `opencode-bench\4090-SETUP.md` L23

```
opencode CLI
    │
    ▼
fix-proxy :4001/v1        ← 修正 Ollama tool_calls index bug
    │
    ▼
LiteLLM :4000/v1          ← OpenAI-compatible API + ollama_chat backend
    │
    ▼
Ollama :11434              ← 模型推理引擎（GPU）
    │
    ▼
RTX 4090 24GB VRAM
```

---

## Sample 180

**Source**: `opencode-bench\ARCHITECTURE.md` L9

```
┌──────────────────────────────────────────────────────────────┐
│                     使用者（Laptop）                          │
│                   RTX 5060 · 8GB VRAM                         │
│                                                               │
│   ┌──────────────────────┐   ┌──────────────────────────┐     │
│   │    Claude Code CLI   │   │     opencode CLI         │     │
│   │   (Anthropic API)    │   │    (@ai-sdk providers)   │     │
│   │                      │   │                          │     │
│   │  /do easy → Gemini  │    │  Providers:              │    │
│   │  /do deep → Gemini  │    │  ├ google/gemini-3-flash │    │
│   │                      │   │  ├ 4090-litellm/*        │     │
│   │  主力開發 +          │   │  └ dgx/*                 │     │
│   │  bench baseline      │   │                          │     │
│   └──────────────────────┘   └──┬──────────┬────────────┘     │
│            │                    │          │                  │
└────────────┼────────────────────┼──────────┼──────────────────┘
             │                    │          │
             │ Anthropic API      │          │
             ▼                    │         │
  ┌────────────────┐              │          │
  │  Claude Cloud  │              │          │
  │  opus-4.6      │              │          │
  │  sonnet-4-6    │              │          │
  └────────────────┘              │          │
                                  │          │
          ┌───── Gemini API ──────┘          │
          ▼                                 │
  ┌────────────────┐                         │
  │  Google Cloud  │                         │
  │  gemini-3-flash│                         │
  │  gemini-3.1-pro│                         │
  └────────────────┘                         │
                                             │
          ┌──────────────────────────────────┘
          │
          ▼
  ┌─────────────────────────┐     ┌──────────────────────────┐
  │   RTX 4090 Server       │     │     DGX Spark            │
  │   10.63.138.16          │     │     10.63.138.198        │
  │   24GB VRAM             │     │     Grace CPU 128GB      │
  │                         │     │                          │
  │   Ollama :11434         │     │   Ollama :11434          │
  │     │                   │     │     │                    │
  │   LiteLLM :4000/v1     │     │   Traefik →              │
  │     │                   │     │   LiteLLM /litellm/v1    │
  │   fix-proxy :4001/v1   │     │                           │
  │     (index bug fix)     │     │   Models:                │
  │                         │     │   ├ qwen3-coder-next     │
  │   Models:               │     │   │  (80B MoE, 52GB)     │
  │   ├ qwen3-coder:30b    │     │   ├ qwen3-coder:30b       │
  │   ├ mistral-nemo        │     │   ├ gemma4:31b           │
  │   └ gemma4:e4b          │     │   └ mistral-nemo         │
  └─────────────────────────┘     └──────────────────────────┘
```

---

## Sample 181

**Source**: `opencode-bench\ARCHITECTURE.md` L79

```
opencode  ──→  fix-proxy :4001  ──→  LiteLLM :4000  ──→  Ollama :11434
                    │
          修正 tool_calls index
          (Ollama streaming 全送
           index:0，導致 @ai-sdk
           合併/丟失多個 tool calls)
```

---

## Sample 182

**Source**: `opencode-bench\dgx-spark-2026-04-08\RESULTS.md` L47

```
dgx-spark-2026-04-08/
├── opencode.json
├── run_bench.sh
├── run_bench.log
├── RESULTS.md            ← 本文件
├── phi4/                 { T1_log (timeout), T2_log (timeout) }
├── mistral-nemo/         { T1_log, T2_log, 產物 }
├── granite33-8b/         { T1_log, T2_log, 產物 }
└── llama31-8b/           { T1_log (timeout), T2_log (timeout), wc_lite.py 部分產出 }
```

---

## Sample 183

**Source**: `opencode-bench\opencode-2026-04-07\README.md` L44

```
<model>/
├── wc_lite.py          # T1 產物
├── test_wc_lite.py     # T1 測試
├── T1_meta.txt         # T1 指標摘錄 (TTFT, wall time, tool calls)
├── summary.md          # T2 產物
└── T2_meta.txt         # T2 指標摘錄
```

---

## Sample 184

**Source**: `opencode-bench\opencode-2026-04-07\RESULTS.md` L120

```
benchmarks/opencode-2026-04-07/
├── README.md, RESULTS.md (本檔), opencode.json
├── run_bench.sh         # 第一輪 driver
├── run_t2_retry.sh      # T2 修正後重跑
├── prompts/T1.md, T2.md, T2_inline.md
└── {gemini3-flash, gemma4-e2b, qwen25-14b, qwen25-16k}/
    ├── T1_log.txt, T1_meta.txt   # 全失敗
    ├── T2_log.txt, T2_meta.txt   # 第一輪（廢）
    └── T2_retry.txt, T2_retry_meta.txt  # 第二輪（有效）
```

---

## Sample 185

**Source**: `opencode-bench\README.md` L67

```
opencode-bench/
├── SUMMARY.md                  # 全平台結果總表（快速參考）
├── RESULTS.md                  # 詳細結果 + 根因分析
├── collect_all.py              # 掃描 *_meta.txt → xlsx 報告
├── fixtures/A3/                # A3 task fixture（mini_queue + TOCTOU bug）
├── fixtures/A4/                # A4 task fixture（thread-safe mini_queue）
├── three-way-2026-04-08/       # 共用 prompt 目錄（A1~A4）
├── a4-bench-2026-04-09/        # A4 全平台 benchmark
├── 4090-litellm-2026-04-09/    # 4090 LiteLLM benchmark（R1）
├── 4090-litellm-2026-04-09-r2/ # 4090 LiteLLM benchmark（R2）
├── dgx-spark-litellm-2026-04-09/ # DGX Spark benchmark
├── fix-proxy/                  # Ollama tool_calls index fix
│   ├── proxy.py                # HTTP streaming proxy（修正 index）
│   ├── bench_3way.sh           # 3-way bench script
│   ├── bench-3way-20260410-*/  # 3-way bench raw results
│   ├── retest-*/               # proxy retest raw results
│   └── batch_retest.sh         # batch retest script
├── a1-dual-file-test/          # A1 雙檔 bug 調查（6 variants × 2 platforms）
├── a1-repeat-4090/             # A1 重複測試（5 runs）
├── a1-repeat-dgx/              # A1 重複測試（5 runs）
└── HANDOFF.md                  # 交接文件
```

---

## Sample 186

**Source**: `opencode_enhance_v0\eval\PLAN.md` L58

```
eval/
├── PLAN.md            # 本文件
├── tasks/             # 8 題 prompt
├── fixtures/          # 測試用程式 / 文件
├── runs/
│   ├── claude/<task-id>/
│   └── opencode/<task-id>/
├── scoreboard.md
└── REPORT.md
```

---

## Sample 187

**Source**: `personal-rag_v1\.doc\.claude\skills\gyro-report\README_載入SOP.md` L7

```
.claude/skills/gyro-report/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   ├── gyro_css_template.css             ← CSS 模板（必須）
│   ├── gyro_style_template.json          ← 品牌設計規範
│   └── content_sample.json              ← JSON schema 範例
└── scripts/
    └── gyro_html_generator.js            ← Legacy JSON→HTML 產生器
```

---

## Sample 188

**Source**: `personal-rag_v1\.doc\.claude\skills\gyro-report\SKILL.md` L79

```html
<pre class="diagram">
 ┌────┐ ┌────┐
 │P-1 │ │P-2 │
 └────┘ └────┘
</pre>
```

---

## Sample 189

**Source**: `personal-rag_v1\.doc\.claude\skills\gyro-report\SKILL.md` L244

```
output_folder/
├── presentation.html      ← slim HTML (~50-60KB)
└── images/
    ├── img_01.png
    ├── img_02.png
    └── ...
```

---

## Sample 190

**Source**: `personal-rag_v1\.doc\_分類建議.md` L16

```
.doc/
├── 00_公司簡介/
├── 01_產品型錄/
├── 02_軟體系統/
├── 10_車型規格/
├── 20_搬運方案/
├── 30_周邊設備/
├── 40_系統整合/
├── 50_安全認證/
├── 60_客戶_封測/
├── 61_客戶_晶圓代工/
├── 62_客戶_記憶體/
├── 63_客戶_面板光電/
├── 64_客戶_系統整合/
├── 65_客戶_其他/
├── 70_業務報價/
├── 75_進度報告/
├── 80_設計規範/
├── 85_研究資料/
├── 90_開發計畫/
├── 91_場地需求/
├── 92_驗收資料/
├── 95_工程開發/
├── _OLD/
├── _專利/
├── _情報/
├── _影片/
└── _其他/
```

---

## Sample 191

**Source**: `personal-rag_v1\flow.md` L5

```
.doc/ (7,388 文件)          .image/ (73,200 圖片)
    ↓ .txt 提取文本              ↓ .md 語意描述
    ↓                            ↓
┌─────────────────────────────────────────┐
│  Gemini gemini-embedding-001 (3072 維)  │
└─────────────────────────────────────────┘
    ↓                            ↓
┌──────────┐              ┌──────────┐
│ docs     │              │ images   │
│ collection│              │ collection │
└──────────┘              └──────────┘
         ChromaDB (.chroma/)
              ↓
┌─────────────────────────────────────────┐
│            FastAPI Backend              │
│  /docs/search  /images/search  /chat    │
│  /images/context  /kb-image/  /health   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│       Chat Frontend (chat.html)         │
│  KB mode · file upload · lightbox       │
│  markdown · badges · persistent history │
└─────────────────────────────────────────┘
```

---

## Sample 192

**Source**: `personal-rag_v1\flow.md` L65

```
Frontend                          Backend (chat.py)
────────                          ─────────────────
輸入文字 + 附件         POST /chat
  ↓ (kb_mode, history,   ──→  收到 ChatRequest
     attachments)                ↓
                            組裝 contents (history + user parts)
                            附加 KB mode system instruction
                                 ↓
                            呼叫 Gemini (gemini-2.0-flash)
                                 ↓
                           ┌─ 有 function_calls? ─┐
                           │  是                   │ 否
                           ↓                       ↓
                      執行 function            直接回傳文字
                      (search/generate)
                           ↓
                      回傳結果給 Gemini
                      (最多 3 輪)
                           ↓
                      Post-check retry
                      (偵測遺漏圖片生成)
                           ↓
                      回傳 ChatResponse
                      (reply, sources,
                       function_calls_made,
                       images)
```

---

## Sample 193

**Source**: `personal-rag_v1\flow.md` L105

```
一般模式 ──/k──→ doc 模式 ──/i──→ img 模式
                    │         ←/q──┘
                    ├──/g──→ gen 模式
                    │         ←/q──┘
                 ←/q──┘ 回到一般模式
```

---

## Sample 194

**Source**: `personal-rag_v1\README.md` L208

```
personal-rag_v1/
├── .doc/                # 文件知識庫 (7,388 份)
│   ├── _index.json      # 文件索引
│   ├── 00_公司簡介/     # ~ 65_客戶_其他 (27 分類)
│   └── ...
├── .image/              # 圖片知識庫 (~73,200 張)
│   ├── 00_其他/         # ~ 10_報告分析 (11 分類)
│   └── ...
├── api/                 # FastAPI 後端
│   ├── main.py          # App + 靜態檔 + kb-image endpoint
│   ├── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── chat.py      # Gemini function calling + RAG
│   │   ├── docs.py      # 文件搜尋 API
│   │   ├── images.py    # 圖片搜尋 API
│   │   └── context.py   # 圖片描述彙整 API
│   └── static/
│       └── chat.html    # Chat 前端 (單檔 HTML)
├── search/              # 語意搜尋模組
│   ├── config.py        # 共用設定
│   ├── embedder.py      # Gemini embedding 客戶端
│   ├── chunker.py       # 文字分塊
│   ├── db.py            # ChromaDB 封裝
│   ├── index_docs.py    # 文件索引 CLI
│   ├── index_images.py  # 圖片索引 CLI
│   ├── doc_search.py    # 文件搜尋 CLI
│   ├── img_search.py    # 圖片搜尋 CLI
│   ├── img_context.py   # Prompt 生成 CLI
│   └── monitor.py       # 進度監控 + email 通知
├── tests/               # 自動化測試 (103 tests)
├── .chroma/             # ChromaDB 存儲 (自動生成)
├── .env                 # API Key (不納入版控)
├── requirements-api.txt # Python 依賴
├── Dockerfile           # Docker 部署
├── flow.md              # 系統流程文件
├── test_report.md       # 測試報告
└── README.md
```

---

## Sample 195

**Source**: `personal-rag_v2\PKB\templates\00_報告產生流程\marp_usage_guide.md` L295

```
/gyro-kb ── 產出 .md 報告
  │
  ├── /gyro-report ── MD → HTML（螢幕預覽、互動式導覽）
  │
  └── Marp CLI ── MD → PPTX / PDF（客戶交付）
```

---

## Sample 196

**Source**: `personal-rag_v2\PKB\templates\00_報告產生流程\report_workflow.md` L97

```
.images/
├── client/      ← 客戶提供（使用者確認正確版本）
├── db/          ← ChromaDB 搜尋（自動）
└── generated/   ← Mermaid 由瀏覽器渲染（不需存檔）
```

---

## Sample 197

**Source**: `personal-rag_v2\PKB\templates\00_報告產生流程\report_workflow.md` L124

```
workspace/CASE##/
├── [原始檔案]                        ← 輸入
├── input_data.json                   ← 理解（結構化提取）
├── params.json                       ← 確認（單一真相）
├── results.json                      ← 計算（非所有類型都需要）
├── verification.xlsx                 ← 驗算（非所有類型都需要）
├── 01_requirements_review.md/.html   ← 需求確認
├── 02_analysis_report.md/.html       ← 分析報告（如適用）
├── 03_[文件類型].md/.html            ← 最終產出
└── .images/
    ├── client/
    ├── db/
    └── generated/
```

---

## Sample 198

**Source**: `personal-rag_v2\PKB\templates\00_報告產生流程\report_workflow_v1.md` L28

```
Phase A：大量撈取    Phase B：統整+圖片     Phase C：報告產出
┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ A1 ChromaDB  │    │ B1 功能統整  │    │ C1 完整版     │
│ A2 客戶歸納  │──▶│ B2 客戶矩陣  │──▶│ C2 精簡版     │
│ A3 產品歸納  │    │ B3 報價分析  │    │ C3 對外版     │
│ A4 核心文件  │    │ IA1 圖片搜尋 │    │ C4 排版       │
└─────────────┘    │ IB1 圖片篩選 │    └──────────────┘
    可平行          └─────────────┘        循序
                       可平行
```

---

## Sample 199

**Source**: `personal-rag_v2\PKB\templates\00_報告產生流程\report_workflow_v1.md` L114

```
workspace/test_XX/
├── requirement.md                ← 輸入
├── A1~A4_*.json                  ← Phase A
├── B1~B3_*.json                  ← Phase B
├── IA1_*.json / IB1_*.json       ← Phase B-IMG
├── 01_xxx.md                     ← 完整版（內部）
├── 02_xxx_summary.md/.html/.pptx ← 精簡版（內部）
├── 03_xxx_external.md/.html      ← 對外版（匿名）
└── .images/db/                   ← 圖片（章節前綴命名）
```

---

## Sample 200

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_CPU_RAM_體檢報告.md` L435

```
syswork.launch (root)
├── alarm_warn_code_gathering.launch
│   ├── alarmcode_gathering
│   └── warncode_gathering
├── MapLocationservice.launch
│   └── maplocation_server
├── CameraLocationservice.launch
│   └── cameralocation_server
├── syschecker.launch
│   └── syschecker (10 Hz)
├── sysindicator.launch
│   └── sysindicator (10 Hz, 125KB)
├── logs_update.launch
│   └── logs_update
├── syncrobotstate.launch
│   └── syncrobotstate (10 Hz)
├── monitor.launch
│   ├── batt_monitor.launch → battery_monitor (1 Hz)
│   ├── relative_monitor.launch → move_relative_monitor
│   ├── modbus_monitor.launch → modbus_monitor (0.5 Hz) + tm_arm_status_check
│   ├── safety_monitor.launch → safety_monitor (0.5 Hz)
│   ├── carvel_monitor.launch → carvel_monitor (10 Hz)
│   ├── camera_monitor.launch → camera_monitor (0.1 Hz)
│   ├── dashcam_monitor.launch → dashcam_monitor (0.5 Hz)
│   ├── slot_monitor.launch → slot_monitor (20 Hz ⚠️)
│   ├── path_log.launch → path_log
│   ├── tag_log.launch → TagLog
│   ├── network_monitor.launch → network_monitor (5+ threads)
│   ├── wirelesscharger_monitor.launch → wirelesscharger_monitor
│   ├── get_imu_log.launch → get_imu_log
│   ├── rosparam_monitor.launch → rosparam_monitor (60s)
│   ├── system_info_monitor.launch → system_info_monitor (0.5 Hz)
│   ├── cpu_monitor.launch → cpu_monitor_new (0.2 Hz + threads)
│   ├── disk_health_monitor.launch → disk_health_monitor (0.001 Hz ⚠️)
│   ├── automode_action_control.launch → automode_action_control
│   └── mqtt_bridge.launch → mqtt_bridge (1 Hz)
├── logclear.launch
│   └── log_clear (0.004 Hz)
├── loggathering.launch
│   └── loggathering (0.05 Hz, sync ⚠️)
└── griptmEMO.launch
    └── griptmEMO (10 Hz)

routemap.launch (separate)
├── armdooraction
├── processjson_server
├── routemap (10 Hz, 343KB ⚠️)
└── Tag_position_recovery (10 Hz)

ethercat SOEM_m.launch (container 2)
└── motor_control (C++, sudo, 50~1000 Hz)

canopen_control.launch (container 3)
├── canopen_controller (100 Hz ⚠️)
├── canopen_log (10 Hz)
└── canopen_motor_data_logger
```

---

## Sample 201

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_CPU優化計畫_v1.md` L23

```
Phase 1 ─ 緊急修復（團隊）     省 ~28%(sys) + 防止 +8.7% 復發
Phase 2 ─ 程式碼優化            省 ~4%(sys)
Phase 3 ─ 運維調整（免改碼）    省 ~4%(sys) + 回收 RAM
Phase 4 ─ 進階優化（可選）      省 ~3%(sys)
                                ─────────────
                          合計目標：82% → ~35-40%(sys)
```

---

## Sample 202

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_撞機事件根因分析.md` L168

```
                    正常狀態                         雪崩狀態
              ┌─────────────────┐            ┌─────────────────┐
              │  loggingCarWork │            │  loggingCarWork  │
              │    = 0.01s      │            │    = 0.01s       │
              │  (100Hz 排程)    │            │  (100Hz 排程)   │
              └────────┬────────┘            └────────┬─────────┘
                       ↓                              ↓
              ┌─────────────────┐            ┌──────────────────┐
              │  log_work() 執行 │            │  log_work() 執行  │
              │  耗時 5ms < 10ms │            │  耗時 15ms > 10ms │
              │  → sleep 5ms    │            │  → 跳過 sleep    │
              │  → 下一次排程    │            │  → 立即排下一次 │
              └─────────────────┘            │  → 堆積 → 連續執行 │
                                             │  → CPU 100%       │
              CPU: 69%                       └──────────────────┘
                                             CPU: 95~100%
```

---

## Sample 203

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_撞機事件根因分析.md` L262

```
每日磁碟消耗估算：
├── 4 台相機錄影（streamfile.py）
│   └── 15 fps × 4 cam × 86400 sec × ~50KB/frame = ~250 GB/天（未壓縮）
│       （壓縮後估 ~5-25 GB/天，取決於 codec）
├── ROS log（output="screen" × 38 節點）
│   └── 估 ~500 MB ~ 2 GB/天
├── CSV 日誌（syswork 各 monitor）
│   └── 估 ~100~500 MB/天
└── 合計：數 GB ~ 數十 GB/天

Day 3: 磁碟接近滿 → write() 阻塞
       → 所有含 file I/O 的節點卡住
       → loggathering.py 的 os.system("sync") 阻塞 10+ 秒
       → 系統凍結 → 導航中斷
```

---

## Sample 204

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_撞機事件根因分析.md` L353

```
Hour 0 ─────────────────────────────────────────────────────
  系統啟動
  CPU: ~45% (全核)    RAM: ~2.0 GB    Disk: 60%
  log_update: 69% (單核)    log_work() 耗時: 5ms < 10ms ✓
  導航延遲: <50ms ✓

Hour 12 ────────────────────────────────────────────────────
  CSV 累積 ~200MB    ROS log 累積 ~500MB
  CPU: ~48%    RAM: ~2.5 GB    Disk: 65%
  log_work() 耗時: 7ms < 10ms ✓（I/O 稍慢）
  導航延遲: <50ms ✓

Hour 24 ────────────────────────────────────────────────────
  CSV 累積 ~500MB    ROS log 累積 ~1.5GB    錄影累積 ~10GB
  CPU: ~52%    RAM: ~3.2 GB    Disk: 72%
  log_work() 耗時: 9ms < 10ms ✓（接近臨界）
  無界 queue 開始微量堆積
  導航延遲: <60ms ✓

Hour 36 ────────────────────────────────────────────────────
  CSV 累積 ~800MB（寫入變慢）
  CPU: ~58%    RAM: ~4.0 GB    Disk: 78%
  log_work() 耗時: 11ms > 10ms ⚠️ 開始排隊
  log_update CPU: 69% → 75%
  導航延遲: ~80ms ⚠️

Hour 48 ────────────────────────────────────────────────────
  CSV > 1GB    磁碟 I/O 延遲上升
  CPU: ~68%    RAM: ~5.5 GB    Disk: 85%
  log_work() 耗時: 15ms >> 10ms ⚠️ 排隊加速
  log_update CPU: 85~90%
  部分 ping timeout → 執行緒累積
  導航延遲: ~150ms ⚠️

Hour 60 ─────────────── ⚡ 臨界點 ──────────────────────────
  RAM: ~7.0 GB（接近 7.7GB 上限）
  Disk: 92%（sync 開始阻塞數秒）
  CPU: ~85%（全核）

  ┌─ 觸發鏈 ──────────────────────────────────┐
  │ log_update scheduler 完全雪崩 → CPU 100%   │
  │ + RAM 接近 OOM → swap thrashing            │
  │ + sync 阻塞 → I/O 凍結                     │
  │ + 執行緒累積 → context switch 200K+/s      │
  │                                             │
  │ = move_base 被搶光 CPU                      │
  │ = amcl 定位更新延遲 > 500ms                 │
  │ = costmap 來不及更新障礙物                  │
  │ = 安全煞車計算超時                          │
  └─────────────────────────────────────────────┘
                       ↓
              ❌ 導航延遲 → 撞擊機台

Hour 60+ ───────────────────────────────────────────────────
  系統可能自行部分恢復（OOM killer 殺掉某些節點）
  但傷害已經造成
```

---

## Sample 205

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_撞機事件根因分析.md` L416

```
                    ┌──────────────┐
                    │  時間累積    │
                    │  （數天運行） │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ CSV 檔案增長  │ │ ROS queue    │ │ 錄影+ROS log │
    │ (log_update) │ │ 堆積         │ │ 持續寫入     │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
           ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ I/O 變慢     │ │ RAM 增長     │ │ 磁碟空間減少 │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
           ↓               │               ↓
    ┌──────────────┐       │        ┌──────────────┐
    │ scheduler    │       │        │ sync 阻塞    │
    │ 排隊雪崩     │       │        │ write 阻塞   │
    └──────┬───────┘       │        └──────┬───────┘
           │               │               │
           └───────────────┼───────────────┘
                           ↓
                    ┌──────────────┐
                    │  CPU 飆高    │
                    │  RAM 耗盡    │
                    │  I/O 凍結    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ move_base    │
                    │ amcl         │
                    │ 計算延遲     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ ❌ 導航失控  │
                    │ ❌ 撞擊機台  │
                    └──────────────┘
```

---

## Sample 206

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_整合分析報告_v2.md` L129

```
CPU%  Load
 82 ┤                                          ████████████
 78 ┤                                     █████
 74 ┤
 70 ┤
 66 ┤
 62 ┤
 58 ┤
 54 ┤              ████████████████████████
 50 ┤         █████
 46 ┤    █████
 42 ┤████
     3/17  18   19   20   21   22   23   24   25   26   27   28
                                          ↑
                                       轉折點
```

---

## Sample 207

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_整合分析報告_精簡_v2.md` L51

```
CPU%(sys)
 82 ┤                                          ████████████
 78 ┤                                     █████
 54 ┤              ████████████████████████
 44 ┤████████████
     3/17  18   19   20   21   22   23   24   25   26   27   28
                                          ↑
                                    AprilTag mux 忘關
```

---

## Sample 208

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L15

```
┌─────────────────────────────────────────────────────────────────┐
│                     Host OS (Ubuntu 20.04)                      │
│                   Intel i7-7700T / 7.7GB RAM                    │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│ Docker 1 │ Docker 2 │ Docker 3 │ Docker 4 │     Docker 5        │
│ gyro-ros │ ethercat │ canopen  │ agvweb   │     mqtt            │
│ :8022    │ :8024    │ :8023    │ :80/:5000│                     │
│          │          │          │          │                     │
│ ROS      │ EtherCAT │ CANopen  │ Flask    │ MQTT Bridge         │
│ Kinetic  │ Noetic   │ Noetic   │ ExtJS    │                     │
│ 50+ pkg  │ 7 pkg    │ 3 pkg    │ 152+ API │                     │
├──────────┴──────────┴──────────┴──────────┴─────────────────────┤
│                  ROS Master (port 11311)                        │
│              rosbridge (port 9090, WebSocket)                   │
├─────────────────────────────────────────────────────────────────┤
│  Hardware: USB2CAN / EtherCAT NIC / RS485 / RealSense / LIDAR   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sample 209

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L222

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

## Sample 210

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L417

```
/static/dbfolder/
├── car_info/json/          # 設定檔
│   ├── processcontrol.json # 流程狀態機（54KB）
│   ├── processjsonmacro.json # 巨集庫（38KB）
│   ├── routemap.json       # 路線資料（237KB）
│   ├── allalarm.json       # 警報定義（100KB）
│   └── itemConf.json, ledConf.json, limit_group_default.json
├── car_setting/            # 車型設定（C4, D2, L4, L12 等）
├── warn_err/               # 錯誤/警告碼
├── errorcode/              # 延伸錯誤資訊
├── map/                    # 路線地圖
├── zip/                    # 日誌壓縮檔
└── tm_image/               # 達明手臂圖片
```

---

## Sample 211

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L441

```
┌─────────────┐    /motor_cmd     ┌──────────────┐
│             │ ────────────────→ │             │
│  gyro-ros   │    /motor_actual  │  ethercat /  │
│  (主系統)    │ ←──────────────── │  canopen   │
│             │    /motorAlarm    │  (馬達控制)  │
│             │ ←──────────────── │             │
└──────┬──────┘                   └──────────────┘
       │
       │  rosbridge (port 9090)
       ↕
┌──────┴──────┐
│   agvweb    │
│   (Web UI)  │
└─────────────┘
```

---

## Sample 212

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L494

```
package/
└── param/
    ├── L8N-BCnn-BLMR-FS54/   # 車型 A 設定
    ├── L4-LFUF-OBLV-FS54/    # 車型 B 設定
    └── default/               # 預設設定
```

---

## Sample 213

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_程式架構分析_v2.md` L674

```
~/maintain_work_logs/
├── ros/$DATE/          # ROS 日誌（每日目錄）
├── syswork/            # 系統監控日誌
├── e84/                # E84 通訊日誌
├── tcpbridge/          # TCP Bridge 日誌
├── TM_Export/          # 達明手臂日誌
├── TM_modbus/          # 達明 Modbus 日誌
├── maintain/           # 維護日誌
├── lidarscan/          # LIDAR 掃描日誌
├── job/                # 任務執行日誌
└── user/               # 使用者操作日誌
```

---

## Sample 214

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\AMR_網路頻寬分析.md` L197

```
RealSense D435 × 4
  ↓ USB 3.0（每台 ~30 MB/s）
  ↓
ROS Driver（realsense-ros）
  ↓ 發布 /d435_*/color/image_raw（30 Hz, 921 KB/frame）
  ↓
┌─────────────────────────────────┐
│ Subscriber 1: camera_monitor    │ ← 接收 4 台 = 110 MB/s
│ Subscriber 2: processjsonservice│ ← 接收 4 台 = 110 MB/s（視覺定位時）
│ Subscriber 3: video_record      │ ← 接收 4 台 = 110 MB/s（錄影時）
│ Subscriber 4: web_video_server  │ ← 接收 4 台 = 110 MB/s（串流時）
└─────────────────────────────────┘
                                    最壞情況：4 subscriber × 110 MB/s = 440 MB/s
                                    = CPU 必須每秒複製/序列化 440 MB 的 image data
```

---

## Sample 215

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\Phase2_原始碼分析報告.md` L39

```
usserver.py
├── __init__()
│   ├── sensor_model: "UB350"（ROS param，實際值 UB350）
│   ├── rate: frame_rate（ROS param，實際值 8Hz）
│   ├── sensor_number: 8 個超音波感測器
│   ├── uslimit[]: 各感測器距離門檻
│   └── Publisher: /usserial (Int16MultiArray)
├── NormalProcess()  ← 主迴圈，threading 運行
│   └── while KeepRunning:
│       ├── usmod.dislimitArray_get()  ← 讀取感測器
│       ├── usserialpub.publish()      ← 發布到 ROS topic
│       └── time.sleep(resttime) 或 busy wait
└── vrstart()  ← 啟動 daemon thread

usmodule_UB350.py（感測器驅動）
├── __init__()
│   ├── baudrate: 115200
│   └── comport: /dev/ttyS0（serial port）
├── start()  ← 開啟 serial port
└── dislimitArray_get()  ← 核心讀取函式
    ├── while True: serial.read(1) 逐 byte 搜尋 header "UT"
    ├── serial.read(13) 讀取剩餘資料
    ├── XOR checksum 驗證
    └── 判斷 8 個感測器距離是否超過門檻
```

---

## Sample 216

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\Phase2_原始碼分析報告.md` L158

```
log_update.py（主程式）
├── runningLog.__init__()
│   ├── loggingCarWork:        0.01s（預設，車上未設定）← 100Hz！
│   ├── loggingMaintenanceTime: 3600s（車上設定）
│   └── loggingStatisticTime:  1s（預設，車上未設定）
├── _runningLog()
│   ├── _runningperiodiclog(0.01, log_work)           ← 每 0.01 秒
│   ├── _runningperiodiclog(3600, log_componentlife)   ← 每 1 小時
│   └── _runningperiodiclog(1, log_consumption)        ← 每 1 秒
└── sched.scheduler.run()  ← 事件迴圈

子模組（每個都是獨立 class）：
├── log_work_update.py    → log_work()        ← 100Hz 呼叫！
├── log_pscmd_update.py   → subscriber callback
├── log_consumption_update.py → log_consumption()  ← 每秒呼叫
├── log_maintenance_update.py → log_maintain_update()
├── log_componentlife_update.py → log_componentlife()
└── log_folder_check.py   → log_folder_check()
```

---

## Sample 217

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\Phase2_原始碼分析報告.md` L183

```
Step 1: 從 12 個 ROS Subscriber 讀取最新狀態
       ├── /carmovestate (routeprogress) → 車輛移動狀態
       ├── /battery_level (Float32)      → 電池電量
       ├── /robot_pose (Pose)            → 機器人位姿
       ├── /sysindicator/error (syserr)  → 警報代碼
       ├── /sysindicator/warn (syswarn)  → 警告代碼
       ├── /rfiderack (String)           → RFID 讀取
       ├── /rfiderack_UHF (String)       → UHF RFID
       ├── /cansns (cansns1)             → CAN 感測器 1
       ├── /cansns4 (cansns4)            → CAN 感測器 4
       ├── /cansns2 (cansns2)            → CAN 感測器 2
       ├── /docking_pose (Float32MultiArray) → 對接位姿
       └── listener class 封裝每個 subscriber

Step 2: 比較 20+ 個 field 的 new vs old 值
       ├── work_status, docking_status, next_point...
       ├── arm_status, battery_level, e84State...
       ├── lotStatus, chargeStationState, alarmcode...
       └── 任一欄位變化 → 觸發寫入

Step 3: 如果有變化
       ├── check_file()       → 驗證 CSV 檔案完整性（讀取整個檔案！）
       ├── 讀取 CSV 最後一行  → 與新資料再次比較
       └── 寫入 CSV            → append 一行（25 個欄位）

Step 4: 更新 old = new（15 個 field）
```

---

## Sample 218

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\README.md` L23

```
AMRCoolDown_v0/
├── syswork/          # ROS 系統監控套件 (v2.16.1, GPLv2)
│   ├── scripts/      # 55+ Python 監控腳本
│   ├── launch/       # 45 ROS launch 檔
│   ├── msg/srv/      # 自定義 ROS 訊息與服務
│   └── errorcode/    # 多語系警報定義
├── routemap/         # ROS 路徑規劃套件 (v1.25.8, GPLv2)
│   ├── scripts/      # 15 Python 核心腳本
│   ├── src/          # C++ 插件 + Python 模組
│   └── launch/       # 8 launch 檔
├── AGVWeb/           # Flask Web 管理介面
│   ├── agvweb/       # Flask 應用套件
│   ├── templates/    # 網頁模板
│   └── Dockerfile    # Docker 部署設定
├── Phase1_*.md       # 環境探索報告
├── Phase2_*.md       # 原始碼分析報告
├── Phase3_*.md       # 程式優化建議報告
├── 結案報告_*.md      # 結案報告
├── 調查方法手冊.md    # 診斷方法論
└── ssh_cmd.py        # SSH 遠端指令工具
```

---

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

## Sample 220

**Source**: `personal-rag_v2\PKB\vault\docs\AMRCoolDown\調查方法手冊.md` L462

```
Phase 1：環境探索（SSH 指令為主）
  ├── 系統資訊 → lscpu, free, uptime, df
  ├── CPU 概覽 → vmstat, top batch
  ├── 記憶體概覽 → free, ps --sort=-%mem
  ├── Docker 容器 → docker ps, docker stats
  ├── ROS 環境 → rosnode list, rosversion
  └── 輸出：Phase1_環境探索報告.md

Phase 2：原始碼深度分析（SSH + Git + /proc）
  ├── 從 CodeCommit clone repo（syswork, routemap, AGVWeb）
  ├── 從 /proc/<PID>/root/ 撈取非 repo 的原始碼（canbus）
  ├── rosparam get 驗證車上實際參數 vs 程式碼預設
  ├── rostopic hz 驗證 topic 發布頻率
  ├── 5 次 top batch 取樣取中位數
  ├── grep -r 搜尋程式碼中的關鍵 pattern
  └── 輸出：Phase2_原始碼分析報告.md

Phase 3：優化建議整理（本地分析為主）
  ├── 對照原始碼 + 即時數據，產出修改建議
  ├── 安全影響分析（最壞情況評估）
  ├── Bug 報告（程式碼品質問題）
  └── 輸出：Phase3_程式優化建議報告.md

審核：多輪交叉驗證
  ├── 獨立審核 agent 進行紅隊式否定審查
  ├── 每輪審核產出補充驗證指令
  ├── 執行補充指令後更新報告
  └── 輸出：Phase1_2_審核報告.md（初審 → 二審 → 三審）
```

---

## Sample 221

**Source**: `personal-rag_v2\PKB\vault\docs\templates\00_報告產生流程\marp_usage_guide.md` L295

```
/gyro-kb ── 產出 .md 報告
  │
  ├── /gyro-report ── MD → HTML（螢幕預覽、互動式導覽）
  │
  └── Marp CLI ── MD → PPTX / PDF（客戶交付）
```

---

## Sample 222

**Source**: `personal-rag_v2\PKB\vault\docs\templates\00_報告產生流程\report_workflow.md` L97

```
.images/
├── client/      ← 客戶提供（使用者確認正確版本）
├── db/          ← ChromaDB 搜尋（自動）
└── generated/   ← Mermaid 由瀏覽器渲染（不需存檔）
```

---

## Sample 223

**Source**: `personal-rag_v2\PKB\vault\docs\templates\00_報告產生流程\report_workflow.md` L124

```
workspace/CASE##/
├── [原始檔案]                        ← 輸入
├── input_data.json                   ← 理解（結構化提取）
├── params.json                       ← 確認（單一真相）
├── results.json                      ← 計算（非所有類型都需要）
├── verification.xlsx                 ← 驗算（非所有類型都需要）
├── 01_requirements_review.md/.html   ← 需求確認
├── 02_analysis_report.md/.html       ← 分析報告（如適用）
├── 03_[文件類型].md/.html            ← 最終產出
└── .images/
    ├── client/
    ├── db/
    └── generated/
```

---

## Sample 224

**Source**: `personal-rag_v2\PKB\vault\docs\templates\00_報告產生流程\report_workflow_v1.md` L28

```
Phase A：大量撈取    Phase B：統整+圖片     Phase C：報告產出
┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ A1 ChromaDB  │    │ B1 功能統整  │    │ C1 完整版     │
│ A2 客戶歸納  │──▶│ B2 客戶矩陣  │──▶│ C2 精簡版     │
│ A3 產品歸納  │    │ B3 報價分析  │    │ C3 對外版     │
│ A4 核心文件  │    │ IA1 圖片搜尋 │    │ C4 排版       │
└─────────────┘    │ IB1 圖片篩選 │    └──────────────┘
    可平行          └─────────────┘        循序
                       可平行
```

---

## Sample 225

**Source**: `personal-rag_v2\PKB\vault\docs\templates\00_報告產生流程\report_workflow_v1.md` L114

```
workspace/test_XX/
├── requirement.md                ← 輸入
├── A1~A4_*.json                  ← Phase A
├── B1~B3_*.json                  ← Phase B
├── IA1_*.json / IB1_*.json       ← Phase B-IMG
├── 01_xxx.md                     ← 完整版（內部）
├── 02_xxx_summary.md/.html/.pptx ← 精簡版（內部）
├── 03_xxx_external.md/.html      ← 對外版（匿名）
└── .images/db/                   ← 圖片（章節前綴命名）
```

---

## Sample 226

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\ERROR_CODE_REFERENCE.md` L113

```
夾爪應該夾緊，但 DI[2]&DI[5] 無信號
  ├─ DI[0] 有信號?  → YES → Error 1115（DI0 異常觸發）
  ├─ DI[1]&DI[2] 有信號? → YES → Error 1116（DI1+DI2 組合異常）
  ├─ DI[3] 有信號?  → YES → Error 1117（DI3 異常觸發）
  └─ 都沒有 → WaitFor 重試
```

---

## Sample 227

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\ERROR_CODE_REFERENCE.md` L137

```
夾爪應該夾緊 (grip_close=true)，正常期望 RS485IO = {1,0,1,1,1,*,0,1}
  ├─ RS485IO[0]==0 & [1]==1?  → YES → Error 1119（近接感測器反向）
  ├─ RS485IO[2]==0?           → YES → Error 1120（壓力感測器無信號）
  ├─ RS485IO[3]==0?
  │   ├─ RS485IO[4]==0?       → YES → Error 1122（位置感測器也無信號）
  │   ├─ RS485IO[6]==1?       → YES → Error 1124（異常偵測觸發）
  │   └─ RS485IO[7]==0?       → YES → Error 1125（重量感測器無信號）
  ├─ RS485IO[3]==1? (Tray 在位)
  │   ├─ RS485IO[4]==0?       → YES → Error 1122
  │   ├─ RS485IO[6]==1?       → YES → Error 1124
  │   └─ RS485IO[7]==0?       → YES → Error 1125
  └─ 都正常 → I/O 記錄 → Error 1121（狀態不一致）
```

---

## Sample 228

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\ERROR_CODE_REFERENCE.md` L178

```
夾爪應該半開 (grip_half=true)
  ├─ RS485IO[0]==0 & [1]==1?  → YES → Error 1133
  ├─ RS485IO[2]==0?           → YES → Error 1134
  ├─ RS485IO[3]==0?           → YES → Error 1135
  ├─ RS485IO[4]==0?           → YES → Error 1136
  ├─ RS485IO[6]==1?           → YES → Error 1138
  └─ RS485IO[7]==0?           → YES → Error 1139
```

---

## Sample 229

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\FLOW_ANALYSIS.md` L55

```
Start
  └─ SubFlow: ARM_parameter（初始化手臂參數）
       ├─ [g_use_RS485IO == false] → 非 RS485 模式初始化
       │    ├─ [g_use_initial_point_setting_from_txt == false] → 直接設 ENCODER/LED
       │    └─ [true] → 從 TXT 檔讀取初始點位（read_file → READ_TXT → 迴圈解析）
       │
       └─ [g_use_RS485IO == true] → RS485 模式初始化
            ├─ 檢查 RS485IO[0..7] 狀態 → SET_ENCODER/LED
            ├─ 同樣支援 TXT 檔讀取
            └─ 設定 I/O Box × 6 + I/O EX × 4 → SET_ARM_POSE

  → Component: AMR_V001_CommunicationNoStop1（Modbus 通訊，持續監聽 AMR 指令）
  → SET: SET_ARM_param → port_name → landmark_id → BARCODE_ID
  → Log: MISSION_START × 3
  → SET: set_var_running

  → [var_var_running_array[0] == 3] → Gateway (主分派器)
       ├─ [0] → NONE_MOVE（待機）
       ├─ [1] → MOVE_TRAY_to_LEFT_multi_EQ（左側設備搬運）
       ├─ [2] → MOVE_TRAY_to_RIGHT_multi_EQ（右側設備搬運）
       └─ [3] → MOVE_INITIAL（回初始位）

  → Log: MISSION_DONE × 3
  → GOTO: AMR_V001_CommunicationNoStop1（回到通訊迴圈）
```

---

## Sample 230

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\FLOW_ANALYSIS.md` L382

```
                    ┌─────────────────────┐
                    │   AMR (Modbus 通訊) │
                    └──────────┬──────────┘
                               │ var_var_running_array
                    ┌──────────▼──────────┐
                    │   ARM_parameter     │ ← 初始化（RS485/TXT 點位）
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Gateway        │ ← 主分派器
                    │  [0]=方向 [3]=目標   │
                    └─┬────┬────┬────┬───┘
                      │    │    │    │
              ┌───────┘    │    │    └────────┐
              ▼            ▼    ▼             ▼
         MOVE_LEFT    MOVE_RIGHT  INITIAL   NONE_MOVE
              │            │        │
    ┌─────┬──┴──┬────┐    ...   ReturnHome
    ▼     ▼     ▼    ▼
  ERACK  EQ   ICOS  STK   ← [3] 目標類型
    │     │          │
  PORT_1~8          TAKE/PLACE ← [4] Port 編號
    │
  ┌─┴─────────────────┐
  │  HT_9046LS_TAKE   │ ← 設備操作
  │  HT_9046LS_PLACE  │
  │  MR_PORT_TAKE     │
  │  MR_PORT_PLACE    │
  │  ERACK_TAKE/PLACE │
  │  STK_TAKE/PLACE   │
  └────────────────────┘
           ↕
    ┌──────────────┐
    │  Vision Jobs  │ ← TMark/AprilTag/Barcode
    │  Sensor Check │ ← 夾爪/雷射/IO
    │  Log/Modbus   │ ← 回報 AMR
    └──────────────┘

背景執行緒（常駐同時運作）：
  - CHECK_GRIP_2        持續監控夾爪（440 節點）
  - CHECK_ENCODER       監控編碼器（17 節點）
  - CHECK_ALL_SENSOR_WHEN_CAR_MOVING_2  移動中安全監控（86 節點）
  - Pause_handle        處理暫停請求（9 節點）
  - Pub_RS485IO         發佈 I/O 狀態（7 節點）
```

---

## Sample 231

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L88

```
IF: var_camera_once_eq_flag==true & g_camera_once==true?
  ├─ [YES] 已經拍過照，跳過 Vision FAR
  │    IF: var_runing > 0?
  │      ├─ [YES] → 直接到 Port 分派（Phase 5）
  │      └─ [NO]  → 移動到 P110 → Phase 5
  │
  └─ [NO] 未拍過照，執行 Vision FAR（Phase 3）
```

---

## Sample 232

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L103

```
Vision: RIGHT_HT_9046LS_right_TMMARK_FAR
  ├─ [成功]
  │    SET: var_coordrobot = Robot[0].CoordRobot          ← 記錄當前機器人座標
  │         var_Log_vision_base = Base["vision_...FAR"]   ← 記錄視覺基座值
  │    Log: 記錄座標
  │
  │    ── 驗證 1：Rz 角度檢查 ──
  │    IF: abs(vision_base[5]) 在 80°~100° 之間?
  │      ├─ [YES] → 驗證 2
  │      └─ [NO]  角度異常
  │           ├─ [重試<g_vision_retry] → vision_count++ → 回到 Vision FAR
  │           └─ [重試>=g_vision_retry]
  │                → Log ERROR → SET: error_code=1227 → STOP
  │
  │    ── 驗證 2：Z 軸距離檢查 ──
  │    IF: |coordrobot[2] - vision_base[2]| <= 350?
  │      ├─ [YES] → 驗證 3
  │      └─ [NO]  Z 軸偏差過大
  │           ├─ [重試<=g_tag_distance_retry] → tag_distance_count++ → 回到 Vision FAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1224/1225 → STOP
  │
  │    ── 驗證 3：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_base[4]| <= g_check_EQ_far_tolerance[4]?
  │      ├─ [YES] → 通過! → 移動到 P70 → Phase 4
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] → count++ → 回到 Vision FAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1223 → STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] → vision_count++ → Log ERROR → 回到 Vision FAR
       └─ [超過重試]
            → Log ERROR → SET: error_code=1223 → STOP
```

---

## Sample 233

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L140

```
移動到 P70（近距拍照位）
SET: 重置所有計數器

Vision: RIGHT_HT_9046LS_right_TMMARK_NEAR
  ├─ [成功]
  │    SET: var_temporary_fl = modbus_read("mtcp_AMR","preset_en_fl")  ← 讀取 AMR 感測器
  │         var_temporary_bl = modbus_read("mtcp_AMR","preset_en_bl")
  │         var_temporary_fr = modbus_read("mtcp_AMR","preset_en_fr")
  │    SET: var_coordrobot = Robot[0].CoordRobot
  │         var_Log_vision_base = Base["vision_...NEAR"]
  │    Log: 記錄座標
  │
  │    ── 驗證：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_NEAR_base[4]| <= g_check_EQ_near_tolerance[4]?
  │      ├─ [YES] → 通過! → Phase 5（Camera Once 分派 或 Port 分派）
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] → count++ → 回到 Vision NEAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1226 → STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] → vision_count++ → 回到 Vision NEAR
       └─ [超過重試]
            → Log ERROR → SET: error_code=1225 → STOP
```

---

## Sample 234

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L170

```
IF: g_use_RS485IO == false?  → Gateway（非 RS485）
IF: g_use_RS485IO == true?   → Gateway（RS485）

Gateway: var_to_port_number
  ├─ [1] EQ_PORT1 → 檢查 EQ_TYPE → HT_9046LS_001_front → check_tray_distance
  ├─ [2] EQ_PORT2 → 檢查 EQ_TYPE → HT_9046LS_002_front → check_tray_distance
  └─ [3] EQ_PORT3 → 檢查 EQ_TYPE → HT_9046LS_003_front → check_tray_distance
```

---

## Sample 235

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L209

```
IF: DIO 數位感測器有信號?
  ├─ [YES] 有 Tray
  │    IF: var_LASER_MEASURE <= g_highest_point & var_laser_volt >= 1.5?
  │      ├─ [YES] 距離正常 → 重試 (count++ → 回到 Vision FAR/NEAR)
  │      └─ [NO]  → 二次確認 (double_check)
  │
  └─ [NO] 無 DIO 信號 → Log ERROR → 回到 Vision FAR/NEAR
```

---

## Sample 236

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L221

```
IF: var_RS485IO[7] == 0?  ← RS485 第 8 位 = Tray 感測器
  ├─ [0] 無 Tray
  │    IF: LASER_MEASURE <= g_highest_point & laser_volt >= 1.5?
  │      ├─ [YES] 雷射也確認無 Tray → 重試
  │      └─ [NO]  → 二次確認 (double_check)
  │
  └─ [非0] 有 Tray → Log ERROR → 回到 Vision FAR/NEAR
```

---

## Sample 237

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L233

```
IF: g_double_check_if_tray_on_EQ_port == true?
  ├─ [YES]
  │    IF: var_LASER_MEASURE >= g_lowest_point?
  │      ├─ [YES] 距離夠遠，確認沒有 Tray
  │      │    SET: var_temp_LASER_MEASURE = var_LASER_MEASURE  ← 暫存
  │      │    Move: in_gyro_move_to_tray                       ← 靠近一點再看
  │      │    WaitFor: 1000ms
  │      │    SET: 重新測量 LASER_MEASURE
  │      │    SET: 重新計算 put_down_distance
  │      │    → 第二輪感測器檢查
  │      │
  │      └─ [NO] 距離太近，可能有 Tray → Gateway 分派到各 Port front
  │           → GOTO 回到主流程
  │
  └─ [NO] 不做二次確認 → 直接到 Port 分派
```

---

## Sample 238

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L253

```
移動到 HT_9046LS_00X_front（Port 前方）

IF: var_LASER_MEASURE >= g_lowest_point?
  ├─ [YES] var_nothing_on_port_can_place = true   ← Port 空的，可以放
  └─ [NO]  var_nothing_on_port_can_place = false   ← Port 有東西，不能放

Log: LASER_DISTANCE
```

---

## Sample 239

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L264

```
IF: g_place_again == true?
  ├─ [YES] → 重置 count=0 → 繼續（允許重試放置）
  └─ [NO]  → Log ERROR → SET: error_code=1014 → STOP
```

---

## Sample 240

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L345

```
HT_9046LS_TMMARK_NORMAL 入口
│
├─ 初始化 (Log, SET grip_in="EQ", 重置計數器)
│
├─ Camera Once 優化?
│   ├─ [已拍過] → 跳過視覺 → Phase 5
│   └─ [未拍過] ↓
│
├─ ═══ Vision FAR ═══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_FAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] → 記錄座標
│   │   ├─ 驗證 1: Rz ∈ [80°, 100°]?
│   │   │   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1227)
│   │   ├─ 驗證 2: |ΔZ| ≤ 350mm?
│   │   │   └─ [失敗] → 重試 ≤ g_tag_distance_retry → STOP(1224)
│   │   └─ 驗證 3: |ΔRy| ≤ far_tolerance?
│   │       └─ [失敗] → 重試 ≤ g_re_try → STOP(1223)
│   │
│   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1223)
│
├─ 移動到 P70（近距位）
│
├─ ═══ Vision NEAR ══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_NEAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] → 記錄座標 + 讀取 AMR 感測器
│   │   └─ 驗證: |ΔRy| ≤ near_tolerance?
│   │       └─ [失敗] → 重試 ≤ g_re_try → STOP(1226)
│   │
│   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1225)
│
├─ ═══ Port 分派 ════════════════════════
│   Gateway: var_to_port_number
│   ├─ [1] → HT_9046LS_001_front → check_tray_distance
│   ├─ [2] → HT_9046LS_002_front → check_tray_distance
│   └─ [3] → HT_9046LS_003_front → check_tray_distance
│
├─ ═══ 雷射測距 ═════════════════════════
│   WaitFor: 1000ms（穩定）
│   LASER = AI[0] × 57.5 + 30 (mm)
│   put_down_distance = LASER - gripper_depth
│
├─ ═══ Tray 存在判斷 ════════════════════
│   │
│   ├─ 第一層: DIO / RS485IO[7] 感測器
│   ├─ 第二層: LASER ≤ highest_point & volt ≥ 1.5V?
│   └─ 第三層: double_check → 靠近再測一次
│
├─ ═══ 最終輸出 ═════════════════════════
│   var_nothing_on_port_can_place = true/false
│   │
│   └─ g_place_again?
│       ├─ [true]  → 允許重試放置
│       └─ [false] → STOP(1014)
│
└─ 收尾 (Log, SET grip_in="", 返回)
```

---

## Sample 241

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\MR_PORT_PLACE_ANALYSIS.md` L93

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") != true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") != true
  ├─ [條件成立] → Port 是空的 → 繼續放置
  └─ [條件不成立] → Port 上有東西
       ├─ [var_PSPL_check < 3] → 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] → 超過重試次數
            → Log: ERROR_CODE
            → SET: ERROR_CODE_MODBUS = 1311
            → STOP（停機）
```

---

## Sample 242

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\MR_PORT_PLACE_ANALYSIS.md` L109

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") == true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") == true
  ├─ [條件成立] → Tray 確認在位 → 後退離開
  └─ [條件不成立] → Tray 不在位
       ├─ [var_PSPL_check < 3] → 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] → 超過重試次數
            → Log: ERROR_CODE
            → SET: ERROR_CODE_MODBUS = 1311
            → STOP（停機）
```

---

## Sample 243

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\MR_PORT_PLACE_ANALYSIS.md` L125

```
IF: var_MR_check_PSPL == true
  ├─ [true]  → 執行 Modbus 讀取 PS/PL 確認
  └─ [false] → 跳過檢查，直接操作
```

---

## Sample 244

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\MR_PORT_PLACE_ANALYSIS.md` L178

```
MR_PORT_PLACE 入口
│
├─ Log: PLACE_TRAY (×2)
├─ SET: var_grip_in = "MR"
├─ SET: var_MR_check_PSPL = false
│
├─ Gateway: MR_PORT_NUMBER (var_MR_port_number)
│   ├─ [1]  → MR_1_front → MR_1_pre_take
│   ├─ [2]  → MR_2_front → MR_2_pre_take
│   ├─ [3]  → MR_3_front → MR_3_pre_take
│   ├─ [4]  → MR_4_front → MR_4_pre_take
│   ├─ [5]  → P22 → MR_5_front → MR_5_pre_take
│   ├─ [6]  → P22 → MR_6_front → MR_6_pre_take
│   ├─ [7]  → P10 → MR_7_front → MR_7_pre_take
│   ├─ [8]  → P10 → MR_8_front → MR_8_pre_take
│   ├─ [9]  → ...
│   └─ [12] → ...
│
│  ===== 以下以 Port 1 為例 =====
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] → 放置前 PSPL 檢查
│   │   ├─ IF: Buffer_1_PS != true & Buffer_1_PL != true?
│   │   │   ├─ [YES] Port 空 → 繼續
│   │   │   └─ [NO]  Port 有東西
│   │   │       ├─ [重試<3] → PSPL_check++, Log, WaitFor 500ms → 回到檢查
│   │   │       └─ [重試>=3] → Log ERROR → Modbus 1311 → STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] → SET: pause_false → 跳過檢查
│
├─ SubFlow: SENSOR_Grip_half（夾爪半開）
│
├─ Point: MR_1_take_up（Port 1 上方）
├─ SET: SET_grip（設定夾爪為 open 狀態）
├─ Point: MR_1_take（下降到放置位）
│
├─ SubFlow: SENSOR_Grip_open（夾爪全開，釋放 Tray）
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] → 放置後 PSPL 確認
│   │   ├─ IF: Buffer_1_PS == true & Buffer_1_PL == true?
│   │   │   ├─ [YES] Tray 在位 → 繼續
│   │   │   └─ [NO]  Tray 不在位
│   │   │       ├─ [重試<3] → PSPL_check++, Log, WaitFor 500ms → 回到確認
│   │   │       └─ [重試>=3] → Log ERROR → Modbus 1311 → STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] → 跳過確認
│
├─ Move: back_15mm（後退 15mm）
├─ Point: MR_1_ready_to_take（準備離開位）
├─ Point: MR_1_front（回到前方安全位）
│
├─ Log: PLACE_TRAY (×2)
├─ SET: var_if_CHECK_ALL_SENSOR_WHEN_CAR_MOVING = true
├─ SET: var_grip_in = "MR"（重設夾爪來源）
│
└─ 結束（返回上層流程）
```

---

## Sample 245

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\TMFLOW_DOMAIN_API_NOTE.md` L71

```
gamepad → Python
  ├─ motion：UIAutomation 點擊 TMflow Jog Panel (Route B)
  └─ save  ：DomainAPI SetProjectPointInfo (Route I-a) ⭐
```

---

## Sample 246

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\TMFLOW_DOMAIN_API_NOTE.md` L82

```
E:\github\UR_Program_Analysis_v0\docs\gRPC\
├─ u16_AEE885grpc.docx                    # 需求文件原檔
├─ 需求管理表_V3.xlsx                     # 23 項需求清單
├─ req.csv                                # csv 版需求表
├─ gRPC連線測試.mp4                       # 連線測試影片
├─ docx_content.txt                       # pip install 備忘
└─ gRPCTest/
   ├─ TMDomainAPI_r20260206.7z            # ⭐ 官方 DomainAPI 包
   │  └─ TmDomainService.proto            # 已解壓到 _TMDomainAPI_extracted/
   │  └─ Readme.txt                       # 版本更新說明
   ├─ Client/TMgrpcClient.exe             # .NET demo client
   ├─ Server/TMgrpcServer.exe             # .NET demo server
   └─ PythonClient/
      ├─ CmdProto.proto                   # hello world sample（不是真的）
      ├─ CmdProto_pb2.py / _pb2_grpc.py   # stub
      └─ gRPCclient.py                    # client 範例（localhost:5005）
```

---

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
|  ├─ HID 事件 → 抽象 intent 事件     |---------------------+
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
|  DomainAPI + Jog RPCs (§4 待 TM 實作)|
+--------------------------------------+
```

---

## Sample 248

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L80

```
使用者在統一 UI 按「存點」
  ├─ (1) gRPC SavePointFromCurrent / UpdatePointPartial → TMflow 專案檔
  └─ (2) 同步更新 GYRO YAML 對應 waypoint → Git commit (optional hook)
```

---

## Sample 249

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L206

```
tmflow_domain_client/
├─ proto/
│  └─ TmDomainService.proto          # 從 TM release 拷貝
├─ _generated/                        # grpc_tools.protoc 產出
│  ├─ TmDomainService_pb2.py
│  └─ TmDomainService_pb2_grpc.py
├─ client.py                          # Channel / stub 管理
├─ session.py                         # TeachSession context manager
├─ teach.py                           # 高階 helpers (jog_cartesian, save_point, ...)
├─ models.py                          # dataclass 對應 proto message
└─ tests/
   ├─ test_with_mock_server.py        # 用 grpcio testing 起 mock server
   └─ test_integration.py             # 需連真機，gated by env var
```

---

## Sample 250

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L256

```
hid_input/
├─ backends/
│  ├─ pygame_backend.py         # Windows/macOS/Linux 通用（搖桿、手把）
│  ├─ hidapi_backend.py         # 底層 HID（自製裝置、SpaceMouse）
│  └─ evdev_backend.py          # Linux-only，低延遲踏板
├─ profiles/                    # YAML profile 目錄（使用者可擴充）
│  ├─ xbox_dual_analog.yaml
│  ├─ spacemouse_compact.yaml
│  ├─ linemaster_3pedal.yaml
│  └─ schema.json               # profile 語法驗證
├─ intents.py                   # intent 事件 dataclass 定義
├─ translator.py                # HID event → intent (profile-driven)
├─ dispatcher.py                # intent → 統一 UI event bus
├─ watchdog.py                  # 連續 jog safety watchdog
└─ tests/
   ├─ test_profile_loader.py
   ├─ test_translator.py        # 用錄製的 HID event 檔重播
   └─ test_watchdog.py
```

---

## Sample 251

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\VISION_ARCHITECTURE.md` L15

```
.job XML ────► parse_job_file() ──┐
                                   ├─► VisionJob[] ──► analyze_vision() ──► VisionAnalysis
profile XML ─► enrich_from_profile()┘                                              │
                                                                                   ▼
.flow JSON ─► FlowGraph.get_vision_node_info() ─► FlowAnalysis.vision_node_info    │
                                       │                                             │
                                       └──► tm_doc_generator ◄─────────────────────┘
                                                  │
                                                  ├─► VISION_SYSTEM_ANALYSIS.md
                                                  ├─► VISION_JOB_MAP.md
                                                  └─► subflows/*.md（Vision 區段）
```

---

## Sample 252

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\VISION_ARCHITECTURE.md` L246

```
experiments/baseline/        ← TM Flow 匯出的最簡 Vision Job
experiments/exp_NN_<name>/   ← 改一項設定後的快照
        │
        ▼
scripts/vision_schema_diff.py
        │
        ▼
docs/findings/exp_NN_*.md    ← 自動 diff 報表
        │
        ▼
docs/VISION_SCHEMA_FINDINGS.md  ← 累積知識庫
```

---

## Sample 253

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\experiments\README.md` L8

```
experiments/
├── README.md          ← 本檔
├── baseline/          ← 共用 baseline vision dir（由 TM Flow 匯出）
├── exp_01_<name>/     ← 每個實驗一個子資料夾
├── exp_02_<name>/
└── ...
```

---

## Sample 254

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\INDEX.md` L77

```
data/
├── ConfigData.xml
├── GlobalVariable.xml
├── Projects/GYRO_FT_RobotARM_Micron_v_0_0_15/
│   ├── *.flow                ← 主 Flow JSON
│   └── bak/                  ← 歷史備份
└── Vision/
    ├── jobs/GYRO_FT_RobotARM_Micron_v_0_0_15/
    │   ├── 35536500.job      ← 68 個 Vision Job 主檔
    │   └── <jobcode>/<jobcode>.xml  ← 各 Job 的 recognition profile
    └── ...
```

---

## Sample 255

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\INDEX.md` L114

```
experiments/
├── README.md            ← 工作流程說明
├── baseline/            ← TM Flow 匯出的最簡 Vision Job baseline
└── exp_NN_<name>/       ← 每個 GUI 設定變更的快照
```

---

## Sample 256

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\README.md` L7

```
├── src/                 Python 工具原始碼
├── scripts/             輔助工具（schema diff 等）
├── data/                TM 解壓資料（從 archive/ 重建）
├── archive/             TM 匯出原始壓縮（.zip + .z01）
├── output/              自動產生的分析文件
├── docs/                文件、官方手冊、findings/
└── experiments/         Vision schema 反向實驗工作區（不入庫）
```

---

## Sample 257

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 258

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L41

```
                    ┌──────────────────┐
    RTDE (reg 0-2)  │   PLC / MES      │
   ◄───────────────►│  (外部控制器)  │
                    └──────────────────┘
                            │
                    ┌───────┴───────┐
                    │    UR30       │
                    │ (Polyscope)   │
                    └──┬───┬───┬───┘
          Modbus TCP   │   │   │  RS485
       ┌───────────────┘   │   └──────────────┐
       ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ PLC/IO 模組  │  │  SensoPart   │  │ TC100 Gripper    │
│ 192.168.1.1  │  │  VISOR       │  │ + RS485 IO Box   │
│ Modbus TCP   │  │  XML-RPC     │  │ Tool Modbus      │
│ port 502     │  │  port 46527  │  │ addr 1,2         │
└──────────────┘  └──────────────┘  └──────────────────┘
```

---

## Sample 259

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L130

```
var_read_RTDE ≔ read_input_integer_register(0)
    │
    ├─ 30001：初始化歸位（開夾 → 依位置回 Home_L 或 Home_R）
    ├─ 30000：移動到啟動位（p_for_startup）
    ├─ 30002：開夾 → 回 Home_R
    ├─ 30009：Fork 感測器檢查
    └─ 其他 ：進入自動作業模式
```

---

## Sample 260

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L142

```
解析外部指令 → 讀取 RS485 IO → 判斷 port_direction
    │
    ├─ port_direction = 1（入料方向）
    │   ├─ to_port_type = 1（Erack）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put（取放 Body）
    │   │   ├─ turnL 路徑轉向（若需跨區）
    │   │   └─ Erack_load_unload
    │   │
    │   ├─ to_port_type = 2（EQ2600 系列）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put
    │   │   └─ EQ2600_port{1-4}_{load/unload}
    │   │
    │   ├─ to_port_type = 3（EQ2800 系列）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put
    │   │   └─ EQ2800_port{1-4}_{load/unload/swap}
    │   │
    │   ├─ to_port_type = 4（EQ2845）
    │   │   └─ EQ2845_port1_load_unload
    │   │
    │   └─ to_port_type = 5（EQ3670）
    │       └─ EQ3670_port{1-2}_{load_unload/backup}
    │
    └─ port_direction = 2（出料方向）
        └─ （與入料對稱，順序反轉）
```

---

## Sample 261

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L330

```
K11_UR30_Project/programs/
├── Gyro/                           # 核心與輔助
│   ├── initial_prog.script/.txt    # 主程式入口（12,241 行）
│   ├── initial_modbus_tcp.script   # Modbus TCP 訊號定義
│   ├── tc100_gripper_open.script   # 夾爪開啟
│   ├── tc100_gripper_close.script  # 夾爪關閉
│   ├── fork_sensor_check.script    # Fork sensor 檢查
│   ├── payload.script              # Payload 計算
│   ├── set_alarm_and_stop.script   # 統一錯誤處理
│   ├── get_command_*.script        # 指令解析
│   ├── gripeer_cover_*.script      # 蓋子開關
│   ├── Loop.script / Loop_initial.script  # 迴圈計數器
│   └── rs485io_read.script         # RS485 IO 讀取
├── Body_*.script/.txt              # Body 取放
├── EQ*.script/.txt                 # 各設備操作
├── Erack_*.script/.txt             # Erack 裝卸
├── .SensoPart/calibsets/*.calib    # VISOR 校正
└── *.urp                           # 二進位程式（未解析）
```

---

## Sample 262

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L361

```
initial_prog (主程式)
├── Body_take_put
├── Erack_load_unload
├── EQ2600_port1_load / port2_unload / port3_load / port4_unload
├── EQ2800_port{1-4}_{load/unload/swap}
├── EQ2800P02_port{1-4}_{load/unload/swap}
├── EQ2845_port1_load_unload
├── EQ3670_port{1-2}_load_unload
├── EQ3800_port1_load_unload
└── [helpers]
    ├── tc100_gripper_open / close
    ├── gripeer_cover_open / close / open_180
    ├── fork_sensor_check
    ├── payload
    ├── set_alarm_and_stop
    ├── initial_modbus_tcp
    ├── get_command_extra_info / portname
    ├── rs485io_read
    └── Loop_initial / Loop
```

---

## Sample 263

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\PHASE2_SPEC.md` L526

```python
# ── 常數 ──
UR30_DH_PARAMS: list[dict]  # [{"a": float, "d": float, "alpha": float}, ...]

# ── 正向運動學 ──
def forward_kinematics(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> list[float]:
    """由關節角度計算末端姿態。
    
    Args:
        joints: [j1, j2, j3, j4, j5, j6]（弧度）
        dh_params: 可選 DH 參數覆蓋，None 使用 UR30 預設
    Returns:
        [x, y, z, rx, ry, rz]（公尺, 弧度 — axis-angle 表示法）
    """

def forward_kinematics_matrix(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> 'numpy.ndarray':
    """由關節角度計算 4x4 齊次變換矩陣。
    
    Returns:
        4x4 numpy array
    """

# ── 逆向運動學 ──
def inverse_kinematics(
    pose: list[float],
    q_near: list[float] | None = None,
    dh_params: list[dict] | None = None
) -> list[list[float]]:
    """由末端姿態計算關節角度（最多 8 組解）。
    
    Args:
        pose: [x, y, z, rx, ry, rz]（公尺, axis-angle 弧度）
        q_near: 偏好解（選最接近此組的解），None 則回傳所有解
        dh_params: 可選 DH 參數覆蓋
    Returns:
        關節角度解的列表，每個解為 [j1..j6]
        如果 q_near 有值，只回傳最接近的一組（list 長度 1）
    """

# ── 工具函式 ──
def pose_to_matrix(pose: list[float]) -> 'numpy.ndarray':
    """axis-angle pose → 4x4 齊次矩陣。"""

def matrix_to_pose(matrix: 'numpy.ndarray') -> list[float]:
    """4x4 齊次矩陣 → axis-angle pose。"""

def rotation_vector_to_matrix(rvec: list[float]) -> 'numpy.ndarray':
    """axis-angle [rx, ry, rz] → 3x3 旋轉矩陣（Rodrigues 公式）。"""

def matrix_to_rotation_vector(R: 'numpy.ndarray') -> list[float]:
    """3x3 旋轉矩陣 → axis-angle [rx, ry, rz]。"""

# ── 驗證函式 ──
def validate_waypoint(
    waypoint: 'URWaypoint',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> dict:
    """驗證一個 waypoint 的 pose 和 joints 是否一致。
    
    用 FK(joints) 計算出 pose，與宣告的 pose 比較。
    
    Args:
        waypoint: URWaypoint 物件
        tolerance_mm: 位置容差（毫米）
        tolerance_deg: 角度容差（度）
    Returns:
        {
            "name": str,
            "valid": bool,
            "position_error_mm": float,
            "orientation_error_deg": float,
            "fk_pose": list[float],    # FK 計算的 pose
            "declared_pose": list[float],  # 宣告的 pose
            "details": str  # 人類可讀的描述
        }
    """

def validate_all_waypoints(
    project: 'URProject',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> list[dict]:
    """驗證專案中所有 waypoint。
    
    Returns:
        驗證結果列表（同 validate_waypoint 的 return 格式）
        只包含有 pose 和 joints 都有值的 waypoint
    """

def generate_validation_report(results: list[dict]) -> str:
    """產生 Markdown 格式的驗證報告。
    
    報告結構：
    ## Waypoint FK/IK 驗證報告
    - 統計：總數 / 通過 / 失敗 / 跳過（缺 pose 或 joints）
    - 失敗清單（表格：名稱、位置誤差、角度誤差、來源檔案）
    - 通過清單（摘要）
    """
```

---

## Sample 264

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\TM_UR_COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 265

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\README.md` L8

```
├── src/                 Python 工具原始碼
├── data/                UR 程式資料（從 K11_UR30_Project 複製）
├── archive/             UR 匯出原始壓縮（.zip）
├── output/              自動產生的分析文件
└── docs/                手動撰寫的分析文件
```

---

## Sample 266

**Source**: `personal-rag_v2\PKB\workspace\teset_04\02_AMHS_AI_Smart_summary.md` L52

```
Phase 1 (0-6月)          Phase 2 (6-12月)         Phase 3 (12-24月)
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ TSC: Alarm AI    │    │ AMR: 語義導航    │    │ Arm: AI 抓取  │
│ RTD: ML 派車     │    │ TSC: RL 派車     │    │ E84: 異常預測 │
│ 電池壽命預測      │    │ 預測性維護       │    │ AI-EAP 配置  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
 投資: ~3-4M NTD/yr     追加: ~2-3M NTD        追加: ~2-3M NTD
 UPH +10-15%            UPH 再+5-10%           FAE 調機 -50%
 Alarm 處理 -40%        停機 -30%              Arm alarm -30%
```

---

## Sample 267

**Source**: `personal-rag_v2\PKB\workspace\teset_04\02_AMHS_AI_Smart_summary_v1.1.md` L56

```
Phase 1 (0-6月)          Phase 2 (6-12月)         Phase 3 (12-24月)
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ TSC: Alarm AI    │    │ AMR: 語義導航    │    │ Arm: AI 抓取  │
│ RTD: ML 派車     │    │ TSC: RL 派車     │    │ E84: 異常預測 │
│ 電池壽命預測      │    │ 預測性維護       │    │ AI-EAP 配置  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Sample 268

**Source**: `personal-rag_v2\PKB\workspace\teset_04\03_AMHS_AI_Smart_external - V0.md` L151

```
Phase 1 (0-6月)          Phase 2 (6-12月)         Phase 3 (12-24月)
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ TSC: Alarm AI    │    │ AMR: 語義導航    │    │ Arm: AI 抓取  │
│ RTD: ML 派車     │    │ TSC: RL 派車     │    │ E84: 異常預測 │
│ 電池壽命預測      │    │ 預測性維護       │    │ AI-EAP 配置  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Sample 269

**Source**: `personal-rag_v2\PKB\workspace\teset_04\03_AMHS_AI_Smart_external.md` L151

```
Phase 1 (0-6月)          Phase 2 (6-12月)         Phase 3 (12-24月)
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ TSC: Alarm AI    │    │ AMR: 語義導航    │    │ Arm: AI 抓取  │
│ RTD: ML 派車     │    │ TSC: RL 派車     │    │ E84: 異常預測 │
│ 電池壽命預測      │    │ 預測性維護       │    │ AI-EAP 配置  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Sample 270

**Source**: `personal-rag_v2\PKB\workspace\test_02\01_mcs_lite_study.md` L99

```
┌─────────────────────────────────────────────────────────┐
│                    客戶 MES / MCS                       │
│              (WEB API / MSMQ / E82/E88)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │    ACS Gateway        │  (Windows 10 Pro)
           │  - MSMQ Bridge        │
           │  - Web UI             │
           └───────────┬───────────┘
                       │ (ACS 專用網域)
           ┌───────────┴───────────┐
           │    TSC + MCS lite     │  (Linux RedHat / Windows Server)
           │  ┌─────────────────┐  │
           │  │    MCS lite     │  │  - 物料管理 / 搬運指令
           │  │  (BYPASS/RTD)   │  │  - SECS E82/E82+/E88
           │  └────────┬────────┘  │
           │           │           │
           │  ┌────────┼────────┐  │
           │  │                 │ │ │
           │ AGVC   E-RACKC  STKC │  - 派車交管 / 貨架管理 / 倉儲管理
           │  │        │        │  │
           └──┼────────┼────────┼──┘
              │        │        │
     ┌────────┴─┐  ┌───┴───┐  ┌┴────────┐
     │ AMR 車輛  │  │E-Rack │  │ Stocker │
     │(Prop.    │  │(TCP/IP│  │(E84/ │
     │ Protocol)│  │ JSON) │  │ SECS) │
     └──────────┘  └───────┘  └─────────┘
         │
    ┌────┴────┐
    │EQ Load  │  (E84 / Virtual E84)
    │Port     │
    └─────────┘
```

---

## Sample 271

**Source**: `personal-rag_v2\PKB\workspace\test_02\02_mcs_lite_study_summary.md` L31

```
客戶 MES/MCS  ──(WEB API / MSMQ / E82/E88)──▶  ACS Gateway (Win10)
                                                       │
                                                TSC + MCS lite (Linux RedHat)
                                                ┌──────┼──────┐
                                              AGVC  E-RACKC  STOCKERC
                                                │      │       │
                                              AMR    E-Rack  Stocker
                                                │
                                           EQ Load Port (E84)
```

---

## Sample 272

**Source**: `personal-rag_v2\PKB\workspace\test_02\03_mcs_lite_study_external.md` L31

```
客戶 MES/MCS  ──(WEB API / MSMQ / E82/E88)──▶  ACS Gateway (Win10)
                                                       │
                                                TSC + MCS lite (Linux RedHat)
                                                ┌──────┼──────┐
                                              AGVC  E-RACKC  STOCKERC
                                                │      │       │
                                              AMR    E-Rack  Stocker
                                                │
                                           EQ Load Port (E84)
```

---

## Sample 273

**Source**: `personal-rag_v2\PKB\workspace\test_03\MCS-lite_說明.md` L18

```
MES / 上位 MCS
        │
    ┌───┴───┐
    │  TSC  │  ← 搬運系統管理（調度核心）
    │+ MCS  │
    │  lite │
    └───┬───┘
        │ Proprietary Protocol / SECS/GEM / Web API / Message Queue
   ┌────┼────────┬────────────┐
   │    │        │            │
 AGVC  StockC  E-RackC     EAP
  │      │       │           │
 AMR  Stocker  E-Rack    Load Port
              (Buffer)   (E84 設備)
```

---

## Sample 274

**Source**: `personal-rag_v2\PKB\workspace\test_05\02_AMHS_AI_x_SoftBank_DC_strategy.md` L450

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   AMHS AI Smart                 SoftBank DC POC             │
│   ─────────────                 ────────────────            │
│   需要 GPU 算力    ◄──── 戰略連結 ────►   整個機房都是 GPU │
│   客戶嫌 GPU 太貴                        GYRO 已在 GPU 生態圈 │
│   IT 管制進不了雲端                      理解 DC 基礎設施   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Sample 275

**Source**: `personal-rag_v2\PKB\workspace\test_05\03_AMHS_AI_Smart_proposal_external.md` L209

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  AMHS AI Smart              Data Center AGV              │
│  ─────────────              ───────────────              │
│  需要 GPU 算力  ◄── 戰略連結 ──►  整個機房都是 GPU     │
│  客戶嫌太貴                      GYRO 深入 GPU 生態圈    │
│  IT 管制進不了雲端               理解 DC 基礎設施        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 276

**Source**: `personal-rag_v2\PKB\workspace\test_06\opencodetest\錼創2026Q1需求討論_V2.1.md` L78

```
 ┌─────────────────── 2600cm ───────────────────┐
 │                                             │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐┌────┐│
 │  │P-1 │ │P-5 │  │A1-1 │ │A1-5│ │A1-9 ││A2  ││
 │  └────┘ └────┘  └─────┘ └────┘ └─────┘│-03 ││
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐└────┘│
 │  │P-2 │ │P-6 │  │A1-2 │ │A1-6│ │A1   │      │
 │  └────┘ └────┘  └─────┘ └────┘ │-10  │      │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ └─────┘┌──────┐ │
 │  │P-3 │ │P-7 │  │A1-3 │ │A1-7│  ┌────┐│A2    │ │
 │  └────┘ └────┘  └─────┘ └────┘  │A2  ││-02   │ │
 │  ┌────┐          ┌─────┐ ┌─────┐ │-01 │└────┘ │
 │  │P-4 │          │A1-4 │ │A1-8 │ └────┘     │
 │  └────┘          └─────┘ └─────┘            │
 │  P ×7            A1 ×10         A2 ×3       │
 └───────────────────────────────────────────────┘
           ↕ 走道 / Move in 動線 (200cm)
 ┌───────────────────────────────────────────────────────┐
 │  ┌────┐                                       3400cm  │
 │  │L-3 │                                         ↕    │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-2 │                                               │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-1 │  ┌─────┐                                      │
 │  └────┘  │PK-1 │                                      │
 │  L ×3    └─────┘                                      │
 │           PK ×1                                       │
 │                                                       │
 │ ┌───────┐ ┌────────┐ ┌───────────────────────────┐    │
 │ │自動   │ │ Wafer  │ │[AMR充電][AMR充電][AMR充電]│    │
 │ │包裝機 │ │ Sorter │ │  Stocker 1  ┌────┐        │    │
 │ │400×350│ │ 320×260│ │  Stocker 2                │ SWAP│      │ │
 │ └───────┘ └────────┘ │[OP PORT][OP PORT]└────┘   │    │
 │                      └───────────────────────────┘    │
 │                       800 × 500 cm                    │
 │                       有效 312 位（V2.1 雙座並排）    │
 │                                                       │
 │  ┌──────────┐   ┌──────────┐                          │
 │  │ E-Rack   │   │ E-Rack   │                          │
 │  │ (Box)    │   │ (FOUP)   │                          │
 │  └──────────┘   └──────────┘                          │
 └───────────────────────────────────────────────────────┘
```

---

## Sample 277

**Source**: `personal-rag_v2\PKB\workspace\test_06\錼創2026Q1需求討論_V2.0.md` L55

```
 ┌─────────────────── 2600cm ───────────────────┐
 │                                              │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐┌────┐│  ┌────────────────────┐
 │  │P-1 │ │P-5 │  │A1-1 │ │A1-5│ │A1-9 ││A2  ││  │ │
 │  └────┘ └────┘  └─────┘ └────┘ └─────┘│-03 ││  │  Stocker + Sorter │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐└────┘│  │  (STK 168位 │
 │  │P-2 │ │P-6 │  │A1-2 │ │A1-6│ │A1   │      │  │   + Sorter 結合) │
 │  └────┘ └────┘  └─────┘ └────┘ │-10  │      │  │ │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ └─────┘┌──────┐ │  │  [CST Box Buffer] │
 │  │P-3 │ │P-7 │  │A1-3 │ │A1-7│  ┌────┐│A2    │ │  │   入庫4 / 出庫4 │
 │  └────┘ └────┘  └─────┘ └────┘  │A2  ││-02   │ │  │   (Total 12) │
 │  ┌────┐          ┌─────┐ ┌─────┐ │-01 │└────┘│  └────────────────────┘
 │  │P-4 │          │A1-4 │ │A1-8 │ └────┘       │
 │  └────┘          └─────┘ └─────┘              │
 │  P ×7            A1 ×10         A2 ×3         │
 └───────────────────────────────────────────────┘
           ↕ 走道
 ┌───────────────────────────────────────────────────────┐
 │  ┌────┐                                       3400cm  │
 │  │L-3 │                                         ↕    │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-2 │                                               │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-1 │  ┌─────┐                                      │
 │  └────┘  │PK-1 │                                      │
 │  L ×3    └─────┘                                      │
 │           PK ×1                                       │
 │  ┌──────────┐   ┌──────────┐                          │
 │  │ E-Rack   │   │ E-Rack   │                          │
 │  │ (Box)    │   │ (FOUP)   │                          │
 │  └──────────┘   └──────────┘                          │
 └───────────────────────────────────────────────────────┘
```

---

## Sample 278

**Source**: `personal-rag_v2\PKB\workspace\test_06\錼創2026Q1需求討論_V2.1.md` L78

```
 ┌─────────────────── 2600cm ───────────────────┐
 │                                             │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐┌────┐│
 │  │P-1 │ │P-5 │  │A1-1 │ │A1-5│ │A1-9 ││A2  ││
 │  └────┘ └────┘  └─────┘ └────┘ └─────┘│-03 ││
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ ┌─────┐└────┘│
 │  │P-2 │ │P-6 │  │A1-2 │ │A1-6│ │A1   │      │
 │  └────┘ └────┘  └─────┘ └────┘ │-10  │      │
 │  ┌────┐ ┌────┐  ┌─────┐ ┌────┐ └─────┘┌──────┐ │
 │  │P-3 │ │P-7 │  │A1-3 │ │A1-7│  ┌────┐│A2    │ │
 │  └────┘ └────┘  └─────┘ └────┘  │A2  ││-02   │ │
 │  ┌────┐          ┌─────┐ ┌─────┐ │-01 │└────┘ │
 │  │P-4 │          │A1-4 │ │A1-8 │ └────┘     │
 │  └────┘          └─────┘ └─────┘            │
 │  P ×7            A1 ×10         A2 ×3       │
 └───────────────────────────────────────────────┘
           ↕ 走道 / Move in 動線 (200cm)
 ┌───────────────────────────────────────────────────────┐
 │  ┌────┐                                       3400cm  │
 │  │L-3 │                                         ↕    │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-2 │                                               │
 │  └────┘                                               │
 │  ┌────┐                                               │
 │  │L-1 │  ┌─────┐                                      │
 │  └────┘  │PK-1 │                                      │
 │  L ×3    └─────┘                                      │
 │           PK ×1                                       │
 │                                                       │
 │ ┌───────┐ ┌────────┐ ┌───────────────────────────┐    │
 │ │自動   │ │ Wafer  │ │[AMR充電][AMR充電][AMR充電]│    │
 │ │包裝機 │ │ Sorter │ │  Stocker 1  ┌────┐        │    │
 │ │400×350│ │ 320×260│ │  Stocker 2                │ SWAP│      │ │
 │ └───────┘ └────────┘ │[OP PORT][OP PORT]└────┘   │    │
 │                      └───────────────────────────┘    │
 │                       800 × 500 cm                    │
 │                       有效 312 位（V2.1 雙座並排）    │
 │                                                       │
 │  ┌──────────┐   ┌──────────┐                          │
 │  │ E-Rack   │   │ E-Rack   │                          │
 │  │ (Box)    │   │ (FOUP)   │                          │
 │  └──────────┘   └──────────┘                          │
 └───────────────────────────────────────────────────────┘
```

---

## Sample 279

**Source**: `personal-rag_v2\PKB\workspace\test_08\8D_Report_Wafer_Damage_AMR04_20260328.md` L148

```
Reset triggered (after alarm)
  └─ TMflow init sequence executes
  └─ Step 1: Modbus write → IAI driver: "Open gripper"   ← No cassette presence check
  └─ Step 2: Modbus write → IAI driver: "Close gripper"  ← Too late — cassette already dropped
  └─ Step 3: Continue init...
```

---

## Sample 280

**Source**: `personal-rag_v2\PKB\workspace\test_08\8D_Report_Wafer_Damage_AMR04_20260328_v1.md` L178

```
Run Project triggered (TM Play pressed)
  └─ TMflow init sequence executes
  └─ Step 1: Modbus write → IAI driver: "Open gripper"   ← No cassette presence check
  └─ Step 2: Modbus write → IAI driver: "Close gripper"  ← Too late — cassette already dropped
  └─ Step 3: Continue init...
```

---

## Sample 281

**Source**: `personal-rag_v2\PKB\workspace\test_08\8D_Report_Wafer_Damage_AMR04_20260328_zh-TW.md` L148

```
Reset 觸發（警報後）
  └─ TMflow 初始化流程執行
  └─ Step 1: Modbus write → IAI driver:「打開夾爪」   ← 未檢查卡匣存在
  └─ Step 2: Modbus write → IAI driver:「關閉夾爪」   ← 太遲 — 卡匣已掉落
  └─ Step 3: 繼續初始化...
```

---

## Sample 282

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L10

```
┌─────────────────────────────────────────────────────────────────┐
│                        AMR04 車體                               │
│                                                                 │
│  ┌───────────┐   LAN     ┌──────────┐    EtherCAT    ┌────────┐ │
│  │  IPC      │ ◄─────────►│ TM 手臂   │◄─────────────►│End     │ │
│  │BOXER-6639 │  T-03     │ 主機      │               │Module  │ │
│  │           │           │          │    Tool Port   │(slot7) │ │
│  │ Docker    │           │ TMflow   │───8pin+5pin──►│→夾爪   │ │
│  │ ├AGVWeb   │           │          │               │ sensor  │ │
│  │ ├rosbridge│           └────┬─────┘               │+DO ctrl│  │
│  │ └ROS      │                │                      └────────┘ │
│  │           │           100PIN 連接器                          │
│  └───────────┘                │                                 │
│   HDMI+USB              ┌────┴──────┐                           │
│        │                │ CAN Board │                           │
│  ┌─────┴──────┐         │(FORCE BD) │                           │
│  │ 觸控螢幕   │          └────┬─────┘                           │
│  │            │              │ CAN bus                          │
│  └────────────┘         ┌────┴──────────────────────┐           │
│                         │ cansns1: FoupIn_Det1~6    │           │
│  ┌────────────┐         │ cansns4: PS[]/PL[]/Door   │           │
│  │ 按鈕面板   │          │ 馬達 FL/FR/RL/RR          │          │
│  │ 鑰匙/復位  │          │ 電池/充電                  │         │
│  │ 剎車/啟停  │          │ Lidar/超音波              │          │
│  └────────────┘         └───────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sample 283

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L43

```
┌─────────────────────────────────┐
│ IPC: BOXER-6639 / 6640          │
│                                 │
│ ├─ USB 3.0 ×2, USB 2.0          │
│ ├─ LAN ×3                       │
│ │   ├─ T-01 → TP-LINK LAN HUB  │
│ │   ├─ T-03 → TM 手臂主機      │ ◄── TM Modbus / ROS 通訊
│ │   └─ T-04 → 外部擴充面板      │
│ │                                │
│ ├─ 擴充面板                      │
│ │   ├─ COM1~COM5 (RS485/232)     │
│ │   ├─ HDMI ×2 ─────────► 觸控螢幕（直接接，非樹莓派）
│ │   ├─ VGA                       │
│ │   └─ 觸控 USB ────────► 觸控螢幕
│ │                                │
│ ├─ Docker 容器                   │
│ │   ├─ AGVWeb (Flask)            │ ◄── Web UI + TM STOP 按鈕
│ │   ├─ rosbridge_websocket :9090 │ ◄── browser JS ↔ ROS
│ │   └─ ROS master                │
│ │                                │
│ └─ LAN HUB-A / HUB-B             │
│     ├─ sensor 網路               │
│     └─ 外部擴充                  │
└─────────────────────────────────┘
```

---

## Sample 284

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L74

```
┌──────────────────────────────────────┐
│ TM 手臂主機                          │
│                                      │
│ 安全回路（左側）                     │
│ ├─ STO-1, STO-2    → 安全扭力關閉   │
│ ├─ SAFE1~SAFE4     → 安全功能       │
│ ├─ SI1-1, SI1-2    → Safety Input   │
│ ├─ DI_9, DI_10, DI_12, DI_13         │
│ └─ Power +24V, DI_COM                │
│                                      │
│ I/O 面板（右側） → 100PIN 連接器    │
│ ├─ DO/MFP, DO/MFF                    │
│ ├─ ST.D/DI-1                         │
│ ├─ R1~R5 (CB00, RB02, 1X_17, etc.)   │
│ ├─ B1~B4 (SB00, SB01, 1X_19, CK11)   │
│ ├─ SAFE-1~SAFE-5, SAFE-Y             │
│ ├─ E/ESTOP                           │
│ └─ RT/EDIM-1                         │
│                                      │
│ End Module (Multi-IO, slot 7)        │
│ ├─ EtherCAT 內部通訊                 │
│ └─ → Tool Port 8-pin + 5-pin        │
└──────────────────────────────────────┘
```

---

## Sample 285

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L104

```
┌─────────────────────────────────────────────┐
│ 大寰 伺服電動夾爪（控制器一體型）            │
│                                              │
│ Tool Port 8-pin 接頭                         │
│ ┌──────┬───────┬────────────────────────┐    │
│ │ Pin  │ TM    │ 接到                    │   │
│ ├──────┼───────┼────────────────────────┤    │
│ │  1   │ +24V  │ 電源                    │   │
│ │  2   │ DI_0  │ PS AND ← 在席 sensor   │   │
│ │  3   │ DI_1  │ PL AND ← 在位 sensor   │   │
│ │  4   │ DI_2  │ BUMP OR ← 碰撞 sensor  │   │
│ │  5   │ DO_0  │ 夾爪控制 ──────► 電動夾爪│ │
│ │  6   │ DO_1  │ 夾爪控制 ──────► 電動夾爪│ │
│ │  7   │ DO_2  │ 夾爪控制 ──────► 電動夾爪│ │
│ │  8   │ 0V    │ GND                     │   │
│ └──────┴───────┴────────────────────────┘    │
│                                              │
│ Tool Port 5-pin 接頭                         │
│ ┌──────┬───────┬────────────────────────┐    │
│ │  1   │ +24V  │ 電源                    │   │
│ │  2   │ DI_3  │ （未標示）              │   │
│ │  3   │ DO_3  │ （未標示）              │   │
│ │  4   │ AI    │ （未標示）              │   │
│ │  5   │ 0V    │ GND                     │   │
│ └──────┴───────┴────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Sample 286

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L135

```
垂直電路板                          水平電路板
┌───────────┐                     ┌───────────┐
│ V-PL01 ─┐ │                     │ H-PL01 ─┐ │
│ V-PL02 ─┤ │                     │ H-PL02 ─┤ │
│ V-PL03 ─┼─► AND (U8)──┐        │ H-PL03 ─┼─► AND (U8)── ┐
│ V-PL04 ─┘ │            │        │ H-PL04 ─┘ │ │
│            │            ▼        │            │            ▼
│ BUMP(L) ──►─ OR ──► DI_2       │ BUMP(R) ──►─ OR ──► DI_2
└───────────┘     ▲               └───────────┘     ▲
                  │                                  │
           PS group AND ──► DI_0              PS group AND ──► DI_0
           PL group AND ──► DI_1              PL group AND ──► DI_1
```

---

## Sample 287

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L152

```
            ┌─── UB350（超音波）
            │
     ┌──────┴──────┐
     │   夾爪本體  │
     │             │
H-PL04 ──┐    ┌── V-PL04
H-PL03 ──┤    │── V-PL03 ── BUMP(R)
     │   CLOSE│OPEN│
H-PL02 ──┤    │── V-PL02
H-PL01 ──┘    └── V-PL01 ── BUMP(L)
     │              │
     └──────────────┘
```

---

## Sample 288

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L171

```
每個 Slot 配置（以 F-U-R 為例，P16）：
┌──────────────────────────┐
│ 二合一電路板 FpD-1        │
│                           │
│ J17, J15 → COVER CLOSE   │──► PS (Presence Sensor)
│ J18      → 前-上-右       │
│ J10      → 背面短路橋接   │
│                            │
│ F-U-R-5 → DOOR CLOSE     │──► PL (Position Lock)
│ F-U-R-4 → DOOR OPEN      │
│ F-U-R-1 → 對照 SENSOR    │
│ F-U-R-2 → EE-SA801-R 1M  │──► 凸片偵測
│ F-U-R-3 → LR-ZB250AN     │──► RFID 天線
│                           │
│ 鋁板背面（配線面）        │
└──────────────────────────┘

4 Slot 配置：
Slot1 = F-U-R（前上右）  Slot2 = F-U-L（前上左）
Slot3 = R-U-R（後上右）  Slot4 = R-U-L（後上左） ← WP0800222 在此
```

---

## Sample 289

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L198

```
┌───────┬──────────┬──────────┬────────────┐
│ 鑰匙   │ 復位按鈕  │ 剎車旋鈕  │ 啟動/停止 │
│ 開關   │          │          │ 按鈕      │
│TN16-  │TN16-     │TN16-     │TN16-       │
│KSR4B  │MBL6BL2   │SSL4B12   │MBL6W2      │
│122A   │          │          │            │
├───────┴──────────┴──────────┴────────────┤
│ → 安全繼電器（UC10F22D1449）            │
│ → 啟停接到 TM Stick Start/Stop          │
└──────────────────────────────────────────┘
```

---

## Sample 290

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L215

```
電池 ──► DROK 安全回路 ──► 24V 主電源
                │
         ┌──────┴──────┐
         │ HIS 光隔離器 │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
 東方馬達     CAN Board    IPC
 FL/FR/RL/RR  (FORCE BD)
```

---

## Sample 291

**Source**: `personal-rag_v2\PKB\workspace\test_08\AMR04_circuit_overview.md` L232

```
┌─────────────────────────────────────────────┐
│ POWER BOARD                                  │
│                                              │
│ 24V 區                    5V 區    12V 區    │
│ ├─ J52: IPC              J55      J56        │
│ ├─ J59: LAN HUB                              │
│ ├─ J56-1: AP                                 │
│ ├─ J56-2: 後貨盤 sensor                      │
│ ├─ J55: 前貨盤 sensor                        │
│ ├─ J58: ISB 模塊          J57-1    J57-2     │
│ │                         外部電源擴充       │
│ │ 24V 區（下排）                             │
│ ├─ J53: 光隔離器                             │
│ ├─ J54: E84 控制板                           │
│ ├─ J51-2: 超音波模組                         │
│ ├─ J51-1: RFID                               │
│ └─ 真空 PCB 板                               │
└─────────────────────────────────────────────┘
```

---

## Sample 292

**Source**: `personal-rag_v2\PKB\workspace\test_08\LOG_Investigation_AMR04_20260328.md` L333

```
時間（CST）  TMflow                 E84 State            carwork / Slot
─────────── ────────────────────── ──────────────────── ─────────────────────────
12:44:27    STOP Project                                 AMR at STK
            (軟體層，arm 未停)
12:44:29                           CMD 31,1,6 (load)    STK, DoorOK2, TM Moving
12:45:14                           succeeded ✓           TM Moving OK 21203
12:46:46                           CMD 2,1,6 (unload)   STK
12:47:28                                                 PS4=True (cassette in)
12:47:32                                                 CST_ID: WP0800222
12:47:34                           succeeded ✓           TM Moving OK -21403
12:47:40                                                 Moving → TEL57
12:48:31                                                 Docking at 7TEL57
12:48:34    ██ Run Project ██                            DockOK at 7TEL57
            (Init → Modbus                               Slot4: WP0800222
             open gripper!)
12:48:36                           CMD 32,0,6 (unload)  Loadunload, PioStart
12:48:39                                                 DoorOK2, TM Moving
12:49:17                           EQ unload goods ack
12:49:18    rapid pause/resume                           ██ TB1000 ██
12:49:18                                                 TB1000;RM1089
12:49:19                                                 ██ TM Moving NG ██
12:49:19                                                 Standby (stopped)
12:51:17                           ██ State1: error ██   EC103B added
                                   EC 103B (TP4 timeout)
12:53:16                           force reset ×2
13:08:59    SafetyIO Pause                               CD0006 (CstDoor err)
```

---

## Sample 293

**Source**: `personal-rag_v2\PKB\workspace\test_08\timeline_detail.md` L345

```
[觸發] 12:48:30 Technician 按 Stick Start 重啟 Project
                                    │
                                    ▼
[正常] 12:48:34~35 Init → gripper_init（自檢：閉→開）
             ├─ CST 在 slot4（FoupLock 固定），不在夾爪中
             └─ gripper_init 結束在「開」= 正常起始狀態
                                    │
                                    ▼
[EtherCAT Direct] 正常操作開始 pick → 此次 pick 走 EtherCAT Direct 模式（DO 由 cyclic PDO 維持）
             ├─ pick 成功（CCTV 推定，DI0=T 未被 modbus 記錄）
             └─ DO 由 PDO 週期更新驅動（非 CMD61 硬體鎖存）
                                    │
                                    ▼
[⚠️ PDO Watchdog — 假說，未驗證] 12:48:42 Lidar Pause #1 → CMDE3,0 暫停 EtherCAT → PDO 停止更新
             ├─ End Module PDO watchdog 逾時（通常 <1s，遠小於 ~15s Pause）
             ├─ **DO 歸零 = 夾爪短暫鬆開**（CST 在無夾持力下靠重力偏移）
             └─ ~15s後 CMDE3,1 恢復 → PDO 重啟 → 夾爪重新夾回，但 CST 已偏移
                                    │
                                    ▼
[鬆動] 12:49:09 DI0=F — CST 偏移到 sensor 失去接觸（夾回但位置不正）
                                    │
                                    ▼
[掉落] ~12:49:1x CST 靠重力從靜止的手臂滑落（CCTV 確認手臂沒動）
                                    │
                                    ▼
[人員反應] 12:49:18 TB1000 — 人員踢 bumper（emergencystop, Driver Board）
             └─ 12:49:19 TS9907 手臂急停
```

---

## Sample 294

**Source**: `personal-rag_v2\PKB\workspace\test_08\timeline_detail.md` L389

```
12:48:35.697  gripper_init RELEASE
              ├─ RUNNING（7 秒）── CMD38 loop + CMD41 移動
12:48:42.433  ██ Lidar Pause #1（15.4 秒）██  ← 程式暫停，無檢查
12:48:57.820  Resume #1
              ├─ RUNNING（12 秒）── CMD38 flow step loop（3628/68/3629/59）
12:49:09.468  ◆ DI0=F ← 此刻程式 RUNNING，但在 CMD38 loop，非 State 33/43
12:49:10.086  ██ Lidar Pause #2 ██
```

---

## Sample 295

**Source**: `personal-rag_v2\PKB\workspace\test_0b\Renesas_Reel_Handling_設計概念整理.md` L71

```
Canister (with IC) ──> EQ ARC Bowl Feeder
Carrier (with Long Tray) ──> EQ ARC Tray Feeder

         ┌─────────────┐
         │ Reel Stack   │
         │   Machine    │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
  REEL        REEL      NG Reel
    │           │           │
    v           v           v
 Reel Cart   Reel Cart   IN/OUT PORT
    │           │
    v           v
 BOX Stocker  Carrier Stocker
```

---

## Sample 296

**Source**: `personal-rag_v2\PKB_專案說明_v2_0316.md` L32

```
personal-rag_v2\PKB\
├── .env                    GOOGLE_API_KEY
├── CLAUDE.md               Claude Code 規則 + 草圖引擎邏輯
├── GYRO_context.md         產品規格 / 客戶 / 公式（≤150 行）
├── vault\                  原始資料備份（唯讀，SHA256 去重）
│   ├── docs\  images\  videos\
├── templates\              報告模板 Markdown
│   ├── 01_客戶提案\  02_技術分析\  03_策略規劃\
│   ├── 04_簡報投影片\  05_行政法務\
├── db\chroma\              pkb_docs + pkb_images
├── images_index.csv        圖片精確標籤
├── sketch\                 草圖 SVG 輸出
├── scripts\                Phase 1–3 腳本
└── workspace\              每次任務工作資料夾
```

---

## Sample 297

**Source**: `personal-rag_v2\PKB_專案說明_v2_0327.md` L54

```
personal-rag_v2\PKB\
├── .env                    GEMINI_API_KEY / GOOGLE_API_KEY
├── CLAUDE.md               Claude Code 規則 + 草圖引擎邏輯
├── GYRO_context.md         產品規格 / 客戶 / 公式（≤150 行）
├── MANIFEST.csv            Phase 1 處理清單（SHA256 去重）
├── SKIPPED_ARCHIVES.csv    跳過的壓縮檔清單（302 個）
├── images_index.csv        圖片精確標籤
├── image_embed_state.db    Phase 3 圖片/影片 embedding 進度
├── vault\                  原始資料備份（唯讀，SHA256 去重）
│   ├── docs\               技術文件（PPTX/PDF/DOCX）
│   ├── images\             圖片
│   ├── videos\             影片
│   └── embedded_images\    文件內嵌圖片
├── templates\              報告模板 Markdown（14 類）
│   ├── 00_報告產生流程\    Marp 使用指南 + 範例
│   ├── 01_客戶提案\        含 8 種子模板
│   ├── 04_測試報告\  05_進度報告\  06_會議記錄\
│   ├── 08_市場分析\  09_設計文件\  10_操作手冊\
│   ├── 12_工作管制表\  13_圖紙\  14_不良分析報告\
│   ├── 16_內部研究\  17_介紹信\  18_AGV規劃\
├── raw_phase3\             Phase 3 歸納中間產出（僅供參考）
│   ├── customers\          客戶分析（24 batches）
│   ├── products\           產品線分析
│   └── templates\          模板原型（18 種）
├── scripts\                所有執行腳本（見下方）
├── sketch\                 草圖 SVG 輸出
├── workspace\              每次任務工作資料夾
├── logs\                   執行日誌
└── db\chroma\              ChromaDB legacy（唯讀，待清除）
```

---

## Sample 298

**Source**: `personal-rag_v2\README.md` L9

```
來源目錄 (F:\機器人專案\06_AGV)
    │
    ▼ Phase 1: vault backup
PKB/vault/ (SHA256 去重)  +  MANIFEST.csv
    │
    ▼ Phase 2: full embedding
PKB/db/chroma/            ChromaDB (pkb_docs + pkb_images)
PKB/images_index.csv      圖片精確標籤
PKB/vault/embedded_images/ 文件內嵌圖片（待 Vision 分析）
    │
    ▼ Phase 3: synthesis (規劃中)
PKB/templates/            報告模板
PKB/GYRO_context.md       產品/客戶知識
```

---

## Sample 299

**Source**: `personal-rag_v2\README.md` L43

```
personal-rag_v2/
├── README.md                          本文件
├── PKB_專案說明_v2_0316.md            原始規格書
├── test_gemini_embed.py               API 驗證腳本
│
└── PKB/
    ├── .env                           API keys + SMTP 設定
    ├── .env.example                   環境變數範本
    ├── MANIFEST.csv                   Phase 1 產出（14,975 筆檔案索引）
    ├── images_index.csv               Phase 2 產出（圖片標籤 CSV）
    ├── embedded_images_pending.csv    文件內嵌圖片待處理清單
    │
    ├── vault/                         原始資料備份（唯讀）
    │   ├── docs/                      PPTX, PDF, DOCX, XLSX, DOC, PPT
    │   ├── images/                    JPG, PNG
    │   ├── videos/                    MP4
    │   └── embedded_images/           文件內嵌圖片（Phase 2 萃取）
    │
    ├── db/
    │   ├── chroma/                    ChromaDB 持久化資料（legacy，唯讀）
    │   └── phase2_state.db            Phase 2 進度追蹤 (SQLite)
    │   # Qdrant 儲存於 D:/PKB_db/qdrant_server/（Docker mount，NTFS）
    │
    ├── scripts/
    │   ├── phase1_vault_backup.py     Phase 1 主程式
    │   ├── phase2_embed.py            Phase 2 主程式（orchestrator）
    │   ├── phase2_extractors.py       檔案萃取器
    │   ├── phase2_gemini.py           Gemini API 封裝
    │   ├── phase2_chroma.py           ChromaDB 操作（legacy）
    │   ├── phase2_qdrant.py           Qdrant 查詢層（主力）
    │   ├── phase2_notify.py           Email 通知
    │   ├── phase2_state.py            進度追蹤 (SQLite)
    │   ├── reembed_ollama.py          Ollama bge-m3 re-embedding
    │   ├── migrate_chroma_to_qdrant.py  ChromaDB → Qdrant 遷移
    │   └── qdrant_check.py            Qdrant 資料驗證
    │
    ├── templates/                     報告模板（Phase 3）
    ├── sketch/                        草圖 SVG 輸出
    └── workspace/                     任務工作區
```

---

## Sample 300

**Source**: `personal-rag_v2\README.md` L117

```
phase2_embed.py (orchestrator)
    ├── phase2_state.py      SQLite 進度追蹤
    ├── phase2_notify.py     Email 通知 (smtplib + Gmail)
    ├── phase2_gemini.py     Gemini API 封裝
    ├── phase2_chroma.py     ChromaDB 讀寫
    └── phase2_extractors.py 檔案萃取器
```

---

## Sample 301

**Source**: `personal-rag_v2\README.md` L128

```
啟動
  → 載入 .env → 驗證 GOOGLE_API_KEY
  → 初始化 SQLite state DB
     ├── 首次：從 MANIFEST.csv 載入 status=copied 的檔案
     └── 續傳：重設 processing → pending，偵測重啟
  → 初始化 ChromaDB (pkb_docs + pkb_images)
  → 註冊 crash handler (atexit + signal)
  → 啟動 2hr 定期 email 通知

處理 images (4 workers 並行)
  → 讀取圖片 bytes
  → Gemini Vision 結構化描述 → {scene, objects, usage, client, caption}
  → Gemini Embedding (3072 dims)
  → 寫入 ChromaDB pkb_images + images_index.csv

處理 docs (4 workers 並行)
  → 萃取文字 + 圖片 (依檔案類型)
     ├── PPTX: python-pptx (slides → text + tables + images)
     ├── PDF:  pymupdf (pages → text + images)
     ├── DOCX: python-docx (paragraphs + images)
     ├── XLSX: openpyxl (sheets → rows)
     ├── XLS:  xlrd
     └── DOC/PPT: LibreOffice headless 轉新格式 → 再萃取
  → 內嵌圖片：存檔至 vault/embedded_images/ + 插入 [IMAGE_REF] 標記
  → 內容去重：MD5 hash 文字內容，跳過重複檔案
  → 長文字切割 (>2000 chars → 1000 chars + 200 overlap)
  → Gemini Embedding → ChromaDB pkb_docs

處理 videos (1 worker，循序)
  → 上傳至 Gemini Files API (ASCII temp path workaround)
  → Vision 時間戳分段描述 [MM:SS-MM:SS]
  → Gemini Embedding → ChromaDB pkb_docs

完成
  → 寄完成通知 email
  → 標記 run complete
```

---

## Sample 302

**Source**: `personal-rag_v2\README.md` L169

```
ThreadPoolExecutor
  ├── images/docs: 4 workers
  └── videos: 1 worker (大檔上傳避免衝突)

Gemini API 速率限制
  ├── deque 追蹤最近 25 次請求時間戳 (thread-safe)
  ├── 超過 25 req/sec → sleep
  └── 429 / RESOURCE_EXHAUSTED → 指數退避 (2^n * 2s, max 120s)

LibreOffice
  └── threading.Lock 全域鎖（不支援 concurrent instances）
```

---

## Sample 303

**Source**: `personal-rag_v2\README.md` L212

```
SQLite: db/phase2_state.db
  ├── progress 表: sha256(PK), status(pending/processing/done/error)
  └── run_log 表:  event(start/crash/complete/email_sent), timestamp

重啟時：
  1. status=processing → 重設為 pending
  2. 偵測上次未完成 → 寄重啟通知
  3. 跳過 status=done 的檔案
```

---

## Sample 304

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01.md` L177

```
資料源                    Phase 1              Phase 2                    Phase 3/4           API
F:\機器人專案\06_AGV    ┌────────────┐     ┌──────────────────┐      ┌──────────────┐    ┌──────────┐
 14,975 files ────────>│ Vault      │────>│ Extractors       │─────>│ Synthesis    │    │ FastAPI  │
                       │ SHA256 dedup│     │ PPTX/PDF/DOCX/   │      │ GYRO_context │    │ :8000   │
mail_index.db ─────────│ MANIFEST   │     │ XLSX/DOC/PPT/IMG/ │      │ Templates    │    │         │
 31,990 emails         └────────────┘     │ Video             │      └──────────────┘    │ /search │
                                          ├──────────────────┤                          │ /deep-   │
                                          │ Gemini 3072d     │──┐                       │  query   │
                                          │ Ollama bge-m3    │  │                       │ /stats   │
                                          │ 1024d            │  │                       └────┬─────┘
                                          └──────────────────┘  │                            │
                                                                v                            v
                                          ┌──────────────────────────────────────────────────────┐
                                          │              Qdrant Docker (qdrant-pkb)              │
                                          │              localhost:6333 | D:/PKB_db/             │
                                          ├──────────────────────────────────────────────────────┤
                                          │ pkb_docs          520,771 pts  3072d  Gemini         │
                                          │ pkb_images        289,932 pts  3072d  Gemini         │
                                          │ pkb_mail          162,446 pts  3072d  Gemini         │
                                          │ pkb_docs_ollama   520,771 pts  1024d  bge-m3         │
                                          │ pkb_images_ollama 289,932 pts  1024d  bge-m3         │
                                          │ pkb_mail_ollama   162,446 pts  1024d  bge-m3         │
                                          │                                                      │
                                          │ Total: ~1.95M vectors | RAM: ~380 MB | on_disk=True  │
                                          └──────────────────────────────────────────────────────┘
```

---

## Sample 305

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_external.md` L107

```
資料源（文件/圖片/影片/Email）
        |
   Phase 1: 備份去重
        |
   Phase 2: 萃取 + Embedding（Gemini 3072d / Ollama bge-m3 1024d）
        |
   Qdrant Docker（6 collections, ~1.95M vectors, on_disk）
        |
   Phase 3: 知識合成 ──> 公司知識庫 + 報告範本
        |
   FastAPI API Server（語意搜尋 / 深度查詢 / 統計）
```

---

## Sample 306

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L50

```
使用者 ──> rag.py CLI
              │
              ├── rag_loaders.py ──> PDF / PPTX / DOCX / 影片截圖
              │
              ├── rag_core.py ────> ChromaDB (embedded, in-memory)
              │                     Gemini embedding-001 (3072d)
              │
              └── query / add / list / remove
```

---

## Sample 307

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L84

```
瀏覽器 ──> FastAPI (port 8000)
              │
              ├── /chat ─────────> Gemini Function Calling
              │                    ├── doc_search()
              │                    ├── img_search()
              │                    ├── img_context()
              │                    └── generate_image()
              │
              ├── /docs/search ──> ChromaDB pkb_docs (7,388 docs)
              ├── /images/search > ChromaDB pkb_images (73,200 images)
              │
              └── chat.html ────> 單頁 Chat UI（拖拉上傳、Lightbox）
                                  Gemini embedding-001 (3072d)
```

---

## Sample 308

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L123

```
資料源 (14,975 files + 31,990 emails)
  │
  ├─ Phase 1: Vault ──> SHA256 dedup → MANIFEST.csv
  │
  ├─ Phase 2: Embed ──> Extractors (7 formats + Email + Video)
  │                     ├── Gemini 2.5-flash (Vision)
  │                     ├── Gemini embedding-2 (3072d)
  │                     └── Ollama bge-m3 (1024d)
  │                              │
  │                     Qdrant Docker (6 collections, 1.95M vectors)
  │                     on_disk=True | RAM 380MB | D:/PKB_db/
  │
  ├─ Phase 3: Synth ──> GYRO_context.md + 14 類報告範本
  │
  └─ Phase 4: API ────> FastAPI :8000
                        ├── /api/search (語意搜尋)
                        ├── /api/deep-query (Agentic RAG + SSE)
                        └── /api/stats (使用統計)
```

---

## Sample 309

**Source**: `personal-rag_v2\reviews\RETROSPECTIVE_2026-04-01_slides_v2.md` L217

```
Browser (Chat UI from v1) ──> docker-compose
                                │
                                ├── FastAPI + Auth ──> API Gateway
                                │                     ├── /api/search
                                │                     ├── /api/deep-query
                                │                     └── OAuth / API Key
                                │
                                ├── Qdrant HA ───────> 向量搜尋 + 自動備份
                                ├── Ollama bge-m3 ──> 本地 Embedding
                                ├── PostgreSQL ─────> State DB (取代 SQLite)
                                │
                                └── Shared Volume (NTFS)
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
        CI/CD                    Monitoring               Knowledge Graph
        ├── GitHub Actions       ├── Prometheus            ├── Entity Extraction
        ├── pytest + coverage    ├── Grafana               └── Graph DB
        └── auto deploy          └── RAG Eval (F1)
```

---

## Sample 310

**Source**: `Reporter_v0\.data\doc-ingest_詳細實作設計.md` L27

```
/doc-ingest <SOURCE_DIR> [TARGET_DIR]
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                    doc-ingest Skill                      │
│                                                          │
│  Step 1: 環境檢查     ──→  _preflight_report.md         │
│  Step 2: 來源掃描     ──→  _scan_report.md              │
│  Step 3: 分類規劃     ──→  _分類建議.md                 │
│  Step 4: 檔案複製     ──→  分類資料夾結構               │
│  Step 5: 文字萃取     ──→  *.txt + _extract_errors.log  │
│  Step 6: 建立索引     ──→  _index.json                  │
│  Step 7: 品質報告     ──→  _quality_report.md           │
│  Step 8: 部署設定     ──→  CLAUDE.md + settings.json    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 311

**Source**: `Reporter_v0\.data\doc-report_詳細實作設計.md` L38

```
/doc-report <客戶需求>
    │
    ▼
┌──────────────────────────────────────────────┐
│               doc-report Skill                │
│                                               │
│  Phase 1: 需求解析                            │
│    ├── 1A. 輸入解析（文字/檔案/郵件）         │
│    ├── 1B. 結構化提取（客戶/載具/機台/場域）  │
│    └── 1C. 缺失偵測 + 產業判斷                │
│                                               │
│  Phase 2: 知識庫搜尋                          │
│    ├── 2A. 索引快速掃描 (_index.json)         │
│    ├── 2B. 同客戶歷史搜尋                     │
│    ├── 2C. 同產業類比搜尋                     │
│    ├── 2D. 產品規格搜尋 (車型/設備/軟體)      │
│    └── 2E. 報價參考搜尋                       │
│                                               │
│  Phase 3: 工程分析                            │
│    ├── 3A. 載具可行性分析                     │
│    ├── 3B. 製程瓶頸分析                       │
│    ├── 3C. 搬運流量建模                       │
│    └── 3D. 設備數量估算                       │
│                                               │
│  Phase 4: 報告撰寫                            │
│    ├── 4A. 按模組組裝                         │
│    ├── 4B. 數據溯源標注                       │
│    ├── 4C. 一致性檢查                         │
│    └── 4D. 輸出 .md 檔案                      │
│                                               │
└──────────────────────────────────────────────┘
```

---

## Sample 312

**Source**: `Reporter_v0\.data\doc-report_詳細實作設計.md` L78

```
輸入 $ARGUMENTS
    │
    ├── 是檔案路徑? ──→ 讀取檔案內容（PDF.txt / .md / .txt）
    ├── 是多行文字? ──→ 當作郵件/需求描述
    └── 是簡短指令? ──→ 如 "錼創的新需求"，需追問細節
```

---

## Sample 313

**Source**: `Reporter_v0\.data\doc-report_詳細實作設計.md` L172

```
  搜尋階段            工具              目標
  ─────────          ─────             ──────
  2A. 索引掃描       Read _index.json   快速篩選相關文件 (< 1 min)
  2B. 同客戶搜尋     Grep/Glob          找歷史案例 (< 1 min)
  2C. 同產業搜尋     Read .txt files    找類比案例 (2-5 min)
  2D. 產品規格       Read .txt files    找產品參數 (2-5 min)
  2E. 報價參考       Grep 70_業務報價    歷史報價區間 (< 1 min)
```

---

## Sample 314

**Source**: `Reporter_v0\.data\DOC_image_extraction_and_classification.md` L26

```
D:\benth\Documents\機器人專案\06_AGV     .images_full/
  7,433 個文件                             188,431 張圖片
  (pptx, pdf, docx, ppt, doc)              ├── 01_產品介紹/  18,557
                                            ├── 02_工程圖面/  14,809
  ┌─────────┐   ┌──────────┐   ┌────────┐  ├── 03_技術規格/  24,071
  │ sample  │──>│ extract  │──>│classify│  ├── 04_認證標準/  22,359
  │ _files  │   │ _images  │   │_images │  ├── 05_電池充電/   8,004
  └─────────┘   └──────────┘   └────┬───┘  ├── 06_系統軟體/  27,569
   50 個取樣     多進程擷取      關鍵字  │  ├── 07_客戶提案/  13,906
                                 分類   │  ├── 08_安全規範/   3,136
                               ┌────────┘  ├── 09_操作手冊/  24,019
                               │           ├── 10_報告分析/  29,932
                          ┌────┴───┐       └── 00_其他/       2,069
                          │  ai    │
                          │classify│
                          └────────┘
                          Gemini Vision
                          再分類 00_其他
```

---

## Sample 315

**Source**: `Reporter_v0\.data\DOC_image_extraction_and_classification.md` L291

```
.images_full/
├── 01_產品介紹/     (18,557 files)  產品型錄、公司簡介
├── 02_工程圖面/     (14,809 files)  CAD 圖面、3D 模型、機構設計
├── 03_技術規格/     (24,071 files)  規格書、Datasheet
├── 04_認證標準/     (22,359 files)  SEMI/CE/RoHS/IEC/ISO 認證文件
├── 05_電池充電/      (8,004 files)  電池、充電系統
├── 06_系統軟體/     (27,569 files)  TSC/MCS/導航/派車軟體
├── 07_客戶提案/     (13,906 files)  提案、報價、會議記錄
├── 08_安全規範/      (3,136 files)  安全規範、風險評估
├── 09_操作手冊/     (24,019 files)  操作手冊、訓練教材
├── 10_報告分析/     (29,932 files)  報告、分析、測試
└── 00_其他/          (2,069 files)  無法歸類的圖片
```

---

## Sample 316

**Source**: `Reporter_v0\.data\README.md` L74

```
scripts/                    # 工具腳本 (14 支)
├── _setup.py               ← 安裝腳本（從這裡開始）
├── _extract.py              ← 文字萃取主控
├── _extract_batch.py        ← 批次萃取引擎
├── _extract_one.py          ← 單檔萃取
├── _build_index.py          ← 索引建置
├── _scan.py                 ← 來源掃描
├── _classify_rules.py       ← 三層分類引擎
├── _copy_files.py           ← 檔案複製
├── _quality_report.py       ← 品質報告
├── _deploy.py               ← 部署設定
├── _search_index.py         ← 索引搜尋（同義詞展開+評分）
├── _find_related.py         ← 關聯文件搜尋
├── _calc_throughput.py      ← 工程計算（瓶頸/流量/設備）
└── _report_init.py          ← 報告骨架產出

skills/                     # Claude Code Skill (2 支)
├── doc-ingest.md            ← 知識庫建置 Skill
└── doc-report.md            ← 需求報告 Skill

docs/                       # 設計文件 (4 份)
├── 文件知識庫建置流程與Skill設計文件.md  ← 主設計文件 V1.3
├── doc-ingest_詳細實作設計.md
├── doc-report_詳細實作設計.md
└── _分類建議.md             ← 分類結構範本
```

---

## Sample 317

**Source**: `Reporter_v0\.data\README.md` L115

```
<知識庫>/
├── .claude/
│   ├── settings.local.json
│   └── skills/
│       ├── doc-ingest.md
│       └── doc-report.md
├── CLAUDE.md               ← Claude Code 搜尋指引
├── _index.json             ← 搜尋索引
├── 00_公司簡介/
├── 01_產品型錄/
├── ...                     ← 25 個語意分類資料夾
├── 60_客戶_封測/
├── 61_客戶_晶圓代工/
├── 62_客戶_記憶體/
├── 63_客戶_面板光電/
├── 64_客戶_系統整合/
├── 65_客戶_其他/
├── 70_業務報價/
└── ...
```

---

## Sample 318

**Source**: `Reporter_v0\.data\README_gyro-report.md` L38

```
├── commands/
│   └── gyro-report.md            # Slash command entry point
├── skills/
│   └── gyro-report/
│       ├── SKILL.md              # Main skill definition
│       ├── README_載入SOP.md      # Desktop loading instructions
│       ├── assets/
│       │   ├── gyro_css_template.css      # CSS template (embed verbatim)
│       │   ├── gyro_style_template.json   # Brand design spec
│       │   └── content_sample.json        # JSON schema example
│       └── scripts/
│           └── gyro_html_generator.js     # Legacy JSON→HTML generator
└── README.md
```

---

## Sample 319

**Source**: `Reporter_v0\.data\README_載入SOP.md` L7

```
.claude/skills/gyro-report/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   ├── gyro_css_template.css             ← CSS 模板（必須）
│   ├── gyro_style_template.json          ← 品牌設計規範
│   └── content_sample.json              ← JSON schema 範例
└── scripts/
    └── gyro_html_generator.js            ← Legacy JSON→HTML 產生器
```

---

## Sample 320

**Source**: `Reporter_v0\.data\SESSION_NOTES.md` L18

```
C:\Users\benth\Documents\GitHub\draft-draw\
├── generate_images.py          # Gemini Imagen API image generation script
├── generate_prompts.py         # Gemini Vision API batch prompt generation script
├── filter_by_date.py           # Date filter: .images_full → .images_main
├── SESSION_NOTES.md            # This file
├── .generate_prompts_checkpoint.json  # Prompt generation checkpoint/resume
├── .generate_prompts.log       # Prompt generation log file
├── .images_full/               # Original 188,431 images (READ-ONLY source)
│   ├── 00_其他/
│   ├── 01_產品介紹/
│   ├── 02_工程圖面/
│   ├── 03_技術規格/
│   ├── 04_認證標準/
│   ├── 05_電池充電/
│   ├── 06_系統軟體/
│   ├── 07_客戶提案/
│   ├── 08_安全規範/
│   ├── 09_操作手冊/
│   ├── 10_報告分析/
│   └── skipped_files.txt
├── .images_sample/             # 50 sample images + 50 .md prompts + 38 generated images
│   └── (same subdirectory structure)
├── detect_text_images.py        # Text/blank image detection and removal
├── .images_main/               # Filtered working directory: 73,058 visual images (2021+, text removed)
│   └── (same subdirectory structure)
├── .images_main_scan_results.csv  # Full scan classification results
├── .images_main_deleted.log       # Log of deleted file paths
└── .claude/
    └── settings.local.json
```

---

## Sample 321

**Source**: `Reporter_v0\.data\SKILL.md` L75

```html
<pre class="diagram">
 ┌────┐ ┌────┐
 │P-1 │ │P-2 │
 └────┘ └────┘
</pre>
```

---

## Sample 322

**Source**: `Reporter_v0\.data\SKILL.md` L240

```
output_folder/
├── presentation.html      ← slim HTML (~50-60KB)
└── images/
    ├── img_01.png
    ├── img_02.png
    └── ...
```

---

## Sample 323

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L123

```
_extract.py (主控程式)
    ├── _extract_batch.py (批次處理子程序)
    └── _extract_one.py   (單檔處理，備用)
```

---

## Sample 324

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L396

```
$TARGET_DIR/
├── .claude/settings.local.json    ← Claude Code 權限設定
├── CLAUDE.md                      ← 知識庫使用指引
├── _extract.py                    ← 主控萃取腳本
├── _extract_batch.py              ← 批次萃取引擎
├── _extract_one.py                ← 單檔萃取（備用）
├── _build_index.py                ← 索引建置腳本
├── _scan.py                       ← 來源掃描（Phase 2 新增）
├── _classify_rules.py             ← 分類引擎（Phase 2 新增）
├── _copy_files.py                 ← 檔案複製（Phase 2 新增）
├── _quality_report.py             ← 品質報告（Phase 2 新增）
├── _deploy.py                     ← 部署設定（Phase 2 新增）
├── _index.json                    ← 全文搜尋索引
├── _分類建議.md                   ← 分類結構說明
├── _extract_errors.log            ← 萃取錯誤記錄
├── 00_分類A/                      ← 分類資料夾
│   ├── 文件.pdf
│   └── 文件.pdf.txt
├── 01_分類B/
│   └── ...
└── ...
```

---

## Sample 325

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L487

```
客戶需求輸入
    │
    ▼
┌─────────────────────┐
│ Phase 1: 需求解析     │  · 結構化提取關鍵參數
│                       │  · 識別缺失資訊
│                       │  · 判斷客戶產業別
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 2: 知識庫搜尋   │  · _index.json 快速篩選
│                       │  · 同客戶歷史案例
│                       │  · 同產業類比案例
│                       │  · 相關產品/設備規格
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 3: 工程計算     │  · 載具尺寸可行性
│                       │  · 製程瓶頸分析
│                       │  · 搬運流量建模
│                       │  · 設備數量估算
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 4: 報告撰寫     │  · 按模組組裝報告
│                       │  · 數據溯源標注
│                       │  · 一致性檢查
└─────────┬───────────┘
          ▼
    輸出 .md 報告
```

---

## Sample 326

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L530

```
_search_index.py → 候選文件清單 (--json)
_find_related.py → 分類關聯文件 (--json)
_calc_throughput.py → 工程計算結果 (--json) ─┐
                                               ├→ _report_init.py → 報告骨架 (.md)
                   客戶需求 JSON ───────────────┘
```

---

## Sample 327

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L590

```
.claude/
└── skills/
    ├── doc-ingest.md    ← Skill A 的 prompt
    └── doc-report.md    ← Skill B 的 prompt
```

---

## Sample 328

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L599

```
~/.claude/
└── skills/
    ├── doc-ingest.md
    └── doc-report.md
```

---

## Sample 329

**Source**: `Reporter_v0\.data\文件知識庫建置流程與Skill設計文件.md` L726

```
.doc/
├── .claude/
│   ├── settings.local.json         ← Claude Code 權限設定
│   └── skills/
│       ├── doc-ingest.md           ← Skill A prompt
│       └── doc-report.md           ← Skill B prompt
│
├── # 既有腳本 (Stage 2-3)
├── _extract.py                     ← 文字萃取主控
├── _extract_batch.py               ← 批次萃取引擎
├── _extract_one.py                 ← 單檔萃取
├── _build_index.py                 ← 索引建置
│
├── # Phase 2 新增: doc-ingest
├── _scan.py                        ← 來源掃描
├── _classify_rules.py              ← 三層分類引擎
├── _copy_files.py                  ← 檔案複製
├── _quality_report.py              ← 品質報告
├── _deploy.py                      ← 部署設定
│
├── # Phase 2 新增: doc-report
├── _search_index.py                ← 索引搜尋（同義詞+評分）
├── _find_related.py                ← 關聯文件搜尋
├── _calc_throughput.py             ← 工程計算
├── _report_init.py                 ← 報告骨架產出
│
├── # 資料與設定
├── _index.json                     ← 搜尋索引 (7,338 筆)
├── _extract_errors.log             ← 錯誤記錄
├── _分類建議.md                    ← 分類結構說明
├── CLAUDE.md                       ← 知識庫使用指引
│
├── # 25 個分類資料夾
├── 00_公司簡介/                    ← 36 files
├── 01_產品型錄/                    ← 62 files
├── 02_軟體系統/                    ← 73 files
├── 10_車型規格/                    ← 118 files
├── 20_搬運方案/                    ← 63 files
├── 30_周邊設備/                    ← 430 files
├── 40_系統整合/                    ← 107 files
├── 50_安全認證/                    ← 340 files
├── 60_客戶_封測/                   ← 3,935 files (最大)
├── 61_客戶_晶圓代工/              ← 748 files
├── 62_客戶_記憶體/                 ← 526 files
├── 63_客戶_面板光電/              ← 55 files
├── 64_客戶_系統整合/              ← 657 files
├── 65_客戶_其他/                   ← 752 files
├── 70_業務報價/                    ← 277 files
├── 75_進度報告/                    ← 33 files
├── 80_設計規範/                    ← 10 files
├── 85_研究資料/                    ← 324 files
├── 90_開發計畫/                    ← 1,578 files
├── 91_場地需求/                    ← 52 files
├── 95_工程開發/                    ← 1,120 files
├── _OLD/                           ← 49 files
├── _其他/                          ← 工具腳本暫存區
├── _專利/                          ← 4 files
├── _情報/                          ← 18 files
└── _影片/                          ← 51 files
```

---

## Sample 330

**Source**: `Reporter_v0\.doc\.claude\skills\gyro-report\README_載入SOP.md` L7

```
.claude/skills/gyro-report/
├── SKILL.md                              ← 主要 skill 定義檔
├── assets/
│   ├── gyro_css_template.css             ← CSS 模板（必須）
│   ├── gyro_style_template.json          ← 品牌設計規範
│   └── content_sample.json              ← JSON schema 範例
└── scripts/
    └── gyro_html_generator.js            ← Legacy JSON→HTML 產生器
```

---

## Sample 331

**Source**: `Reporter_v0\.doc\.claude\skills\gyro-report\SKILL.md` L79

```html
<pre class="diagram">
 ┌────┐ ┌────┐
 │P-1 │ │P-2 │
 └────┘ └────┘
</pre>
```

---

## Sample 332

**Source**: `Reporter_v0\.doc\.claude\skills\gyro-report\SKILL.md` L244

```
output_folder/
├── presentation.html      ← slim HTML (~50-60KB)
└── images/
    ├── img_01.png
    ├── img_02.png
    └── ...
```

---

## Sample 333

**Source**: `Reporter_v0\.doc\_分類建議.md` L16

```
.doc/
├── 00_公司簡介/
├── 01_產品型錄/
├── 02_軟體系統/
├── 10_車型規格/
├── 20_搬運方案/
├── 30_周邊設備/
├── 40_系統整合/
├── 50_安全認證/
├── 60_客戶_封測/
├── 61_客戶_晶圓代工/
├── 62_客戶_記憶體/
├── 63_客戶_面板光電/
├── 64_客戶_系統整合/
├── 65_客戶_其他/
├── 70_業務報價/
├── 75_進度報告/
├── 80_設計規範/
├── 85_研究資料/
├── 90_開發計畫/
├── 91_場地需求/
├── 92_驗收資料/
├── 95_工程開發/
├── _OLD/
├── _專利/
├── _情報/
├── _影片/
└── _其他/
```

---

## Sample 334

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L74

```
┌─────────────────────────────┐
│  EC2 (t3.medium, Ubuntu)    │
│                             │
│  ├── Python 3.8+            │
│  ├── Reporter_v0 腳本       │
│  ├── .doc/ 知識庫 (~55MB)   │
│  ├── Claude Code CLI        │
│  └── Chrome (PDF 輸出)      │
└─────────────────────────────┘
```

---

## Sample 335

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L93

```
┌──────────────────┐     ┌──────────────┐
│  EC2 (運算)       │ ←→  │  S3 (儲存) │
│  Python 腳本      │     │  .doc/ 知識庫 │
│  FastAPI (可選)   │     │  報告輸出   │
│  Claude API      │     │  _index.json │
└──────────────────┘     └──────────────┘
```

---

## Sample 336

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L109

```
┌───────────┐    ┌──────────────────┐    ┌─────┐
│ API GW    │ →  │ ECS/Fargate      │ ←→ │ S3 │
│           │    │ Docker 容器       │    │    │
└───────────┘    │ FastAPI          │    └─────┘
                 │ Python 腳本      │
                 │                  │    ┌────────────────┐
                 │  gemini client ──│──→ │ Google Gemini │
                 │                  │    │ - Embedding API │
                 └──────────────────┘    │ - Chat/Gen API │
                                         └────────────────┘
```

---

## Sample 337

**Source**: `Reporter_v0\docs\aws-migration-discussion.md` L176

```
┌──────────┐    ┌─────────────────────┐    ┌─────┐
│ API GW   │ →  │ Fargate Container   │ ←→ │ S3 │
│ or Web   │    │                     │    │ .txt files
└──────────┘    │ FastAPI             │    │ templates
                │ ├── /report (生成)   │    └─────┘
                │ ├── /search (搜尋)   │
                │ ├── /calc   (計算)   │        ┌──────────┐
                │ └── gemini_client ───│──────→ │ Gemini │
                │                     │        │ 2.5 Pro │
                │ _calc_throughput.py  │        └──────────┘
                │ gyro-report gen     │
                └─────────────────────┘
```

---

## Sample 338

**Source**: `Reporter_v0\plan.md` L12

```
_build_vectors.py              _search_vectors.py
(一次性建置)                    (搜尋時使用)
     │                              │
     ▼                              ▼
讀取 _index.json            語意搜尋 (cosine)
     │                      + 關鍵字搜尋 (FTS5)
     ▼                      + RRF 混合排序
讀取 5,636 個 .txt                  │
     │                              ▼
     ▼                        候選文件清單
分段 (chunk)                  (含分數+路徑+摘要)
     │
     ▼
Gemini embedding-001
(768-dim, batch 100)
     │
     ▼
_vectors.db (SQLite)
```

---

## Sample 339

**Source**: `Reporter_v0\request_02\report.md` L320

```
$TARGET_DIR/
├── .claude/settings.local.json     ← Claude Code 權限設定
├── CLAUDE.md                       ← 知識庫使用指引
├── _extract.py                     ← 主控萃取腳本
├── _extract_batch.py               ← 批次萃取引擎
├── _extract_one.py                 ← 單檔萃取（備用）
├── _build_index.py                 ← 索引建置腳本
├── _scan.py                        ← 來源掃描（Phase 2）
├── _classify_rules.py              ← 分類引擎（Phase 2）
├── _copy_files.py                  ← 檔案複製（Phase 2）
├── _quality_report.py              ← 品質報告（Phase 2）
├── _deploy.py                      ← 部署設定（Phase 2）
├── _index.json                     ← 全文搜尋索引
├── _分類建議.md                    ← 分類結構說明
├── 00_分類A/ ... 95_分類Z/         ← 分類資料夾
│   ├── 文件.pdf
│   └── 文件.pdf.txt
└── ...
```

---

## Sample 340

**Source**: `Reporter_v0\request_02\report.md` L440

```
.claude/skills/
  ├── doc-ingest.md    ← Skill A prompt
  └── doc-report.md    ← Skill B prompt
```

---

## Sample 341

**Source**: `Reporter_v0\request_02\report.md` L447

```
~/.claude/skills/
  ├── doc-ingest.md
  └── doc-report.md
```

---

## Sample 342

**Source**: `Reporter_v0\request_02\report.md` L570

```
.doc/
├── .claude/
│   ├── settings.local.json
│   └── skills/
│       ├── doc-ingest.md
│       └── doc-report.md
│
├── # 既有腳本 (Stage 2-3)
├── _extract.py / _extract_batch.py / _extract_one.py
├── _build_index.py
│
├── # Phase 2: doc-ingest
├── _scan.py / _classify_rules.py / _copy_files.py
├── _quality_report.py / _deploy.py
│
├── # Phase 2: doc-report
├── _search_index.py / _find_related.py
├── _calc_throughput.py / _report_init.py
│
├── _index.json          ← 搜尋索引 (7,338 筆)
├── _分類建議.md          ← 分類結構說明
├── CLAUDE.md            ← 知識庫使用指引
│
├── 00_公司簡介/  ... 50_安全認證/    ← 產品技術 (1,229 files)
├── 60_客戶_封測/ ... 65_客戶_其他/   ← 客戶專案 (6,673 files)
├── 70_業務報價/  ... 95_工程開發/    ← 業務工程 (3,394 files)
└── _OLD/ _其他/ _專利/ _情報/ _影片/ ← 雜項 (1,729 files)
```

---

## Sample 343

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L123

```
_extract.py (主控程式)
    ├── _extract_batch.py (批次處理子程序)
    └── _extract_one.py   (單檔處理，備用)
```

---

## Sample 344

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L396

```
$TARGET_DIR/
├── .claude/settings.local.json    ← Claude Code 權限設定
├── CLAUDE.md                      ← 知識庫使用指引
├── _extract.py                    ← 主控萃取腳本
├── _extract_batch.py              ← 批次萃取引擎
├── _extract_one.py                ← 單檔萃取（備用）
├── _build_index.py                ← 索引建置腳本
├── _scan.py                       ← 來源掃描（Phase 2 新增）
├── _classify_rules.py             ← 分類引擎（Phase 2 新增）
├── _copy_files.py                 ← 檔案複製（Phase 2 新增）
├── _quality_report.py             ← 品質報告（Phase 2 新增）
├── _deploy.py                     ← 部署設定（Phase 2 新增）
├── _index.json                    ← 全文搜尋索引
├── _分類建議.md                   ← 分類結構說明
├── _extract_errors.log            ← 萃取錯誤記錄
├── 00_分類A/                      ← 分類資料夾
│   ├── 文件.pdf
│   └── 文件.pdf.txt
├── 01_分類B/
│   └── ...
└── ...
```

---

## Sample 345

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L487

```
客戶需求輸入
    │
    ▼
┌─────────────────────┐
│ Phase 1: 需求解析     │  · 結構化提取關鍵參數
│                       │  · 識別缺失資訊
│                       │  · 判斷客戶產業別
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 2: 知識庫搜尋   │  · _index.json 快速篩選
│                       │  · 同客戶歷史案例
│                       │  · 同產業類比案例
│                       │  · 相關產品/設備規格
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 3: 工程計算     │  · 載具尺寸可行性
│                       │  · 製程瓶頸分析
│                       │  · 搬運流量建模
│                       │  · 設備數量估算
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 4: 報告撰寫     │  · 按模組組裝報告
│                       │  · 數據溯源標注
│                       │  · 一致性檢查
└─────────┬───────────┘
          ▼
    輸出 .md 報告
```

---

## Sample 346

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L530

```
_search_index.py → 候選文件清單 (--json)
_find_related.py → 分類關聯文件 (--json)
_calc_throughput.py → 工程計算結果 (--json) ─┐
                                               ├→ _report_init.py → 報告骨架 (.md)
                   客戶需求 JSON ───────────────┘
```

---

## Sample 347

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L590

```
.claude/
└── skills/
    ├── doc-ingest.md    ← Skill A 的 prompt
    └── doc-report.md    ← Skill B 的 prompt
```

---

## Sample 348

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L599

```
~/.claude/
└── skills/
    ├── doc-ingest.md
    └── doc-report.md
```

---

## Sample 349

**Source**: `Reporter_v0\request_02\文件知識庫建置流程與Skill設計文件.md` L726

```
.doc/
├── .claude/
│   ├── settings.local.json         ← Claude Code 權限設定
│   └── skills/
│       ├── doc-ingest.md           ← Skill A prompt
│       └── doc-report.md           ← Skill B prompt
│
├── # 既有腳本 (Stage 2-3)
├── _extract.py                     ← 文字萃取主控
├── _extract_batch.py               ← 批次萃取引擎
├── _extract_one.py                 ← 單檔萃取
├── _build_index.py                 ← 索引建置
│
├── # Phase 2 新增: doc-ingest
├── _scan.py                        ← 來源掃描
├── _classify_rules.py              ← 三層分類引擎
├── _copy_files.py                  ← 檔案複製
├── _quality_report.py              ← 品質報告
├── _deploy.py                      ← 部署設定
│
├── # Phase 2 新增: doc-report
├── _search_index.py                ← 索引搜尋（同義詞+評分）
├── _find_related.py                ← 關聯文件搜尋
├── _calc_throughput.py             ← 工程計算
├── _report_init.py                 ← 報告骨架產出
│
├── # 資料與設定
├── _index.json                     ← 搜尋索引 (7,338 筆)
├── _extract_errors.log             ← 錯誤記錄
├── _分類建議.md                    ← 分類結構說明
├── CLAUDE.md                       ← 知識庫使用指引
│
├── # 25 個分類資料夾
├── 00_公司簡介/                    ← 36 files
├── 01_產品型錄/                    ← 62 files
├── 02_軟體系統/                    ← 73 files
├── 10_車型規格/                    ← 118 files
├── 20_搬運方案/                    ← 63 files
├── 30_周邊設備/                    ← 430 files
├── 40_系統整合/                    ← 107 files
├── 50_安全認證/                    ← 340 files
├── 60_客戶_封測/                   ← 3,935 files (最大)
├── 61_客戶_晶圓代工/              ← 748 files
├── 62_客戶_記憶體/                 ← 526 files
├── 63_客戶_面板光電/              ← 55 files
├── 64_客戶_系統整合/              ← 657 files
├── 65_客戶_其他/                   ← 752 files
├── 70_業務報價/                    ← 277 files
├── 75_進度報告/                    ← 33 files
├── 80_設計規範/                    ← 10 files
├── 85_研究資料/                    ← 324 files
├── 90_開發計畫/                    ← 1,578 files
├── 91_場地需求/                    ← 52 files
├── 95_工程開發/                    ← 1,120 files
├── _OLD/                           ← 49 files
├── _其他/                          ← 工具腳本暫存區
├── _專利/                          ← 4 files
├── _情報/                          ← 18 files
└── _影片/                          ← 51 files
```

---

## Sample 350

**Source**: `Reporter_v0\request_05\取代E84的方案.md` L40

```
Webcam ──(影像辨識)──► 邊緣主機 ──(寫入狀態)──► 資料庫
                                                    ▲
AMR ──(每3秒輪詢)──────────────────────────────────┘
                                                    │
EAP ◄──(Port狀態通知)──── 資料庫 ────(PODON/BUSY)──►│
```

---

## Sample 351

**Source**: `Reporter_v0\request_06\progress_report_0304_0310.md` L244

```
D455_LidarScan_v0          Line_bot_v0              personal-rag_v1
(即時 3D 感測)             (LINE Bot 入口)           (RAG 搜尋引擎)
       │                        │                         │
       │                        │──── HTTP :8000 ─────────│
       │                        │  /search/docs           │
       │                        │  /search/images         │
       │                        │  /context/images        │
       │                        │                         │
       └── Gemini AI ───────────┴──── Gemini AI ──────────┘
           (Depth Anything V2)     (2.5 Flash + Embedding + Image)
```

---

## Sample 352

**Source**: `Reporter_v0\templates\10_技術文件.md` L195

```
{根目錄}/
├── {子目錄 1}/
│   ├── {檔案}
│   └── {檔案}
├── {子目錄 2}/
│   └── {檔案}
├── {設定檔}
└── {主程式}
```

---

## Sample 353

**Source**: `Reporter_v1\README.md` L58

```
Reporter_v1/
├── gen_gyro_pptx.py          # 主程式（MD 解析 + 雙引擎渲染）
├── README.md
└── WORKSPACE/
    └── TEST_CASE/
        ├── *.md              # 測試用 Markdown 報告
        └── .images/
            └── diagrams/     # Mermaid 圖表（.mmd / .png / .svg）
```

---

## Sample 354

**Source**: `Reporter_v1\WORKSPACE\a01\01_arch.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬───────────────┘
               │                       │
       install.ps1 / install.sh        │
               │                       │
               ▼                      │
  ┌────────────────────┐               │
  │  ~/.claude/         │              │
  │  commands/          │              │
  │  skills/            │              │
  │  settings.json      │              │
  │  CLAUDE.md          │              │
  └────────────────────┘───────────────│
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│           Google Cloud Backend             │
├─────────────┬──────────────┬───────────────┤
│ Google Chat │ Google Sheet │ Apps Script   │
│  Webhook    │  Dashboard   │  Web App      │
└─────────────┴──────────────┴──────────────┘
```

---

## Sample 355

**Source**: `Reporter_v1\WORKSPACE\a01\01_arch_v0.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬───────────────┘
               │                       │
       install.ps1 / install.sh        │
               │                       │
               ▼                      │
  ┌────────────────────┐               │
  │  ~/.claude/         │              │
  │  commands/          │              │
  │  skills/            │              │
  │  settings.json      │              │
  │  CLAUDE.md          │              │
  └────────────────────┘───────────────│
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│           Google Cloud Backend             │
├─────────────┬──────────────┬───────────────┤
│ Google Chat │ Google Sheet │ Apps Script   │
│  Webhook    │  Dashboard   │  Web App      │
└─────────────┴──────────────┴──────────────┘
```

---

## Sample 356

**Source**: `Reporter_v1\WORKSPACE\a01\01_arch_v0.md` L41

```
  ┌────────────────────────────────────────────────────┐
  │            Claude Code CLI / OpenCode CLI          │
  ├──────────┬──────────┬───────────┬──────────────────┤
  │ 8 命令   │ 8 技能   │ Statusline│ MCP Servers      │
  │ /pm 系列 │ report   │ quota     │ Playwright       │
  │ /do 委派 │ gmail    │ JS/Shell  │ Windows MCP      │
  │ /clip    │ browser  │           │ Google WS        │
  └────┬─────┴────┬─────┴─────┬─────┴─────────────────┘
       │          │           │
       │   install.ps1 / install.sh
       │          │
       ▼          ▼
  ┌───────────────────────┐
  │  ~/.claude/           │
  │  commands/ skills/    │
  │  settings.json        │
  │  CLAUDE.md            │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────┬──────────┬──────────────────┐
  │ Google   │ Google   │ Apps Script      │
  │ Chat     │ Sheet    │ Web App          │
  │ Webhook  │ 儀表板   │ (自動化後端)     │
  └──────────┴──────────┴──────────────────┘
```

---

## Sample 357

**Source**: `Reporter_v1\WORKSPACE\a01\01_arch_v0.md` L72

```
  ┌───────────────────────────────────────────────────┐
  │            Claude Code CLI / OpenCode CLI         │
  ├──────────┬──────────┬───────────┬─────────────────┤
  │ 8 命令   │ 8 技能   │ Statusline│ MCP Servers     │
  │ /pm 系列 │ report   │ quota     │ Playwright      │
  │ /do 委派 │ gmail    │ JS/Shell  │ Windows MCP     │
  │ /clip    │ browser  │           │ Google WS       │
  └────┬─────┴────┬─────┴───────────┴─────────────────┘
       │          │           
       │   install.ps1 / install.sh
       │          │
       ▼         ▼
  ┌──────────────────────┐
  │  ~/.claude/          │
  │  commands/ skills/   │
  │  settings.json       │
  │  CLAUDE.md           │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────┬──────────┬──────────────────┐
  │ Google   │ Google   │ Apps Script      │
  │ Chat     │ Sheet    │ Web App          │
  │ Webhook  │ 儀表板   │ (自動化後端)     │
  └──────────┴──────────┴──────────────────┘
```

---

## Sample 358

**Source**: `Reporter_v1\WORKSPACE\a01\01_claude-dotfiles.md` L41

```
/pm          → 開工
  工作中
  ├─ /smart-commit      → 完成功能時
  ├─ /opencode-do auto  → 委派簡單任務
  ├─ ctx ≈ 60%          → /pm-bye → /clear → /pm
/pm-bye      → 收工
```

---

## Sample 359

**Source**: `Reporter_v1\WORKSPACE\a01\01_claude-dotfiles.md` L54

```
├── global-claude.md             # 全域指令（→ ~/.claude/CLAUDE.md）
├── settings.json                # Hooks、plugins、statusline
├── mcp.json                     # MCP server config
├── statusline.js / .sh          # Status Line 腳本
├── pm-update.sh                 # /pm 狀態更新
├── commands/                    # Claude Code slash commands（8 個）
├── commands-opencode/           # opencode slash commands（7 個）
├── skills/                      # Custom skills（8 個）
├── opencode-config/             # opencode 全域設定
├── dual-engine/                 # Dual Engine SOP + 範例
├── docs/                        # 設定指南（Google Workspace、MCP、plugins…）
├── install.ps1 / install.sh     # 安裝腳本
└── reviews/                     # 程式碼審核報告
```

---

## Sample 360

**Source**: `Reporter_v1\WORKSPACE\a01\02_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                    │
│    Delegation SOP: Claude Code ←→ OpenCode              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐  ┌───────────────────────┐      │
│  │   Claude Code        │   │   OpenCode             │    │
│  │   (Decision-Maker)   │ ──→│   (Executor)           │  │
│  └──────────────────────┘  └───────────────────────┘      │
│                                                           │
├───────────────────────────────────────────────────────────┤
│  Delegation Levels                                        │
│                                                           │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐      │
│  │ L1        │ │ L2           │  │ L3              │      │
│  │ New Files │ │ Controlled   │  │ Task-Level      │      │
│  │           │ │ Edits        │  │ Autonomy        │      │
│  │           │ │              │  │ ≤5 parallel     │      │
│  │           │ │              │  │ agents          │      │
│  └───────────┘ └──────────────┘  └─────────────────┘      │
│                                                           │
│  Status: Archived → merged into claude-dotfiles          │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 361

**Source**: `Reporter_v1\WORKSPACE\a01\02_arch.md` L28

```
┌──────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                   │
│    Delegation SOP: Claude Code ←→ OpenCode             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐    ┌───────────────────────┐   │
│  │   Claude Code        │    │   OpenCode            │   │
│  │   (Decision-Maker)   │ ─→│   (Executor)          │   │
│  └──────────────────────┘    └───────────────────────┘   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  Delegation Levels                                       │
│                                                          │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐     │
│  │ L1        │ │ L2           │  │ L3              │     │
│  │ New Files │ │ Controlled   │  │ Task-Level      │     │
│  │           │ │ Edits        │  │ Autonomy        │     │
│  │           │ │              │  │ ≤5 parallel     │     │
│  │           │ │              │  │ agents          │     │
│  └───────────┘ └──────────────┘  └─────────────────┘     │
│                                                          │
│  Status: Archived → merged into claude-dotfiles         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 362

**Source**: `Reporter_v1\WORKSPACE\a01\02_DuelEngineSOP_v0.md` L55

```
├── README.md
├── dual-engine-sop.md                  # SOP 完整規格
├── commands/
│   ├── claude-code/opencode-do.md      # Claude Code 端指令
│   └── opencode/do.md                  # opencode 端指令
├── examples/                           # 自動化測試範例（8 個 Python 工具）
│   ├── calc.py, counter.py, greet.py
│   ├── temp.py, passgen.py, wc.py
│   ├── jsonf.py, b64.py
└── reviews/                            # 審核報告
```

---

## Sample 363

**Source**: `Reporter_v1\WORKSPACE\a01\03_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│                  HaloScan (Planning 0%)                    │
│          360° Safety Zone for AMR                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│       LiDAR 1        LiDAR 2       LiDAR 3  LiDAR 4        │
│   ┌──────────┐   ┌──────────┐   ┌────────┐ ┌────────┐      │
│   │ Livox    │   │ Livox    │   │ Livox  │ │ Livox  │      │
│   │ Mid-360  │   │ Mid-360  │   │Mid-360 │ │Mid-360 │      │
│   │ 905nm    │   │ 905nm    │   │ 905nm  │ │ 905nm  │      │
│   └────┬─────┘   └────┬─────┘   └───┬────┘ └───┬────┘      │
│        │              │              │          │          │
│        └──────┬───────┴──────┬───────┘          │          │
│               │   Ethernet UDP / PTP Sync       │          │
│               └──────────┬──────────────────────┘          │
│                          │                                 │
│                          ▼                                │
│              ┌───────────────────────┐                     │
│              │   Raspberry Pi 5      │                     │
│              │   C++ / ROS2 / PCL    │                     │
│              │   CropBox 3D Detect   │                     │
│              └─────────┬─────────────┘                     │
│                ┌───────┴───────┐                           │
│                │               │                           │
│                ▼               ▼                         │
│  ┌──────────────────┐ ┌────────────────────┐               │
│  │ Path A           │ │ Path B             │               │
│  │ 3D Safety Zone   │ │ 2D LaserScan Nav2  │               │
│  └────────┬─────────┘ └────────┬───────────┘               │
│           └────────┬───────────┘                           │
│                    ▼                                      │
│         ┌───────────────────┐                              │
│         │ Output            │                              │
│         │ 0=safe 1=slow     │                              │
│         │ 2=stop            │                              │
│         └───────────────────┘                              │
│                                                            │
│  Risk: 905nm IR interference in semiconductor fabs         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 364

**Source**: `Reporter_v1\WORKSPACE\a01\03_HaloScan_v0.md` L43

```
├── CLAUDE.md
├── README.md
├── docs/
│   ├── 01_會議計畫書_v0.md
│   ├── 02_會議計畫書_v1.md
│   ├── 03_感測器融合提案.md
│   ├── 04_Mid360_技術計畫_初版.md
│   ├── 05_楷浚討論筆記.md
│   ├── 06_會議簡報_v0.html
│   ├── 07_UAM-05LP_設定檔解析.md
│   ├── 08_開發環境規格.md
│   └── 09_UAM安全區視覺化.html        # 極座標互動視覺化
├── refs/
│   ├── mid360/                         # Mid-360 技術參考（7 篇）
│   ├── UAM-05LP_設定檔_sample.xml
│   └── UAMProjectDesigner_XML文件格式.pdf
└── .opencode-task.md                   # opencode 委派任務 spec
```

---

## Sample 365

**Source**: `Reporter_v1\WORKSPACE\a01\04_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│              UR Program Analysis                          │
│      Offline Toolchain for UR30 Cobot                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  72 files, 64,503 lines                                   │
│            │                                              │
│            ▼                                             │
│  ┌───────────────────┐                                    │
│  │  Python CLI       │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Parser           │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Tree Parser      │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Project Loader   │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Flow Analyzer    │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│     ┌─────┼──────────────┐                                │
│     │                    │ │                              │
│     ▼     ▼              ▼                             │
│  ┌─────┐ ┌───────────┐ ┌───────────────┐                  │
│  │ Doc │ │ Simplifier│ │ FK Kinematics │                  │
│  │ Gen │ │           │ │ 91.5% pass    │                  │
│  └─────┘ └───────────┘ └───────────────┘                  │
│                                                           │
│  Output: 82 analysis docs, 46 tests                       │
└────────────────────────────────────────────────────────┘
```

---

## Sample 366

**Source**: `Reporter_v1\WORKSPACE\a01\04_UR_Program_Analysis_v0.md` L47

```
├── src/
│   ├── ur_script_parser.py       # URScript 解析器
│   ├── ur_tree_parser.py         # 樹狀結構解析
│   ├── ur_project_loader.py      # 專案載入器
│   ├── ur_flow_analyzer.py       # Flow 分析
│   ├── ur_doc_generator.py       # 文件自動產生
│   ├── ur_analyze.py             # CLI 主程式
│   ├── ur_flow_editor.py         # 語意級腳本編輯（Phase 2）
│   ├── ur_flow_simplifier.py     # 跨檔案重複偵測（Phase 2）
│   ├── ur30_kinematics.py        # FK 驗證 + Rodrigues（Phase 2）
│   ├── ur_script_editor.py
│   ├── ur_script_simplifier.py
│   ├── test_core.py              # 31 個測試
│   ├── test_phase2.py            # 15 個測試
│   └── test_refactor.py
├── K11_UR30_Project/programs/    # UR 程式原始檔（160+ 檔案）
├── output/                       # 自動產生的 82 份分析文件
├── docs/                         # 手動撰寫的分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   ├── PHASE2_SPEC.md
│   └── gRPC/                    # GYRO gRPC 整合資料
└── archive/                      # UR 匯出壓縮
```

---

## Sample 367

**Source**: `Reporter_v1\WORKSPACE\a01\05_arch.md` L1

```
┌───────────────────────────────────────────────┐
│        OpenCode Enhance (Archived)            │
│        OpenCode CLI Config                    │
├───────────────────────────────────────────────┤
│                                               │
│  ┌────────────────────────────────────────┐   │
│  │  OpenCode CLI (TypeScript)             │   │
│  ├────────────────────────────────────────┤   │
│  │  Model: Gemini 3 Flash Preview         │   │
│  │  MCP Integration                       │   │
│  │  AGENTS.md                             │   │
│  │  Git-Attribution Plugin                │   │
│  └────────────────────────────────────────┘   │
│                                               │
│  Status: Archived → merged into              │
│          claude-dotfiles                      │
└──────────────────────────────────────────────┘
```

---

## Sample 368

**Source**: `Reporter_v1\WORKSPACE\a01\05_opencode_enhance_v0.md` L38

```
├── env-setup/              # 環境安裝與設定紀錄
├── opencode-config/        # OpenCode 設定檔
│   ├── opencode.json       # Model + MCP + permissions
│   ├── AGENTS.md           # 行為指引
│   ├── .env.example
│   └── .opencode/plugins/  # git-attribution plugin
├── usage-records/          # 任務指示紀錄
├── docs/
│   ├── daily-log-2026-04-02.md
│   ├── mcp-setup.md
│   ├── opencode-vs-claude-code.md
│   ├── usage-scenarios.md
│   └── verification-notes.md
└── update.cmd              # 更新腳本
```

---

## Sample 369

**Source**: `Reporter_v1\WORKSPACE\a01\06_arch.md` L1

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Personal RAG (PKB)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sources                                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Engineering  │ │ Email        │ │ Images           │     │
│  │ Docs         │ │ (.mbox)      │ │                  │     │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘     │
│         └────────────────┼──────────────────┘               │
│                          │                                  │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dual Embedding                                      │   │
│  │  ┌─────────────────────┐  ┌────────────────────────┐ │   │
│  │                                                      │ Gemini              │  │ Ollama bge-m3          │ │ │
│  │                                                      │ embedding-2-preview │  │ 1024d                  │ │ │
│  │                                                      │ 3072d               │  │                        │ │ │
│  │  └─────────┬───────────┘  └───────────┬────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│               └─────────────┬────────────┘                  │
│                             ▼                              │
│           ┌─────────────────────────────────┐               │
│           │  Qdrant (Docker)                │               │
│           │  6 collections, ~1.95M vectors  │               │
│           └───────────────┬─────────────────┘               │
│                           │                                 │
│                           ▼                                │
│           ┌─────────────────────────────────┐               │
│           │  FastAPI                        │               │
│           │  Gemini 2.5 Flash (Vision+LLM)  │               │
│           ├─────────────────────────────────┤               │
│           │  /api/search                    │               │
│           │  /api/deep-query (SSE)          │               │
│           │  /api/stats                     │               │
│           └─────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Sample 370

**Source**: `Reporter_v1\WORKSPACE\a01\06_personal-rag_v2.md` L49

```
├── PKB/
│   ├── CLAUDE.md
│   ├── scripts/
│   │   ├── api_server.py              # FastAPI RAG API
│   │   ├── phase1_vault_backup.py     # Phase 1：備份
│   │   ├── phase1m_mail_ingest.py     # Phase 1m：郵件匯入
│   │   ├── phase1m_zip_extract.py     # ZIP 解壓
│   │   ├── phase2_embed.py            # Phase 2：Gemini embedding
│   │   ├── phase2_qdrant.py           # Qdrant 查詢層
│   │   ├── phase2m_mail_embed.py      # 郵件 embedding
│   │   ├── phase3_preprocess.py       # Phase 3：圖片預處理
│   │   ├── phase3_batch_api.py        # 批次 Gemini API
│   │   ├── phase3_synthesize.py       # 知識合成
│   │   ├── reembed_ollama_qdrant.py   # bge-m3 re-embedding
│   │   ├── qdrant_check.py            # 驗證腳本
│   │   └── check_quota.py             # API 配額檢查
│   ├── raw_phase3/                    # Phase 3 合成知識
│   │   ├── customers/（24 batches）
│   │   ├── products/（12 files）
│   │   └── templates/（18 templates）
│   └── templates/                     # 文件模板（18 類）
├── reviews/                           # 7 份審核報告 + Q1 回顧
├── tests/                             # API + collection + embedding 測試
├── README.md
└── PKB_API_GUIDE.md
```

---

## Sample 371

**Source**: `Reporter_v1\WORKSPACE\a01\07_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│              TM Program Analysis                           │
│      Offline Toolchain for TM12 Cobot .flow                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  4,444 nodes                                               │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Python CLI       │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Flow Parser      │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Analyzer         │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│     ┌─────┼──────────────────┐                             │
│     │                        │ │                           │
│     ▼     ▼                  ▼                          │
│  ┌─────┐ ┌───────────────┐ ┌──────────────────────┐        │
│  │ Doc │ │ Vision        │ │ FK/IK Kinematics     │        │
│  │ Gen │ │ Analyzer      │ │                      │        │
│  └─────┘ └───────────────┘ └──────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │  MutableFlowDocument (Edit)                      │      │
│  └──────────────┬───────────────────────────────────┘      │
│                 │                                          │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Simplifier                                      │      │
│  │  452 chains, 2021 duplicates                     │      │
│  │  70 simplification plans                         │      │
│  └──────────────────────────────────────────────────┘      │
│                                                            │
│  Output: 49 docs, 34 tests                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Sample 372

**Source**: `Reporter_v1\WORKSPACE\a01\07_TM-Program-Analysis-v0.md` L50

```
├── src/
│   ├── tm_flow_parser.py          # .flow 格式解析器
│   ├── tm_flow_analyzer.py        # Flow 分析
│   ├── tm_doc_generator.py        # 文件自動產生
│   ├── tm_analyze.py              # CLI 主程式
│   ├── tm_vision_analyzer.py      # 68 Vision Job XML 分析
│   ├── tm12_kinematics.py         # FK/IK 運動學
│   ├── tm_flow_editor.py          # MutableFlowDocument 語意編輯（Phase 2）
│   ├── tm_flow_simplifier.py      # 重複鏈偵測（Phase 2）
│   └── test_core.py               # 34 個測試
├── output/                        # 49 份自動產生分析文件
│   ├── INDEX.md
│   ├── MainFlow.md
│   ├── SUBFLOW_CALL_GRAPH.md
│   ├── VARIABLE_USAGE_MAP.md
│   ├── VISION_JOB_MAP.md
│   ├── VISION_SYSTEM_ANALYSIS.md
│   ├── DUPLICATE_ANALYSIS.md
│   ├── subflows/（37 個）
│   └── threads/（5 個）
├── docs/                          # 手動分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   └── HT_9046LS / MR_PORT 深度分析
├── data/                          # TM 解壓資料
├── archive/                       # TM 匯出壓縮
└── reviews/                       # 審核報告
```

---

## Sample 373

**Source**: `Reporter_v1\WORKSPACE\a01\08_arch.md` L1

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Chat Bot                                 │
│      Google Chat Bot for @gyro.com.tw                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐                                        │
│  │ Google Chat   │                                        │
│  │ @gyro.com.tw  │                                        │
│  └───────────────┘                                        │
│         │  /kb --doc / --mail / --img                     │
│         ▼                                                │
│  ┌──────────────────────┐                                 │
│  │ GCP Cloud Run        │                                 │
│  │ (JWT / OIDC auth)    │                                 │
│  └──────────┬───────────┘                                 │
│             │ ngrok tunnel                                │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Local FastAPI RAG Backend                       │     │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │     │
│  │                                                  │ Qdrant      │ │ Gemini     │ │ Ollama      │  │ │
│  │                                                  │ │ │ 2.5 Flash  │ │ bge-m3      │  │ │
│  │  └─────────────┘ └────────────┘ └─────────────┘  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Apps Script          │                                 │
│  │ Daily Stats          │                                 │
│  └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 374

**Source**: `Reporter_v1\WORKSPACE\a01\08_Chat_bot_v1.md` L49

```
├── app.py                    # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py                # RAG backend（本機, API key 驗證）
├── rag.py                    # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── rate_limit.py             # Rate limiting
├── start-backend.sh          # Backend 啟動腳本
├── stop-backend.sh           # Backend 停止腳本
├── autostart-backend.vbs     # Windows 開機自啟
├── Dockerfile                # Cloud Run 映像
├── docker-compose.yml        # 本機 Qdrant
├── apps-script/              # Google Apps Script（每日統計報表 trigger）
│   ├── Code.gs
│   └── appsscript.json
├── tests/
│   ├── test_unit.py
│   └── test_thin_proxy.py
├── reviews/                  # 5 份審核報告
├── architecture.md           # 架構文件
├── 使用指引.md               # 使用者指南
└── conv_logger.py / drive_*.py  # （已停用）對話記錄功能
```

---

## Sample 375

**Source**: `Reporter_v1\WORKSPACE\a01\09_arch.md` L1

```
┌───────────────────────────────────────┐
│          public-assets                │
│   GitHub Static Asset Hosting         │
├───────────────────────────────────────┤
│                                       │
│  ┌────────────────────────────────┐   │
│  │  GYRO Logo (256x256 PNG)       │   │
│  │  Version A    Version B        │   │
│  └────────────────────────────────┘   │
│                 │                     │
│        GitHub raw URL                 │
│                 │                     │
│       ┌─────────┴─────────┐           │
│       │                   │           │
│       ▼                   ▼         │
│  ┌──────────┐     ┌────────────┐      │
│  │ Chat Bot │     │ Other      │      │
│  │ Avatar   │     │ Projects   │      │
│  └──────────┘     └────────────┘      │
└──────────────────────────────────────┘
```

---

## Sample 376

**Source**: `Reporter_v1\WORKSPACE\a01\10_arch.md` L1

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│               PM v2 (Archived)                           │
│       Claude Code /pm Workflow                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────┐    ┌──────────┐    ┌───────────┐    ┌─────┐  │
│  │ /pm    │───→│ /pm sync │───→│ /pm review│───→│/pm  │ │
│  │ start  │    │ 5 options│    │ red-team  │    │bye  │  │
│  │        │    │ menu     │    │ subagent  │    │     │  │
│  └────────┘    └──────────┘    └───────────┘    └──┬──┘  │
│                                                    │     │
│                                            ┌───────┘     │
│                                            │             │
│                                            ▼            │
│                                   ┌──────────────────┐   │
│                                   │ Code Review      │   │
│                                   │ QA + Retro       │   │
│                                   └──────────────────┘   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Integration                                       │  │
│  │  Status Line                                       │ Google Sheet │ progress.md          │ │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Status: Archived → merged into claude-dotfiles         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 377

**Source**: `Reporter_v1\WORKSPACE\a01\10_PM_v2.md` L37

```
├── commands/
│   ├── pm.md          # 統一 PM 指令
│   ├── hello.md       # （已棄用，redirects to /pm）
│   ├── sc.md          # （已棄用，redirects to /pm-sync）
│   └── bye.md         # （已棄用，redirects to /pm-bye）
├── pm-v2-design.md    # v2 設計文件
└── reviews/           # 審核報告
```

---

## Sample 378

**Source**: `Reporter_v1\WORKSPACE\a01\11_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                  Mail Checker                             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Google Takeout .mbox │                                 │
│  └──────────┬───────────┘                                 │
│             │                                             │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Attachment Extractor (MD5 Dedup)                │     │
│  └──────────────────────┬───────────────────────────┘     │
│                         │                                 │
│                         ▼                                │
│  ┌───────────────────────────────────────────────────┐    │
│  │  mail_indexer.py                                  │    │
│  │  Metadata → SQLite FTS5                          │    │
│  │  Gemini 2.0 Flash Batch Summarization             │    │
│  │  140 emails/min (10x speedup)                     │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐     │
│  │  progress_mailer.py                              │     │
│  │  Hourly HTML Reports via SMTP                    │     │
│  └──────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 379

**Source**: `Reporter_v1\WORKSPACE\a01\11_Mail_Checker_v0.md` L51

```
├── extract_attachments.py     # 附件擷取主程式
├── mail_indexer.py            # 郵件索引 + Gemini 摘要
├── progress_mailer.py         # 進度報告信
├── dedup_attachments.py       # 事後去重
├── check_duplicate_mails.py   # 重複探測
├── split_mbox_by_quarter.py   # 季度拆分
├── verify_and_dedup.py        # 驗證去重
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

---

## Sample 380

**Source**: `Reporter_v1\WORKSPACE\a01\12_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                    StockSage                              │
│             ML Stock Prediction                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Model                                    │      │
│  │  Transformer Encoder                            │      │
│  │  5-day × 30 features, 3-class                   │      │
│  │  OOS accuracy: 48.9%                            │      │
│  └────────────────────┬────────────────────────────┘      │
│                       │                                   │
│                       ▼                                  │
│  ┌──────────────────────────────────────────────────┐     │
│  │  GMP Model                                       │     │
│  │  LightGBM (~55 tickers)                          │     │
│  │  555 features                                    │     │
│  │  Vectorized: 4min → 10s                         │     │
│  └──────────────────────────────────────────────────┘     │
│                       │                                   │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Email via Gmail API                      │      │
│  └─────────────────────────────────────────────────┘      │
│                                                           │
│  Scheduler: Windows Task Scheduler                        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 381

**Source**: `Reporter_v1\WORKSPACE\a01\12_StockSage_v0.md` L50

```
├── pipeline/
│   ├── daily_update.py       # 每日資料更新
│   ├── feature_builder.py    # 特徵工程
│   ├── model.py              # Transformer model
│   ├── auto_trainer.py       # 自動訓練
│   └── weekly_runner.py      # 週排程
├── fetchers/
│   ├── tw_market.py          # 台股資料
│   └── us_market.py          # 美股資料
├── gmp/                      # Global Market Predictor
│   ├── predictor.py
│   ├── trainer.py
│   ├── model.py              # LightGBM
│   ├── feature_engineer.py
│   ├── fetcher.py
│   └── symbols.py            # ~55 tickers
├── backtest/
│   └── gap_backtest.py       # 回測
├── scripts/
│   ├── daily_predict_email.py   # 每日信件
│   ├── run_daily.bat            # Windows 排程
│   └── setup_schedule.bat       # Task Scheduler 設定
├── config.py
├── db/schema.py
├── docs/TRADING_GUIDE.md
├── README.md / README_DEV.md
└── reviews/
```

---

## Sample 382

**Source**: `Reporter_v1\WORKSPACE\a01\13_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                     win_drive                             │
│       Windows Desktop Automation MCP Server               │
├───────────────────────────────────────────────────────────┤
│  C++20 │ stdio JSON-RPC │ Per-Monitor DPI Aware V2        │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐     │
│  │  15 Tools                                        │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  screenshot (GDI)      │ mouse control           │     │
│  │  keyboard input        │ draw_path               │     │
│  │  window list/focus     │ batch ops               │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  UI Automation                                   │     │
│  │  inspect │ find │ click                          │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  Gemini Screen Analysis                          │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────┐    ┌───────────────────────────┐        │
│  │ Claude Code  │───→│ win_drive (stdio)         │       │
│  │ MCP Client   │←───│ JSON-RPC responses        │       │
│  └──────────────┘    └───────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 383

**Source**: `Reporter_v1\WORKSPACE\a01\13_win_drive_v0.md` L51

```
├── src/
│   ├── main.cpp
│   ├── mcp_server.cpp / .h       # MCP 協定實作
│   ├── tool_registry.cpp / .h    # 工具註冊
│   ├── tools/
│   │   ├── screenshot.cpp / .h   # 截圖
│   │   ├── mouse.cpp / .h        # 滑鼠
│   │   ├── keyboard.cpp / .h     # 鍵盤
│   │   ├── window.cpp / .h       # 視窗管理
│   │   ├── uia.cpp / .h          # UI Automation
│   │   ├── batch.cpp / .h        # 批次操作
│   │   ├── gemini.cpp / .h       # Gemini 分析
│   │   └── shared.h
│   └── util/
│       ├── logger.cpp / .h       # Logging 模組
│       ├── png_encode.cpp / .h
│       ├── screen_buffer.cpp / .h
│       ├── base64.h, env_loader.h, input_guard.h, json_helpers.h
├── vendor/
│   ├── nlohmann/json.hpp
│   └── stb_image_write.h
├── xmake.lua
├── CHANGELOG.md
└── README.md
```

---

## Sample 384

**Source**: `Reporter_v1\WORKSPACE\a01\14_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v0                                │
│      Intel RealSense D435i → Simulated 2D LiDAR               │
│      Python ~1500 lines                                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  │  Stereo Camera      │                                       │
│  └─────────────────────┘                                       │
│       ┌────┴────────────────┐                                  │
│       │                     │                                  │
│       ▼                     ▼                                │
│  ┌──────────────┐   ┌───────────────────┐                      │
│  │ Native       │   │ CREStereo ONNX    │                      │
│  │ Stereo       │   │ 89% coverage      │                      │
│  │ 11% coverage │   │ 95mm MAE          │                      │
│  │ 32mm MAE     │   │                   │                      │
│  └──────┬───────┘   └────────┬──────────┘                      │
│         └──────────┬─────────┘                                 │
│                    │  Combined ~100%                           │
│                    ▼                                          │
│       ┌────────────────────────┐                               │
│       │  Two Output Modes      │                               │
│       ├────────────────────────┤                               │
│       │ LiDAR 1: Horizontal    │                               │
│       │          Obstacle      │                               │
│       │ LiDAR 2: Ground Scan   │                               │
│       └────────────┬───────────┘                               │
│                    │                                           │
│            ┌───────┴───────┐                                   │
│            │               │                                   │
│            ▼               ▼                                 │
│  ┌──────────────┐ ┌──────────────┐                             │
│  │ ROS2         │ │ UDP          │                             │
│  │ LaserScan    │ │ Output       │                             │
│  └──────────────┘ └──────────────┘                             │
│                                                                │
│  Limitation: Semiconductor fabs ban IR                         │
│              → passive stereo only 9-11%                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 385

**Source**: `Reporter_v1\WORKSPACE\a01\14_D435i_LidarScan.md` L46

```
├── d435i_lidar_scan.py       # 主程式（最新版）
├── d435i_lidar_scan_v1.py    # v1 版本
├── d435i_lidar_scan_v2.py    # v2 版本
├── d435i_lidar_scan_v3.py    # v3 版本
├── calibrate_mono.py         # Mono depth 校正
├── compare_fusion.py         # 融合比較
├── compare_mono.py           # Mono depth 比較
├── diagnose_mono.py          # Mono depth 診斷
├── download_model.py         # 模型下載
├── test_crestereo.py         # CREStereo 測試
├── test_ir_quality.py        # IR 品質測試
├── REPORT_v3_depth_compensation.md  # 深度補償報告
├── FLOW.md                   # 流程說明
├── CLAUDE.md
├── CHANGELOG.md
├── README.md
└── requirements.txt
```

---

## Sample 386

**Source**: `Reporter_v1\WORKSPACE\a01\15_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v3                                │
│      Multi-Mode BEV System for AMR Navigation                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  └─────────────────────┘                                       │
│     │             │                                            │
│     ▼             ▼                                          │
│  ┌───────────────────────┐  ┌──────────────────────────────┐   │
│  │ SegFormer-B0          │  │ Depth Anything V2            │   │
│  │ ADE20K Semantic       │  │ Depth Calibration            │   │
│  │ Floor Detection       │  │ Emitter Pulse 100ms          │   │
│  └───────────┬───────────┘  └──────────────┬───────────────┘   │
│              └──────────┬──────────────────┘                   │
│                         │                                      │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  5 BEV Modes                                         │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │  1. IPM                                             │       │
│  │  2. Point Cloud                                     │       │
│  │  3. Hybrid (recommended)                            │       │
│  │  4. Dual IR                                         │       │
│  │  5. Vertical Scan                                   │       │
│  └──────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 387

**Source**: `Reporter_v1\WORKSPACE\a01\15_D435i_LidarScan_v3.md` L40

```
├── main.py                   # 主程式
├── capture_snapshot.py       # 快照擷取（含深度 debug）
├── src/
│   ├── bev.py                # BEV 投影核心
│   ├── camera.py             # D435i 相機控制
│   ├── depth_calibrator.py   # DA v2 深度校正
│   ├── segmentation.py       # SegFormer 語意分割
│   └── __init__.py
├── test_emitter_pulse.py     # Emitter 脈衝測試
├── CHANGELOG.md
├── README.md
└── requirements.txt
```

---

## Sample 388

**Source**: `Reporter_v1\WORKSPACE\a01\16_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│              D435i LidarScan v2                               │
│      6-Stage 3D Point Cloud Pipeline                          │
│      Bottleneck: 500ms vs 50ms target (10x gap)               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐                                      │
│  │  Intel D435i        │                                      │
│  └─────────────────────┘                                      │
│            │                                                  │
│            ▼                                                 │
│  ┌─────────────────────────┐                                  │
│  │ Stage 1: Capture        │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 2: NLSPN Depth    │                                  │
│  │ Completion (>200ms)     │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 3: YOLO Detection │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 4: Point Cloud    │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 5: Scene Analysis │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────────────┐                          │
│  │ Stage 6: SegFormer-B0 FP16      │                          │
│  │          + Rerun 3D Viz         │                          │
│  └─────────────────────────────────┘                          │
│                                                               │
│  Requires: CUDA                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 389

**Source**: `Reporter_v1\WORKSPACE\a01\16_D435i_LidarScan_v2.md` L45

```
├── src/
│   ├── camera.py              # D435i 相機（含 depth→color alignment）
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
│   ├── output.py              # 輸出（含 label → voxel downsample）
│   ├── rerun_logger.py        # Rerun 視覺化
│   └── gate.py                # Gate 控制
├── config/gate_config.yaml    # 延遲閾值 + 相機外參
├── CHANGELOG.md
├── CLAUDE.md
└── requirements.txt
```

---

## Sample 390

**Source**: `Reporter_v1\WORKSPACE\a01\17_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│                  WebCamToLidarScan                            │
│   Monocular RGB → Virtual 2D LiDAR                           │
│   Phase 1 done, Phase 2 partial, idle ~6 weeks                │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────┐                           │
│  │  Webcam / D435i RGB            │                           │
│  └───────────────┬────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  Depth Anything V2 ViT-S       │                           │
│  │  ONNX (DML / CUDA / CPU)       │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  RANSAC Ground Calibration     │                           │
│  │  (IMU Gravity)                 │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  LUT Conversion                │                           │
│  │  ~650 bin LaserScan            │                           │
│  │  <3ms CPU, <0.3ms CUDA         │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  IMU EMA Temporal Filtering    │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  ROS 2 /virtual_scan           │                           │
│  └────────────────────────────────┘                           │
│                                                               │
│  Target: Jetson Thor (Blackwell, 128GB, 144 TOPS)             │
│  Unsolved: AI global depth drift                              │
└──────────────────────────────────────────────────────────────┘
```

---

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

## Sample 392

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L35

```
                        AMR 深度感測需求
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
      相機方案（D435i）    單目 AI 方案      LiDAR 方案
            │                 │                 │
    ┌───────┼───────┐         │                 │
    │       │       │         │                 │
   v0      v2      v3   WebCamTo           HaloScan
  2D融合  3D管線   BEV   LidarScan         4×Mid-360
```

---

## Sample 393

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L149

```
D435i (IR OFF)
  ├→ 內建 stereo depth ──→ 覆蓋率 ~11%（32mm MAE）
  └→ CREStereo ONNX ────→ 覆蓋率 ~89%（95mm MAE）
       └→ 融合（stereo 優先）──→ ~100% 覆蓋率
            └→ 水平切片 → 1081-bin LaserScan
                 └→ UDP / ROS2 LaserScan
```

---

## Sample 394

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L163

```
D435i (IR OFF)
  └→ Stage 1: 資料擷取
       └→ Stage 2: NLSPN 深度補全（>200ms）
            └→ Stage 3: YOLO 物體偵測（non-blocking）
                 └→ Stage 4: 點雲處理 + RANSAC
                      └→ Stage 5: 場景分析
                           └→ Stage 6: SegFormer 分割 + Rerun 3D
```

---

## Sample 395

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L178

```
D435i (IR OFF)
  ├→ RGB ──→ SegFormer-B0 地板偵測
  ├→ RGB ──→ DA V2 深度校正（需 emitter pulse）
  └→ Depth ──→ 5 種 BEV 模式
       ├→ IPM（平面假設）
       ├→ Point Cloud（3D 投影）
       ├→ Hybrid（推薦：IPM 地板 + 深度物體）
       ├→ Dual IR
       └→ Vertical
```

---

## Sample 396

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L195

```
RGB (webcam / D435i)
  └→ DA V2 ViT-S ONNX (94.5MB)
       └→ Metric Depth Map
            └→ RANSAC 地面校正（IMU gravity constraint）
                 └→ LUT 單次遍歷 → ~650 bins LaserScan
                      └→ EMA 時序濾波（IMU-aware）
                           └→ [選用] Ego-motion 多幀拼接
                                └→ ROS 2 /virtual_scan
```

---

## Sample 397

**Source**: `Reporter_v1\WORKSPACE\a01\19_Vision_Depth_Integration.md` L211

```
4× Livox Mid-360 (Ethernet UDP)
  └→ PTP 時間同步
       └→ 點雲合併
            ├→ 路徑 A: CropBox 3D 安全區偵測 → 停車/減速（RPi 5, C++）
            ├→ 路徑 B: 高度過濾 → 2D LaserScan → Nav2 costmap
            └→ 路徑 C（規劃中）: 4× 魚眼 + YOLOv8-seg（Jetson Orin NX）
```

---

## Sample 398

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\01_arch.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬────────────────┘
               │                      │
       install.ps1 / install.sh       │
               │                      │
               ▼                     │
  ┌────────────────────┐              │
  │  ~/.claude/        │              │
  │  commands/         │              │
  │  skills/           │              │
  │  settings.json     │              │
  │  CLAUDE.md         │              │
  └────────────────────┘              │
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌───────────────────────────────────────────┐
│           Google Cloud Backend            │
├─────────────┬──────────────┬──────────────┤
│ Google Chat │ Google Sheet │ Apps Script  │
│  Webhook    │  Dashboard   │  Web App     │
└─────────────┴──────────────┴──────────────┘
```

---

## Sample 399

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\02_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                    │
│    Delegation SOP: Claude Code ←→ OpenCode              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐    ┌───────────────────────┐    │
│  │   Claude Code        │    │   OpenCode            │    │
│  │   (Decision-Maker)   │ ─→│   (Executor)          │    │
│  └──────────────────────┘    └───────────────────────┘    │
│                                                           │
├───────────────────────────────────────────────────────────┤
│  Delegation Levels                                        │
│                                                           │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐      │
│  │ L1        │ │ L2           │  │ L3              │      │
│  │ New Files │ │ Controlled   │  │ Task-Level      │      │
│  │           │ │ Edits        │  │ Autonomy        │      │
│  │           │ │              │  │ ≤5 parallel     │      │
│  │           │ │              │  │ agents          │      │
│  └───────────┘ └──────────────┘  └─────────────────┘      │
│                                                           │
│  Status: Archived → merged into claude-dotfiles          │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 400

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\03_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│                  HaloScan (Planning 0%)                    │
│          360° Safety Zone for AMR                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│       LiDAR 1        LiDAR 2       LiDAR 3  LiDAR 4        │
│   ┌──────────┐   ┌──────────┐   ┌────────┐ ┌────────┐      │
│   │ Livox    │   │ Livox    │   │ Livox  │ │ Livox  │      │
│   │ Mid-360  │   │ Mid-360  │   │Mid-360 │ │Mid-360 │      │
│   │ 905nm    │   │ 905nm    │   │ 905nm  │ │ 905nm  │      │
│   └────┬─────┘   └────┬─────┘   └───┬────┘ └───┬────┘      │
│        │              │             │          │           │
│        └──────┬───────┴──────┬──────┘          │           │
│               │   Ethernet UDP / PTP Sync      │           │
│               └──────────┬─────────────────────┘           │
│                          │                                 │
│                          ▼                                │
│              ┌───────────────────────┐                     │
│              │   Raspberry Pi 5      │                     │
│              │   C++ / ROS2 / PCL    │                     │
│              │   CropBox 3D Detect   │                     │
│              └─────────┬─────────────┘                     │
│                ┌───────┴───────┐                           │
│                │               │                           │
│                ▼              ▼                          │
│  ┌──────────────────┐ ┌────────────────────┐               │
│  │ Path A           │ │ Path B             │               │
│  │ 3D Safety Zone   │ │ 2D LaserScan Nav2  │               │
│  └────────┬─────────┘ └────────┬───────────┘               │
│           └────────┬───────────┘                           │
│                    ▼                                      │
│         ┌───────────────────┐                              │
│         │ Output            │                              │
│         │ 0=safe 1=slow     │                              │
│         │ 2=stop            │                              │
│         └───────────────────┘                              │
│                                                            │
│  Risk: 905nm IR interference in semiconductor fabs         │
└────────────────────────────────────────────────────────────┘
```

---

## Sample 401

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\04_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│              UR Program Analysis                          │
│      Offline Toolchain for UR30 Cobot                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  72 files, 64,503 lines                                   │
│            │                                              │
│            ▼                                             │
│  ┌───────────────────┐                                    │
│  │  Python CLI       │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Parser           │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Tree Parser      │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Project Loader   │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Flow Analyzer    │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│     ┌─────┼──────────────┐                                │
│     │                    │ │                              │
│     ▼    ▼             ▼                               │
│  ┌─────┐ ┌───────────┐ ┌───────────────┐                  │
│  │ Doc │ │ Simplifier│ │ FK Kinematics │                  │
│  │ Gen │ │           │ │ 91.5% pass    │                  │
│  └─────┘ └───────────┘ └───────────────┘                  │
│                                                           │
│  Output: 82 analysis docs, 46 tests                       │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 402

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\05_arch.md` L1

```
┌──────────────────────────────────────────────┐
│        OpenCode Enhance (Archived)           │
│        OpenCode CLI Config                   │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  OpenCode CLI (TypeScript)             │  │
│  ├────────────────────────────────────────┤  │
│  │  Model: Gemini 3 Flash Preview         │  │
│  │  MCP Integration                       │  │
│  │  AGENTS.md                             │  │
│  │  Git-Attribution Plugin                │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  Status: Archived → merged into             │
│          claude-dotfiles                     │
└──────────────────────────────────────────────┘
```

---

## Sample 403

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\06_arch.md` L1

```
┌─────────────────────────────────────────────────────────────┐
│                  Personal RAG (PKB)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sources                                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Engineering  │ │ Email        │ │ Images           │     │
│  │ Docs         │ │ (.mbox)      │ │                  │     │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘     │
│         └────────────────┼──────────────────┘               │
│                          │                                  │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dual Embedding                                      │   │
│  │  ┌─────────────────────┐  ┌────────────────────────┐ │   │
│  │                                                      │ Gemini              │  │ Ollama bge-m3          │ │ │
│  │                                                      │ embedding-2-preview │  │ 1024d                  │ │ │
│  │                                                      │ 3072d               │  │                        │ │ │
│  │  └─────────┬───────────┘  └───────────┬────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│               └─────────────┬────────────┘                  │
│                             ▼                              │
│           ┌─────────────────────────────────┐               │
│           │  Qdrant (Docker)                │               │
│           │  6 collections, ~1.95M vectors  │               │
│           └───────────────┬─────────────────┘               │
│                           │                                 │
│                           ▼                                │
│           ┌─────────────────────────────────┐               │
│           │  FastAPI                        │               │
│           │  Gemini 2.5 Flash (Vision+LLM)  │               │
│           ├─────────────────────────────────┤               │
│           │  /api/search                    │               │
│           │  /api/deep-query (SSE)          │               │
│           │  /api/stats                     │               │
│           └─────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Sample 404

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\07_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│              TM Program Analysis                           │
│      Offline Toolchain for TM12 Cobot .flow                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  4,444 nodes                                               │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Python CLI       │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Flow Parser      │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Analyzer         │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│     ┌─────┼──────────────────┐                             │
│     │                        │ │                           │
│     ▼    ▼                 ▼                            │
│  ┌─────┐ ┌───────────────┐ ┌──────────────────────┐        │
│  │ Doc │ │ Vision        │ │ FK/IK Kinematics     │        │
│  │ Gen │ │ Analyzer      │ │                      │        │
│  └─────┘ └───────────────┘ └──────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │  MutableFlowDocument (Edit)                      │      │
│  └──────────────┬───────────────────────────────────┘      │
│                 │                                          │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Simplifier                                      │      │
│  │  452 chains, 2021 duplicates                     │      │
│  │  70 simplification plans                         │      │
│  └──────────────────────────────────────────────────┘      │
│                                                            │
│  Output: 49 docs, 34 tests                                 │
└────────────────────────────────────────────────────────────┘
```

---

## Sample 405

**Source**: `Reporter_v1\WORKSPACE\a01\修正版\08_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                  Chat Bot                                 │
│      Google Chat Bot for @gyro.com.tw                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐                                        │
│  │ Google Chat   │                                        │
│  │ @gyro.com.tw  │                                        │
│  └───────────────┘                                        │
│         │  /kb --doc / --mail / --img                     │
│         ▼                                                │
│  ┌──────────────────────┐                                 │
│  │ GCP Cloud Run        │                                 │
│  │ (JWT / OIDC auth)    │                                 │
│  └──────────┬───────────┘                                 │
│             │ ngrok tunnel                                │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Local FastAPI RAG Backend                       │     │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │     │
│  │                                                  │ Qdrant      │ │ Gemini     │ │ Ollama      │  │ │
│  │                                                  │ │ │ 2.5 Flash  │ │ bge-m3      │  │ │
│  │  └─────────────┘ └────────────┘ └─────────────┘  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Apps Script          │                                 │
│  │ Daily Stats          │                                 │
│  └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 406

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\01_arch.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬───────────────┘
               │                       │
       install.ps1 / install.sh        │
               │                       │
               ▼                      │
  ┌────────────────────┐               │
  │  ~/.claude/         │              │
  │  commands/          │              │
  │  skills/            │              │
  │  settings.json      │              │
  │  CLAUDE.md          │              │
  └────────────────────┘───────────────│
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│           Google Cloud Backend             │
├─────────────┬──────────────┬───────────────┤
│ Google Chat │ Google Sheet │ Apps Script   │
│  Webhook    │  Dashboard   │  Web App      │
└─────────────┴──────────────┴──────────────┘
```

---

## Sample 407

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\02_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                    │
│    Delegation SOP: Claude Code ←→ OpenCode              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐  ┌───────────────────────┐      │
│  │   Claude Code        │   │   OpenCode             │    │
│  │   (Decision-Maker)   │ ──→│   (Executor)           │  │
│  └──────────────────────┘  └───────────────────────┘      │
│                                                           │
├───────────────────────────────────────────────────────────┤
│  Delegation Levels                                        │
│                                                           │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐      │
│  │ L1        │ │ L2           │  │ L3              │      │
│  │ New Files │ │ Controlled   │  │ Task-Level      │      │
│  │           │ │ Edits        │  │ Autonomy        │      │
│  │           │ │              │  │ ≤5 parallel     │      │
│  │           │ │              │  │ agents          │      │
│  └───────────┘ └──────────────┘  └─────────────────┘      │
│                                                           │
│  Status: Archived → merged into claude-dotfiles          │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 408

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\03_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│                  HaloScan (Planning 0%)                    │
│          360° Safety Zone for AMR                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│       LiDAR 1        LiDAR 2       LiDAR 3  LiDAR 4        │
│   ┌──────────┐   ┌──────────┐   ┌────────┐ ┌────────┐      │
│   │ Livox    │   │ Livox    │   │ Livox  │ │ Livox  │      │
│   │ Mid-360  │   │ Mid-360  │   │Mid-360 │ │Mid-360 │      │
│   │ 905nm    │   │ 905nm    │   │ 905nm  │ │ 905nm  │      │
│   └────┬─────┘   └────┬─────┘   └───┬────┘ └───┬────┘      │
│        │              │              │          │          │
│        └──────┬───────┴──────┬───────┘          │          │
│               │   Ethernet UDP / PTP Sync       │          │
│               └──────────┬──────────────────────┘          │
│                          │                                 │
│                          ▼                                │
│              ┌───────────────────────┐                     │
│              │   Raspberry Pi 5      │                     │
│              │   C++ / ROS2 / PCL    │                     │
│              │   CropBox 3D Detect   │                     │
│              └─────────┬─────────────┘                     │
│                ┌───────┴───────┐                           │
│                │               │                           │
│                ▼               ▼                         │
│  ┌──────────────────┐ ┌────────────────────┐               │
│  │ Path A           │ │ Path B             │               │
│  │ 3D Safety Zone   │ │ 2D LaserScan Nav2  │               │
│  └────────┬─────────┘ └────────┬───────────┘               │
│           └────────┬───────────┘                           │
│                    ▼                                      │
│         ┌───────────────────┐                              │
│         │ Output            │                              │
│         │ 0=safe 1=slow     │                              │
│         │ 2=stop            │                              │
│         └───────────────────┘                              │
│                                                            │
│  Risk: 905nm IR interference in semiconductor fabs         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 409

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\04_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│              UR Program Analysis                          │
│      Offline Toolchain for UR30 Cobot                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  72 files, 64,503 lines                                   │
│            │                                              │
│            ▼                                             │
│  ┌───────────────────┐                                    │
│  │  Python CLI       │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Parser           │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Tree Parser      │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Project Loader   │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Flow Analyzer    │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│     ┌─────┼──────────────┐                                │
│     │                    │ │                              │
│     ▼     ▼              ▼                             │
│  ┌─────┐ ┌───────────┐ ┌───────────────┐                  │
│  │ Doc │ │ Simplifier│ │ FK Kinematics │                  │
│  │ Gen │ │           │ │ 91.5% pass    │                  │
│  └─────┘ └───────────┘ └───────────────┘                  │
│                                                           │
│  Output: 82 analysis docs, 46 tests                       │
└────────────────────────────────────────────────────────┘
```

---

## Sample 410

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\05_arch.md` L1

```
┌───────────────────────────────────────────────┐
│        OpenCode Enhance (Archived)            │
│        OpenCode CLI Config                    │
├───────────────────────────────────────────────┤
│                                               │
│  ┌────────────────────────────────────────┐   │
│  │  OpenCode CLI (TypeScript)             │   │
│  ├────────────────────────────────────────┤   │
│  │  Model: Gemini 3 Flash Preview         │   │
│  │  MCP Integration                       │   │
│  │  AGENTS.md                             │   │
│  │  Git-Attribution Plugin                │   │
│  └────────────────────────────────────────┘   │
│                                               │
│  Status: Archived → merged into              │
│          claude-dotfiles                      │
└──────────────────────────────────────────────┘
```

---

## Sample 411

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\06_arch.md` L1

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Personal RAG (PKB)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sources                                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Engineering  │ │ Email        │ │ Images           │     │
│  │ Docs         │ │ (.mbox)      │ │                  │     │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘     │
│         └────────────────┼──────────────────┘               │
│                          │                                  │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dual Embedding                                      │   │
│  │  ┌─────────────────────┐  ┌────────────────────────┐ │   │
│  │                                                      │ Gemini              │  │ Ollama bge-m3          │ │ │
│  │                                                      │ embedding-2-preview │  │ 1024d                  │ │ │
│  │                                                      │ 3072d               │  │                        │ │ │
│  │  └─────────┬───────────┘  └───────────┬────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│               └─────────────┬────────────┘                  │
│                             ▼                              │
│           ┌─────────────────────────────────┐               │
│           │  Qdrant (Docker)                │               │
│           │  6 collections, ~1.95M vectors  │               │
│           └───────────────┬─────────────────┘               │
│                           │                                 │
│                           ▼                                │
│           ┌─────────────────────────────────┐               │
│           │  FastAPI                        │               │
│           │  Gemini 2.5 Flash (Vision+LLM)  │               │
│           ├─────────────────────────────────┤               │
│           │  /api/search                    │               │
│           │  /api/deep-query (SSE)          │               │
│           │  /api/stats                     │               │
│           └─────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Sample 412

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\07_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│              TM Program Analysis                           │
│      Offline Toolchain for TM12 Cobot .flow                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  4,444 nodes                                               │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Python CLI       │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Flow Parser      │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Analyzer         │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│     ┌─────┼──────────────────┐                             │
│     │                        │ │                           │
│     ▼     ▼                  ▼                          │
│  ┌─────┐ ┌───────────────┐ ┌──────────────────────┐        │
│  │ Doc │ │ Vision        │ │ FK/IK Kinematics     │        │
│  │ Gen │ │ Analyzer      │ │                      │        │
│  └─────┘ └───────────────┘ └──────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │  MutableFlowDocument (Edit)                      │      │
│  └──────────────┬───────────────────────────────────┘      │
│                 │                                          │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Simplifier                                      │      │
│  │  452 chains, 2021 duplicates                     │      │
│  │  70 simplification plans                         │      │
│  └──────────────────────────────────────────────────┘      │
│                                                            │
│  Output: 49 docs, 34 tests                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Sample 413

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\08_arch.md` L1

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Chat Bot                                 │
│      Google Chat Bot for @gyro.com.tw                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐                                        │
│  │ Google Chat   │                                        │
│  │ @gyro.com.tw  │                                        │
│  └───────────────┘                                        │
│         │  /kb --doc / --mail / --img                     │
│         ▼                                                │
│  ┌──────────────────────┐                                 │
│  │ GCP Cloud Run        │                                 │
│  │ (JWT / OIDC auth)    │                                 │
│  └──────────┬───────────┘                                 │
│             │ ngrok tunnel                                │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Local FastAPI RAG Backend                       │     │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │     │
│  │                                                  │ Qdrant      │ │ Gemini     │ │ Ollama      │  │ │
│  │                                                  │ │ │ 2.5 Flash  │ │ bge-m3      │  │ │
│  │  └─────────────┘ └────────────┘ └─────────────┘  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Apps Script          │                                 │
│  │ Daily Stats          │                                 │
│  └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 414

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\09_arch.md` L1

```
┌───────────────────────────────────────┐
│          public-assets                │
│   GitHub Static Asset Hosting         │
├───────────────────────────────────────┤
│                                       │
│  ┌────────────────────────────────┐   │
│  │  GYRO Logo (256x256 PNG)       │   │
│  │  Version A    Version B        │   │
│  └────────────────────────────────┘   │
│                 │                     │
│        GitHub raw URL                 │
│                 │                     │
│       ┌─────────┴─────────┐           │
│       │                   │           │
│       ▼                   ▼         │
│  ┌──────────┐     ┌────────────┐      │
│  │ Chat Bot │     │ Other      │      │
│  │ Avatar   │     │ Projects   │      │
│  └──────────┘     └────────────┘      │
└──────────────────────────────────────┘
```

---

## Sample 415

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\10_arch.md` L1

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│               PM v2 (Archived)                           │
│       Claude Code /pm Workflow                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────┐    ┌──────────┐    ┌───────────┐    ┌─────┐  │
│  │ /pm    │───→│ /pm sync │───→│ /pm review│───→│/pm  │ │
│  │ start  │    │ 5 options│    │ red-team  │    │bye  │  │
│  │        │    │ menu     │    │ subagent  │    │     │  │
│  └────────┘    └──────────┘    └───────────┘    └──┬──┘  │
│                                                    │     │
│                                            ┌───────┘     │
│                                            │             │
│                                            ▼            │
│                                   ┌──────────────────┐   │
│                                   │ Code Review      │   │
│                                   │ QA + Retro       │   │
│                                   └──────────────────┘   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Integration                                       │  │
│  │  Status Line                                       │ Google Sheet │ progress.md          │ │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Status: Archived → merged into claude-dotfiles         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 416

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\11_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                  Mail Checker                             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Google Takeout .mbox │                                 │
│  └──────────┬───────────┘                                 │
│             │                                             │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Attachment Extractor (MD5 Dedup)                │     │
│  └──────────────────────┬───────────────────────────┘     │
│                         │                                 │
│                         ▼                                │
│  ┌───────────────────────────────────────────────────┐    │
│  │  mail_indexer.py                                  │    │
│  │  Metadata → SQLite FTS5                          │    │
│  │  Gemini 2.0 Flash Batch Summarization             │    │
│  │  140 emails/min (10x speedup)                     │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐     │
│  │  progress_mailer.py                              │     │
│  │  Hourly HTML Reports via SMTP                    │     │
│  └──────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 417

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\12_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                    StockSage                              │
│             ML Stock Prediction                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Model                                    │      │
│  │  Transformer Encoder                            │      │
│  │  5-day × 30 features, 3-class                   │      │
│  │  OOS accuracy: 48.9%                            │      │
│  └────────────────────┬────────────────────────────┘      │
│                       │                                   │
│                       ▼                                  │
│  ┌──────────────────────────────────────────────────┐     │
│  │  GMP Model                                       │     │
│  │  LightGBM (~55 tickers)                          │     │
│  │  555 features                                    │     │
│  │  Vectorized: 4min → 10s                         │     │
│  └──────────────────────────────────────────────────┘     │
│                       │                                   │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Email via Gmail API                      │      │
│  └─────────────────────────────────────────────────┘      │
│                                                           │
│  Scheduler: Windows Task Scheduler                        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 418

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\13_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                     win_drive                             │
│       Windows Desktop Automation MCP Server               │
├───────────────────────────────────────────────────────────┤
│  C++20 │ stdio JSON-RPC │ Per-Monitor DPI Aware V2        │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐     │
│  │  15 Tools                                        │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  screenshot (GDI)      │ mouse control           │     │
│  │  keyboard input        │ draw_path               │     │
│  │  window list/focus     │ batch ops               │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  UI Automation                                   │     │
│  │  inspect │ find │ click                          │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  Gemini Screen Analysis                          │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────┐    ┌───────────────────────────┐        │
│  │ Claude Code  │───→│ win_drive (stdio)         │       │
│  │ MCP Client   │←───│ JSON-RPC responses        │       │
│  └──────────────┘    └───────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 419

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\14_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v0                                │
│      Intel RealSense D435i → Simulated 2D LiDAR               │
│      Python ~1500 lines                                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  │  Stereo Camera      │                                       │
│  └─────────────────────┘                                       │
│       ┌────┴────────────────┐                                  │
│       │                     │                                  │
│       ▼                     ▼                                │
│  ┌──────────────┐   ┌───────────────────┐                      │
│  │ Native       │   │ CREStereo ONNX    │                      │
│  │ Stereo       │   │ 89% coverage      │                      │
│  │ 11% coverage │   │ 95mm MAE          │                      │
│  │ 32mm MAE     │   │                   │                      │
│  └──────┬───────┘   └────────┬──────────┘                      │
│         └──────────┬─────────┘                                 │
│                    │  Combined ~100%                           │
│                    ▼                                          │
│       ┌────────────────────────┐                               │
│       │  Two Output Modes      │                               │
│       ├────────────────────────┤                               │
│       │ LiDAR 1: Horizontal    │                               │
│       │          Obstacle      │                               │
│       │ LiDAR 2: Ground Scan   │                               │
│       └────────────┬───────────┘                               │
│                    │                                           │
│            ┌───────┴───────┐                                   │
│            │               │                                   │
│            ▼               ▼                                 │
│  ┌──────────────┐ ┌──────────────┐                             │
│  │ ROS2         │ │ UDP          │                             │
│  │ LaserScan    │ │ Output       │                             │
│  └──────────────┘ └──────────────┘                             │
│                                                                │
│  Limitation: Semiconductor fabs ban IR                         │
│              → passive stereo only 9-11%                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 420

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\15_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v3                                │
│      Multi-Mode BEV System for AMR Navigation                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  └─────────────────────┘                                       │
│     │             │                                            │
│     ▼             ▼                                          │
│  ┌───────────────────────┐  ┌──────────────────────────────┐   │
│  │ SegFormer-B0          │  │ Depth Anything V2            │   │
│  │ ADE20K Semantic       │  │ Depth Calibration            │   │
│  │ Floor Detection       │  │ Emitter Pulse 100ms          │   │
│  └───────────┬───────────┘  └──────────────┬───────────────┘   │
│              └──────────┬──────────────────┘                   │
│                         │                                      │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  5 BEV Modes                                         │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │  1. IPM                                             │       │
│  │  2. Point Cloud                                     │       │
│  │  3. Hybrid (recommended)                            │       │
│  │  4. Dual IR                                         │       │
│  │  5. Vertical Scan                                   │       │
│  └──────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 421

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\16_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│              D435i LidarScan v2                               │
│      6-Stage 3D Point Cloud Pipeline                          │
│      Bottleneck: 500ms vs 50ms target (10x gap)               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐                                      │
│  │  Intel D435i        │                                      │
│  └─────────────────────┘                                      │
│            │                                                  │
│            ▼                                                 │
│  ┌─────────────────────────┐                                  │
│  │ Stage 1: Capture        │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 2: NLSPN Depth    │                                  │
│  │ Completion (>200ms)     │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 3: YOLO Detection │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 4: Point Cloud    │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 5: Scene Analysis │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────────────┐                          │
│  │ Stage 6: SegFormer-B0 FP16      │                          │
│  │          + Rerun 3D Viz         │                          │
│  └─────────────────────────────────┘                          │
│                                                               │
│  Requires: CUDA                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 422

**Source**: `Reporter_v1\WORKSPACE\a01\原版-不可修改\17_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│                  WebCamToLidarScan                            │
│   Monocular RGB → Virtual 2D LiDAR                           │
│   Phase 1 done, Phase 2 partial, idle ~6 weeks                │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────┐                           │
│  │  Webcam / D435i RGB            │                           │
│  └───────────────┬────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  Depth Anything V2 ViT-S       │                           │
│  │  ONNX (DML / CUDA / CPU)       │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  RANSAC Ground Calibration     │                           │
│  │  (IMU Gravity)                 │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  LUT Conversion                │                           │
│  │  ~650 bin LaserScan            │                           │
│  │  <3ms CPU, <0.3ms CUDA         │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  IMU EMA Temporal Filtering    │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  ROS 2 /virtual_scan           │                           │
│  └────────────────────────────────┘                           │
│                                                               │
│  Target: Jetson Thor (Blackwell, 128GB, 144 TOPS)             │
│  Unsolved: AI global depth drift                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 423

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\01_arch.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬───────────────┘
               │                       │
       install.ps1 / install.sh        │
               │                       │
               ▼                      │
  ┌────────────────────┐               │
  │  ~/.claude/         │              │
  │  commands/          │              │
  │  skills/            │              │
  │  settings.json      │              │
  │  CLAUDE.md          │              │
  └────────────────────┘───────────────│
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│           Google Cloud Backend             │
├─────────────┬──────────────┬───────────────┤
│ Google Chat │ Google Sheet │ Apps Script   │
│  Webhook    │  Dashboard   │  Web App      │
└─────────────┴──────────────┴──────────────┘
```

---

## Sample 424

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\02_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                    │
│    Delegation SOP: Claude Code ←→ OpenCode              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐  ┌───────────────────────┐      │
│  │   Claude Code        │   │   OpenCode             │    │
│  │   (Decision-Maker)   │ ──→│   (Executor)           │  │
│  └──────────────────────┘  └───────────────────────┘      │
│                                                           │
├───────────────────────────────────────────────────────────┤
│  Delegation Levels                                        │
│                                                           │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐      │
│  │ L1        │ │ L2           │  │ L3              │      │
│  │ New Files │ │ Controlled   │  │ Task-Level      │      │
│  │           │ │ Edits        │  │ Autonomy        │      │
│  │           │ │              │  │ ≤5 parallel     │      │
│  │           │ │              │  │ agents          │      │
│  └───────────┘ └──────────────┘  └─────────────────┘      │
│                                                           │
│  Status: Archived → merged into claude-dotfiles          │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 425

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\03_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│                  HaloScan (Planning 0%)                    │
│          360° Safety Zone for AMR                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│       LiDAR 1        LiDAR 2       LiDAR 3  LiDAR 4        │
│   ┌──────────┐   ┌──────────┐   ┌────────┐ ┌────────┐      │
│   │ Livox    │   │ Livox    │   │ Livox  │ │ Livox  │      │
│   │ Mid-360  │   │ Mid-360  │   │Mid-360 │ │Mid-360 │      │
│   │ 905nm    │   │ 905nm    │   │ 905nm  │ │ 905nm  │      │
│   └────┬─────┘   └────┬─────┘   └───┬────┘ └───┬────┘      │
│        │              │              │          │          │
│        └──────┬───────┴──────┬───────┘          │          │
│               │   Ethernet UDP / PTP Sync       │          │
│               └──────────┬──────────────────────┘          │
│                          │                                 │
│                          ▼                                │
│              ┌───────────────────────┐                     │
│              │   Raspberry Pi 5      │                     │
│              │   C++ / ROS2 / PCL    │                     │
│              │   CropBox 3D Detect   │                     │
│              └─────────┬─────────────┘                     │
│                ┌───────┴───────┐                           │
│                │               │                           │
│                ▼               ▼                         │
│  ┌──────────────────┐ ┌────────────────────┐               │
│  │ Path A           │ │ Path B             │               │
│  │ 3D Safety Zone   │ │ 2D LaserScan Nav2  │               │
│  └────────┬─────────┘ └────────┬───────────┘               │
│           └────────┬───────────┘                           │
│                    ▼                                      │
│         ┌───────────────────┐                              │
│         │ Output            │                              │
│         │ 0=safe 1=slow     │                              │
│         │ 2=stop            │                              │
│         └───────────────────┘                              │
│                                                            │
│  Risk: 905nm IR interference in semiconductor fabs         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 426

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\04_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│              UR Program Analysis                          │
│      Offline Toolchain for UR30 Cobot                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  72 files, 64,503 lines                                   │
│            │                                              │
│            ▼                                             │
│  ┌───────────────────┐                                    │
│  │  Python CLI       │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Parser           │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Tree Parser      │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Project Loader   │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Flow Analyzer    │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│     ┌─────┼──────────────┐                                │
│     │                    │ │                              │
│     ▼     ▼              ▼                             │
│  ┌─────┐ ┌───────────┐ ┌───────────────┐                  │
│  │ Doc │ │ Simplifier│ │ FK Kinematics │                  │
│  │ Gen │ │           │ │ 91.5% pass    │                  │
│  └─────┘ └───────────┘ └───────────────┘                  │
│                                                           │
│  Output: 82 analysis docs, 46 tests                       │
└────────────────────────────────────────────────────────┘
```

---

## Sample 427

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\05_arch.md` L1

```
┌───────────────────────────────────────────────┐
│        OpenCode Enhance (Archived)            │
│        OpenCode CLI Config                    │
├───────────────────────────────────────────────┤
│                                               │
│  ┌────────────────────────────────────────┐   │
│  │  OpenCode CLI (TypeScript)             │   │
│  ├────────────────────────────────────────┤   │
│  │  Model: Gemini 3 Flash Preview         │   │
│  │  MCP Integration                       │   │
│  │  AGENTS.md                             │   │
│  │  Git-Attribution Plugin                │   │
│  └────────────────────────────────────────┘   │
│                                               │
│  Status: Archived → merged into              │
│          claude-dotfiles                      │
└──────────────────────────────────────────────┘
```

---

## Sample 428

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\06_arch.md` L1

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Personal RAG (PKB)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sources                                                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Engineering  │ │ Email        │ │ Images           │     │
│  │ Docs         │ │ (.mbox)      │ │                  │     │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘     │
│         └────────────────┼──────────────────┘               │
│                          │                                  │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dual Embedding                                      │   │
│  │  ┌─────────────────────┐  ┌────────────────────────┐ │   │
│  │                                                      │ Gemini              │  │ Ollama bge-m3          │ │ │
│  │                                                      │ embedding-2-preview │  │ 1024d                  │ │ │
│  │                                                      │ 3072d               │  │                        │ │ │
│  │  └─────────┬───────────┘  └───────────┬────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│               └─────────────┬────────────┘                  │
│                             ▼                              │
│           ┌─────────────────────────────────┐               │
│           │  Qdrant (Docker)                │               │
│           │  6 collections, ~1.95M vectors  │               │
│           └───────────────┬─────────────────┘               │
│                           │                                 │
│                           ▼                                │
│           ┌─────────────────────────────────┐               │
│           │  FastAPI                        │               │
│           │  Gemini 2.5 Flash (Vision+LLM)  │               │
│           ├─────────────────────────────────┤               │
│           │  /api/search                    │               │
│           │  /api/deep-query (SSE)          │               │
│           │  /api/stats                     │               │
│           └─────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Sample 429

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\07_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│              TM Program Analysis                           │
│      Offline Toolchain for TM12 Cobot .flow                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  4,444 nodes                                               │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Python CLI       │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Flow Parser      │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Analyzer         │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│     ┌─────┼──────────────────┐                             │
│     │                        │ │                           │
│     ▼     ▼                  ▼                          │
│  ┌─────┐ ┌───────────────┐ ┌──────────────────────┐        │
│  │ Doc │ │ Vision        │ │ FK/IK Kinematics     │        │
│  │ Gen │ │ Analyzer      │ │                      │        │
│  └─────┘ └───────────────┘ └──────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │  MutableFlowDocument (Edit)                      │      │
│  └──────────────┬───────────────────────────────────┘      │
│                 │                                          │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Simplifier                                      │      │
│  │  452 chains, 2021 duplicates                     │      │
│  │  70 simplification plans                         │      │
│  └──────────────────────────────────────────────────┘      │
│                                                            │
│  Output: 49 docs, 34 tests                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Sample 430

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\08_arch.md` L1

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Chat Bot                                 │
│      Google Chat Bot for @gyro.com.tw                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐                                        │
│  │ Google Chat   │                                        │
│  │ @gyro.com.tw  │                                        │
│  └───────────────┘                                        │
│         │  /kb --doc / --mail / --img                     │
│         ▼                                                │
│  ┌──────────────────────┐                                 │
│  │ GCP Cloud Run        │                                 │
│  │ (JWT / OIDC auth)    │                                 │
│  └──────────┬───────────┘                                 │
│             │ ngrok tunnel                                │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Local FastAPI RAG Backend                       │     │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │     │
│  │                                                  │ Qdrant      │ │ Gemini     │ │ Ollama      │  │ │
│  │                                                  │ │ │ 2.5 Flash  │ │ bge-m3      │  │ │
│  │  └─────────────┘ └────────────┘ └─────────────┘  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Apps Script          │                                 │
│  │ Daily Stats          │                                 │
│  └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 431

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\09_arch.md` L1

```
┌───────────────────────────────────────┐
│          public-assets                │
│   GitHub Static Asset Hosting         │
├───────────────────────────────────────┤
│                                       │
│  ┌────────────────────────────────┐   │
│  │  GYRO Logo (256x256 PNG)       │   │
│  │  Version A    Version B        │   │
│  └────────────────────────────────┘   │
│                 │                     │
│        GitHub raw URL                 │
│                 │                     │
│       ┌─────────┴─────────┐           │
│       │                   │           │
│       ▼                   ▼         │
│  ┌──────────┐     ┌────────────┐      │
│  │ Chat Bot │     │ Other      │      │
│  │ Avatar   │     │ Projects   │      │
│  └──────────┘     └────────────┘      │
└──────────────────────────────────────┘
```

---

## Sample 432

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\10_arch.md` L1

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│               PM v2 (Archived)                           │
│       Claude Code /pm Workflow                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────┐    ┌──────────┐    ┌───────────┐    ┌─────┐  │
│  │ /pm    │───→│ /pm sync │───→│ /pm review│───→│/pm  │ │
│  │ start  │    │ 5 options│    │ red-team  │    │bye  │  │
│  │        │    │ menu     │    │ subagent  │    │     │  │
│  └────────┘    └──────────┘    └───────────┘    └──┬──┘  │
│                                                    │     │
│                                            ┌───────┘     │
│                                            │             │
│                                            ▼            │
│                                   ┌──────────────────┐   │
│                                   │ Code Review      │   │
│                                   │ QA + Retro       │   │
│                                   └──────────────────┘   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Integration                                       │  │
│  │  Status Line                                       │ Google Sheet │ progress.md          │ │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Status: Archived → merged into claude-dotfiles         │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 433

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\11_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                  Mail Checker                             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Google Takeout .mbox │                                 │
│  └──────────┬───────────┘                                 │
│             │                                             │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Attachment Extractor (MD5 Dedup)                │     │
│  └──────────────────────┬───────────────────────────┘     │
│                         │                                 │
│                         ▼                                │
│  ┌───────────────────────────────────────────────────┐    │
│  │  mail_indexer.py                                  │    │
│  │  Metadata → SQLite FTS5                          │    │
│  │  Gemini 2.0 Flash Batch Summarization             │    │
│  │  140 emails/min (10x speedup)                     │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐     │
│  │  progress_mailer.py                              │     │
│  │  Hourly HTML Reports via SMTP                    │     │
│  └──────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 434

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\12_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                    StockSage                              │
│             ML Stock Prediction                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Model                                    │      │
│  │  Transformer Encoder                            │      │
│  │  5-day × 30 features, 3-class                   │      │
│  │  OOS accuracy: 48.9%                            │      │
│  └────────────────────┬────────────────────────────┘      │
│                       │                                   │
│                       ▼                                  │
│  ┌──────────────────────────────────────────────────┐     │
│  │  GMP Model                                       │     │
│  │  LightGBM (~55 tickers)                          │     │
│  │  555 features                                    │     │
│  │  Vectorized: 4min → 10s                         │     │
│  └──────────────────────────────────────────────────┘     │
│                       │                                   │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐      │
│  │  Daily Email via Gmail API                      │      │
│  └─────────────────────────────────────────────────┘      │
│                                                           │
│  Scheduler: Windows Task Scheduler                        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 435

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\13_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                     win_drive                             │
│       Windows Desktop Automation MCP Server               │
├───────────────────────────────────────────────────────────┤
│  C++20 │ stdio JSON-RPC │ Per-Monitor DPI Aware V2        │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐     │
│  │  15 Tools                                        │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  screenshot (GDI)      │ mouse control           │     │
│  │  keyboard input        │ draw_path               │     │
│  │  window list/focus     │ batch ops               │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  UI Automation                                   │     │
│  │  inspect │ find │ click                          │     │
│  ├──────────────────────────────────────────────────┤     │
│  │  Gemini Screen Analysis                          │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────┐    ┌───────────────────────────┐        │
│  │ Claude Code  │───→│ win_drive (stdio)         │       │
│  │ MCP Client   │←───│ JSON-RPC responses        │       │
│  └──────────────┘    └───────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 436

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\14_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v0                                │
│      Intel RealSense D435i → Simulated 2D LiDAR               │
│      Python ~1500 lines                                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  │  Stereo Camera      │                                       │
│  └─────────────────────┘                                       │
│       ┌────┴────────────────┐                                  │
│       │                     │                                  │
│       ▼                     ▼                                │
│  ┌──────────────┐   ┌───────────────────┐                      │
│  │ Native       │   │ CREStereo ONNX    │                      │
│  │ Stereo       │   │ 89% coverage      │                      │
│  │ 11% coverage │   │ 95mm MAE          │                      │
│  │ 32mm MAE     │   │                   │                      │
│  └──────┬───────┘   └────────┬──────────┘                      │
│         └──────────┬─────────┘                                 │
│                    │  Combined ~100%                           │
│                    ▼                                          │
│       ┌────────────────────────┐                               │
│       │  Two Output Modes      │                               │
│       ├────────────────────────┤                               │
│       │ LiDAR 1: Horizontal    │                               │
│       │          Obstacle      │                               │
│       │ LiDAR 2: Ground Scan   │                               │
│       └────────────┬───────────┘                               │
│                    │                                           │
│            ┌───────┴───────┐                                   │
│            │               │                                   │
│            ▼               ▼                                 │
│  ┌──────────────┐ ┌──────────────┐                             │
│  │ ROS2         │ │ UDP          │                             │
│  │ LaserScan    │ │ Output       │                             │
│  └──────────────┘ └──────────────┘                             │
│                                                                │
│  Limitation: Semiconductor fabs ban IR                         │
│              → passive stereo only 9-11%                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 437

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\15_arch.md` L1

```
┌────────────────────────────────────────────────────────────────┐
│              D435i LidarScan v3                                │
│      Multi-Mode BEV System for AMR Navigation                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐                                       │
│  │  Intel D435i        │                                       │
│  └─────────────────────┘                                       │
│     │             │                                            │
│     ▼             ▼                                          │
│  ┌───────────────────────┐  ┌──────────────────────────────┐   │
│  │ SegFormer-B0          │  │ Depth Anything V2            │   │
│  │ ADE20K Semantic       │  │ Depth Calibration            │   │
│  │ Floor Detection       │  │ Emitter Pulse 100ms          │   │
│  └───────────┬───────────┘  └──────────────┬───────────────┘   │
│              └──────────┬──────────────────┘                   │
│                         │                                      │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  5 BEV Modes                                         │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │  1. IPM                                             │       │
│  │  2. Point Cloud                                     │       │
│  │  3. Hybrid (recommended)                            │       │
│  │  4. Dual IR                                         │       │
│  │  5. Vertical Scan                                   │       │
│  └──────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 438

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\16_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│              D435i LidarScan v2                               │
│      6-Stage 3D Point Cloud Pipeline                          │
│      Bottleneck: 500ms vs 50ms target (10x gap)               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐                                      │
│  │  Intel D435i        │                                      │
│  └─────────────────────┘                                      │
│            │                                                  │
│            ▼                                                 │
│  ┌─────────────────────────┐                                  │
│  │ Stage 1: Capture        │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 2: NLSPN Depth    │                                  │
│  │ Completion (>200ms)     │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 3: YOLO Detection │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 4: Point Cloud    │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │ Stage 5: Scene Analysis │                                  │
│  └────────────┬────────────┘                                  │
│               │                                               │
│               ▼                                              │
│  ┌─────────────────────────────────┐                          │
│  │ Stage 6: SegFormer-B0 FP16      │                          │
│  │          + Rerun 3D Viz         │                          │
│  └─────────────────────────────────┘                          │
│                                                               │
│  Requires: CUDA                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 439

**Source**: `Reporter_v1\WORKSPACE\a01\待修版\17_arch.md` L1

```
┌───────────────────────────────────────────────────────────────┐
│                  WebCamToLidarScan                            │
│   Monocular RGB → Virtual 2D LiDAR                           │
│   Phase 1 done, Phase 2 partial, idle ~6 weeks                │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────┐                           │
│  │  Webcam / D435i RGB            │                           │
│  └───────────────┬────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  Depth Anything V2 ViT-S       │                           │
│  │  ONNX (DML / CUDA / CPU)       │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  RANSAC Ground Calibration     │                           │
│  │  (IMU Gravity)                 │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  LUT Conversion                │                           │
│  │  ~650 bin LaserScan            │                           │
│  │  <3ms CPU, <0.3ms CUDA         │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  IMU EMA Temporal Filtering    │                           │
│  └────────────────────────────────┘                           │
│                  │                                            │
│                  ▼                                           │
│  ┌────────────────────────────────┐                           │
│  │  ROS 2 /virtual_scan           │                           │
│  └────────────────────────────────┘                           │
│                                                               │
│  Target: Jetson Thor (Blackwell, 128GB, 144 TOPS)             │
│  Unsolved: AI global depth drift                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 440

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\01_arch.md` L1

```
┌──────────────────────────────────────────────────────┐
│                  claude-dotfiles                     │
│        Claude Code Config Framework                  │
├──────────────────────────────────────────────────────┤
│  Commands (×8)          Skills (×8)                  │
│  /pm /pm-sync           ascii-align                  │
│  /pm-bye /pm-review     report-easy                  │
│  /do /bye /hello /sc    report-gyro ...              │
├──────────────────────────────────────────────────────┤
│  Statusline (JS/Shell)                               │
│  MCP Servers: Playwright │ Windows MCP │ Google WS   │
└──────────────┬──────────────────────┬────────────────┘
               │                       │
       install.ps1 / install.sh        │
               │                       │
               ▼                      │
  ┌────────────────────┐               │
  │  ~/.claude/         │              │
  │  commands/          │              │
  │  skills/            │              │
  │  settings.json      │              │
  │  CLAUDE.md          │              │
  └────────────────────┘               │
                                      │
          ┌───────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│           Google Cloud Backend             │
├─────────────┬──────────────┬───────────────┤
│ Google Chat │ Google Sheet │ Apps Script   │
│  Webhook    │  Dashboard   │  Web App      │
└─────────────┴──────────────┴───────────────┘
```

---

## Sample 441

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\02_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│               DuelEngineSOP (Archived)                    │
│    Delegation SOP: Claude Code ←→ OpenCode              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐   ┌────────────────────────┐    │
│  │   Claude Code        │   │   OpenCode             │    │
│  │   (Decision-Maker)   │ →│   (Executor)           │    │
│  └──────────────────────┘   └────────────────────────┘    │
│                                                           │
├───────────────────────────────────────────────────────────┤
│  Delegation Levels                                        │
│                                                           │
│  ┌───────────┐ ┌──────────────┐  ┌─────────────────┐      │
│  │ L1        │ │ L2           │  │ L3              │      │
│  │ New Files │ │ Controlled   │  │ Task-Level      │      │
│  │           │ │ Edits        │  │ Autonomy        │      │
│  │           │ │              │  │ ≤5 parallel     │      │
│  │           │ │              │  │ agents          │      │
│  └───────────┘ └──────────────┘  └─────────────────┘      │
│                                                           │
│  Status: Archived → merged into claude-dotfiles          │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 442

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\03_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│                  HaloScan (Planning 0%)                    │
│          360° Safety Zone for AMR                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│       LiDAR 1        LiDAR 2       LiDAR 3  LiDAR 4        │
│   ┌──────────┐   ┌──────────┐   ┌────────┐ ┌────────┐      │
│   │ Livox    │   │ Livox    │   │ Livox  │ │ Livox  │      │
│   │ Mid-360  │   │ Mid-360  │   │Mid-360 │ │Mid-360 │      │
│   │ 905nm    │   │ 905nm    │   │ 905nm  │ │ 905nm  │      │
│   └────┬─────┘   └────┬─────┘   └───┬────┘ └───┬────┘      │
│        │              │              │          │          │
│        └──────┬───────┴──────┬───────┘          │          │
│               │   Ethernet UDP / PTP Sync       │          │
│               └──────────┬──────────────────────┘          │
│                          │                                 │
│                          ▼                                │
│              ┌───────────────────────┐                     │
│              │   Raspberry Pi 5      │                     │
│              │   C++ / ROS2 / PCL    │                     │
│              │   CropBox 3D Detect   │                     │
│              └─────────┬─────────────┘                     │
│                ┌───────┴───────┐                           │
│                │               │                           │
│                ▼              ▼                          │
│  ┌──────────────────┐ ┌────────────────────┐               │
│  │ Path A           │ │ Path B             │               │
│  │ 3D Safety Zone   │ │ 2D LaserScan Nav2  │               │
│  └────────┬─────────┘ └────────┬───────────┘               │
│           └────────┬───────────┘                           │
│                    ▼                                      │
│         ┌───────────────────┐                              │
│         │ Output            │                              │
│         │ 0=safe 1=slow     │                              │
│         │ 2=stop            │                              │
│         └───────────────────┘                              │
│                                                            │
│  Risk: 905nm IR interference in semiconductor fabs         │
└────────────────────────────────────────────────────────────┘
```

---

## Sample 443

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\04_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│              UR Program Analysis                          │
│      Offline Toolchain for UR30 Cobot                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  72 files, 64,503 lines                                   │
│            │                                              │
│            ▼                                             │
│  ┌───────────────────┐                                    │
│  │  Python CLI       │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Parser           │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Tree Parser      │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Project Loader   │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│           ▼                                              │
│  ┌───────────────────┐                                    │
│  │  Flow Analyzer    │                                    │
│  └───────────────────┘                                    │
│           │                                               │
│     ┌─────┼──────────────┐                                │
│     │                    │ │                              │
│     ▼     ▼              ▼                             │
│  ┌─────┐ ┌───────────┐ ┌───────────────┐                  │
│  │ Doc │ │ Simplifier│ │ FK Kinematics │                  │
│  │ Gen │ │           │ │ 91.5% pass    │                  │
│  └─────┘ └───────────┘ └───────────────┘                  │
│                                                           │
│  Output: 82 analysis docs, 46 tests                       │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 444

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\05_arch.md` L1

```
┌───────────────────────────────────────────────┐
│        OpenCode Enhance (Archived)            │
│        OpenCode CLI Config                    │
├───────────────────────────────────────────────┤
│                                               │
│  ┌────────────────────────────────────────┐   │
│  │  OpenCode CLI (TypeScript)             │   │
│  ├────────────────────────────────────────┤   │
│  │  Model: Gemini 3 Flash Preview         │   │
│  │  MCP Integration                       │   │
│  │  AGENTS.md                             │   │
│  │  Git-Attribution Plugin                │   │
│  └────────────────────────────────────────┘   │
│                                               │
│  Status: Archived → merged into              │
│          claude-dotfiles                      │
└───────────────────────────────────────────────┘
```

---

## Sample 445

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\06_arch.md` L1

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  Personal RAG (PKB)                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│  Sources                                                                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐                                                         │
│  │ Engineering  │ │ Email        │ │ Images           │                                                         │
│  │ Docs         │ │ (.mbox)      │ │                  │                                                         │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘                                                         │
│         └────────────────┼──────────────────┘                                                                   │
│                          │                                                                                      │
│                          ▼                                                                                     │
│  ┌──────────────────────────────────────────────────────┐                                                       │
│  │  Dual Embedding                                      │                                                       │
│  │  ┌─────────────────────┐  ┌────────────────────────┐ │                                                       │
│  │                                                      │ Gemini              │  │ Ollama bge-m3          │ │   │
│  │                                                      │ embedding-2-preview │  │ 1024d                  │ │   │
│  │                                                      │ 3072d               │  │                        │ │   │
│  │  └─────────┬───────────┘  └───────────┬────────────┘ │                                                       │
│  └──────────────────────────────────────────────────────┘                                                       │
│               └─────────────┬────────────┘                                                                      │
│                             ▼                                                                                  │
│           ┌─────────────────────────────────┐                                                                   │
│           │  Qdrant (Docker)                │                                                                   │
│           │  6 collections, ~1.95M vectors  │                                                                   │
│           └───────────────┬─────────────────┘                                                                   │
│                           │                                                                                     │
│                           ▼                                                                                    │
│           ┌─────────────────────────────────┐                                                                   │
│           │  FastAPI                        │                                                                   │
│           │  Gemini 2.5 Flash (Vision+LLM)  │                                                                   │
│           ├─────────────────────────────────┤                                                                   │
│           │  /api/search                    │                                                                   │
│           │  /api/deep-query (SSE)          │                                                                   │
│           │  /api/stats                     │                                                                   │
│           └─────────────────────────────────┘                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Sample 446

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\07_arch.md` L1

```
┌────────────────────────────────────────────────────────────┐
│              TM Program Analysis                           │
│      Offline Toolchain for TM12 Cobot .flow                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  4,444 nodes                                               │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Python CLI       │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Flow Parser      │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│           ▼                                               │
│  ┌───────────────────┐                                     │
│  │  Analyzer         │                                     │
│  └───────────────────┘                                     │
│           │                                                │
│     ┌─────┼──────────────────┐                             │
│     │                        │ │                           │
│     ▼     ▼                  ▼                          │
│  ┌─────┐ ┌───────────────┐ ┌──────────────────────┐        │
│  │ Doc │ │ Vision        │ │ FK/IK Kinematics     │        │
│  │ Gen │ │ Analyzer      │ │                      │        │
│  └─────┘ └───────────────┘ └──────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │  MutableFlowDocument (Edit)                      │      │
│  └──────────────┬───────────────────────────────────┘      │
│                 │                                          │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Simplifier                                      │      │
│  │  452 chains, 2021 duplicates                     │      │
│  │  70 simplification plans                         │      │
│  └──────────────────────────────────────────────────┘      │
│                                                            │
│  Output: 49 docs, 34 tests                                 │
└────────────────────────────────────────────────────────────┘
```

---

## Sample 447

**Source**: `Reporter_v1\WORKSPACE\a01\測試區\08_arch.md` L1

```
┌───────────────────────────────────────────────────────────┐
│                  Chat Bot                                 │
│      Google Chat Bot for @gyro.com.tw                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐                                        │
│  │ Google Chat   │                                        │
│  │ @gyro.com.tw  │                                        │
│  └───────────────┘                                        │
│          │  /kb --doc / --mail / --img                    │
│          ▼                                               │
│  ┌──────────────────────┐                                 │
│  │ GCP Cloud Run        │                                 │
│  │ (JWT / OIDC auth)    │                                 │
│  └──────────┬───────────┘                                 │
│             │ ngrok tunnel                                │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Local FastAPI RAG Backend                       │     │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │     │
│  │                                                  │ Qdrant      │ │ Gemini     │ │ Ollama      │  │ │
│  │                                                  │ │ │ 2.5 Flash  │ │ bge-m3      │  │ │
│  │  └─────────────┘ └────────────┘ └─────────────┘  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                           │
│  ┌──────────────────────┐                                 │
│  │ Apps Script          │                                 │
│  │ Daily Stats          │                                 │
│  └──────────────────────┘                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 448

**Source**: `Reporter_v1\WORKSPACE\a02\AI全面導入計畫_2026.md` L122

```
MES (e.g. Applied Materials)
  ↓ SECS/GEM
RTD (Real-Time Dispatch)
  ↓
MCS / MCS Lite (Material Control System)
  ├→ TSC (Traffic System Controller) → AMR Fleet
  ├→ Stocker Controller → Stocker
  ├→ E-Rack Controller → E-Rack
  ├→ Sorter
  └→ EAP (Equipment Automation Program) → Load Port (E84)
```

---

## Sample 449

**Source**: `Reporter_v1\WORKSPACE\a02\AMHS_Edge_Agent_架構.md` L27

```
╔═══════════════════════════════════════════════════════════╗
║                 廠內封閉網路（Air-Gapped）                  ║
║                                                           ║
║  ┌─ Server GPU / DGX Spark（廠內機房）─────────────────┐  ║
║  │                                                     │  ║
║  │  n8n（觸發 + 預分類，指定 Skill + 參數）             │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  LLM Agent                                          │  ║
║  │    Phase 1-2: 直接 Ollama REST API                  │  ║
║  │    Phase 3:   採用 LangGraph 管理多步 workflow        │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  5 Skill（封裝 MCP 呼叫，回傳精簡結果）              │  ║
║  │    dispatch ─→ mcp-mcs + mcp-tsc      (Fast 8B)    │  ║
║  │    diagnose ─→ mcp-eap + mcp-pkb      (Full 72B)   │  ║
║  │    schedule ─→ mcp-mcs + mcp-tsc      (Full 72B)   │  ║
║  │    inventory → mcp-erack + mcp-mcs    (Fast 8B)    │  ║
║  │    traffic ──→ mcp-tsc                (Fast 8B)    │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  MCP Servers + rule_validate（紅線檢查，不用 LLM）   │  ║
║  │  mcp-mcs · mcp-tsc · mcp-eap · mcp-pkb · mcp-erack │  ║
║  │    │                                                │  ║
║  │    ▼                                                │  ║
║  │  ROS 2 Bridge ←→ AMR        Grafana（監控，零 LLM）  │  ║
║  │                                                     │  ║
║  │  Ollama（72B + 8B）· PKB Qdrant · MCS Lite · TSC    │  ║
║  └─────────────────────┬───────────────────────────────┘  ║
║                        │ 廠內 LAN / Wi-Fi                  ║
║  ┌─────────────────────▼───────────────────────────────┐  ║
║  │  AMR IPC ×N                                         │  ║
║  │  [平時] ROS node（純執行器）                          │  ║
║  │  [斷線] Ollama Tiny 1.7B → L1 收尾 + 停靠           │  ║
║  └─────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Sample 450

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L22

```
case01/260319_260328_195945_L4STR-nnUF-FD124-FS54/
├── job/            carwork_*.csv         (1-2 Hz, ~3MB/天)    車輛狀態、位置、電池、alarm
├── statistics/     consumption_*.csv     (1 Hz, ~12MB/天)     馬達負載、電池、輪距、TM 電流
│                   WIFI_Coor_*.csv       (高頻, ~8MB/天)      WiFi 座標、訊號強度
├── tcpbridge/      pscmd_*.csv           (依指令, ~3MB/天)    AMR ↔ TSC TCP 指令
│                   log/*inputlog.txt.log                      TCP 序列號原始記錄
│                   log/*outputlog.txt.log
├── maintain/       carmaintain_*.csv     (稀疏, ~KB)          維修記錄
│                   carmeterage_*.csv     (1 Hz, ~2KB/天)      里程、電池循環數
├── e84/            *_PIO1.log            (~37KB/天)           E84 硬體錯誤碼
│                   errorlog.txt                               歷史錯誤彙總
├── ros/            rostopic_*.log        (2,761 檔, ~480MB)   ROS node 啟動、topic 連線
└── syswork/        cpu_monitor 輸出      (每 5s, ~1MB/天)     CPU% / RAM / Load
```

---

## Sample 451

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L237

```
ROS topics ──┐
CSV 來源 ────┤── Bridge process ──→ SQLite（本地）
E84 log ─────┘       │
                     │ 背景執行緒（每 5-10 秒）
                     │ SELECT * FROM <table> WHERE synced = 0 LIMIT 1000
                     │ → influxdb_client.write_points(rows)
                     │ → UPDATE SET synced = 1
                     ▼
              Server InfluxDB
```

---

## Sample 452

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L426

```
[瀏覽器] 匯出鈕
  → POST /getlogzipfile/               (AGVWeb/webextjs.py:5935 getLogZipFile)
  → Unix socket mysocket.s              (car_info/reset_connection/ReadSocket.py:13-27)
  → ROS service LogGatherSrv(requestname, {startdate, enddate})
  → syswork/scripts/loggathering.py LogGatherServer (line 545)
       兩個分支都會走相同 collect+zip 流程：
       ├─ TSCGatheringFile  分支 (line 554)  ← 一般 log 匯出
       └─ GatheringFile     分支 (line 582)  ← E84 完整匯出
       共同步驟：
       ├─ ReloadGatherLogPathFile  ← 讀 loggather.json 白名單（用於來源檔案搜集）
       ├─ shutil.rmtree + mkdir(LogDestFolder)
       ├─ TSCCollectFile(start, end)  ← 把符合 filter/fileextension 的檔案複製到 LogDestFolder
       └─ TSCZipFolder(LogDestFolder, ...) → YYMMDD_YYMMDD_HHMMSS_$ROBOT.zip
  → /getlogzipfilebyname/<name> 下載
```

---

## Sample 453

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L467

```
ROS topics ──→ 現有 CSV 寫入（不動）
           ──→ 新 Bridge 同時寫 SQLite（新增）
```

---

## Sample 454

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L526

```
ROS topics ──→ prometheus_bridge.py (port 9200) ──→ Prometheus (port 80) ──→ Grafana
           ──→ influxdb_bridge.py               ──→ InfluxDB (port 8181) ──→ Grafana
```

---

## Sample 455

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L573

```
現在（兩條 Bridge，直接 push Server，無斷線保護）：

  ROS topics ──→ prometheus_bridge ──→ Server Prometheus
             ──→ influxdb_bridge  ──→ Server InfluxDB

合併後（一條 Bridge，本地 buffer，統一 push）：

  ROS topics ─┐
  CSV 來源 ───┼→ amr_bridge ──→ Edge SQLite ──batch push──→ Server InfluxDB
  E84 log ────┘                     ↑
                              Tiny Agent 斷線時讀取
```

---

## Sample 456

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L57

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

## Sample 457

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L311

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

## Sample 458

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L354

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）
```

---

## Sample 459

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.marp.md` L558

```
Claude Code 開發 Skill + MCP Server + Bridge
  │
  ▼
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP → API 連接、查詢準確率
  │
  ▼
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite→InfluxDB 同步
  │
  ▼
DGX Spark 產線部署 ──── Phase 1 → 2 → 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  ▼
Production（24/7 離線運行）
```

---

## Sample 460

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.md` L26

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

## Sample 461

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.md` L223

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

## Sample 462

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.md` L263

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）
```

---

## Sample 463

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書.md` L437

```
Claude Code 開發 Skill + MCP Server + Bridge
  │
  ▼
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP → API 連接、查詢準確率
  │
  ▼
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite→InfluxDB 同步
  │
  ▼
DGX Spark 產線部署 ──── Phase 1 → 2 → 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  ▼
Production（24/7 離線運行）
```

---

## Sample 464

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書_elk.md` L26

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

## Sample 465

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書_elk.md` L223

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

## Sample 466

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書_elk.md` L263

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）
```

---

## Sample 467

**Source**: `Reporter_v1\WORKSPACE\a02\GYRO_AI_AMHS_技術白皮書_elk.md` L437

```
Claude Code 開發 Skill + MCP Server + Bridge
  │
  ▼
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP → API 連接、查詢準確率
  │
  ▼
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite→InfluxDB 同步
  │
  ▼
DGX Spark 產線部署 ──── Phase 1 → 2 → 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  ▼
Production（24/7 離線運行）
```

---

## Sample 468

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L36

```
┌────────────────────────────────────────────────────────┐
│  Server（DGX Spark, 128GB 統一記憶體）                  │
│                                                         │
│  ┌───────────────┐ ┌──────────────┐  ┌──────────────┐   │
│  │  InfluxDB     │  │  Qdrant/PKB  │  │  Ollama LLM  │  │
│  │  時序資料     │  │  企業知識    │  │  Full 72B    │  │
│  │  (過去)       │  │  (知識)  ★   │  │  Fast  8B    │ │
│  └───────────────┘ └──────────────┘  └──────────────┘   │
│         ▲                  ▲                  ▲      │
│         └────── 5 個 Skill ─────────┐         │         │
│                                      │         │        │
│  MCS-Lite / TSC / EAP ←── MCP Servers ─── Agent        │
│  (現在 — 即時狀態 + 指令)                              │
└─────────────────────────────────────────────────────────┘
              ▲
              │ heartbeat / batch push
              ▼
┌─────────────────────────────────────────────────────────┐
│  Edge（AMR / Stocker / OHCV IPC）                       │
│  ROS + Bridge + SQLite buffer + Tiny 1.7B (斷線備援)    │
└──────────────────────────────────────────────────────────┘
```

---

## Sample 469

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L64

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）  ★
```

---

## Sample 470

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L125

```
週次   日期        里程碑                              對應專案
─────  ──────────  ──────────────────────────────────  ──────────────
W1     02-23       RAG 流水線概念驗證                  04 personal-rag
W2-3   03-03       向量索引建置規劃（plan）            07 Reporter_v0
W2-3   03-04~10    多模態 KB + Web Chat                05 personal-rag_v1
W4     03-04~09    LINE Bot + Function Calling         02 Line_bot_v0
W4     03-06       Caddy 整合架構（Phase 0）           03 LineBot_Reporter_v1
W5-6   03-25~04-02 PKB v2.0 三階段架構成形             06 personal-rag_v2
W6     03-27~30    Google Chat Bot 上線               01 Chat_bot_v1
W6     03-30       GYRO PPTX 報告生成器                08 Reporter_v1
```

---

## Sample 471

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L213

```
F:\機器人專案\06_AGV (來源目錄)
        ↓
┌─────────────────────────────────────────────┐
│ Phase 1: Vault Backup                        │
│   phase1_vault_backup.py                     │
│   ├─ 掃描來源                                │
│   ├─ SHA256 去重                             │
│   └─ 複製至 PKB/vault/（唯讀）               │
└─────────────────────────────────────────────┘
        ↓ MANIFEST.csv (14,975 檔案)
┌─────────────────────────────────────────────┐
│ Phase 2: Full Embedding                      │
│   phase2_embed.py (orchestrator)             │
│   ├─ phase2_extractors.py (多格式萃取)       │
│   ├─ phase2_gemini.py (Vision + embedding)   │
│   ├─ phase2_qdrant.py (Qdrant 索引)          │
│   ├─ phase2m_mail_embed.py (郵件嵌入)        │
│   ├─ reembed_ollama_qdrant.py (bge-m3)       │
│   └─ phase2_notify.py (Email 進度)           │
└─────────────────────────────────────────────┘
        ↓ Qdrant (4 collections, 1M+ pts)
┌─────────────────────────────────────────────┐
│ Phase 3: API & Synthesis                     │
│   ├─ phase3_batch_api.py (API server)        │
│   ├─ phase3_synthesize.py (報告生成)         │
│   └─ 日使用統計追蹤                          │
└─────────────────────────────────────────────┘
```

---

## Sample 472

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L258

```
Google Chat (@gyro.com.tw)
        ↓
GCP Cloud Run thin proxy (asia-east1)
  ├─ JWT (OIDC) 驗證
  ├─ Rate limiting
  └─ 轉發 → ngrok tunnel
        ↓
本機 Backend (FastAPI)
  ├─ API key 驗證
  ├─ rag.py (async embedding)
  ├─ Ollama bge-m3 (本機 embedding)
  ├─ Gemini 2.5 Flash (LLM)
  └─ Qdrant Docker (並行 3 collections)
```

---

## Sample 473

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L305

```
   ┌──────────────────────────────────────────────────────┐
   │           Support Agent 軸線完整交付鏈                │
   │                                                       │
   │   全員 ──→ Chat_bot_v1 (Google Chat /kb)             │
   │              ↓                                       │
   │           PKB v2.0 (Qdrant + Ollama bge-m3)           │
   │              ↑                                       │
   │   AMHS ──→ diagnose Skill (Full 72B + PKB)           │
   │              ↓                                       │
   │           Reporter_v1 (Markdown → GYRO PPTX)         │
   └──────────────────────────────────────────────────────┘
```

---

## Sample 474

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L440

```
              Phase 1 (工具)        Phase 2 (顧問)         Phase 3 (自主)
              ─────────────         ─────────────          ─────────────
PKB 需求      不阻塞                diagnose 需 PKB         高可用 + 低延遲
PKB 狀態      ✅ 後端就緒           🟡 待補維修/客訴         🔴 待上 DGX Spark
Chat_bot_v1   ✅ 已上線              ✅ 持續服務            🔴 待上雲
Reporter_v1   ✅ 工具完成            持續使用                持續使用
```

---

## Sample 475

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L491

```
DGX Spark（產線機房，Air-Gapped）
├─ Ollama LLM Runtime
│   ├─ Full 72B (Q4) ~42GB  → diagnose / schedule
│   └─ Fast 8B  (Q4) ~5GB   → dispatch / inventory / traffic
│
├─ PKB v3 (本軸線交付)
│   ├─ Qdrant Docker (on_disk) ~4GB   ← 6 collections / 195 萬筆
│   ├─ Ollama bge-m3 ~2GB             ← 1024 維 embedding
│   └─ PKB API Server (FastAPI)       ← /kb/search /pkb/diagnose/search /pkb/sop/lookup
│
├─ 監控與資料
│   ├─ InfluxDB ~2-3GB
│   └─ Grafana
│
└─ AMHS 控制面
    ├─ MCS-Lite / TSC / EAP
    └─ MCP Servers
```

---

## Sample 476

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L105

```
週次   日期        里程碑                              對應專案
─────  ──────────  ──────────────────────────────────  ──────────────
W1     02-23       RAG 流水線概念驗證                  04 personal-rag
W2-3   03-03       向量索引建置規劃（plan）            07 Reporter_v0
W2-3   03-04~10    多模態 KB + Web Chat                05 personal-rag_v1
W4     03-04~09    LINE Bot + Function Calling         02 Line_bot_v0
W4     03-06       Caddy 整合架構（Phase 0）           03 LineBot_Reporter_v1
W5-6   03-25~04-02 PKB v2.0 三階段架構成形             06 personal-rag_v2
W6     03-27~30    Google Chat Bot 上線               01 Chat_bot_v1
W6     03-30       GYRO PPTX 報告生成器                08 Reporter_v1
```

---

## Sample 477

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L235

```
   ┌──────────────────────────────────────────────────────┐
   │           Support Agent 軸線完整交付鏈                │
   │                                                       │
   │   全員 ──→ Chat_bot_v1 (Google Chat /kb)             │
   │              ↓                                       │
   │           PKB v2.0 (Qdrant + Ollama bge-m3)           │
   │              ↑                                       │
   │   AMHS ──→ diagnose Skill (Full 72B + PKB)           │
   │              ↓                                       │
   │           Reporter_v1 (Markdown → GYRO PPTX)         │
   └──────────────────────────────────────────────────────┘
```

---

## Sample 478

**Source**: `Reporter_v1\WORKSPACE\a04\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L376

```
              Phase 1 (工具)        Phase 2 (顧問)         Phase 3 (自主)
              ─────────────         ─────────────          ─────────────
PKB 需求      不阻塞                diagnose 需 PKB         高可用 + 低延遲
PKB 狀態      ✅ 後端就緒           🟡 待補維修/客訴         🔴 待上 DGX Spark
Chat_bot_v1   ✅ 已上線              ✅ 持續服務            🔴 待上雲
Reporter_v1   ✅ 工具完成            持續使用                持續使用
```

---

## Sample 479

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L50

```
Google Chat (@gyro.com.tw)
        │
        ▼
GCP Cloud Run thin proxy (asia-east1)
  ├─ JWT (OIDC) 驗證
  ├─ Rate limiting
  └─ 轉發 → ngrok tunnel
        │
        ▼
本機 Backend (FastAPI + Uvicorn)
  ├─ API key 驗證
  ├─ rag.py（async embedding）
  ├─ Ollama bge-m3（本機 embedding）
  ├─ Gemini 2.5 Flash（LLM 推理）
  └─ Qdrant Docker（並行 3 collections 搜尋）
```

---

## Sample 480

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L98

```
LINE 使用者
    │
    ▼
ngrok HTTPS tunnel
    │
    ▼
n8n:5678 webhook
    ├─ Log Handler → chat-log (JSON, 3 天)
    ├─ AI Smart Handler (Gemini Function Calling)
    │   ├─ search_documents
    │   ├─ search_images
    │   ├─ generate_image_context
    │   └─ generate_image (use_kb param)
    └─ Summary Handler (@SUM / @SUMD)
        └─ Gemini 2.5 Flash thinking mode

nginx:80 → /images/* (AI 生成圖片靜態服務)
```

---

## Sample 481

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L141

```
Internet :80 / :443
        │
    ┌───┴───┐
    │ Caddy │  反向代理 + HTTPS 自動憑證
    └───┬───┘
        │
   ┌────┼────┐
/webhook  /api  /images
   │      │      │
 [n8n]  [reporter-api]  [static]
 :5678    :8000          /srv/images/
   │      │
LINE Bot  FastAPI 知識庫
Gemini    + ChromaDB + Gemini embedding
```

---

## Sample 482

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L181

```
檔案輸入 (PDF/PPTX/DOCX/MP4)
    │
    ▼
rag_loaders.py
  ├─ PDFLoader (pdfplumber)
  ├─ PPTXLoader (python-pptx)
  ├─ DOCXLoader (python-docx)
  └─ VideoLoader (ffmpeg + Whisper)
    │
    ▼
rag_core.py (RAGEngine)
  ├─ Chunking (size=800, overlap=100)
  ├─ Embedding (sentence-transformers multilingual)
  ├─ ChromaDB (cosine similarity)
  └─ Gemini 2.0 Flash chat（串流）
    │
    ▼
rag.py (CLI)
```

---

## Sample 483

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L223

```
Web 前端（單檔 HTML + vanilla JS）
  ├─ Lightbox 圖片檢視
  ├─ 拖曳/Ctrl+V 上傳
  └─ localStorage 對話持久化（3 天 / 10MB）
    │
    ▼
FastAPI 後端 (api/main.py)
  ├─ /chat (Gemini Function Calling 入口)
  │   ├─ search_documents
  │   ├─ search_images
  │   ├─ generate_image_context
  │   └─ generate_image (use_kb param)
  ├─ /docs/search   (語意搜尋)
  ├─ /images/search (語意搜尋)
  ├─ /kb-image/{path} (靜態服務)
  └─ /health
    │
    ▼
ChromaDB（本地持久化）
  + gemini-embedding-001 (3072 維)
  + gemini-2.0-flash (Chat)
  + gemini-2.5-flash-image (生成)
```

---

## Sample 484

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L272

```
F:\機器人專案\06_AGV (來源目錄)
        │
        ▼ Phase 1: Vault Backup
phase1_vault_backup.py
  ├─ 掃描來源
  ├─ SHA256 去重
  └─ 複製至 PKB/vault/（唯讀）
        │
        ▼ → MANIFEST.csv (14,975 檔案)
        │
        ▼ Phase 2: Full Embedding (orchestrator)
phase2_embed.py
  ├─ phase2_extractors.py     (PPTX/PDF/DOCX/XLSX 萃取)
  ├─ phase2_gemini.py         (Vision 分析 + embedding)
  ├─ phase2_qdrant.py         (Qdrant 索引)
  ├─ phase2m_mail_embed.py    (郵件嵌入)
  ├─ reembed_ollama_qdrant.py (Ollama bge-m3 re-embed)
  └─ phase2_notify.py         (Email 進度通知)
        │
        ▼ → Qdrant (4 collections, 1M+ pts) + SQLite progress
        │
        ▼ Phase 3: API & Synthesis
phase3_batch_api.py
  ├─ API server（搜尋 / 深度查詢 / 郵件搜尋）
  ├─ 批次 pipeline
  └─ 日使用統計追蹤
phase3_synthesize.py
  └─ 報告生成
```

---

## Sample 485

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L328

```
_build_vectors.py (一次性建置)
    │
    ▼
讀取 _index.json + 5,636 個 .txt
    │
    ▼
分段 (chunk_size=1500, overlap=300)
    │
    ▼
Gemini embedding-001 (768 維, batch=100)
    │
    ▼
_vectors.db (SQLite BLOB)
    │
    ▼ ← 查詢時
_search_vectors.py
    ├─ 語意搜尋 (cosine)
    ├─ 關鍵字搜尋 (SQLite FTS5 BM25)
    └─ RRF (Reciprocal Rank Fusion)
        │
        ▼
候選文件清單（含分數+路徑+摘要）
```

---

## Sample 486

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L377

```
input.md (Markdown 報告)
    │
    ▼
gen_gyro_pptx.py (解析器)
    │
    ▼
Slide Plan 生成（共享）
  └─ 投影片序列、內容規劃
    │
    ├──────────────┬──────────────┐
    │                             │
Marp 引擎（高品質）          python-pptx 引擎（可編輯）
    ├─ {prefix}_marp.md           ├─ 直接寫 PPTX
    ├─ Marp CLI                   ├─ GYRO 品牌樣式注入
    └─ {prefix}_marp.pptx/PDF     └─ {prefix}_editable.pptx
```

---

## Sample 487

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L541

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）   ← 本報告主線
```

---

## Sample 488

**Source**: `Reporter_v1\WORKSPACE\a04\00_REVIEW.md` L609

```
                    ┌─────────────────────────────────────┐
                    │     GYRO 全公司 AI 平台（Server）     │
                    │                                       │
   全員 ───────→  Chat_bot_v1 (Google Chat)                │
                       │                                    │
                       ├──→ PKB v2.0 (Qdrant)              │
                       │     ↑                             │
   AMHS Edge Agent ────┼─────┘ (diagnose Skill)             │
   (Service Agent)     │                                    │
                       │                                    │
   Reporter_v1 ←───────┘ (文件輸出)                        │
                                                            │
                    └─────────────────────────────────────┘
```

---

## Sample 489

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L10

```
GYRO 全公司 AI 四軸策略
┌─────────────────────────────────────────────────────┐
│                                                       │
│  ① Coding Agent      ② Service Agent                │
│  軟體標準化           AMHS Edge Agent                 │
│                                                       │
│  ③ Support Agent  ★  ④ Smart Robot                 │
│  企業知識大腦         具身智能                        │
│  (PKB v2.0)                                           │
│                                                       │
└─────────────────────────────────────────────────────┘
              ★ = 本報告範圍
```

---

## Sample 490

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L29

```
   ┌──────────── Agent 的三個資料來源 ────────────┐
   │                                                 │
   │  MCP Servers ──→ 現在（即時狀態 + 指令）       │
   │  InfluxDB    ──→ 過去（歷史趨勢）              │
   │  Qdrant/PKB  ──→ 知識（維修經驗 + SOP）  ★    │
   │                                                 │
   └─────────────────────────────────────────────────┘
                          ↓
                    5 個 Skill
   ┌──────────────────────────────────────────────┐
   │  Skill        Model       使用 PKB？          │
   │  ──────────   ─────────   ──────────          │
   │  dispatch     Fast 8B     ✗                  │
   │  diagnose     Full 72B    ✅ 歷史案例 + SOP   │
   │  schedule     Full 72B    ✗                  │
   │  inventory    Fast 8B     ✗                  │
   │  traffic      Fast 8B     ✗                  │
   └──────────────────────────────────────────────┘
```

---

## Sample 491

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L56

```
W1          W2-3              W4                W5-6
02-23       03-03~10          03-04~09          03-25~04-02
│           │                 │                 │
原型        多模態 KB         LINE Bot          PKB v2.0
│           Web Chat          n8n + ngrok       Qdrant + bge-m3
│           │                 Caddy 整合        │
│           索引規劃           (停滯)            Google Chat 上線
│           │                                   報告生成器
▼           ▼                 ▼                 ▼
04          05, 07            02, 03            06, 01, 08
personal-   personal-rag_v1   Line_bot_v0       personal-rag_v2
rag         Reporter_v0       LineBot_Reporter  Chat_bot_v1
                                                Reporter_v1
```

---

## Sample 492

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L83

```
🎯 核心交付（Support Agent 完整鏈）
   ┌────────────────────────────────────┐
   │ 06 PKB v2.0   ← 主力後端          │
   │ 01 Chat_bot_v1 ← 企業 ChatBot     │
   │ 08 Reporter_v1 ← 報告生成工具     │
   └────────────────────────────────────┘

🟡 平行 / 過渡
   02 Line_bot_v0       (LINE 對話通道)
   05 personal-rag_v1   (過渡多模態版)

🔵 規劃 / 已停滯
   03 LineBot_Reporter_v1  (Phase 0 後停滯)
   07 Reporter_v0          (RRF 設計，未實作)

⚪ 歷史原型（建議 archive）
   04 personal-rag (v0)
```

---

## Sample 493

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L120

```
   全員 ─────→ Chat_bot_v1 (Google Chat /kb)
                    ↓
                PKB v2.0 (Qdrant + Ollama bge-m3)
                    ↑
   AMHS ─────→ diagnose Skill (Full 72B + PKB)
                    ↓
                Reporter_v1 (Markdown → GYRO PPTX)
```

---

## Sample 494

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L154

```
              Phase 1         Phase 2         Phase 3
              工具            顧問            自主
              ────            ────            ────
PKB 需求      不阻塞          ✅ diagnose 必需 高可用
PKB 後端      ✅ 就緒         🟡 待補資料     🔴 待上雲
Chat_bot_v1   ✅ 上線         ✅ 持續服務     🔴 待上雲
Reporter_v1   ✅ 工具完成     持續使用        持續使用
```

---

## Sample 495

**Source**: `Reporter_v1\WORKSPACE\a04\00_Support_Agent_簡報版.md` L168

```
🔴 極高
└─ Chat_bot_v1 / PKB 本機 backend 單點故障
   影響：全員查詢中斷 + AMHS diagnose Skill 失能

🟡 中
├─ PKB 規格與白皮書不一致（195 萬 vs 1M+）
├─ 缺維修經驗 / 客訴記錄 collection
└─ diagnose Skill 專屬 API 未定義

🟢 低
├─ personal-rag v0/v1 應 archive
├─ LineBot_Reporter_v1 應正式停止
└─ Reporter_v0 RRF 設計未實作（可選改進）
```

---

## Sample 496

**Source**: `Reporter_v1\WORKSPACE\a04\01_Chat_bot_v1.md` L49

```
├── app.py                    # Thin proxy（Cloud Run, JWT 驗證 + 轉發）
├── backend.py                # RAG backend（本機, API key 驗證）
├── rag.py                    # RAG 模組（async embedding + Qdrant + Gemini LLM）
├── rate_limit.py             # Rate limiting
├── start-backend.sh          # Backend 啟動腳本
├── stop-backend.sh           # Backend 停止腳本
├── autostart-backend.vbs     # Windows 開機自啟
├── Dockerfile                # Cloud Run 映像
├── docker-compose.yml        # 本機 Qdrant
├── apps-script/              # Google Apps Script（每日統計報表 trigger）
│   ├── Code.gs
│   └── appsscript.json
├── tests/
│   ├── test_unit.py
│   └── test_thin_proxy.py
├── reviews/                  # 5 份審核報告
├── architecture.md           # 架構文件
├── 使用指引.md               # 使用者指南
└── conv_logger.py / drive_*.py  # （已停用）對話記錄功能
```

---

## Sample 497

**Source**: `Reporter_v1\WORKSPACE\a04\02_Line_bot_v0.md` L28

```
LINE 使用者 → ngrok HTTPS tunnel → n8n:5678 webhook
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         │                                                     │
    Log Handler → chat-log (JSON)                    AI Smart Handler
    @?/@ai/@KD/@img (Function Calling)               │
    @SUM/@SUMD (聊天摘要)                            ├─ search_documents
                                                     ├─ search_images
                                                     ├─ generate_image_context
                                                     └─ generate_image (use_kb param)

    nginx:80 → /images/* (AI 生成圖片靜態服務)
```

---

## Sample 498

**Source**: `Reporter_v1\WORKSPACE\a04\02_Line_bot_v0.md` L58

```
Line_bot_v0/
├── docker-compose.yml           # 三服務編排 (n8n + nginx + ngrok)
├── README.md                    # 文檔及指令說明
├── changelog.md                 # 30+ 項特性與修復紀錄
├── .env.example                 # 環境變數模板
├── nginx/
│   └── default.conf            # 反向代理 + 靜態檔案配置
├── workflows/
│   ├── line-bot-gemini.json    # n8n workflow JSON
│   └── ai-smart-handler-fc.js  # Function Calling 實現
├── images/                      # AI 生成圖片 (runtime)
└── n8n-data/
    ├── chat-log/               # 訊息記錄 (JSON + MD, 保留 3 天)
    ├── chat-history/           # 對話記憶 (per-user, 30 min TTL)
    ├── pending/                # 待辦結果 (5 min TTL)
    └── daily-summaries/        # 每日摘要存檔 (4AM 自動生成)
```

---

## Sample 499

**Source**: `Reporter_v1\WORKSPACE\a04\03_LineBot_Reporter_v1.md` L28

```
Internet:80/443
        │
    [ Caddy ]  (反向代理 + HTTPS)
    /   |   \
   /    |    \
/webhook/* /api/* /images/*
  │         │        │
[n8n]  [reporter-api]  [static]
:5678      :8000        /srv/images/
  │         │
LINE Bot  知識庫搜尋 (FastAPI)
Gemini    + ChromaDB vector DB
         + Gemini embedding
```

---

## Sample 500

**Source**: `Reporter_v1\WORKSPACE\a04\03_LineBot_Reporter_v1.md` L59

```
LineBot_Reporter_v1/
├── docker-compose.yml          # 三服務定義 (caddy + n8n + reporter-api)
├── Caddyfile                   # Caddy 反向代理配置
├── .env.example                # 環境變數模板
├── docs/
│   ├── phase0-report.md        # Phase 0 完成報告
│   ├── unified-aws-migration.md # AWS 遷移規劃
│   ├── aws-migration-discussion.md
│   └── line-bot-aws-migration.md
├── reporter/                   # FastAPI 知識庫應用
├── workflows/                  # n8n workflow JSON
├── knowledge-base/             # 知識庫檔案掛載點
├── images/                     # n8n 生成圖片
└── n8n-data/                   # n8n 持久化資料
```

---

## Sample 501

**Source**: `Reporter_v1\WORKSPACE\a04\04_personal-rag.md` L29

```
檔案輸入 (PDF/PPTX/DOCX/MP4)
    │
    ▼
rag_loaders.py
├─ PDFLoader (pdfplumber)
├─ PPTXLoader (python-pptx)
├─ DOCXLoader (python-docx)
└─ VideoLoader (ffmpeg + Whisper)
    │
    ▼
rag_core.py (RAGEngine)
├─ Chunking (chunk_size=800, overlap=100)
├─ Embedding (sentence-transformers)
├─ ChromaDB (向量存儲)
└─ Gemini Chat (生成式回答)
    │
    ▼
rag.py (CLI)
```

---

## Sample 502

**Source**: `Reporter_v1\WORKSPACE\a04\04_personal-rag.md` L64

```
personal-rag/
├── rag.py                  # CLI 入口
├── rag_core.py             # RAG 引擎核心（Embedding + DB + Chat）
├── rag_loaders.py          # 檔案加載器（PDF/PPTX/DOCX/MP4）
├── requirements.txt        # 依賴清單
├── install.sh              # 安裝腳本
└── test_doc.txt            # 測試文檔
```

---

## Sample 503

**Source**: `Reporter_v1\WORKSPACE\a04\05_personal-rag_v1.md` L30

```
FastAPI 後端 (api/main.py)
├─ /chat (GET/POST) - Chat 前端 + API
├─ /docs/search - 文件語意搜尋
├─ /images/search - 圖片語意搜尋
├─ /images/context - 圖片描述彙整 Prompt
├─ /kb-image/{path} - 知識庫圖片靜態服務
└─ /health - ChromaDB 健康檢查

Chrome 端
└─ localStorage (對話歷史 + 設定)
```

---

## Sample 504

**Source**: `Reporter_v1\WORKSPACE\a04\05_personal-rag_v1.md` L58

```
personal-rag_v1/
├── README.md                # 完整文檔
├── flow.md                  # Chat 系統架構說明
├── CHANGELOG.md             # 版本紀錄
├── Dockerfile               # 容器化配置
├── requirements-api.txt     # Python 依賴
├── api/
│   └── main.py              # FastAPI 應用入口
├── search/                  # 搜尋模塊 (doc_search, img_search, img_context)
├── .doc/                    # 7,388 份文件庫
├── .image/                  # 73,200 張圖片庫
└── .chroma/                 # ChromaDB 持久化存儲
```

---

## Sample 505

**Source**: `Reporter_v1\WORKSPACE\a04\06_personal-rag_v2.md` L29

```
來源目錄 (F:\機器人專案\06_AGV)
    │
    ▼ Phase 1
PKB/vault/ (SHA256 去重) → MANIFEST.csv
    │
    ▼ Phase 2 (orchestrator)
├─ phase2_extractors.py (PPTX/PDF/DOCX 轉文本/影像)
├─ phase2_gemini.py (Vision 分析 + embedding 呼叫)
├─ phase2_qdrant.py (Qdrant Docker 索引)
├─ reembed_ollama_qdrant.py (Ollama bge-m3 re-embed)
└─ phase2_notify.py (Email 進度)
    │
    ▼ Phase 3
├─ phase3_batch_api.py (API server + 批次 pipeline)
├─ phase3_synthesize.py (報告生成)
└─ PKB_db/ (Qdrant Docker)
```

---

## Sample 506

**Source**: `Reporter_v1\WORKSPACE\a04\06_personal-rag_v2.md` L64

```
personal-rag_v2/
├── README.md
├── PKB_專案說明_v2_0316.md
├── PKB_API_GUIDE.md
├── CHANGELOG.md
├── test_gemini_embed.py
└── PKB/
    ├── MANIFEST.csv                   # Phase 1 輸出（14,975 檔案）
    ├── images_index.csv               # Phase 2 輸出（圖片標籤）
    ├── vault/                         # 原始資料備份（唯讀）
    │   ├── docs/                      # PPTX, PDF, DOCX, XLSX
    │   ├── images/                    # JPG, PNG
    │   ├── videos/                    # MP4
    │   └── embedded_images/           # 文件內嵌圖片
    ├── db/
    │   ├── chroma/                    # ChromaDB legacy (唯讀)
    │   └── phase2_state.db            # SQLite 進度追蹤
    ├── scripts/
    │   ├── phase1_vault_backup.py     # 掃描+去重+備份
    │   ├── phase2_embed.py            # orchestrator
    │   ├── phase2_extractors.py       # 檔案萃取
    │   ├── phase2_gemini.py           # Gemini API 封裝
    │   ├── phase2_qdrant.py           # Qdrant 操作
    │   ├── phase2m_mail_embed.py      # 郵件嵌入
    │   ├── reembed_ollama_qdrant.py   # Re-embedding
    │   ├── phase3_batch_api.py        # API 服務
    │   └── qdrant_check.py            # 資料驗證
    └── templates/                     # 報告模板 (Phase 3)
```

---

## Sample 507

**Source**: `Reporter_v1\WORKSPACE\a04\07_Reporter_v0.md` L29

```
_build_vectors.py (一次性)      _search_vectors.py (查詢時)
    │                              │
    ▼                              ▼
讀取 _index.json           語意搜尋 (cosine)
    │                      + 關鍵字搜尋 (FTS5 BM25)
    ▼                      + RRF 混合排序
讀取 5,636 個 .txt              │
    │                          ▼
    ▼                    候選文件清單
分段 (chunk)            (含分數+路徑+摘要)
    │
    ▼
Gemini embedding-001
(768-dim, batch 100)
    │
    ▼
_vectors.db (SQLite BLOB)
```

---

## Sample 508

**Source**: `Reporter_v1\WORKSPACE\a04\07_Reporter_v0.md` L63

```
Reporter_v0/
├── plan.md                  # 專案規劃與設計文檔
├── request/                 # 原始需求文件
├── request_01/~request_06/  # 分階段需求與進展
├── docs/
│   └── aws-migration-discussion.md
└── templates/               # 報告模板
```

---

## Sample 509

**Source**: `Reporter_v1\WORKSPACE\a04\08_Reporter_v1.md` L30

```
input.md (Markdown 報告)
    │
    ▼
gen_gyro_pptx.py (解析器)
    │
    ├─ Slide Plan 生成
    │  (投影片序列、內容規劃)
    │
    ├─ Marp 引擎 (高品質)
    │  → {prefix}_marp.md (中間格式)
    │  → Marp CLI (marp-cli)
    │  → {prefix}_marp.pptx / PDF
    │
    └─ python-pptx 引擎 (可編輯)
       → {prefix}_editable.pptx
```

---

## Sample 510

**Source**: `Reporter_v1\WORKSPACE\a04\08_Reporter_v1.md` L62

```
Reporter_v1/
├── gen_gyro_pptx.py           # 主程式 (MD 解析 + 雙引擎渲染)
├── README.md                  # 使用文檔
└── WORKSPACE/
    └── a04/                   # 工作區
        ├── *.md               # 測試用 Markdown 報告
        └── .images/
            └── diagrams/      # Mermaid 圖表 (.mmd / .png / .svg)
```

---

## Sample 511

**Source**: `Reporter_v1\WORKSPACE\a05\TM_UR_COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 512

**Source**: `Reporter_v1\WORKSPACE\a05\TM_UR_COMPLETED_SUMMARY_elk.md` L319

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 513

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L36

```
┌───────────────────────────────────────────────────────────┐
│  Server（DGX Spark, 128GB 統一記憶體）                    │
│                                                           │
│  ┌───────────────┐ ┌──────────────┐  ┌──────────────┐     │
│  │  InfluxDB     │  │  Qdrant/PKB  │  │  Ollama LLM  │    │
│  │  時序資料     │  │  企業知識    │  │  Full 72B    │    │
│  │  (過去)       │  │  (知識)  ★   │  │  Fast  8B    │   │
│  └───────────────┘ └──────────────┘  └──────────────┘     │
│         ▲                  ▲                  ▲        │
│         └────── 5 個 Skill ─────────┐         │           │
│                                      │         │          │
│  MCS-Lite / TSC / EAP ←── MCP Servers ─── Agent          │
│  (現在 — 即時狀態 + 指令)                                │
└───────────────────────────────────────────────────────────┘
              ▲
              │ heartbeat / batch push
              ▼
┌───────────────────────────────────────────────────────────┐
│  Edge（AMR / Stocker / OHCV IPC）                         │
│  ROS + Bridge + SQLite buffer + Tiny 1.7B (斷線備援)      │
└───────────────────────────────────────────────────────────┘
```

---

## Sample 514

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L64

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）  ★
```

---

## Sample 515

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L125

```
週次   日期        里程碑                              對應專案
─────  ──────────  ──────────────────────────────────  ──────────────
W1     02-23       RAG 流水線概念驗證                  04 personal-rag
W2-3   03-03       向量索引建置規劃（plan）            07 Reporter_v0
W2-3   03-04~10    多模態 KB + Web Chat                05 personal-rag_v1
W4     03-04~09    LINE Bot + Function Calling         02 Line_bot_v0
W4     03-06       Caddy 整合架構（Phase 0）           03 LineBot_Reporter_v1
W5-6   03-25~04-02 PKB v2.0 三階段架構成形             06 personal-rag_v2
W6     03-27~30    Google Chat Bot 上線               01 Chat_bot_v1
W6     03-30       GYRO PPTX 報告生成器                08 Reporter_v1
```

---

## Sample 516

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L213

```
F:\機器人專案\06_AGV (來源目錄)
        ↓
┌──────────────────────────────────────────────┐
│ Phase 1: Vault Backup                        │
│   phase1_vault_backup.py                     │
│   ├─ 掃描來源                                │
│   ├─ SHA256 去重                             │
│   └─ 複製至 PKB/vault/（唯讀）               │
└──────────────────────────────────────────────┘
        ↓ MANIFEST.csv (14,975 檔案)
┌──────────────────────────────────────────────┐
│ Phase 2: Full Embedding                      │
│   phase2_embed.py (orchestrator)             │
│   ├─ phase2_extractors.py (多格式萃取)       │
│   ├─ phase2_gemini.py (Vision + embedding)   │
│   ├─ phase2_qdrant.py (Qdrant 索引)          │
│   ├─ phase2m_mail_embed.py (郵件嵌入)        │
│   ├─ reembed_ollama_qdrant.py (bge-m3)       │
│   └─ phase2_notify.py (Email 進度)           │
└──────────────────────────────────────────────┘
        ↓ Qdrant (4 collections, 1M+ pts)
┌──────────────────────────────────────────────┐
│ Phase 3: API & Synthesis                     │
│   ├─ phase3_batch_api.py (API server)        │
│   ├─ phase3_synthesize.py (報告生成)         │
│   └─ 日使用統計追蹤                          │
└──────────────────────────────────────────────┘
```

---

## Sample 517

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L258

```
Google Chat (@gyro.com.tw)
        ↓
GCP Cloud Run thin proxy (asia-east1)
  ├─ JWT (OIDC) 驗證
  ├─ Rate limiting
  └─ 轉發 → ngrok tunnel
        ↓
本機 Backend (FastAPI)
  ├─ API key 驗證
  ├─ rag.py (async embedding)
  ├─ Ollama bge-m3 (本機 embedding)
  ├─ Gemini 2.5 Flash (LLM)
  └─ Qdrant Docker (並行 3 collections)
```

---

## Sample 518

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L305

```
   ┌───────────────────────────────────────────────────────┐
   │           Support Agent 軸線完整交付鏈                │
   │                                                       │
   │   全員 ──→ Chat_bot_v1 (Google Chat /kb)             │
   │              ↓                                       │
   │           PKB v2.0 (Qdrant + Ollama bge-m3)           │
   │              ↑                                       │
   │   AMHS ──→ diagnose Skill (Full 72B + PKB)           │
   │              ↓                                       │
   │           Reporter_v1 (Markdown → GYRO PPTX)         │
   └───────────────────────────────────────────────────────┘
```

---

## Sample 519

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L440

```
              Phase 1 (工具)        Phase 2 (顧問)         Phase 3 (自主)
              ─────────────         ─────────────          ─────────────
PKB 需求      不阻塞                diagnose 需 PKB         高可用 + 低延遲
PKB 狀態      ✅ 後端就緒           🟡 待補維修/客訴         🔴 待上 DGX Spark
Chat_bot_v1   ✅ 已上線              ✅ 持續服務            🔴 待上雲
Reporter_v1   ✅ 工具完成            持續使用                持續使用
```

---

## Sample 520

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告.md` L491

```
DGX Spark（產線機房，Air-Gapped）
├─ Ollama LLM Runtime
│   ├─ Full 72B (Q4) ~42GB  → diagnose / schedule
│   └─ Fast 8B  (Q4) ~5GB   → dispatch / inventory / traffic
 │
├─ PKB v3 (本軸線交付)
│   ├─ Qdrant Docker (on_disk) ~4GB   ← 6 collections / 195 萬筆
│   ├─ Ollama bge-m3 ~2GB             ← 1024 維 embedding
│   └─ PKB API Server (FastAPI)       ← /kb/search /pkb/diagnose/search /pkb/sop/lookup
 │
├─ 監控與資料
│   ├─ InfluxDB ~2-3GB
│   └─ Grafana
 │
└─ AMHS 控制面
    ├─ MCS-Lite / TSC / EAP
    └─ MCP Servers
```

---

## Sample 521

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L105

```
週次   日期        里程碑                              對應專案
─────  ──────────  ──────────────────────────────────  ──────────────
W1     02-23       RAG 流水線概念驗證                  04 personal-rag
W2-3   03-03       向量索引建置規劃（plan）            07 Reporter_v0
W2-3   03-04~10    多模態 KB + Web Chat                05 personal-rag_v1
W4     03-04~09    LINE Bot + Function Calling         02 Line_bot_v0
W4     03-06       Caddy 整合架構（Phase 0）           03 LineBot_Reporter_v1
W5-6   03-25~04-02 PKB v2.0 三階段架構成形             06 personal-rag_v2
W6     03-27~30    Google Chat Bot 上線               01 Chat_bot_v1
W6     03-30       GYRO PPTX 報告生成器                08 Reporter_v1
```

---

## Sample 522

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L235

```
   ┌───────────────────────────────────────────────────────┐
   │           Support Agent 軸線完整交付鏈                │
   │                                                       │
   │   全員 ──→ Chat_bot_v1 (Google Chat /kb)             │
   │              ↓                                       │
   │           PKB v2.0 (Qdrant + Ollama bge-m3)           │
   │              ↑                                       │
   │   AMHS ──→ diagnose Skill (Full 72B + PKB)           │
   │              ↓                                       │
   │           Reporter_v1 (Markdown → GYRO PPTX)         │
   └───────────────────────────────────────────────────────┘
```

---

## Sample 523

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\00_GYRO_AI_AMHS_Support_Agent_整合報告_elk.md` L376

```
              Phase 1 (工具)        Phase 2 (顧問)         Phase 3 (自主)
              ─────────────         ─────────────          ─────────────
PKB 需求      不阻塞                diagnose 需 PKB         高可用 + 低延遲
PKB 狀態      ✅ 後端就緒           🟡 待補維修/客訴         🔴 待上 DGX Spark
Chat_bot_v1   ✅ 已上線              ✅ 持續服務            🔴 待上雲
Reporter_v1   ✅ 工具完成            持續使用                持續使用
```

---

## Sample 524

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\AI全面導入計畫_2026.md` L122

```
MES (e.g. Applied Materials)
  ↓ SECS/GEM
RTD (Real-Time Dispatch)
  ↓
MCS / MCS Lite (Material Control System)
  ├→ TSC (Traffic System Controller) → AMR Fleet
  ├→ Stocker Controller → Stocker
  ├→ E-Rack Controller → E-Rack
  ├→ Sorter
  └→ EAP (Equipment Automation Program) → Load Port (E84)
```

---

## Sample 525

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書.md` L26

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

## Sample 526

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書.md` L223

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

## Sample 527

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書.md` L263

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）
```

---

## Sample 528

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書.md` L437

```
Claude Code 開發 Skill + MCP Server + Bridge
 │
  ▼
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP → API 連接、查詢準確率
 │
  ▼
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite→InfluxDB 同步
 │
  ▼
DGX Spark 產線部署 ──── Phase 1 → 2 → 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  ▼
Production（24/7 離線運行）
```

---

## Sample 529

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書_elk.md` L26

```
MES (e.g. Applied Materials)
  │ SECS/GEM (E82+/E88) or WebAPI
  ▼
RTD ── GYRO GTCS（即時派工引擎）
  │ WebAPI (W1001-W1003)
  ▼
MCS-Lite ─────────────────────────────── EAP Server (SECS/GEM to EQ)
  │ 整合 AGVC + eRackC + StockerC        │ W3001-W3002
  │                                       ▼
  ├→ AGVC ──→ AMR Fleet（專有協議）     Load Port（E84 PIO）
  ├→ eRackC ─→ E-Rack（TCP/IP）
  ├→ StockerC → Stocker（Socket IO）
  └→ Sorter
```

---

## Sample 530

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書_elk.md` L223

```
① 設備即時資料
   ROS topics / API poll ──→ Bridge ──→ Edge SQLite (synced=0)

② 正常同步
   Bridge 背景執行緒 → SELECT synced=0 LIMIT 1000 → push Server InfluxDB → UPDATE synced=1

③ 斷線時
   Bridge 繼續寫 SQLite（synced=0 累積）
   Tiny Agent 讀本地 SQLite 做 L1 收尾 + 停靠

④ 重連
   背景執行緒掃 synced=0 → batch push 回補 → Server 時間軸完整

⑤ 現場除錯（臨時）
   NB 同步小工具 ←── Edge SQLite → NB InfluxDB + Grafana
```

---

## Sample 531

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書_elk.md` L263

```
Skill 內部 ──→ MCP Servers ──→ 現在（即時狀態 + 指令）
           ──→ InfluxDB    ──→ 過去（歷史趨勢 + 事件回溯）
           ──→ Qdrant/PKB  ──→ 知識（維修經驗 + SOP）
```

---

## Sample 532

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\GYRO\GYRO_AI_AMHS_技術白皮書_elk.md` L437

```
Claude Code 開發 Skill + MCP Server + Bridge
 │
  ▼
Gemini API 雲端試驗 ─── 驗證 Skill 邏輯、MCP → API 連接、查詢準確率
 │
  ▼
Ollama 本地測試 ─────── 驗證本地 model 推理品質、延遲、SQLite→InfluxDB 同步
 │
  ▼
DGX Spark 產線部署 ──── Phase 1 → 2 → 3 逐步開放
  │                     Phase 1–2：直接 API 呼叫
  │                     Phase 3：採用 LangGraph 管理多步 workflow / state
  ▼
Production（24/7 離線運行）
```

---

## Sample 533

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TEACH\UNIFIED_UI_TM_TEACH_PLAN.md` L33

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
|  ├─ HID 事件 → 抽象 intent 事件     |---------------------+
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
|  DomainAPI + Jog RPCs (§4 待 TM 實作)|
+--------------------------------------+
```

---

## Sample 534

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TEACH\UNIFIED_UI_TM_TEACH_PLAN.md` L80

```
使用者在統一 UI 按「存點」
  ├─ (1) gRPC SavePointFromCurrent / UpdatePointPartial → TMflow 專案檔
  └─ (2) 同步更新 GYRO YAML 對應 waypoint → Git commit (optional hook)
```

---

## Sample 535

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TEACH\UNIFIED_UI_TM_TEACH_PLAN.md` L206

```
tmflow_domain_client/
├─ proto/
│  └─ TmDomainService.proto          # 從 TM release 拷貝
├─ _generated/                        # grpc_tools.protoc 產出
│  ├─ TmDomainService_pb2.py
│  └─ TmDomainService_pb2_grpc.py
├─ client.py                          # Channel / stub 管理
├─ session.py                         # TeachSession context manager
├─ teach.py                           # 高階 helpers (jog_cartesian, save_point, ...)
├─ models.py                          # dataclass 對應 proto message
└─ tests/
   ├─ test_with_mock_server.py        # 用 grpcio testing 起 mock server
   └─ test_integration.py             # 需連真機，gated by env var
```

---

## Sample 536

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TEACH\UNIFIED_UI_TM_TEACH_PLAN.md` L256

```
hid_input/
├─ backends/
│  ├─ pygame_backend.py         # Windows/macOS/Linux 通用（搖桿、手把）
│  ├─ hidapi_backend.py         # 底層 HID（自製裝置、SpaceMouse）
│  └─ evdev_backend.py          # Linux-only，低延遲踏板
├─ profiles/                    # YAML profile 目錄（使用者可擴充）
│  ├─ xbox_dual_analog.yaml
│  ├─ spacemouse_compact.yaml
│  ├─ linemaster_3pedal.yaml
│  └─ schema.json               # profile 語法驗證
├─ intents.py                   # intent 事件 dataclass 定義
├─ translator.py                # HID event → intent (profile-driven)
├─ dispatcher.py                # intent → 統一 UI event bus
├─ watchdog.py                  # 連續 jog safety watchdog
└─ tests/
   ├─ test_profile_loader.py
   ├─ test_translator.py        # 用錄製的 HID event 檔重播
   └─ test_watchdog.py
```

---

## Sample 537

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TM_UR\04_UR_Program_Analysis_v0.md` L47

```
├── src/
│   ├── ur_script_parser.py       # URScript 解析器
│   ├── ur_tree_parser.py         # 樹狀結構解析
│   ├── ur_project_loader.py      # 專案載入器
│   ├── ur_flow_analyzer.py       # Flow 分析
│   ├── ur_doc_generator.py       # 文件自動產生
│   ├── ur_analyze.py             # CLI 主程式
│   ├── ur_flow_editor.py         # 語意級腳本編輯（Phase 2）
│   ├── ur_flow_simplifier.py     # 跨檔案重複偵測（Phase 2）
│   ├── ur30_kinematics.py        # FK 驗證 + Rodrigues（Phase 2）
│   ├── ur_script_editor.py
│   ├── ur_script_simplifier.py
│   ├── test_core.py              # 31 個測試
│   ├── test_phase2.py            # 15 個測試
│   └── test_refactor.py
├── K11_UR30_Project/programs/    # UR 程式原始檔（160+ 檔案）
├── output/                       # 自動產生的 82 份分析文件
├── docs/                         # 手動撰寫的分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   ├── PHASE2_SPEC.md
│   └── gRPC/                    # GYRO gRPC 整合資料
└── archive/                      # UR 匯出壓縮
```

---

## Sample 538

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TM_UR\07_TM-Program-Analysis-v0.md` L50

```
├── src/
│   ├── tm_flow_parser.py          # .flow 格式解析器
│   ├── tm_flow_analyzer.py        # Flow 分析
│   ├── tm_doc_generator.py        # 文件自動產生
│   ├── tm_analyze.py              # CLI 主程式
│   ├── tm_vision_analyzer.py      # 68 Vision Job XML 分析
│   ├── tm12_kinematics.py         # FK/IK 運動學
│   ├── tm_flow_editor.py          # MutableFlowDocument 語意編輯（Phase 2）
│   ├── tm_flow_simplifier.py      # 重複鏈偵測（Phase 2）
│   └── test_core.py               # 34 個測試
├── output/                        # 49 份自動產生分析文件
│   ├── INDEX.md
│   ├── MainFlow.md
│   ├── SUBFLOW_CALL_GRAPH.md
│   ├── VARIABLE_USAGE_MAP.md
│   ├── VISION_JOB_MAP.md
│   ├── VISION_SYSTEM_ANALYSIS.md
│   ├── DUPLICATE_ANALYSIS.md
│   ├── subflows/（37 個）
│   └── threads/（5 個）
├── docs/                          # 手動分析文件
│   ├── FLOW_ANALYSIS.md
│   ├── ERROR_CODE_REFERENCE.md
│   ├── POINT_DATA.md
│   └── HT_9046LS / MR_PORT 深度分析
├── data/                          # TM 解壓資料
├── archive/                       # TM 匯出壓縮
└── reviews/                       # 審核報告
```

---

## Sample 539

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TM_UR\TM_UR_COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 540

**Source**: `Reporter_v1\WORKSPACE\a06\.DOC\TM_UR\TM_UR_COMPLETED_SUMMARY_elk.md` L319

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 541

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_Architecture.md` L56

```
┌──────────────────────────────────────────────────────────────┐
│                    Unified Web / HMI UI                      │
│   (React/Vue)  設定 · 操作 · 監控 · 教導 · 模擬              │
├──────────────────────────────────────────────────────────────┤
│                  gRPC Gateway (Proto3)                       │
│   統一 API 層 — 平台無關的操作語意                          │
├──────────────────────┬───────────────────────────────────────┤
│   Module A           │   Module B                            │
│   GYRO 解析層        │   硬體即時通訊層                      │
│   (離線 / 設定)      │   (線上 / 操控)                       │
│                      │                                       │
│   ┌─ DSL Engine ──┐  │   ┌─ Protocol Adapters ───────────┐   │
│   │ GYRO-DSL      │  │   │ UR:  RTDE + Modbus TCP        │   │
│   │ GYRO-Compiler │  │   │ TM:  Modbus TCP + EtherCAT    │   │
│   └───────────────┘  │   │ AMR: ROS2 Action/Topic        │   │
│                      │   │ 人型: ROS2 + MoveIt2 + MCP    │   │
│   ┌─ Platform ─────┐ │   └───────────────────────────────┘   │
│   │ Parsers        │ │                                       │
│   │ TM: flow_parser│ │   ┌─ Safety Layer ────────────────┐   │
│   │ UR: script_    │ │   │ 碰撞偵測 · 力矩限制 · E-Stop  │   │
│   │     parser     │ │   │ 安全區域 · 速度限制           │   │
│   │ Editors        │ │   └───────────────────────────────┘   │
│   │ Kinematics     │ │                                       │
│   └────────────────┘ │                                       │
├──────────────────────┴───────────────────────────────────────┤
│              Data Layer (Git + DB)                           │
│   task.gyro.yaml (唯一真實來源) · SQLite logs · Prometheus   │
└──────────────────────────────────────────────────────────────┘
```

---

## Sample 542

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_Architecture.md` L224

```
RobotAdapter
├── URAdapter          (單臂 — UR30)
├── TMAdapter          (單臂 — TM12/TM14M)
├── AMRAdapter         (移動平台 — AMRA04/AMRW)
│   └── nav2_client    (ROS2 Action)
├── DualArmAdapter     (雙臂組合)
│   ├── left: TMAdapter
│   ├── right: TMAdapter
│   └── coordinator: DualArmCoordinator
└── TriArmAdapter      (三臂組合)
    ├── arms: [TMAdapter, TMAdapter, URAdapter]
    └── coordinator: TriArmCoordinator
```

---

## Sample 543

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_投資人版.md` L25

```
                    ┌────────────────────────────┐
                    │   統一 Web / HMI 介面     │  ← 一個介面操控所有機器人
                    └────────────┬───────────────┘
                                 │ gRPC
                    ┌────────────┴───────────────┐
                    │    GYRO 中間件伺服器       │  ← 自主研發核心
                    │  ┌────────┐ ┌───────────┐  │
                    │  │解析引擎│ │即時通訊層 │  │
                    │  │DSL     │ │協議轉換   │  │
                    │  └────────┘ └───────────┘  │
                    └──┬─────┬─────┬─────┬───────┘
                       │     │     │             │
                      TM    UR   AMR   人型       ← 插件式擴展
```

---

## Sample 544

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_投資人版.md` L76

```
2026 H2              2027                 2028
┌──────────┐    ┌──────────────┐    ┌───────────────┐
│ Phase 3  │    │   Phase 4    │    │   Phase 5     │
│          │    │              │    │               │
│ 統一     │──→ │ 多臂 + AMR  │──→ │ 人型機器人   │
│ TM / UR  │    │ 車隊管理     │    │ AI 自主       │
│ 介面     │    │              │    │               │
│          │    │              │    │               │
│ 營收起點 │    │ 規模化       │    │ 願景市場      │
└──────────┘    └──────────────┘    └───────────────┘
```

---

## Sample 545

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L9

```
                        MainFlow (113 節點)
                             │
          ┌──────────┬───────┴───────┬───────────┐
          │          │               │           │
    37 SubFlow   5 MultiThread  68 Vision   244 變數
          │          │               Job    370 點位
          │          │
  ┌───────┴───────┐  ├─ CHECK_ALL_SENSOR_WHEN_CAR_MOVING
  │ MR_PORT_PLACE │  ├─ CHECK_ENCODER
  │  (423 節點)   │  ├─ CHECK_GRIP
  │               │  ├─ Pause_handle
  │ HT_9046LS_    │  └─ Pub_RS485IO
  │ TMMARK_NORMAL │
  │  (259 節點)   │
  └───────────────┘

  設計哲學：模組化 · 數據驅動 · 主人模式（主動 Modbus 監聽自主決策）
```

---

## Sample 546

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L31

```
            initial_prog.script (12,241 行 / 1,341 moves)
                              │
       ┌──────────┬───────────┼───────────┬───────────────┐
       │          │           │           │               │
   73 程式     719 點位    Modbus TCP   SensoPart   RS485
   64,503 行  (unique 321)  /RTU        VISOR

   ┌──────────────────────────────────────────────────────┐
   │ 設備群組程式分佈                                     │
   ├──────────┬───────┬───────────────────────────────────┤
   │ Body     │  3 支 │ Body_take_put (4,145行/405 moves) │
   │ EQ2600   │  7 支 │ port load/unload                  │
   │ EQ2800   │ 14 支 │ port swap                         │
   │ EQ3670   │  4 支 │ 最大 6,870行/651 moves            │
   │ Erack    │  7 支 │ load/unload                       │
   │ Gyro_util│ 20 支 │ initial_prog 主控                 │
   └──────────┴───────┴───────────────────────────────────┘

  設計哲學：巨石腳本 · 指令驅動 · 僕人模式（被動等 PLC RTDE 指令）
```

---

## Sample 547

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L69

```
  ┌───────────────────────────────────────────────────────────────────┐
  │                    兩套工具鏈（各 80% 完成）                      │
  │                                                                   │
  │   TM 工具鏈 (8 模組 · 4,003 行)    UR 工具鏈 (11 模組 · 3,629 行) │
  │                                                                   │
  │   .flow XML ──→ Parser ──→ Analyzer ──→ Doc Generator          │
  │       ↑                                      │                   │
  │       └──── Editor (MutableFlowDocument) ←───┘                   │
  │              Simplifier (重複偵測)                                │
  │              Kinematics (FK/IK)                                   │
  │                                                                   │
  │   .script ──→ Parser ──→ Loader ──→ Analyzer ──→ Doc Gen      │
  │       ↑                                           │              │
  │       └──── Editor (ScriptEditor) ←───────────────┘              │
  │              Simplifier (跨檔重複)                                │
  │              Kinematics (FK/IK)                                   │
  └───────────────────────────────────────────────────────────────────┘

  已自動產出：50+ 份 TM 分析文件 ｜ 81+ 份 UR 分析文件
  測試覆蓋：  34 tests (TM)      ｜ 46 tests (UR)
  FK/IK：    TM12 DH 驗證通過    ｜ UR30 DH 驗證通過
```

---

## Sample 548

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L97

```
  現 況                                              目 標

  TM → TMFlow (原廠)                    ┌──────────────────────────┐
  UR → PolyScope (原廠)      ────→     │  GYRO 統一操控平台       │
  AMR → ROS (自研)                      │  一個介面 · 所有機器人   │
  每案重寫控制邏輯                       └──────────────────────────┘
```

---

## Sample 549

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L110

```
┌───────────────────────────────────────────────────────────────┐
│               統一 Web / HMI 操作介面                         │
│   監控 · 點位管理 · 程式編輯 · 3D 視覺化 · 搖桿教點           │
├───────────────────────────────────────────────────────────────┤
│                    gRPC 統一 API 層                           │
├─────────────────────────┬─────────────────────────────────────┤
│     解析引擎            │          即時通訊層                 │
│                         │                                     │
│   GYRO-DSL 編譯器       │    TM  ← Modbus / EtherCAT         │
│   程式解析/編輯         │    UR  ← RTDE / Modbus             │
│   自動重構              │    AMR ← ROS2                      │
│   運動學 FK/IK          │    人型 ← ROS2 + MoveIt2           │
├─────────────────────────┴─────────────────────────────────────┤
│            資料層：GYRO-DSL 設定檔 (Git 版控)                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Sample 550

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L134

```
  痛點                                    解法

  TMflow 原廠 Jog Panel                  統一 UI + 外接 HID
  ┌──────────────────────┐                 ┌───────────────────────────┐
  │ 按鈕小、手離工件     │                 │ 手不離工件 · 眼不離對準   │
  │ 視線在螢幕↔工件切換 │     ────→      │                           │
  │ 每次教點：點滑鼠     │                 │ 搖桿 / SpaceMouse / 踏板  │
  │ 效率低、易出錯       │                 │ 教點速度提升 30%+         │
  └──────────────────────┘                 └───────────────────────────┘

  支援裝置：
  ┌───────────────┬──────────────────┬──────────────────┬───────────────┐
  │ Xbox/DualShock│ 3Dconnexion      │ 三踏板腳踏開關   │ 自製 HID      │
  │ 雙類比搖桿    │ SpaceMouse       │                  │ 面板          │
  ├───────────────┼──────────────────┼──────────────────┼───────────────┤
  │ 左桿=平移     │ 6-DOF 連續 Jog   │ Deadman          │ Teensy/QMK    │
  │ 右桿=旋轉     │ 最直覺           │ FreeDrive 切換   │ 完全自定義    │
  │ D-pad=Step    │                  │ 一鍵存點         │               │
  │ 按鈕=存點     │                  │                  │               │
  └───────────────┴──────────────────┴──────────────────┴───────────────┘

  教點工作流：
  ① Free Drive 粗定位 → ② Step Jog 精調 (0.1mm) → ③ 一鍵存點
  → ④ 閉環視覺校正 (≤0.05mm) → ⑤ 自動同步 GYRO YAML + Git
```

---

## Sample 551

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L163

```
  task.gyro.yaml (平台無關)
  ┌───────────────────────────────────────────────────────────────────────┐
  │ waypoints:              │                                             │
  │   pick_pos: [x,y,z,r]   │       GYRO-Compiler                         │
  │ sequences:              │      ┌──────────────┐                       │
  │   pick_and_place:       │────→│ --target=tm  │──→ .flow (TM 原生)   │
  │     - move_linear: pick │      │ --target=ur  │──→ .script (UR 原生) │
  │     - gripper: close    │      └──────────────┘                       │
  │     - move_linear: place│                                             │
  │     - gripper: open     │  Git 版控 · 可 diff · 可 review             │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## Sample 552

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L179

```
  ① 粗定位（手動/搖桿）
        │
       ▼
  ② 高解析相機拍照
        │
       ▼
  ③ 計算偏差 dX / dY / dR
        │
       ▼
  ④ 自動補償運動         ←── 重複直到 delta ≤ 容差
        │
       ▼
  ⑤ 最終作業 (精度 ≤ 0.05mm)
```

---

## Sample 553

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L197

```
  傳統模式                          Swap 模式
  ┌─────┐   空跑   ┌─────┐       ┌──────┐  同時取放   ┌───────┐
  │ 放A │ ──────→ │ 取B │       │取B放A│ ────────→  │取A放B │
  └─────┘          └─────┘       └──────┘             └───────┘
  2 趟 = 2 個停靠週期               1 趟 = 1 個停靠週期
                                   產量 ~18 moves/hr/AMR
```

---

## Sample 554

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L208

```
  現有程式                    自動分析                   一鍵簡化
  ┌───────────┐              ┌───────────┐             ┌───────────┐
  │ 452 chains│    ────→    │ 偵測 2,021│    ────→   │ 70 個     │
  │ 重複邏輯  │   Simplifier │ 處重複    │    apply    │ 簡化方案  │
  └───────────┘              └───────────┘             └───────────┘
```

---

## Sample 555

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L236

```
2026 H2                    2027                      2028
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 ┏━━━━━━━━━━━━━━━┓
 ┃   Phase 3     ┃
 ┃   統一 TM/UR  ┃    ┏━━━━━━━━━━━━━━━━━━━┓
 ┃               ┃──→┃   Phase 4         ┃
 ┃ · 跨品牌監控  ┃    ┃   多臂 + AMR      ┃    ┏━━━━━━━━━━━━━━━━━┓
 ┃ · 搖桿教點    ┃    ┃                   ┃──→┃   Phase 5       ┃
 ┃ · 程式編輯    ┃    ┃ · 雙臂/三臂協調   ┃    ┃   人型機器人    ┃
 ┃ · DSL v1      ┃    ┃ · AMR 車隊地圖    ┃    ┃                 ┃
 ┃ · 視覺校正    ┃    ┃ · MCS-Lite 整合   ┃    ┃ · 全身控制      ┃
 ┗━━━━━━━━━━━━━━━┛    ┃ · DSL 多臂語法    ┃    ┃ · 步態/平衡     ┃
                      ┗━━━━━━━━━━━━━━━━━━━┛    ┃ · AI 動作生成   ┃
                                               ┃ · Digital Twin  ┃
                                               ┃ · 語音指令      ┃
                                               ┗━━━━━━━━━━━━━━━━━┛
```

---

## Sample 556

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L273

```
  Phase 3                    Phase 4                     Phase 5
  單臂                       多臂 + 移動平台              全身

  ┌────────┐          ┌──────────────────┐         ┌───────────────┐
  │ TM     │          │  DualArm         │         │ Humanoid      │
  │ Adapter│─┐        │  ├ left: TM      │         │ ├ left_arm    │
  └────────┘ │        │  ├ right: TM     │         │ ├ right_arm   │
             ├──共用→│  └ coordinator   │──共用─→│ ├ legs        │
  ┌────────┐ │  介面  ├──────────────────┤  介面   │ ├ torso       │
  │ UR     │─┘        │  AMR             │         │ └ AI policy   │
  │ Adapter│          │  └ ROS2 nav2     │         └───────────────┘
  └────────┘          └──────────────────┘
                       TriArm
                       ├ arm1: TM
                       ├ arm2: TM
                       └ arm3: UR

  關鍵：手臂的 Adapter 介面從 Phase 3 到 Phase 5 完全複用
```

---

## Sample 557

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版.md` L298

```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
  │  降低成本    │  │  加速交付    │  │  精度提升    │  │  戰略卡位  │
  │              │  │              │  │              │  │            │
  │  一套介面    │  │  DSL 寫一次  │  │  搖桿教點    │  │  自有軟體  │
  │  取代多套    │  │  編譯到      │  │  + 閉環視覺  │  │  平台公司  │
  │  原廠軟體    │  │  任何平台    │  │  ≤ 0.05mm    │  │            │
  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘
```

---

## Sample 558

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L9

```
                        MainFlow (113 節點)
                             │
          ┌──────────┬───────┴───────┬───────────┐
          │          │               │           │
    37 SubFlow   5 MultiThread  68 Vision   244 變數
          │          │               Job    370 點位
          │          │
  ┌───────┴───────┐  ├─ CHECK_ALL_SENSOR_WHEN_CAR_MOVING
  │ MR_PORT_PLACE │  ├─ CHECK_ENCODER
  │  (423 節點)   │  ├─ CHECK_GRIP
  │               │  ├─ Pause_handle
  │ HT_9046LS_    │  └─ Pub_RS485IO
  │ TMMARK_NORMAL │
  │  (259 節點)   │
  └───────────────┘

  設計哲學：模組化 · 數據驅動 · 主人模式（主動 Modbus 監聽自主決策）
```

---

## Sample 559

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L31

```
            initial_prog.script (12,241 行 / 1,341 moves)
                              │
       ┌──────────┬───────────┼───────────┬───────────────┐
       │          │           │           │               │
   73 程式     719 點位    Modbus TCP   SensoPart   RS485
   64,503 行  (unique 321)  /RTU        VISOR

   ┌──────────────────────────────────────────────────────┐
   │ 設備群組程式分佈                                     │
   ├──────────┬───────┬───────────────────────────────────┤
   │ Body     │  3 支 │ Body_take_put (4,145行/405 moves) │
   │ EQ2600   │  7 支 │ port load/unload                  │
   │ EQ2800   │ 14 支 │ port swap                         │
   │ EQ3670   │  4 支 │ 最大 6,870行/651 moves            │
   │ Erack    │  7 支 │ load/unload                       │
   │ Gyro_util│ 20 支 │ initial_prog 主控                 │
   └──────────┴───────┴───────────────────────────────────┘

  設計哲學：巨石腳本 · 指令驅動 · 僕人模式（被動等 PLC RTDE 指令）
```

---

## Sample 560

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L69

```
  ┌───────────────────────────────────────────────────────────────────┐
  │                    兩套工具鏈（各 80% 完成）                      │
  │                                                                   │
  │   TM 工具鏈 (8 模組 · 4,003 行)    UR 工具鏈 (11 模組 · 3,629 行) │
  │                                                                   │
  │   .flow XML ──→ Parser ──→ Analyzer ──→ Doc Generator          │
  │       ↑                                      │                   │
  │       └──── Editor (MutableFlowDocument) ←───┘                   │
  │              Simplifier (重複偵測)                                │
  │              Kinematics (FK/IK)                                   │
  │                                                                   │
  │   .script ──→ Parser ──→ Loader ──→ Analyzer ──→ Doc Gen      │
  │       ↑                                           │              │
  │       └──── Editor (ScriptEditor) ←───────────────┘              │
  │              Simplifier (跨檔重複)                                │
  │              Kinematics (FK/IK)                                   │
  └───────────────────────────────────────────────────────────────────┘

  已自動產出：50+ 份 TM 分析文件 ｜ 81+ 份 UR 分析文件
  測試覆蓋：  34 tests (TM)      ｜ 46 tests (UR)
  FK/IK：    TM12 DH 驗證通過    ｜ UR30 DH 驗證通過
```

---

## Sample 561

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L97

```
  現 況                                              目 標

  TM → TMFlow (原廠)                    ┌──────────────────────────┐
  UR → PolyScope (原廠)      ────→     │  GYRO 統一操控平台       │
  AMR → ROS (自研)                      │  一個介面 · 所有機器人   │
  每案重寫控制邏輯                       └──────────────────────────┘
```

---

## Sample 562

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L110

```
┌───────────────────────────────────────────────────────────────┐
│               統一 Web / HMI 操作介面                         │
│   監控 · 點位管理 · 程式編輯 · 3D 視覺化 · 搖桿教點           │
├───────────────────────────────────────────────────────────────┤
│                    gRPC 統一 API 層                           │
├─────────────────────────┬─────────────────────────────────────┤
│     解析引擎            │          即時通訊層                 │
│                         │                                     │
│   GYRO-DSL 編譯器       │    TM  ← Modbus / EtherCAT         │
│   程式解析/編輯         │    UR  ← RTDE / Modbus             │
│   自動重構              │    AMR ← ROS2                      │
│   運動學 FK/IK          │    人型 ← ROS2 + MoveIt2           │
├─────────────────────────┴─────────────────────────────────────┤
│            資料層：GYRO-DSL 設定檔 (Git 版控)                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Sample 563

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L134

```
  痛點                                    解法

  TMflow 原廠 Jog Panel                  統一 UI + 外接 HID
  ┌──────────────────────┐                 ┌───────────────────────────┐
  │ 按鈕小、手離工件     │                 │ 手不離工件 · 眼不離對準   │
  │ 視線在螢幕↔工件切換 │     ────→      │                           │
  │ 每次教點：點滑鼠     │                 │ 搖桿 / SpaceMouse / 踏板  │
  │ 效率低、易出錯       │                 │ 教點速度提升 30%+         │
  └──────────────────────┘                 └───────────────────────────┘

  支援裝置：
  ┌───────────────┬──────────────────┬──────────────────┬───────────────┐
  │ Xbox/DualShock│ 3Dconnexion      │ 三踏板腳踏開關   │ 自製 HID      │
  │ 雙類比搖桿    │ SpaceMouse       │                  │ 面板          │
  ├───────────────┼──────────────────┼──────────────────┼───────────────┤
  │ 左桿=平移     │ 6-DOF 連續 Jog   │ Deadman          │ Teensy/QMK    │
  │ 右桿=旋轉     │ 最直覺           │ FreeDrive 切換   │ 完全自定義    │
  │ D-pad=Step    │                  │ 一鍵存點         │               │
  │ 按鈕=存點     │                  │                  │               │
  └───────────────┴──────────────────┴──────────────────┴───────────────┘

  教點工作流：
  ① Free Drive 粗定位 → ② Step Jog 精調 (0.1mm) → ③ 一鍵存點
  → ④ 閉環視覺校正 (≤0.05mm) → ⑤ 自動同步 GYRO YAML + Git
```

---

## Sample 564

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L163

```
  task.gyro.yaml (平台無關)
  ┌───────────────────────────────────────────────────────────────────────┐
  │ waypoints:              │                                             │
  │   pick_pos: [x,y,z,r]   │       GYRO-Compiler                         │
  │ sequences:              │      ┌──────────────┐                       │
  │   pick_and_place:       │────→│ --target=tm  │──→ .flow (TM 原生)   │
  │     - move_linear: pick │      │ --target=ur  │──→ .script (UR 原生) │
  │     - gripper: close    │      └──────────────┘                       │
  │     - move_linear: place│                                             │
  │     - gripper: open     │  Git 版控 · 可 diff · 可 review             │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## Sample 565

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L179

```
  ① 粗定位（手動/搖桿）
        │
       ▼
  ② 高解析相機拍照
        │
       ▼
  ③ 計算偏差 dX / dY / dR
        │
       ▼
  ④ 自動補償運動         ←── 重複直到 delta ≤ 容差
        │
       ▼
  ⑤ 最終作業 (精度 ≤ 0.05mm)
```

---

## Sample 566

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L197

```
  傳統模式                          Swap 模式
  ┌─────┐   空跑   ┌─────┐       ┌──────┐  同時取放   ┌───────┐
  │ 放A │ ──────→ │ 取B │       │取B放A│ ────────→  │取A放B │
  └─────┘          └─────┘       └──────┘             └───────┘
  2 趟 = 2 個停靠週期               1 趟 = 1 個停靠週期
                                   產量 ~18 moves/hr/AMR
```

---

## Sample 567

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L208

```
  現有程式                    自動分析                   一鍵簡化
  ┌───────────┐              ┌───────────┐             ┌───────────┐
  │ 452 chains│    ────→    │ 偵測 2,021│    ────→   │ 70 個     │
  │ 重複邏輯  │   Simplifier │ 處重複    │    apply    │ 簡化方案  │
  └───────────┘              └───────────┘             └───────────┘
```

---

## Sample 568

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L236

```
2026 H2                    2027                      2028
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 ┏━━━━━━━━━━━━━━━┓
 ┃   Phase 3     ┃
 ┃   統一 TM/UR  ┃    ┏━━━━━━━━━━━━━━━━━━━┓
 ┃               ┃──→┃   Phase 4         ┃
 ┃ · 跨品牌監控  ┃    ┃   多臂 + AMR      ┃    ┏━━━━━━━━━━━━━━━━━┓
 ┃ · 搖桿教點    ┃    ┃                   ┃──→┃   Phase 5       ┃
 ┃ · 程式編輯    ┃    ┃ · 雙臂/三臂協調   ┃    ┃   人型機器人    ┃
 ┃ · DSL v1      ┃    ┃ · AMR 車隊地圖    ┃    ┃                 ┃
 ┃ · 視覺校正    ┃    ┃ · MCS-Lite 整合   ┃    ┃ · 全身控制      ┃
 ┗━━━━━━━━━━━━━━━┛    ┃ · DSL 多臂語法    ┃    ┃ · 步態/平衡     ┃
                      ┗━━━━━━━━━━━━━━━━━━━┛    ┃ · AI 動作生成   ┃
                                               ┃ · Digital Twin  ┃
                                               ┃ · 語音指令      ┃
                                               ┗━━━━━━━━━━━━━━━━━┛
```

---

## Sample 569

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L273

```
  Phase 3                    Phase 4                     Phase 5
  單臂                       多臂 + 移動平台              全身

  ┌────────┐          ┌──────────────────┐         ┌───────────────┐
  │ TM     │          │  DualArm         │         │ Humanoid      │
  │ Adapter│─┐        │  ├ left: TM      │         │ ├ left_arm    │
  └────────┘ │        │  ├ right: TM     │         │ ├ right_arm   │
             ├──共用→│  └ coordinator   │──共用─→│ ├ legs        │
  ┌────────┐ │  介面  ├──────────────────┤  介面   │ ├ torso       │
  │ UR     │─┘        │  AMR             │         │ └ AI policy   │
  │ Adapter│          │  └ ROS2 nav2     │         └───────────────┘
  └────────┘          └──────────────────┘
                       TriArm
                       ├ arm1: TM
                       ├ arm2: TM
                       └ arm3: UR

  關鍵：手臂的 Adapter 介面從 Phase 3 到 Phase 5 完全複用
```

---

## Sample 570

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_0.md` L298

```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
  │  降低成本    │  │  加速交付    │  │  精度提升    │  │  戰略卡位  │
  │              │  │              │  │              │  │            │
  │  一套介面    │  │  DSL 寫一次  │  │  搖桿教點    │  │  自有軟體  │
  │  取代多套    │  │  編譯到      │  │  + 閉環視覺  │  │  平台公司  │
  │  原廠軟體    │  │  任何平台    │  │  ≤ 0.05mm    │  │            │
  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘
```

---

## Sample 571

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L9

```
                        MainFlow (113 節點)
                             │
          ┌──────────┬───────┴───────┬───────────┐
          │          │               │           │
    37 SubFlow   5 MultiThread  68 Vision   244 變數
          │          │               Job    370 點位
          │          │
  ┌───────┴───────┐  ├─ CHECK_ALL_SENSOR_WHEN_CAR_MOVING
  │ MR_PORT_PLACE │  ├─ CHECK_ENCODER
  │  (423 節點)   │  ├─ CHECK_GRIP
  │               │  ├─ Pause_handle
  │ HT_9046LS_    │  └─ Pub_RS485IO
  │ TMMARK_NORMAL │
  │  (259 節點)   │
  └───────────────┘

  設計哲學：模組化 · 數據驅動 · 主人模式（主動 Modbus 監聽自主決策）
```

---

## Sample 572

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L31

```
            initial_prog.script (12,241 行 / 1,341 moves)
                              │
       ┌──────────┬───────────┼───────────┬───────────────┐
       │          │           │           │               │
   73 程式     719 點位    Modbus TCP   SensoPart   RS485
   64,503 行  (unique 321)  /RTU        VISOR

   ┌──────────────────────────────────────────────────────┐
   │ 設備群組程式分佈                                     │
   ├──────────┬───────┬───────────────────────────────────┤
   │ Body     │  3 支 │ Body_take_put (4,145行/405 moves) │
   │ EQ2600   │  7 支 │ port load/unload                  │
   │ EQ2800   │ 14 支 │ port swap                         │
   │ EQ3670   │  4 支 │ 最大 6,870行/651 moves            │
   │ Erack    │  7 支 │ load/unload                       │
   │ Gyro_util│ 20 支 │ initial_prog 主控                 │
   └──────────┴───────┴───────────────────────────────────┘

  設計哲學：巨石腳本 · 指令驅動 · 僕人模式（被動等 PLC RTDE 指令）
```

---

## Sample 573

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L69

```
  ┌───────────────────────────────────────────────────────────────────┐
  │                    兩套工具鏈（各 80% 完成）                      │
  │                                                                   │
  │   TM 工具鏈 (8 模組 · 4,003 行)    UR 工具鏈 (11 模組 · 3,629 行) │
  │                                                                   │
  │   .flow XML ──→ Parser ──→ Analyzer ──→ Doc Generator          │
  │       ↑                                      │                   │
  │       └──── Editor (MutableFlowDocument) ←───┘                   │
  │              Simplifier (重複偵測)                                │
  │              Kinematics (FK/IK)                                   │
  │                                                                   │
  │   .script ──→ Parser ──→ Loader ──→ Analyzer ──→ Doc Gen      │
  │       ↑                                           │              │
  │       └──── Editor (ScriptEditor) ←───────────────┘              │
  │              Simplifier (跨檔重複)                                │
  │              Kinematics (FK/IK)                                   │
  └───────────────────────────────────────────────────────────────────┘

  已自動產出：50+ 份 TM 分析文件 ｜ 81+ 份 UR 分析文件
  測試覆蓋：  34 tests (TM)      ｜ 46 tests (UR)
  FK/IK：    TM12 DH 驗證通過    ｜ UR30 DH 驗證通過
```

---

## Sample 574

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L97

```
  現 況                                              目 標

  TM → TMFlow (原廠)                    ┌──────────────────────────┐
  UR → PolyScope (原廠)      ────→     │  GYRO 統一操控平台       │
  AMR → ROS (自研)                      │  一個介面 · 所有機器人   │
  每案重寫控制邏輯                       └──────────────────────────┘
```

---

## Sample 575

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L110

```
┌───────────────────────────────────────────────────────────────┐
│               統一 Web / HMI 操作介面                         │
│   監控 · 點位管理 · 程式編輯 · 3D 視覺化 · 搖桿教點           │
├───────────────────────────────────────────────────────────────┤
│                    gRPC 統一 API 層                           │
├─────────────────────────┬─────────────────────────────────────┤
│     解析引擎            │          即時通訊層                 │
│                         │                                     │
│   GYRO-DSL 編譯器       │    TM  ← Modbus / EtherCAT         │
│   程式解析/編輯         │    UR  ← RTDE / Modbus             │
│   自動重構              │    AMR ← ROS2                      │
│   運動學 FK/IK          │    人型 ← ROS2 + MoveIt2           │
├─────────────────────────┴─────────────────────────────────────┤
│            資料層：GYRO-DSL 設定檔 (Git 版控)                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Sample 576

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L134

```
  痛點                                    解法

  TMflow 原廠 Jog Panel                  統一 UI + 外接 HID
  ┌──────────────────────┐                 ┌───────────────────────────┐
  │ 按鈕小、手離工件     │                 │ 手不離工件 · 眼不離對準   │
  │ 視線在螢幕↔工件切換 │     ────→      │                           │
  │ 每次教點：點滑鼠     │                 │ 搖桿 / SpaceMouse / 踏板  │
  │ 效率低、易出錯       │                 │ 教點速度提升 30%+         │
  └──────────────────────┘                 └───────────────────────────┘

  支援裝置：
  ┌───────────────┬──────────────────┬──────────────────┬───────────────┐
  │ Xbox/DualShock│ 3Dconnexion      │ 三踏板腳踏開關   │ 自製 HID      │
  │ 雙類比搖桿    │ SpaceMouse       │                  │ 面板          │
  ├───────────────┼──────────────────┼──────────────────┼───────────────┤
  │ 左桿=平移     │ 6-DOF 連續 Jog   │ Deadman          │ Teensy/QMK    │
  │ 右桿=旋轉     │ 最直覺           │ FreeDrive 切換   │ 完全自定義    │
  │ D-pad=Step    │                  │ 一鍵存點         │               │
  │ 按鈕=存點     │                  │                  │               │
  └───────────────┴──────────────────┴──────────────────┴───────────────┘

  教點工作流：
  ① Free Drive 粗定位 → ② Step Jog 精調 (0.1mm) → ③ 一鍵存點
  → ④ 閉環視覺校正 (≤0.05mm) → ⑤ 自動同步 GYRO YAML + Git
```

---

## Sample 577

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L163

```
  task.gyro.yaml (平台無關)
  ┌───────────────────────────────────────────────────────────────────────┐
  │ waypoints:              │                                             │
  │   pick_pos: [x,y,z,r]   │       GYRO-Compiler                         │
  │ sequences:              │      ┌──────────────┐                       │
  │   pick_and_place:       │────→│ --target=tm  │──→ .flow (TM 原生)   │
  │     - move_linear: pick │      │ --target=ur  │──→ .script (UR 原生) │
  │     - gripper: close    │      └──────────────┘                       │
  │     - move_linear: place│                                             │
  │     - gripper: open     │  Git 版控 · 可 diff · 可 review             │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## Sample 578

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L179

```
  ① 粗定位（手動/搖桿）
        │
       ▼
  ② 高解析相機拍照
        │
       ▼
  ③ 計算偏差 dX / dY / dR
        │
       ▼
  ④ 自動補償運動         ←── 重複直到 delta ≤ 容差
        │
       ▼
  ⑤ 最終作業 (精度 ≤ 0.05mm)
```

---

## Sample 579

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L197

```
  傳統模式                          Swap 模式
  ┌─────┐   空跑   ┌─────┐       ┌──────┐  同時取放   ┌───────┐
  │ 放A │ ──────→ │ 取B │       │取B放A│ ────────→  │取A放B │
  └─────┘          └─────┘       └──────┘             └───────┘
  2 趟 = 2 個停靠週期               1 趟 = 1 個停靠週期
                                   產量 ~18 moves/hr/AMR
```

---

## Sample 580

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L208

```
  現有程式                    自動分析                   一鍵簡化
  ┌───────────┐              ┌───────────┐             ┌───────────┐
  │ 452 chains│    ────→    │ 偵測 2,021│    ────→   │ 70 個     │
  │ 重複邏輯  │   Simplifier │ 處重複    │    apply    │ 簡化方案  │
  └───────────┘              └───────────┘             └───────────┘
```

---

## Sample 581

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L236

```
2026 H2                    2027                      2028
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 ┏━━━━━━━━━━━━━━━┓
 ┃   Phase 3     ┃
 ┃   統一 TM/UR  ┃    ┏━━━━━━━━━━━━━━━━━━━┓
 ┃               ┃──→┃   Phase 4         ┃
 ┃ · 跨品牌監控  ┃    ┃   多臂 + AMR      ┃    ┏━━━━━━━━━━━━━━━━━┓
 ┃ · 搖桿教點    ┃    ┃                   ┃──→┃   Phase 5       ┃
 ┃ · 程式編輯    ┃    ┃ · 雙臂/三臂協調   ┃    ┃   人型機器人    ┃
 ┃ · DSL v1      ┃    ┃ · AMR 車隊地圖    ┃    ┃                 ┃
 ┃ · 視覺校正    ┃    ┃ · MCS-Lite 整合   ┃    ┃ · 全身控制      ┃
 ┗━━━━━━━━━━━━━━━┛    ┃ · DSL 多臂語法    ┃    ┃ · 步態/平衡     ┃
                      ┗━━━━━━━━━━━━━━━━━━━┛    ┃ · AI 動作生成   ┃
                                               ┃ · Digital Twin  ┃
                                               ┃ · 語音指令      ┃
                                               ┗━━━━━━━━━━━━━━━━━┛
```

---

## Sample 582

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L273

```
  Phase 3                    Phase 4                     Phase 5
  單臂                       多臂 + 移動平台              全身

  ┌────────┐          ┌──────────────────┐         ┌───────────────┐
  │ TM     │          │  DualArm         │         │ Humanoid      │
  │ Adapter│─┐        │  ├ left: TM      │         │ ├ left_arm    │
  └────────┘ │        │  ├ right: TM     │         │ ├ right_arm   │
             ├──共用→│  └ coordinator   │──共用─→│ ├ legs        │
  ┌────────┐ │  介面  ├──────────────────┤  介面   │ ├ torso       │
  │ UR     │─┘        │  AMR             │         │ └ AI policy   │
  │ Adapter│          │  └ ROS2 nav2     │         └───────────────┘
  └────────┘          └──────────────────┘
                       TriArm
                       ├ arm1: TM
                       ├ arm2: TM
                       └ arm3: UR

  關鍵：手臂的 Adapter 介面從 Phase 3 到 Phase 5 完全複用
```

---

## Sample 583

**Source**: `Reporter_v1\WORKSPACE\a06\GYRO_Unified_Robot_UI_決策版_test.md` L298

```
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
  │  降低成本    │  │  加速交付    │  │  精度提升    │  │  戰略卡位  │
  │              │  │              │  │              │  │            │
  │  一套介面    │  │  DSL 寫一次  │  │  搖桿教點    │  │  自有軟體  │
  │  取代多套    │  │  編譯到      │  │  + 閉環視覺  │  │  平台公司  │
  │  原廠軟體    │  │  任何平台    │  │  ≤ 0.05mm    │  │            │
  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘
```

---

## Sample 584

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L36

```
Start
  │
  ▼
ARM_parameter（初始化）
  ├─ RS485IO == false → 直接設 ENCODER/LED
  └─ RS485IO == true  → 檢查 RS485IO[0..7] → SET_ARM_POSE
  │
  ▼
AMR_V001_CommunicationNoStop1（Modbus 持續監聽 AMR 指令）
  │
  ▼
讀取 var_var_running_array[0]
  │
  ├─ [0] → 待機（NONE_MOVE）
  ├─ [1] → MOVE_TRAY_to_LEFT_multi_EQ  ─→ 左側設備搬運
  ├─ [2] → MOVE_TRAY_to_RIGHT_multi_EQ ─→ 右側設備搬運
  └─ [3] → MOVE_INITIAL（回初始位）
  │
  ▼
MISSION_DONE → GOTO 回通訊迴圈
```

---

## Sample 585

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L69

```
MainFlow (113 節點)
  ├─ ARM_parameter（初始化）
  ├─ MOVE_to_port_number（移動到指定 port）
  └─ Gateway（主分派器）
       │
       ├─ MOVE_INITIAL（回初始位）
       │    └─ SENSOR_Grip_half / tight
       │
       ├─ MOVE_TRAY_to_LEFT_multi_EQ ───────────────────────────────┐
       │    ├─ ERACK_LEFT_LOWER ─┐                                  │
       │    ├─ ERACK_LEFT_UPPER ─┤                                  │
       │    │    ├─ ERACK_TMMARK ─→ 視覺定位 + 條碼讀取            │
       │    │    ├─ ERACK_TAKE   ─→ 感測驗證 + 夾取                │
       │    │    ├─ ERACK_PLACE  ─→ 感測驗證 + 放置                │
       │    │    ├─ MR_PORT_TAKE (151) ─→ 從 MR Port 取 Tray       │
       │    │    └─ MR_PORT_PLACE (423) ─→ 放 Tray 到 MR Port      │
       │    │                                                       │
       │    ├─ HT_9046LS_LEFT_NORMAL (223)                          │
       │    │    ├─ HT_9046LS_TMMARK_NORMAL (259) ─→ 視覺定位      │
       │    │    ├─ HT_9046LS_TAKE (109) ─→ 取件                   │
       │    │    ├─ HT_9046LS_PLACE (123) ─→ 放件                  │
       │    │    ├─ MR_PORT_TAKE                                    │
       │    │    └─ MR_PORT_PLACE                                   │
       │    │                                                       │
       │    ├─ STK_LEFT_LOWER (77) ─┐                               │
       │    └─ STK_LEFT_UPPER (90) ─┤                               │
       │         ├─ STK_TMmark (97) ─→ STK 視覺定位                │
       │         ├─ STK_TAKE (87)                                   │
       │         ├─ STK_PLACE (93)                                  │
       │         ├─ MR_PORT_TAKE                                    │
       │         └─ MR_PORT_PLACE                                   │
       │                                                            │
       └─ MOVE_TRAY_to_RIGHT_multi_EQ ──────────────────────────────┘
            ├─ ERACK_RIGHT_LOWER / UPPER（同左側對稱）
            └─ HT_9046LS_RIGHT_NORMAL（同左側對稱）
```

---

## Sample 586

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L190

```
                    ┌──────────────────┐
    RTDE (reg 0-2)  │   PLC / MES      │
  ◄──────────────►│  (外部控制器)    │
                    └──────────────────┘
                            │
                    ┌───────┴───────┐
                    │    UR30       │
                    │ (Polyscope)   │
                    └──┬───┬───┬────┘
          Modbus TCP   │   │   │  RS485
       ┌───────────────┘   │   └──────────────┐
       ▼                  ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ PLC/IO 模組  │  │  SensoPart   │  │ TC100 Gripper    │
│ 192.168.1.1  │  │  VISOR       │  │ + RS485 IO Box   │
│ port 502     │  │  XML-RPC     │  │ addr 1,2         │
└──────────────┘  └──────────────┘  └──────────────────┘
```

---

## Sample 587

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L232

```
var_read_RTDE = read_input_integer_register(0)
  │
  ├─ 30001 → 初始化歸位（開夾 → 回 Home_L 或 Home_R）
  ├─ 30000 → 移動到啟動位 p_for_startup
  ├─ 30002 → 開夾 → 回 Home_R
  ├─ 30009 → Fork 感測器檢查
  │
  └─ 其他 → 自動作業模式
       │
       ▼
  解析外部指令 → 讀取 RS485 IO → 判斷 port_direction
       │
       ├─ direction = 1（入料）
       │    ├─ type=1 Erack  → VISOR 拍照 → Body_take_put → Erack_load_unload
       │    ├─ type=2 EQ2600 → VISOR 拍照 → Body_take_put → EQ2600_port{1-4}
       │    ├─ type=3 EQ2800 → VISOR 拍照 → Body_take_put → EQ2800_port{1-4}
       │    ├─ type=4 EQ2845 → EQ2845_port1_load_unload
       │    └─ type=5 EQ3670 → EQ3670_port{1-2}
       │
       └─ direction = 2（出料）
            └─ 與入料對稱，順序反轉
```

---

## Sample 588

**Source**: `Reporter_v1\WORKSPACE\a06\TM_UR_程式架構完整版.md` L258

```
initial_prog.script (12,241 行 / 1,341 moves)
  │
  ├─ 常駐載入 Helper Scripts ───────────────────────────────────────┐
  │    tc100_gripper_open / close     夾爪開關                      │
  │    gripeer_cover_open / close     蓋子開關                      │
  │    fork_sensor_check              叉子感測器驗證（4 sensors）   │
  │    payload.script                 計算載重                      │
  │    initial_modbus_tcp             Modbus 初始化                 │
  │    get_command_*                  解析外部指令                  │
  │    rs485io_read                   讀取 IO Box                   │
  │    set_alarm_and_stop             報警停機                      │
  │    Loop / Loop_initial            迴圈控制                      │
  │                                                                 │
  ├─ Body ────────────────────────────────────────────────────────  │
  │    Body_take_put (4,145 行 / 405 moves)                         │
  │      呼叫: fork_sensor_check, payload, tc100_*                  │
  │                                                                 │
  ├─ EQ2600 ──────────────────────────────────────────────────────  │
  │    port1_load / port2_unload / port3_load / port4_unload        │
  │      呼叫: fork_sensor_check, payload, tc100_*                  │
  │                                                                 │
  ├─ EQ2800 ──────────────────────────────────────────────────────  │
  │    port1_unload / port2_load / port3_unload / port4_load        │
  │    port14_swap（交換模式）                                      │
  │    EQ2800P02_* 變體                                             │
  │      呼叫: fork_sensor_check, payload, set_alarm_and_stop       │
  │                                                                 │
  ├─ EQ2845 ─── port1_load_unload                                   │
  ├─ EQ3670 ─── port1/port2_load_unload + backup                    │
  ├─ EQ3800 ─── port1_load_unload                                   │
  │                                                                 │
  └─ Erack ───────────────────────────────────────────────────────  │
       Erack_load_unload (1,195 行 / 73 moves)                      │
       Erack_teach / Erack_teach123（教導模式）                     │
         呼叫: fork_sensor_check, payload, tc100_*, gripeer_cover   │
```

---

## Sample 589

**Source**: `Reporter_v1\WORKSPACE\a07\opencode_enhance_comparison.md` L172

```
需要 AI 編程助手？
│
├─ 有外網？
│   ├─ YES → 預算充足？
│   │   ├─ YES → 在線 強力（Claude Code）
│   │   │         最強深度推理，複雜重構首選
│   │   └─ NO  → 在線 節省（Gemini Free + opencode）
│   │             零成本，品質 93%，速度快 2x
│   │
│   └─ NO → 完全離線（4090 + opencode）
│            唯一選擇，品質等同雲端
│
├─ 資料敏感 / 不可出站？
│   └─ → 完全離線（4090 + opencode）
│
├─ 中國環境？
│   └─ → 完全離線（4090 + opencode）
│
└─ 混合需求？
    └─ → Claude（複雜任務）+ Gemini（日常量產）+ 4090（離線備援）
```

---

## Sample 590

**Source**: `Reporter_v1\WORKSPACE\a07\opencode_enhance_history.md` L55

```
opencode_enhance_v0/
├── .gitignore
├── README.md
├── update.cmd
├── AGENTS.md                          # OpenCode 行為指引
├── docs/
│   ├── daily-log-2026-04-02.md
│   ├── mcp-setup.md                   # MCP 設定架構文件
│   ├── opencode-vs-claude-code.md
│   ├── usage-scenarios.md
│   └── verification-notes.md
├── env-setup/
│   └── README.md                      # 安裝指引（含 Ollama Docker）
├── opencode-config/
│   ├── opencode.json                  # Model + MCP + permissions
│   ├── global-opencode.json           # 全域設定（MCP 預設關閉）
│   ├── AGENTS.md
│   ├── AGENTS-ur.md
│   ├── .env.example
│   ├── package.json
│   └── .opencode/
│       ├── plugins/git-attribution.ts
│       └── skills/project-status/SKILL.md
└── usage-records/
    ├── review-instructions.md
    └── test-code-review.md
```

---

## Sample 591

**Source**: `Reporter_v1\WORKSPACE\a07\opencode_enhance_history.md` L152

```
opencode-bench/
├── README.md                   # 專案概覽
├── RESULTS.md                  # 詳細結果 + 根因分析
├── SUMMARY.md                  # 全平台結果總表
├── BENCHMARK-REPORT.md         # 最終效能評測報告
├── ARCHITECTURE.md             # 系統架構說明
├── HANDOFF.md                  # 交接文件
├── 4090-SETUP.md               # RTX 4090 環境設定
├── 4090-DEPLOYMENT.md          # 部署提案（含成本分析）
├── collect_all.py              # 掃描 *_meta.txt → xlsx（109 rows）
├── opencode_enhance_all_benchmarks.xlsx  # 全量 benchmark 報告
├── fixtures/                   # A3/A4 task fixtures
│
├── # ── Benchmark 腳本 ──
├── bench_4090_5runs.sh
├── bench_dgx.sh
├── bench_gemini_5runs.sh
├── bench_a5_5runs.sh / bench_a5_quick.sh
├── bench_stress.sh
├── run_a1_repeat.sh / run_a1_extra.sh
│
├── # ── 結果目錄（按平台×日期）──
├── opencode-2026-04-07/        # 最初測試
├── three-way-2026-04-08/       # 早期三方對照
├── 4090-2026-04-08/
├── 4090-real-2026-04-08/
├── dgx-spark-2026-04-08/
├── gemini-3way-2026-04-08/
├── 4090-ollama-2026-04-09/     # 直連 Ollama（全滅）
├── 4090-litellm-2026-04-09/    # LiteLLM R1
├── 4090-litellm-2026-04-09-r2/ # LiteLLM R2
├── dgx-spark-litellm-2026-04-09/
├── a4-bench-2026-04-09/        # A4 專題
├── a1-dual-file-test/          # A1 雙檔 bug 調查
├── a1-repeat-4090/ + a1-repeat-dgx/  # A1 重複測試
├── fix-proxy/                  # Ollama index bug 修復 + retest
│   ├── proxy.py
│   ├── bench_3way.sh
│   └── bench-3way-20260410-*/
├── 4090-5runs-20260410-*/      # 5-run 穩定性
├── dgx-5runs-20260410-*/
├── gemini-5runs-20260410-*/
├── a5-5runs-20260410-*/
├── a5-quick-20260410-*/
└── stress-20260410-*/          # 壓力測試
```

---

## Sample 592

**Source**: `Reporter_v1\WORKSPACE\TEST_CASE\8D_Report_Wafer_Damage_AMR04_20260328.md` L148

```
Reset triggered (after alarm)
  └─ TMflow init sequence executes
  └─ Step 1: Modbus write → IAI driver: "Open gripper"   ← No cassette presence check
  └─ Step 2: Modbus write → IAI driver: "Close gripper"  ← Too late — cassette already dropped
  └─ Step 3: Continue init...
```

---

## Sample 593

**Source**: `Reporter_v1\WORKSPACE\TEST_CASE\8D_Report_Wafer_Damage_AMR04_20260328_marp.md` L252

```
Reset triggered (after alarm)
  └─ TMflow init sequence executes
  └─ Step 1: Modbus write → IAI driver: "Open gripper"   ← No cassette presence check
  └─ Step 2: Modbus write → IAI driver: "Close gripper"  ← Too late — cassette already dropped
  └─ Step 3: Continue init...
```

---

## Sample 594

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L26

```
yfinance / FinMind API
        │
        ▼
┌─────────────────┐     ┌───────────────────┐
│   US Market      │     │   TW Market        │
│   Fetcher        │     │   Fetcher          │
│  (20+ symbols)   │     │  (法人/期貨/融資)  │
└────────┬────────┘     └────────┬──────────┘
         │                       │
         ▼                       ▼
    ┌────────────────────────────────┐
    │       daily_features (SQLite)  │
    │   25 global + 8 TAIEX 技術指標 │
    └──────────────┬─────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  FeatureBuilder [5, 30]   GMP FeatureEngineer
         │                   │
    ┌────┴────┐         LightGBM
    ▼         ▼         (週/月報酬)
Transformer  RL PPO
 (分類)     (交易)
    │         │
    ▼         ▼
 prediction_log ──► Daily Email
```

---

## Sample 595

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L156

```
Input [batch, 5, 30]
  │
  ├─ Feature Attention Gate: Linear(30,30) → sigmoid 逐特徵加權
  ├─ Projection: Linear(30, 64)
  ├─ Learnable Positional Embedding(5, 64)
  ├─ TransformerEncoder × 2 (ffn=256, GELU)
  ├─ Attention Pooling: Linear(64,1) → softmax 加權聚合
  └─ Classification Head (with residual)
       ├─ LayerNorm(64) → Linear(64,64) → GELU → Dropout
       └─ Linear(64, 3) + residual
```

---

## Sample 596

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L192

```
資料時間軸：────────────────────────────────────────►
├── Train (500 days) ──┤ Val (60) ┤
            ├── Train (560 days) ──┤ Val (60) ┤
                        ├── Train (620 days) ──┤ Val (60) ┤
                                    ...
```

---

## Sample 597

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L253

```
                真實標籤
動作       下跌(0)    持平(1)    上漲(2)
─────────────────────────────────────
SKIP(0)    -0.05      +0.30      -0.05
LONG(1)    -1.20      -0.30      +1.00
SHORT(2)   +1.00      -0.30      -1.20
```

---

## Sample 598

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L270

```
Observation [150]
  ├─ Policy Net: Linear(150,64) → Tanh → Linear(64,64) → Tanh
  │    └─ Action Net: Linear(64, 3) → Categorical Distribution
  └─ Value Net:  Linear(150,64) → Tanh → Linear(64,64) → Tanh
       └─ Linear(64, 1) → V(s)
```

---

## Sample 599

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L308

```
├── Train (500 days) ──┤ Val (60) ┤  ← Worker 1
            ├── Train (560 days) ──┤ Val (60) ┤  ← Worker 2
                        ├── Train (620 days) ──┤ Val (60) ┤  ← Worker 3
                                    ...          ← Worker 4~8
```

---

## Sample 600

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L448

```
1. 檢查是否為交易日（跳過週末 & 台股假日）
2. 更新全球 + 台灣市場資料
3. 回填昨日實際結果
4. 執行預測（Transformer 或 RL，依 STOCKSAGE_USE_RL）
5. 寫入 prediction_log
6. 組成 HTML Email：
   ├─ 昨日回顧（實際 vs 預測）
   ├─ 今日訊號（動作 + 機率分布）
   ├─ GMP 全球展望（選用）
   └─ 近期準確率統計
7. 透過 Gmail SMTP 寄送
```

---

## Sample 601

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L486

```bash
# ─── 日常操作 ───
python run.py                              # 每日預測（預設）
python run.py --status                     # 資料庫 & 模型狀態

# ─── 初始化 & 訓練 ───
python run.py --init                       # 首次：全量建庫 + 訓練
python run.py --train                      # 強制重訓 Transformer
python run.py --train-until DATE           # 訓練資料截止日

# ─── RL 引擎 ───
python run.py --rl-train                   # 訓練 PPO agent
python run.py --rl-predict                 # 單次 RL 預測
python run.py --rl-compare                 # RL vs Transformer 比較
python run.py --rl-compare --oos           # 僅樣本外比較

# ─── GMP ───
python run.py --gmp-init                   # 初始化 + 訓練 GMP
python run.py --gmp-train                  # 重訓 GMP
python run.py --gmp-predict                # GMP 預測

# ─── 回測 ───
python run.py --backtest                   # 小台，全樣本
python run.py --backtest --contract full   # 大台
python run.py --backtest --oos             # 僅樣本外
python run.py --backtest --start-date DATE # 指定起始日
python run.py --backtest --no-confidence-filter
```

---

## Sample 602

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L575

```
StockSage_v0/
├── run.py                     # 主入口 CLI
├── config.py                  # 全域設定
├── pipeline/                  # Transformer 引擎
│   ├── model.py               #   StockTransformer 模型
│   ├── feature_builder.py     #   特徵工程
│   ├── auto_trainer.py        #   訓練（WF-CV）
│   ├── daily_update.py        #   每日資料更新
│   └── weekly_runner.py       #   推論 & 排程
├── rl/                        # RL PPO 引擎
│   ├── env.py                 #   TradingEnv (Gymnasium)
│   ├── policy.py              #   Policy 網路定義
│   ├── config.py              #   RL 超參數
│   ├── trainer.py             #   訓練（平行 WF-CV）
│   ├── predictor.py           #   推論
│   └── evaluate.py            #   模型比較工具
├── gmp/                       # GMP 全球市場預測
│   ├── feature_engineer.py    #   50+ 維特徵
│   ├── model.py               #   LightGBM 週/月模型
│   ├── predictor.py           #   預測
│   └── trainer.py             #   訓練
├── fetchers/                  # 資料擷取
│   ├── us_market.py           #   美股 & 全球（yfinance）
│   └── tw_market.py           #   台灣法人（FinMind）
├── backtest/                  # 回測
│   └── gap_backtest.py        #   隔夜跳空策略
├── db/                        # 資料庫
│   ├── schema.py              #   SQLAlchemy schema
│   └── stocksage.db           #   SQLite 資料檔
├── scripts/                   # 排程腳本
│   ├── daily_predict_email.py #   每日 Email 管線
│   ├── run_daily.bat          #   Windows 排程用
│   └── setup_schedule.bat     #   建立排程
├── models/                    # 訓練好的模型（gitignored）
├── docs/                      # 文件
└── .env                       # 環境變數（gitignored）
```

---

## Sample 603

**Source**: `StockSage_v0\README.md` L191

```
StockSage_v0/
├── run.py                        # 唯一入口（所有 CLI 指令）
├── config.py                     # 全域設定
├── requirements.txt
│
├── db/
│   └── schema.py                 # SQLAlchemy ORM
│
├── fetchers/
│   ├── base.py                   # 重試、upsert、日誌
│   ├── us_market.py              # yfinance：全球指數
│   └── tw_market.py              # FinMind：台股籌碼
│
├── pipeline/
│   ├── model.py                  # Transformer Encoder
│   ├── feature_builder.py        # 特徵組裝 + TAIEX 技術指標
│   ├── auto_trainer.py           # Walk-Forward 訓練
│   └── weekly_runner.py          # 每日預測主流程
│
├── rl/                           # 強化學習模組
│   ├── config.py                 # RL 超參數
│   ├── env.py                    # Gymnasium TradingEnv
│   ├── policy.py                 # Transformer feature extractor for SB3
│   ├── trainer.py                # Walk-Forward PPO 訓練
│   ├── predictor.py              # RL 推論
│   └── evaluate.py               # RL vs Transformer 比較
│
├── gmp/                          # Global Market Predictor
│   ├── config.py                 # GMP 設定
│   ├── fetcher.py                # 全球市場資料抓取
│   ├── feature_engineer.py       # 48 維特徵工程
│   ├── trainer.py                # LightGBM 訓練
│   └── predictor.py              # 週/月報酬率預測
│
├── scripts/
│   ├── daily_predict_email.py    # 每日 Email（完整 pipeline + 昨日回顧）
│   ├── run_daily.bat             # Task Scheduler 執行用 wrapper
│   └── setup_schedule.bat        # 排程安裝腳本
│
├── backtest/
│   └── gap_backtest.py           # 夜盤結算→開盤跳空回測
│
└── models/
    ├── stocksage_model.pt        # Transformer 模型權重
    ├── model_meta.pkl            # Transformer 訓練 metadata
    ├── rl_ppo_agent.zip          # RL PPO agent
    ├── rl_meta.pkl               # RL 訓練 metadata
    └── gmp_model.pkl             # GMP LightGBM 模型
```

---

## Sample 604

**Source**: `StockSage_v0\README_DEV.md` L9

```
yfinance (全球指數)  →  daily_features (DB)  ──┐
FinMind (台股籌碼)   →  daily_features (DB)  ──┤  前 5 天
yfinance (^TWII)    →  TAIEX 技術指標 (記憶體) ─┘  [5, 30]
                                                    ↓
                                             Transformer
                                                    ↓
                                     {下跌, 持平, 上漲} 機率
```

---

## Sample 605

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L32

```
                    True Label
Action      Down(-1)    Flat(0)    Up(+1)
─────────────────────────────────────────
Skip         -0.05      +0.30      -0.05
Long         -1.20      -0.30      +1.00
Short        +1.00      -0.30      -1.20
```

---

## Sample 606

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L50

```
rl/
├── config.py       # 超參數（reward、PPO、walk-forward）
├── env.py          # TradingEnv — Gymnasium 環境
├── policy.py       # TransformerFeaturesExtractor（實驗用，目前未啟用）
├── trainer.py      # RLTrainer — Walk-Forward PPO 訓練
├── predictor.py    # get_rl_prediction() — 推論
└── evaluate.py     # ModelComparator — RL vs Transformer 比較
```

---

## Sample 607

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L115

```
Day:  0 ────── 500 ── 560 ── 620 ── ... ── N
      │ Fold 1 train │ val1 │
      │         Fold 2 train │ val2 │
      │              Fold 3 train   │ val3 │

窗口: train=expanding, val=sliding 60 days, step=60 days
```

---

## Sample 608

**Source**: `StockSage_v0\rl\ARCHITECTURE.md` L132

```
models/
├── rl_ppo_agent.zip    # PPO 模型（SB3 格式）
└── rl_meta.pkl         # metadata:
                        #   feat_mean, feat_std（正規化參數）
                        #   trained_at, wf_details（各 fold 結果）
                        #   final_metrics（最終模型訓練集表現）
```

---

## Sample 609

**Source**: `TM_Program_Analysis_v0\docs\ERROR_CODE_REFERENCE.md` L113

```
夾爪應該夾緊，但 DI[2]&DI[5] 無信號
  ├─ DI[0] 有信號?  → YES → Error 1115（DI0 異常觸發）
  ├─ DI[1]&DI[2] 有信號? → YES → Error 1116（DI1+DI2 組合異常）
  ├─ DI[3] 有信號?  → YES → Error 1117（DI3 異常觸發）
  └─ 都沒有 → WaitFor 重試
```

---

## Sample 610

**Source**: `TM_Program_Analysis_v0\docs\ERROR_CODE_REFERENCE.md` L137

```
夾爪應該夾緊 (grip_close=true)，正常期望 RS485IO = {1,0,1,1,1,*,0,1}
  ├─ RS485IO[0]==0 & [1]==1?  → YES → Error 1119（近接感測器反向）
  ├─ RS485IO[2]==0?           → YES → Error 1120（壓力感測器無信號）
  ├─ RS485IO[3]==0?
  │   ├─ RS485IO[4]==0?       → YES → Error 1122（位置感測器也無信號）
  │   ├─ RS485IO[6]==1?       → YES → Error 1124（異常偵測觸發）
  │   └─ RS485IO[7]==0?       → YES → Error 1125（重量感測器無信號）
  ├─ RS485IO[3]==1? (Tray 在位)
  │   ├─ RS485IO[4]==0?       → YES → Error 1122
  │   ├─ RS485IO[6]==1?       → YES → Error 1124
  │   └─ RS485IO[7]==0?       → YES → Error 1125
  └─ 都正常 → I/O 記錄 → Error 1121（狀態不一致）
```

---

## Sample 611

**Source**: `TM_Program_Analysis_v0\docs\ERROR_CODE_REFERENCE.md` L178

```
夾爪應該半開 (grip_half=true)
  ├─ RS485IO[0]==0 & [1]==1?  → YES → Error 1133
  ├─ RS485IO[2]==0?           → YES → Error 1134
  ├─ RS485IO[3]==0?           → YES → Error 1135
  ├─ RS485IO[4]==0?           → YES → Error 1136
  ├─ RS485IO[6]==1?           → YES → Error 1138
  └─ RS485IO[7]==0?           → YES → Error 1139
```

---

## Sample 612

**Source**: `TM_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L55

```
Start
  └─ SubFlow: ARM_parameter（初始化手臂參數）
       ├─ [g_use_RS485IO == false] → 非 RS485 模式初始化
       │    ├─ [g_use_initial_point_setting_from_txt == false] → 直接設 ENCODER/LED
       │    └─ [true] → 從 TXT 檔讀取初始點位（read_file → READ_TXT → 迴圈解析）
       │
       └─ [g_use_RS485IO == true] → RS485 模式初始化
            ├─ 檢查 RS485IO[0..7] 狀態 → SET_ENCODER/LED
            ├─ 同樣支援 TXT 檔讀取
            └─ 設定 I/O Box × 6 + I/O EX × 4 → SET_ARM_POSE

  → Component: AMR_V001_CommunicationNoStop1（Modbus 通訊，持續監聽 AMR 指令）
  → SET: SET_ARM_param → port_name → landmark_id → BARCODE_ID
  → Log: MISSION_START × 3
  → SET: set_var_running

  → [var_var_running_array[0] == 3] → Gateway (主分派器)
       ├─ [0] → NONE_MOVE（待機）
       ├─ [1] → MOVE_TRAY_to_LEFT_multi_EQ（左側設備搬運）
       ├─ [2] → MOVE_TRAY_to_RIGHT_multi_EQ（右側設備搬運）
       └─ [3] → MOVE_INITIAL（回初始位）

  → Log: MISSION_DONE × 3
  → GOTO: AMR_V001_CommunicationNoStop1（回到通訊迴圈）
```

---

## Sample 613

**Source**: `TM_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L382

```
                    ┌─────────────────────┐
                    │   AMR (Modbus 通訊) │
                    └──────────┬──────────┘
                               │ var_var_running_array
                    ┌──────────▼──────────┐
                    │   ARM_parameter     │ ← 初始化（RS485/TXT 點位）
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Gateway        │ ← 主分派器
                    │  [0]=方向 [3]=目標   │
                    └─┬────┬────┬────┬───┘
                      │    │    │    │
              ┌───────┘    │    │    └────────┐
              ▼            ▼    ▼             ▼
         MOVE_LEFT    MOVE_RIGHT  INITIAL   NONE_MOVE
              │            │        │
    ┌─────┬──┴──┬────┐    ...   ReturnHome
    ▼     ▼     ▼    ▼
  ERACK  EQ   ICOS  STK   ← [3] 目標類型
    │     │          │
  PORT_1~8          TAKE/PLACE ← [4] Port 編號
    │
  ┌─┴─────────────────┐
  │  HT_9046LS_TAKE   │ ← 設備操作
  │  HT_9046LS_PLACE  │
  │  MR_PORT_TAKE     │
  │  MR_PORT_PLACE    │
  │  ERACK_TAKE/PLACE │
  │  STK_TAKE/PLACE   │
  └────────────────────┘
           ↕
    ┌──────────────┐
    │  Vision Jobs  │ ← TMark/AprilTag/Barcode
    │  Sensor Check │ ← 夾爪/雷射/IO
    │  Log/Modbus   │ ← 回報 AMR
    └──────────────┘

背景執行緒（常駐同時運作）：
  - CHECK_GRIP_2        持續監控夾爪（440 節點）
  - CHECK_ENCODER       監控編碼器（17 節點）
  - CHECK_ALL_SENSOR_WHEN_CAR_MOVING_2  移動中安全監控（86 節點）
  - Pause_handle        處理暫停請求（9 節點）
  - Pub_RS485IO         發佈 I/O 狀態（7 節點）
```

---

## Sample 614

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L88

```
IF: var_camera_once_eq_flag==true & g_camera_once==true?
  ├─ [YES] 已經拍過照，跳過 Vision FAR
  │    IF: var_runing > 0?
  │      ├─ [YES] → 直接到 Port 分派（Phase 5）
  │      └─ [NO]  → 移動到 P110 → Phase 5
  │
  └─ [NO] 未拍過照，執行 Vision FAR（Phase 3）
```

---

## Sample 615

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L103

```
Vision: RIGHT_HT_9046LS_right_TMMARK_FAR
  ├─ [成功]
  │    SET: var_coordrobot = Robot[0].CoordRobot          ← 記錄當前機器人座標
  │         var_Log_vision_base = Base["vision_...FAR"]   ← 記錄視覺基座值
  │    Log: 記錄座標
  │
  │    ── 驗證 1：Rz 角度檢查 ──
  │    IF: abs(vision_base[5]) 在 80°~100° 之間?
  │      ├─ [YES] → 驗證 2
  │      └─ [NO]  角度異常
  │           ├─ [重試<g_vision_retry] → vision_count++ → 回到 Vision FAR
  │           └─ [重試>=g_vision_retry]
  │                → Log ERROR → SET: error_code=1227 → STOP
  │
  │    ── 驗證 2：Z 軸距離檢查 ──
  │    IF: |coordrobot[2] - vision_base[2]| <= 350?
  │      ├─ [YES] → 驗證 3
  │      └─ [NO]  Z 軸偏差過大
  │           ├─ [重試<=g_tag_distance_retry] → tag_distance_count++ → 回到 Vision FAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1224/1225 → STOP
  │
  │    ── 驗證 3：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_base[4]| <= g_check_EQ_far_tolerance[4]?
  │      ├─ [YES] → 通過! → 移動到 P70 → Phase 4
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] → count++ → 回到 Vision FAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1223 → STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] → vision_count++ → Log ERROR → 回到 Vision FAR
       └─ [超過重試]
            → Log ERROR → SET: error_code=1223 → STOP
```

---

## Sample 616

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L140

```
移動到 P70（近距拍照位）
SET: 重置所有計數器

Vision: RIGHT_HT_9046LS_right_TMMARK_NEAR
  ├─ [成功]
  │    SET: var_temporary_fl = modbus_read("mtcp_AMR","preset_en_fl")  ← 讀取 AMR 感測器
  │         var_temporary_bl = modbus_read("mtcp_AMR","preset_en_bl")
  │         var_temporary_fr = modbus_read("mtcp_AMR","preset_en_fr")
  │    SET: var_coordrobot = Robot[0].CoordRobot
  │         var_Log_vision_base = Base["vision_...NEAR"]
  │    Log: 記錄座標
  │
  │    ── 驗證：Ry 角度偏差檢查 ──
  │    IF: |g_check_EQ_goal_tolerance[4] - vision_NEAR_base[4]| <= g_check_EQ_near_tolerance[4]?
  │      ├─ [YES] → 通過! → Phase 5（Camera Once 分派 或 Port 分派）
  │      └─ [NO]  Ry 偏差過大
  │           ├─ [重試<g_re_try] → count++ → 回到 Vision NEAR
  │           └─ [超過重試] → Log ERROR → SET: error_code=1226 → STOP
  │
  └─ [失敗]
       ├─ [重試<g_vision_retry] → vision_count++ → 回到 Vision NEAR
       └─ [超過重試]
            → Log ERROR → SET: error_code=1225 → STOP
```

---

## Sample 617

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L170

```
IF: g_use_RS485IO == false?  → Gateway（非 RS485）
IF: g_use_RS485IO == true?   → Gateway（RS485）

Gateway: var_to_port_number
  ├─ [1] EQ_PORT1 → 檢查 EQ_TYPE → HT_9046LS_001_front → check_tray_distance
  ├─ [2] EQ_PORT2 → 檢查 EQ_TYPE → HT_9046LS_002_front → check_tray_distance
  └─ [3] EQ_PORT3 → 檢查 EQ_TYPE → HT_9046LS_003_front → check_tray_distance
```

---

## Sample 618

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L209

```
IF: DIO 數位感測器有信號?
  ├─ [YES] 有 Tray
  │    IF: var_LASER_MEASURE <= g_highest_point & var_laser_volt >= 1.5?
  │      ├─ [YES] 距離正常 → 重試 (count++ → 回到 Vision FAR/NEAR)
  │      └─ [NO]  → 二次確認 (double_check)
  │
  └─ [NO] 無 DIO 信號 → Log ERROR → 回到 Vision FAR/NEAR
```

---

## Sample 619

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L221

```
IF: var_RS485IO[7] == 0?  ← RS485 第 8 位 = Tray 感測器
  ├─ [0] 無 Tray
  │    IF: LASER_MEASURE <= g_highest_point & laser_volt >= 1.5?
  │      ├─ [YES] 雷射也確認無 Tray → 重試
  │      └─ [NO]  → 二次確認 (double_check)
  │
  └─ [非0] 有 Tray → Log ERROR → 回到 Vision FAR/NEAR
```

---

## Sample 620

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L233

```
IF: g_double_check_if_tray_on_EQ_port == true?
  ├─ [YES]
  │    IF: var_LASER_MEASURE >= g_lowest_point?
  │      ├─ [YES] 距離夠遠，確認沒有 Tray
  │      │    SET: var_temp_LASER_MEASURE = var_LASER_MEASURE  ← 暫存
  │      │    Move: in_gyro_move_to_tray                       ← 靠近一點再看
  │      │    WaitFor: 1000ms
  │      │    SET: 重新測量 LASER_MEASURE
  │      │    SET: 重新計算 put_down_distance
  │      │    → 第二輪感測器檢查
  │      │
  │      └─ [NO] 距離太近，可能有 Tray → Gateway 分派到各 Port front
  │           → GOTO 回到主流程
  │
  └─ [NO] 不做二次確認 → 直接到 Port 分派
```

---

## Sample 621

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L253

```
移動到 HT_9046LS_00X_front（Port 前方）

IF: var_LASER_MEASURE >= g_lowest_point?
  ├─ [YES] var_nothing_on_port_can_place = true   ← Port 空的，可以放
  └─ [NO]  var_nothing_on_port_can_place = false   ← Port 有東西，不能放

Log: LASER_DISTANCE
```

---

## Sample 622

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L264

```
IF: g_place_again == true?
  ├─ [YES] → 重置 count=0 → 繼續（允許重試放置）
  └─ [NO]  → Log ERROR → SET: error_code=1014 → STOP
```

---

## Sample 623

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L345

```
HT_9046LS_TMMARK_NORMAL 入口
│
├─ 初始化 (Log, SET grip_in="EQ", 重置計數器)
│
├─ Camera Once 優化?
│   ├─ [已拍過] → 跳過視覺 → Phase 5
│   └─ [未拍過] ↓
│
├─ ═══ Vision FAR ═══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_FAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] → 記錄座標
│   │   ├─ 驗證 1: Rz ∈ [80°, 100°]?
│   │   │   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1227)
│   │   ├─ 驗證 2: |ΔZ| ≤ 350mm?
│   │   │   └─ [失敗] → 重試 ≤ g_tag_distance_retry → STOP(1224)
│   │   └─ 驗證 3: |ΔRy| ≤ far_tolerance?
│   │       └─ [失敗] → 重試 ≤ g_re_try → STOP(1223)
│   │
│   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1223)
│
├─ 移動到 P70（近距位）
│
├─ ═══ Vision NEAR ══════════════════════
│   │  Job: RIGHT_HT_9046LS_right_TMMARK_NEAR
│   │  辨識: Landmark (TM Mark)
│   │
│   ├─ [成功] → 記錄座標 + 讀取 AMR 感測器
│   │   └─ 驗證: |ΔRy| ≤ near_tolerance?
│   │       └─ [失敗] → 重試 ≤ g_re_try → STOP(1226)
│   │
│   └─ [失敗] → 重試 ≤ g_vision_retry → STOP(1225)
│
├─ ═══ Port 分派 ════════════════════════
│   Gateway: var_to_port_number
│   ├─ [1] → HT_9046LS_001_front → check_tray_distance
│   ├─ [2] → HT_9046LS_002_front → check_tray_distance
│   └─ [3] → HT_9046LS_003_front → check_tray_distance
│
├─ ═══ 雷射測距 ═════════════════════════
│   WaitFor: 1000ms（穩定）
│   LASER = AI[0] × 57.5 + 30 (mm)
│   put_down_distance = LASER - gripper_depth
│
├─ ═══ Tray 存在判斷 ════════════════════
│   │
│   ├─ 第一層: DIO / RS485IO[7] 感測器
│   ├─ 第二層: LASER ≤ highest_point & volt ≥ 1.5V?
│   └─ 第三層: double_check → 靠近再測一次
│
├─ ═══ 最終輸出 ═════════════════════════
│   var_nothing_on_port_can_place = true/false
│   │
│   └─ g_place_again?
│       ├─ [true]  → 允許重試放置
│       └─ [false] → STOP(1014)
│
└─ 收尾 (Log, SET grip_in="", 返回)
```

---

## Sample 624

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L93

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") != true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") != true
  ├─ [條件成立] → Port 是空的 → 繼續放置
  └─ [條件不成立] → Port 上有東西
       ├─ [var_PSPL_check < 3] → 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] → 超過重試次數
            → Log: ERROR_CODE
            → SET: ERROR_CODE_MODBUS = 1311
            → STOP（停機）
```

---

## Sample 625

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L109

```
IF: modbus_read("mtcp_AMR", "preset_Buffer_X_PS") == true
  & modbus_read("mtcp_AMR", "preset_Buffer_X_PL") == true
  ├─ [條件成立] → Tray 確認在位 → 後退離開
  └─ [條件不成立] → Tray 不在位
       ├─ [var_PSPL_check < 3] → 重試（計數+1, 等 500ms, 再檢查）
       └─ [var_PSPL_check >= 3] → 超過重試次數
            → Log: ERROR_CODE
            → SET: ERROR_CODE_MODBUS = 1311
            → STOP（停機）
```

---

## Sample 626

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L125

```
IF: var_MR_check_PSPL == true
  ├─ [true]  → 執行 Modbus 讀取 PS/PL 確認
  └─ [false] → 跳過檢查，直接操作
```

---

## Sample 627

**Source**: `TM_Program_Analysis_v0\docs\MR_PORT_PLACE_ANALYSIS.md` L178

```
MR_PORT_PLACE 入口
│
├─ Log: PLACE_TRAY (×2)
├─ SET: var_grip_in = "MR"
├─ SET: var_MR_check_PSPL = false
│
├─ Gateway: MR_PORT_NUMBER (var_MR_port_number)
│   ├─ [1]  → MR_1_front → MR_1_pre_take
│   ├─ [2]  → MR_2_front → MR_2_pre_take
│   ├─ [3]  → MR_3_front → MR_3_pre_take
│   ├─ [4]  → MR_4_front → MR_4_pre_take
│   ├─ [5]  → P22 → MR_5_front → MR_5_pre_take
│   ├─ [6]  → P22 → MR_6_front → MR_6_pre_take
│   ├─ [7]  → P10 → MR_7_front → MR_7_pre_take
│   ├─ [8]  → P10 → MR_8_front → MR_8_pre_take
│   ├─ [9]  → ...
│   └─ [12] → ...
│
│  ===== 以下以 Port 1 為例 =====
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] → 放置前 PSPL 檢查
│   │   ├─ IF: Buffer_1_PS != true & Buffer_1_PL != true?
│   │   │   ├─ [YES] Port 空 → 繼續
│   │   │   └─ [NO]  Port 有東西
│   │   │       ├─ [重試<3] → PSPL_check++, Log, WaitFor 500ms → 回到檢查
│   │   │       └─ [重試>=3] → Log ERROR → Modbus 1311 → STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] → SET: pause_false → 跳過檢查
│
├─ SubFlow: SENSOR_Grip_half（夾爪半開）
│
├─ Point: MR_1_take_up（Port 1 上方）
├─ SET: SET_grip（設定夾爪為 open 狀態）
├─ Point: MR_1_take（下降到放置位）
│
├─ SubFlow: SENSOR_Grip_open（夾爪全開，釋放 Tray）
│
├─ SET: reset_PSPL_counter (var_PSPL_check = 0)
│
├─ IF: var_MR_check_PSPL == true?
│   ├─ [YES] → 放置後 PSPL 確認
│   │   ├─ IF: Buffer_1_PS == true & Buffer_1_PL == true?
│   │   │   ├─ [YES] Tray 在位 → 繼續
│   │   │   └─ [NO]  Tray 不在位
│   │   │       ├─ [重試<3] → PSPL_check++, Log, WaitFor 500ms → 回到確認
│   │   │       └─ [重試>=3] → Log ERROR → Modbus 1311 → STOP
│   │   └─ SET: reset_PSPL_counter
│   │
│   └─ [NO] → 跳過確認
│
├─ Move: back_15mm（後退 15mm）
├─ Point: MR_1_ready_to_take（準備離開位）
├─ Point: MR_1_front（回到前方安全位）
│
├─ Log: PLACE_TRAY (×2)
├─ SET: var_if_CHECK_ALL_SENSOR_WHEN_CAR_MOVING = true
├─ SET: var_grip_in = "MR"（重設夾爪來源）
│
└─ 結束（返回上層流程）
```

---

## Sample 628

**Source**: `TM_Program_Analysis_v0\docs\TMFLOW_DOMAIN_API_NOTE.md` L71

```
gamepad → Python
  ├─ motion：UIAutomation 點擊 TMflow Jog Panel (Route B)
  └─ save  ：DomainAPI SetProjectPointInfo (Route I-a) ⭐
```

---

## Sample 629

**Source**: `TM_Program_Analysis_v0\docs\TMFLOW_DOMAIN_API_NOTE.md` L82

```
E:\github\UR_Program_Analysis_v0\docs\gRPC\
├─ u16_AEE885grpc.docx                    # 需求文件原檔
├─ 需求管理表_V3.xlsx                     # 23 項需求清單
├─ req.csv                                # csv 版需求表
├─ gRPC連線測試.mp4                       # 連線測試影片
├─ docx_content.txt                       # pip install 備忘
└─ gRPCTest/
   ├─ TMDomainAPI_r20260206.7z            # ⭐ 官方 DomainAPI 包
   │  └─ TmDomainService.proto            # 已解壓到 _TMDomainAPI_extracted/
   │  └─ Readme.txt                       # 版本更新說明
   ├─ Client/TMgrpcClient.exe             # .NET demo client
   ├─ Server/TMgrpcServer.exe             # .NET demo server
   └─ PythonClient/
      ├─ CmdProto.proto                   # hello world sample（不是真的）
      ├─ CmdProto_pb2.py / _pb2_grpc.py   # stub
      └─ gRPCclient.py                    # client 範例（localhost:5005）
```

---

## Sample 630

**Source**: `TM_Program_Analysis_v0\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L33

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
|  ├─ HID 事件 → 抽象 intent 事件     |---------------------+
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
|  DomainAPI + Jog RPCs (§4 待 TM 實作)|
+--------------------------------------+
```

---

## Sample 631

**Source**: `TM_Program_Analysis_v0\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L80

```
使用者在統一 UI 按「存點」
  ├─ (1) gRPC SavePointFromCurrent / UpdatePointPartial → TMflow 專案檔
  └─ (2) 同步更新 GYRO YAML 對應 waypoint → Git commit (optional hook)
```

---

## Sample 632

**Source**: `TM_Program_Analysis_v0\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L206

```
tmflow_domain_client/
├─ proto/
│  └─ TmDomainService.proto          # 從 TM release 拷貝
├─ _generated/                        # grpc_tools.protoc 產出
│  ├─ TmDomainService_pb2.py
│  └─ TmDomainService_pb2_grpc.py
├─ client.py                          # Channel / stub 管理
├─ session.py                         # TeachSession context manager
├─ teach.py                           # 高階 helpers (jog_cartesian, save_point, ...)
├─ models.py                          # dataclass 對應 proto message
└─ tests/
   ├─ test_with_mock_server.py        # 用 grpcio testing 起 mock server
   └─ test_integration.py             # 需連真機，gated by env var
```

---

## Sample 633

**Source**: `TM_Program_Analysis_v0\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L256

```
hid_input/
├─ backends/
│  ├─ pygame_backend.py         # Windows/macOS/Linux 通用（搖桿、手把）
│  ├─ hidapi_backend.py         # 底層 HID（自製裝置、SpaceMouse）
│  └─ evdev_backend.py          # Linux-only，低延遲踏板
├─ profiles/                    # YAML profile 目錄（使用者可擴充）
│  ├─ xbox_dual_analog.yaml
│  ├─ spacemouse_compact.yaml
│  ├─ linemaster_3pedal.yaml
│  └─ schema.json               # profile 語法驗證
├─ intents.py                   # intent 事件 dataclass 定義
├─ translator.py                # HID event → intent (profile-driven)
├─ dispatcher.py                # intent → 統一 UI event bus
├─ watchdog.py                  # 連續 jog safety watchdog
└─ tests/
   ├─ test_profile_loader.py
   ├─ test_translator.py        # 用錄製的 HID event 檔重播
   └─ test_watchdog.py
```

---

## Sample 634

**Source**: `TM_Program_Analysis_v0\docs\VISION_ARCHITECTURE.md` L15

```
.job XML ────► parse_job_file() ──┐
                                   ├─► VisionJob[] ──► analyze_vision() ──► VisionAnalysis
profile XML ─► enrich_from_profile()┘                                              │
                                                                                   ▼
.flow JSON ─► FlowGraph.get_vision_node_info() ─► FlowAnalysis.vision_node_info    │
                                       │                                             │
                                       └──► tm_doc_generator ◄─────────────────────┘
                                                  │
                                                  ├─► VISION_SYSTEM_ANALYSIS.md
                                                  ├─► VISION_JOB_MAP.md
                                                  └─► subflows/*.md（Vision 區段）
```

---

## Sample 635

**Source**: `TM_Program_Analysis_v0\docs\VISION_ARCHITECTURE.md` L246

```
experiments/baseline/        ← TM Flow 匯出的最簡 Vision Job
experiments/exp_NN_<name>/   ← 改一項設定後的快照
        │
        ▼
scripts/vision_schema_diff.py
        │
        ▼
docs/findings/exp_NN_*.md    ← 自動 diff 報表
        │
        ▼
docs/VISION_SCHEMA_FINDINGS.md  ← 累積知識庫
```

---

## Sample 636

**Source**: `TM_Program_Analysis_v0\experiments\README.md` L8

```
experiments/
├── README.md          ← 本檔
├── baseline/          ← 共用 baseline vision dir（由 TM Flow 匯出）
├── exp_01_<name>/     ← 每個實驗一個子資料夾
├── exp_02_<name>/
└── ...
```

---

## Sample 637

**Source**: `TM_Program_Analysis_v0\INDEX.md` L77

```
data/
├── ConfigData.xml
├── GlobalVariable.xml
├── Projects/GYRO_FT_RobotARM_Micron_v_0_0_15/
│   ├── *.flow                ← 主 Flow JSON
│   └── bak/                  ← 歷史備份
└── Vision/
    ├── jobs/GYRO_FT_RobotARM_Micron_v_0_0_15/
    │   ├── 35536500.job      ← 68 個 Vision Job 主檔
    │   └── <jobcode>/<jobcode>.xml  ← 各 Job 的 recognition profile
    └── ...
```

---

## Sample 638

**Source**: `TM_Program_Analysis_v0\INDEX.md` L114

```
experiments/
├── README.md            ← 工作流程說明
├── baseline/            ← TM Flow 匯出的最簡 Vision Job baseline
└── exp_NN_<name>/       ← 每個 GUI 設定變更的快照
```

---

## Sample 639

**Source**: `TM_Program_Analysis_v0\README.md` L7

```
├── src/                 Python 工具原始碼
├── scripts/             輔助工具（schema diff 等）
├── data/                TM 解壓資料（從 archive/ 重建）
├── archive/             TM 匯出原始壓縮（.zip + .z01）
├── output/              自動產生的分析文件
├── docs/                文件、官方手冊、findings/
└── experiments/         Vision schema 反向實驗工作區（不入庫）
```

---

## Sample 640

**Source**: `UR_Program_Analysis_v0\docs\COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 641

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L41

```
                    ┌──────────────────┐
    RTDE (reg 0-2)  │   PLC / MES      │
   ◄───────────────►│  (外部控制器)  │
                    └──────────────────┘
                            │
                    ┌───────┴───────┐
                    │    UR30       │
                    │ (Polyscope)   │
                    └──┬───┬───┬───┘
          Modbus TCP   │   │   │  RS485
       ┌───────────────┘   │   └──────────────┐
       ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ PLC/IO 模組  │  │  SensoPart   │  │ TC100 Gripper    │
│ 192.168.1.1  │  │  VISOR       │  │ + RS485 IO Box   │
│ Modbus TCP   │  │  XML-RPC     │  │ Tool Modbus      │
│ port 502     │  │  port 46527  │  │ addr 1,2         │
└──────────────┘  └──────────────┘  └──────────────────┘
```

---

## Sample 642

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L130

```
var_read_RTDE ≔ read_input_integer_register(0)
    │
    ├─ 30001：初始化歸位（開夾 → 依位置回 Home_L 或 Home_R）
    ├─ 30000：移動到啟動位（p_for_startup）
    ├─ 30002：開夾 → 回 Home_R
    ├─ 30009：Fork 感測器檢查
    └─ 其他 ：進入自動作業模式
```

---

## Sample 643

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L142

```
解析外部指令 → 讀取 RS485 IO → 判斷 port_direction
    │
    ├─ port_direction = 1（入料方向）
    │   ├─ to_port_type = 1（Erack）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put（取放 Body）
    │   │   ├─ turnL 路徑轉向（若需跨區）
    │   │   └─ Erack_load_unload
    │   │
    │   ├─ to_port_type = 2（EQ2600 系列）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put
    │   │   └─ EQ2600_port{1-4}_{load/unload}
    │   │
    │   ├─ to_port_type = 3（EQ2800 系列）
    │   │   ├─ VISOR 拍照定位
    │   │   ├─ Body_take_put
    │   │   └─ EQ2800_port{1-4}_{load/unload/swap}
    │   │
    │   ├─ to_port_type = 4（EQ2845）
    │   │   └─ EQ2845_port1_load_unload
    │   │
    │   └─ to_port_type = 5（EQ3670）
    │       └─ EQ3670_port{1-2}_{load_unload/backup}
    │
    └─ port_direction = 2（出料方向）
        └─ （與入料對稱，順序反轉）
```

---

## Sample 644

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L330

```
K11_UR30_Project/programs/
├── Gyro/                           # 核心與輔助
│   ├── initial_prog.script/.txt    # 主程式入口（12,241 行）
│   ├── initial_modbus_tcp.script   # Modbus TCP 訊號定義
│   ├── tc100_gripper_open.script   # 夾爪開啟
│   ├── tc100_gripper_close.script  # 夾爪關閉
│   ├── fork_sensor_check.script    # Fork sensor 檢查
│   ├── payload.script              # Payload 計算
│   ├── set_alarm_and_stop.script   # 統一錯誤處理
│   ├── get_command_*.script        # 指令解析
│   ├── gripeer_cover_*.script      # 蓋子開關
│   ├── Loop.script / Loop_initial.script  # 迴圈計數器
│   └── rs485io_read.script         # RS485 IO 讀取
├── Body_*.script/.txt              # Body 取放
├── EQ*.script/.txt                 # 各設備操作
├── Erack_*.script/.txt             # Erack 裝卸
├── .SensoPart/calibsets/*.calib    # VISOR 校正
└── *.urp                           # 二進位程式（未解析）
```

---

## Sample 645

**Source**: `UR_Program_Analysis_v0\docs\FLOW_ANALYSIS.md` L361

```
initial_prog (主程式)
├── Body_take_put
├── Erack_load_unload
├── EQ2600_port1_load / port2_unload / port3_load / port4_unload
├── EQ2800_port{1-4}_{load/unload/swap}
├── EQ2800P02_port{1-4}_{load/unload/swap}
├── EQ2845_port1_load_unload
├── EQ3670_port{1-2}_load_unload
├── EQ3800_port1_load_unload
└── [helpers]
    ├── tc100_gripper_open / close
    ├── gripeer_cover_open / close / open_180
    ├── fork_sensor_check
    ├── payload
    ├── set_alarm_and_stop
    ├── initial_modbus_tcp
    ├── get_command_extra_info / portname
    ├── rs485io_read
    └── Loop_initial / Loop
```

---

## Sample 646

**Source**: `UR_Program_Analysis_v0\docs\PHASE2_SPEC.md` L526

```python
# ── 常數 ──
UR30_DH_PARAMS: list[dict]  # [{"a": float, "d": float, "alpha": float}, ...]

# ── 正向運動學 ──
def forward_kinematics(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> list[float]:
    """由關節角度計算末端姿態。
    
    Args:
        joints: [j1, j2, j3, j4, j5, j6]（弧度）
        dh_params: 可選 DH 參數覆蓋，None 使用 UR30 預設
    Returns:
        [x, y, z, rx, ry, rz]（公尺, 弧度 — axis-angle 表示法）
    """

def forward_kinematics_matrix(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> 'numpy.ndarray':
    """由關節角度計算 4x4 齊次變換矩陣。
    
    Returns:
        4x4 numpy array
    """

# ── 逆向運動學 ──
def inverse_kinematics(
    pose: list[float],
    q_near: list[float] | None = None,
    dh_params: list[dict] | None = None
) -> list[list[float]]:
    """由末端姿態計算關節角度（最多 8 組解）。
    
    Args:
        pose: [x, y, z, rx, ry, rz]（公尺, axis-angle 弧度）
        q_near: 偏好解（選最接近此組的解），None 則回傳所有解
        dh_params: 可選 DH 參數覆蓋
    Returns:
        關節角度解的列表，每個解為 [j1..j6]
        如果 q_near 有值，只回傳最接近的一組（list 長度 1）
    """

# ── 工具函式 ──
def pose_to_matrix(pose: list[float]) -> 'numpy.ndarray':
    """axis-angle pose → 4x4 齊次矩陣。"""

def matrix_to_pose(matrix: 'numpy.ndarray') -> list[float]:
    """4x4 齊次矩陣 → axis-angle pose。"""

def rotation_vector_to_matrix(rvec: list[float]) -> 'numpy.ndarray':
    """axis-angle [rx, ry, rz] → 3x3 旋轉矩陣（Rodrigues 公式）。"""

def matrix_to_rotation_vector(R: 'numpy.ndarray') -> list[float]:
    """3x3 旋轉矩陣 → axis-angle [rx, ry, rz]。"""

# ── 驗證函式 ──
def validate_waypoint(
    waypoint: 'URWaypoint',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> dict:
    """驗證一個 waypoint 的 pose 和 joints 是否一致。
    
    用 FK(joints) 計算出 pose，與宣告的 pose 比較。
    
    Args:
        waypoint: URWaypoint 物件
        tolerance_mm: 位置容差（毫米）
        tolerance_deg: 角度容差（度）
    Returns:
        {
            "name": str,
            "valid": bool,
            "position_error_mm": float,
            "orientation_error_deg": float,
            "fk_pose": list[float],    # FK 計算的 pose
            "declared_pose": list[float],  # 宣告的 pose
            "details": str  # 人類可讀的描述
        }
    """

def validate_all_waypoints(
    project: 'URProject',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> list[dict]:
    """驗證專案中所有 waypoint。
    
    Returns:
        驗證結果列表（同 validate_waypoint 的 return 格式）
        只包含有 pose 和 joints 都有值的 waypoint
    """

def generate_validation_report(results: list[dict]) -> str:
    """產生 Markdown 格式的驗證報告。
    
    報告結構：
    ## Waypoint FK/IK 驗證報告
    - 統計：總數 / 通過 / 失敗 / 跳過（缺 pose 或 joints）
    - 失敗清單（表格：名稱、位置誤差、角度誤差、來源檔案）
    - 通過清單（摘要）
    """
```

---

## Sample 647

**Source**: `UR_Program_Analysis_v0\docs\TM_UR_COMPLETED_SUMMARY.md` L313

```
Web/HMI UI
  ↓ gRPC (Proto3)
gRPC Middleware Server
  ├─ GYRO 離線解析模組（Python，呼叫 ur_tree_parser / ur_script_editor 等）
  └─ 硬體即時通訊模組（RTDE / Modbus）
       ↓                    ↓
  task.gyro.yaml        Robot Controller
  (Git，唯一真實來源)    (UR / Techman 實體)
```

---

## Sample 648

**Source**: `UR_Program_Analysis_v0\README.md` L8

```
├── src/                 Python 工具原始碼
├── data/                UR 程式資料（從 K11_UR30_Project 複製）
├── archive/             UR 匯出原始壓縮（.zip）
├── output/              自動產生的分析文件
└── docs/                手動撰寫的分析文件
```

---

## Sample 649

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L51

```
sensor_msgs/Image (深度圖, 16UC1 or 32FC1)
  +
sensor_msgs/CameraInfo (相機內參)
        │
        ▼
  ┌─────────────────────────────────────────────────────┐
  │  ⓪ 預計算查找表 (LUT)  — 僅在啟動/參數變更時執行一次 │
  │                                                     │
  │  對每個像素 (u, v) 預先計算:                        │
  │    • ray_x = (u - cx) / fx                          │
  │    • ray_y = (v - cy) / fy                          │
  │    • 水平角度 angle = atan2(ray_x, 1.0)             │
  │    • 對應的 angular bin index                       │
  │    • 地平面高度係數 (用於快速高度計算)              │
  └─────────────────┬───────────────────────────────────┘
                    │ (一次性, 啟動時)
                    ▼
  ┌─────────────────────────────────────────────────────┐
  │  ① 地平面校正  — 啟動時收集 N 幀，RANSAC 擬合一次 │
  │                                                     │
  │  校正完成後，對每個像素預計算:                      │
  │    height_coeff[u,v] = (a·ray_x + b·ray_y + c) / ‖n‖│
  │  使得: 像素高度 = depth × height_coeff[u,v] + d/‖n‖ │
  └─────────────────┬───────────────────────────────────┘
                    │ (一次性, 校正後)
                    ▼
  ┌─────────────────────────────────────────────────────┐
  │  ② 單次遍歷核心（每幀執行）                        │
  │                                                     │
  │  for each pixel (u, v):                             │
  │    depth = depth_image[v][u]                        │
  │    if depth < range_min or depth > range_max:       │
  │        continue                  // 距離無效        │
  │                                                     │
  │    height = depth × height_coeff[u][v] + d_offset   │
  │    if height < h_min or height > h_max:             │
  │        continue                  // 高度不在避障範圍 │
  │                                                     │
  │    bin = bin_index_lut[u]        // 查表取角度 bin  │
  │    range = depth × range_coeff[u][v]  // 水平距離   │
  │                                                     │
  │    if range < scan[bin]:                            │
  │        scan[bin] = range         // 保留最近點      │
  │                                                     │
  └─────────────────┬───────────────────────────────────┘
                    │
                    ▼
          sensor_msgs/LaserScan (虛擬 2D LiDAR)
```

---

## Sample 650

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L263

```
    ┌───────────────┐
    │  UNCONFIGURED │
    └──────┬────────┘
           │ on_configure():
           │   • 載入參數
           │   • 初始化 subscriber / publisher
           │   • 等待第一幀 CameraInfo
           ▼
    ┌───────────────┐
    │   INACTIVE    │
    └──────┬────────┘
           │ on_activate():
           │   • 收到 CameraInfo → 建立 bin_index LUT
           │   • 開始收集校正幀
           ▼
    ┌───────────────┐
    │  CALIBRATING   │  收集 N 幀 → 取樣 → RANSAC
    │                │  → 建立 height_coeff + range_coeff LUT
    └──────┬────────┘
           │ 校正完成 → 發布 calibration_done = true
           ▼
    ┌───────────────┐
    │    ACTIVE      │  每幀: 讀深度圖 → 單次遍歷 → 發布 LaserScan
    └───────────────┘
           │ recalibrate_ground service
           ▼
         回到 CALIBRATING
```

---

## Sample 651

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L301

```
桌面 GPU (RTX 4090):
  CPU RAM ←── PCIe 4.0 (32 GB/s) ──→ GPU VRAM (24GB)
  → 必須顯式 cudaMemcpy，延遲高

Jetson Thor:
  ┌──────────────────────────────────────┐
  │   128 GB LPDDR5X 統一記憶體          │
  │   (273 GB/s 頻寬)                    │
  │                                      │
  │   CPU 可存取 ◄──────► GPU 可存取   │
  │   同一塊實體記憶體，無需拷貝         │
  └──────────────────────────────────────┘
  → cudaMallocManaged / 零拷貝映射直接共享
```

---

## Sample 652

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L321

```
┌─────────────────────────────────────────────────────────────┐
│                    GPU Memory (統一記憶體)                 │
│                                                            │
│  ┌───────────────┐    ┌───────────────┐    ┌─────────────┐ │
│  │ Depth Any V3  │    │   LUT 常數    │     │  scan_bins  │ │
│  │ TensorRT 輸出 │     │ (啟動時上傳)  │     │ (~650 floats│ │
│  │               │    │              │     │             │ │
│  │ float[H×W]    │    │ height_coeff │     │ 初始: inf   │ │
│  │ (已在 GPU)    │    │ range_coeff  │     │ atomicMin   │ │
│  │               │    │ bin_index    │     │ 更新        │ │
│  └───────────────┘    └──────┬───────┘     └──────┬──────┘ │
│         │                    │                    │        │
│         └─────────┬──────────┘                    │        │
│                   ▼                               │       │
│         ┌──────────────────┐                      │        │
│         │  CUDA Kernel     │──── 寫入 ───────────→│       │
│         │  depth_to_scan   │                               │
│         │  (307K threads)  │                               │
│         └──────────────────┘                               │
│                                                            │
└─────────────────────────────────────────────────────────────┘
                                                      │
                        cudaMemcpy D→H 僅 1.4 KB       │
                        (或直接統一記憶體讀取)          │
                                                      ▼
                                              ┌──────────────┐
                                              │  ROS 2 發布   │
                                              │  LaserScan    │
                                              │  (CPU 端)     │
                                              └──────────────┘
```

---

## Sample 653

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L555

```
時間軸 →

TensorRT stream:  [===推論===]
                              │ cudaEventRecord(trt_done)
                              ▼
Scan stream:                  │ cudaStreamWaitEvent(trt_done)
                              │
                              ├─ reset_scan_bins <<<1,256>>>        (~0.001 ms)
                              │
                              ├─ depth_to_scan <<<(20,60),(32,8)>>> (~0.2 ms)
                              │
                              ├─ cudaStreamSynchronize              (~0.01 ms)
                              │
                              └─ CPU: 讀 scan_bins (統一記憶體)      (~0.001 ms)
                                 → 填入 LaserScan message
                                 → 發布到 /virtual_scan

單幀總延遲: ~0.3 ms（不含 TensorRT 推論）
```

---

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

---

## Sample 655

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L707

```
                        v1 路徑（冗餘）
                    ┌─ Depth Image → PointCloud2 ─→ virtual_lidar_node
Depth Anything V3 ─┤
(TensorRT)          └─ Depth Image ─────────────────→ virtual_lidar_node
                        v2 路徑（直接）
```

---

## Sample 656

**Source**: `WebCamToLidarScan\docs\REQUIREMENTS.md` L963

```
時間軸 →

TensorRT stream:  [===推論===]
                             │
Scan stream:                 ├─ reset_scan_bins          (~0.001 ms)
                             ├─ depth_to_scan            (~0.2 ms)
                             ├─ apply_ema_filter         (~0.001 ms)  ← 新增
                             ├─ cudaStreamSynchronize
                             │
CPU:                         ├─ 讀 filtered_bins          (~0.001 ms)
                             ├─ ego-motion 合併（如啟用）  (~0.3 ms)   ← 新增
                             └─ 發布 LaserScan

單幀總延遲:
  無時間融合: ~0.3 ms
  +EMA:       ~0.3 ms（無感）
  +Ego-motion: ~0.6 ms（仍遠低於目標 3 ms）
```

---

## Sample 657

**Source**: `WebCamToLidarScan\docs\TECHNICAL.md` L370

```
Per-frame breakdown (current):
  AI depth inference:    ~80ms   (GPU, DmlExecutionProvider)  ← bottleneck
  Depth-to-scan (LUT):  ~1ms    (CPU, numpy vectorized)
  EMA filter:            ~0.5ms  (CPU, ~650 bins)
  IMU processing:        ~0.1ms  (CPU)
  Ground calibration:    ~50ms   (one-time at startup)
  ──────────────────────────────
  Total:                ~82ms/frame = ~12 FPS
```

---

## Sample 658

**Source**: `WebCamToLidarScan\README.md` L15

```
深度圖 (640×480)
    │
    ├─ 啟動時一次 ─→ RANSAC 地平面校正 → 建立 LUT
    │
    └─ 每幀執行 ──→ 逐像素: 查 LUT → 高度過濾 → 角度分割 → 取最近點
                                                              │
                                                              ▼
                                                   Raw LaserScan (~650 bins)
                                                              │
                                              ┌───────────────┼───────────────┐
                                              │ (可選)         │ (可選)       │
                                              ▼               ▼               ▼
                                           EMA 濾波     中位數濾波    Ego-motion
                                          (自適應平滑)  (抗異常值)    多幀拼接
                                              │               │          (擴展 FOV)
                                              └───────────────┼───────────────┘
                                                              ▼
                                                     LaserScan 發布
```

---

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

---
