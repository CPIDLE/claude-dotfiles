## Sample 007

**Source**: `AMRCoolDown_v0\AMR_撞機事件根因分析.md` L262

```
每日磁碟消耗估算：
├── 4 台相機錄影（streamfile.py）
│   └── 15 fps x  4 cam x  86400 sec x  ~50KB/frame = ~250 GB/天（未壓縮）
│       （壓縮後估 ~5-25 GB/天，取決於 codec）
├── ROS log（output="screen" x  38 節點）
│   └── 估 ~500 MB ~ 2 GB/天
├── CSV 日誌（syswork 各 monitor）
│   └── 估 ~100~500 MB/天
└── 合計：數 GB ~ 數十 GB/天

Day 3: 磁碟接近滿 --> write() 阻塞
       --> 所有含 file I/O 的節點卡住
       --> loggathering.py 的 os.system("sync") 阻塞 10+ 秒
       --> 系統凍結 --> 導航中斷
```

