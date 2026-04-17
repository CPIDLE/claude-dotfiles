## Sample 599

**Source**: `StockSage_v0\docs\ARCHITECTURE.md` L308

```
├── Train (500 days) ──┤ Val (60) ┤  ← Worker 1
            ├── Train (560 days) ──┤ Val (60) ┤  ← Worker 2
                        ├── Train (620 days) ──┤ Val (60) ┤  ← Worker 3
                                    ...          ← Worker 4~8
```

---

