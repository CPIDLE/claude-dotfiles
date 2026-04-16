## Sample 260

**Source**: `personal-rag_v2\PKB\vault\docs\UR-Program-Analysis\docs\FLOW_ANALYSIS.md` L142

```
解析外部指令 --> 讀取 RS485 IO --> 判斷 port_direction
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

