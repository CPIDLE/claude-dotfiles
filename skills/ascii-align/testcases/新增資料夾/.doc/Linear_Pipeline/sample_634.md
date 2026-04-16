## Sample 634

**Source**: `TM_Program_Analysis_v0\docs\VISION_ARCHITECTURE.md` L15

```
.job XML ─────> parse_job_file() ────┐
                                   ├──> VisionJob[] ───> analyze_vision() ───> VisionAnalysis
profile XML ──> enrich_from_profile()┘                                               │
                                                                                   v 
.flow JSON ──> FlowGraph.get_vision_node_info() ──> FlowAnalysis.vision_node_info    │
                                     │                                           │
                                       └───> tm_doc_generator <──────────────────────┘
                                                  │
                                                  ├──> VISION_SYSTEM_ANALYSIS.md
                                                  ├──> VISION_JOB_MAP.md
                                                  └──> subflows/*.md（Vision 區段）
```

