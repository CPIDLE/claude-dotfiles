## Sample 116

**Source**: `D455_LidarScan\README.md` L250

```
Flat ground:                    Pit encountered:

line0: ─────────────────        line0: ────────╲    ╱──────
line1: ─────────────────        line1: ──────────╲╱────────
       (both stable,                   (line0 sees into pit first,
        Δrange ~= constant)              Δrange spikes)

Bump encountered:               Slope / ramp:

line0: ─────╱╲──────────        line0: ──────────────╲╲╲
line1: ───╱╲────────────        line1: ──────────────╲╲╲
       (line1 hits bump first,         (both shift together,
        Δrange drops)                   Δrange ~= constant)
```

