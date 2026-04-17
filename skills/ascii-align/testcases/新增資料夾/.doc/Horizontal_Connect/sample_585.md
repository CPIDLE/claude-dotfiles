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

