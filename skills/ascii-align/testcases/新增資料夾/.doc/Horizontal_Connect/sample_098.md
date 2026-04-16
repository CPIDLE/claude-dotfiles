## Sample 098

**Source**: `D435i_LidarScan\README.md` L88

```
Side view:
    Camera ──── horizontal ────
      ╲  ╲
  line0 ╲  ╲ line1        Flat ground: both lines stable, D range ~= constant
   (a °)  ╲  ╲ (a +D °)     Pit:  line0 range jumps --> D range spikes
          ╲  ╲             Bump: line1 range drops --> D range dips
───────────╲──╲──── ground
```

