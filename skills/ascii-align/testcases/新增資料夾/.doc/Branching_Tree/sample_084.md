## Sample 084

**Source**: `D435i_LidarScan\FLOW.md` L69

```
Available presets (--lidar-model):
┌──────────────┬─────────────────┬───────┬───────────┬───────────────┬───────┐
│ Key          │ Name            │ FOV   │ Res (deg) │ Range (m)     │ Steps │
├──────────────┼─────────────────┼───────┼───────────┼───────────────┼───────┤
│ hokuyo_urg   │ Hokuyo URG-04LX │ 240°  │ 0.36      │ 0.02 - 5.6    │ 683   │
│ hokuyo_utm   │ Hokuyo UTM-30LX │ 270°  │ 0.25      │ 0.1  - 30.0   │ 1081  │
│ hokuyo_ust   │ Hokuyo UST-10LX │ 270°  │ 0.25      │ 0.06 - 10.0   │ 1081  │
│ rplidar_a2   │ RPLIDAR A2      │ 360°  │ 0.45      │ 0.15 - 12.0   │ 800   │
│ sick_tim561  │ SICK TiM561     │ 270°  │ 0.33      │ 0.05 - 10.0   │ 811   │
│ custom       │ (user-defined)  │ 87°*  │ user      │ user          │ user  │
└──────────────┴─────────────────┴───────┴───────────┴───────────────┴───────┘
* custom mode uses D435i's native ~87° FOV

Note: D435i has ~87° HFOV. Only that angular portion has real data.
      Bins outside D435i coverage = inf (no data).
```

