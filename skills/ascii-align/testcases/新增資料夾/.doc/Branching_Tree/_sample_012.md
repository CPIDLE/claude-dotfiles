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
│                  ROS Master (port 11311)                         │
│              rosbridge (port 9090, WebSocket)                    │
├─────────────────────────────────────────────────────────────────┤
│  Hardware: USB2CAN / EtherCAT NIC / RS485 / RealSense / LIDAR  │
└─────────────────────────────────────────────────────────────────┘
```

---
