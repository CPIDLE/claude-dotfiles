## Sample 622

**Source**: `TM_Program_Analysis_v0\docs\HT_9046LS_TMMARK_NORMAL_ANALYSIS.md` L264

```
IF: g_place_again == true?
  ├─ [YES] --> 重置 count=0 --> 繼續（允許重試放置）
  └─ [NO]  --> Log ERROR --> SET: error_code=1014 --> STOP
```

