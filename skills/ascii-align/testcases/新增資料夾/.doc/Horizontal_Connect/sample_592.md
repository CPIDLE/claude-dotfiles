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

