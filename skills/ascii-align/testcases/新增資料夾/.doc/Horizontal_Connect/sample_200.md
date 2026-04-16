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
│   ├── batt_monitor.launch --> battery_monitor (1 Hz)
│   ├── relative_monitor.launch --> move_relative_monitor
│   ├── modbus_monitor.launch --> modbus_monitor (0.5 Hz) + tm_arm_status_check
│   ├── safety_monitor.launch --> safety_monitor (0.5 Hz)
│   ├── carvel_monitor.launch --> carvel_monitor (10 Hz)
│   ├── camera_monitor.launch --> camera_monitor (0.1 Hz)
│   ├── dashcam_monitor.launch --> dashcam_monitor (0.5 Hz)
│   ├── slot_monitor.launch --> slot_monitor (20 Hz ! )
│   ├── path_log.launch --> path_log
│   ├── tag_log.launch --> TagLog
│   ├── network_monitor.launch --> network_monitor (5+ threads)
│   ├── wirelesscharger_monitor.launch --> wirelesscharger_monitor
│   ├── get_imu_log.launch --> get_imu_log
│   ├── rosparam_monitor.launch --> rosparam_monitor (60s)
│   ├── system_info_monitor.launch --> system_info_monitor (0.5 Hz)
│   ├── cpu_monitor.launch --> cpu_monitor_new (0.2 Hz + threads)
│   ├── disk_health_monitor.launch --> disk_health_monitor (0.001 Hz ! )
│   ├── automode_action_control.launch --> automode_action_control
│   └── mqtt_bridge.launch --> mqtt_bridge (1 Hz)
├── logclear.launch
│   └── log_clear (0.004 Hz)
├── loggathering.launch
│   └── loggathering (0.05 Hz, sync ! )
└── griptmEMO.launch
    └── griptmEMO (10 Hz)

routemap.launch (separate)
├── armdooraction
├── processjson_server
├── routemap (10 Hz, 343KB ! )
└── Tag_position_recovery (10 Hz)

ethercat SOEM_m.launch (container 2)
└── motor_control (C++, sudo, 50~1000 Hz)

canopen_control.launch (container 3)
├── canopen_controller (100 Hz ! )
├── canopen_log (10 Hz)
└── canopen_motor_data_logger
```

