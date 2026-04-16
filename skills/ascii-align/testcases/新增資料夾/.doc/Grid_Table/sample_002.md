## Sample 002

**Source**: `ai-sdk-fix\architecture\stream-text-loop-control.md` L60

````
┌────────────────────────────────────────────────────────────┐
│           FUNNEL IN: N STEP STREAMS                        │
│          (sequential, not parallel)                        │
└────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐            ┌──────────────┐
│   Step 0     │  │   Step 1     │            │   Step N     │
│   model.do   │  │   model.do   │            │   model.do   │
│   Stream()   │  │   Stream()   │    ...     │   Stream()   │
└──────┬───────┘  └──────┬───────┘            └──────┬───────┘
       │                 │                           │
 tool callbacks    tool callbacks              tool callbacks
       │                 │                           │
 tool execution    tool execution              tool execution
       │                 │                           │
 step metadata     step metadata               step metadata
 + start/finish    + start/finish              + start/finish
       │                 │                           │
       v                  v                            v 
┌────────────────────────────────────────────────────────────┐
│        addStream()    addStream()         addStream()      │
│                                                            │
│                   STITCHABLE STREAM                        │
│     (sequential queue -- consumes one at a time,           │
│      next step added on recursion from flush)              │
└─────────────────────────┬──────────────────────────────────┘
                          │
══════════════════════════╪═══════════════════════════════════
                          │
             ┌────────────┴────────────────────────┐
             │         MIDDLE PIPELINE             │
             │    (single linear transform chain)  │
             └────────────┬────────────────────────┘
                          │
                          v 
                  resilient stream
             (abort handling + start event)
                          │
                          v 
                      stop gate
                 (stopStream() support)
                          │
                          v 
                   user transforms
               (experimental_transform[])
                          │
                          v 
                   output transform
               (enrich w/ partialOutput)
                          │
                          v 
                   event processor
                 (onChunk, onStepFinish,
                  accumulate content,
                 resolve delayed promises)
                          │
══════════════════════════╪═══════════════════════════════════
                          │
        ┌─────────────────┴─────────────────────┐
        │      FUNNEL OUT: ON-DEMAND .tee()     │
        │                                       │
        │             BASE STREAM               │
        │    (each .tee() splits into two:      │
        │     one for consumer, one remains     │
        │     as baseStream for next tee)       │
        │                                       │
        │   each can be called multiple times   │
        └──┬─────┬──────┬────┬──────┬────┬──────┘
           │     │      │    │      │    │
           v      v       v     v       v     v 
         text  full  partial elem   UI  consume
        Stream Stream Output Stream Msg  Stream
                      Stream       Stream
        (text  (all  (json (output (maps (drains
        deltas parts) parse) spec) to UI) stream,
        only)                             resolves
                                          promises)
````