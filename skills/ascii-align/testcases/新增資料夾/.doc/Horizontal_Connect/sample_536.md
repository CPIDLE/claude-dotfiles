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
├─ translator.py                # HID event --> intent (profile-driven)
├─ dispatcher.py                # intent --> 統一 UI event bus
├─ watchdog.py                  # 連續 jog safety watchdog
└─ tests/
   ├─ test_profile_loader.py
   ├─ test_translator.py        # 用錄製的 HID event 檔重播
   └─ test_watchdog.py
```

