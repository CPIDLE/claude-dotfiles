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

