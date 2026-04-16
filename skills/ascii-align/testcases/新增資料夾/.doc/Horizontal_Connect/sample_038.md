## Sample 038

**Source**: `AMRCoolDown_v0\調查方法手冊.md` L462

```
Phase 1：環境探索（SSH 指令為主）
  ├── 系統資訊 --> lscpu, free, uptime, df
  ├── CPU 概覽 --> vmstat, top batch
  ├── 記憶體概覽 --> free, ps --sort=-%mem
  ├── Docker 容器 --> docker ps, docker stats
  ├── ROS 環境 --> rosnode list, rosversion
  └── 輸出：Phase1_環境探索報告.md

Phase 2：原始碼深度分析（SSH + Git + /proc）
  ├── 從 CodeCommit clone repo（syswork, routemap, AGVWeb）
  ├── 從 /proc/<PID>/root/ 撈取非 repo 的原始碼（canbus）
  ├── rosparam get 驗證車上實際參數 vs 程式碼預設
  ├── rostopic hz 驗證 topic 發布頻率
  ├── 5 次 top batch 取樣取中位數
  ├── grep -r 搜尋程式碼中的關鍵 pattern
  └── 輸出：Phase2_原始碼分析報告.md

Phase 3：優化建議整理（本地分析為主）
  ├── 對照原始碼 + 即時數據，產出修改建議
  ├── 安全影響分析（最壞情況評估）
  ├── Bug 報告（程式碼品質問題）
  └── 輸出：Phase3_程式優化建議報告.md

審核：多輪交叉驗證
  ├── 獨立審核 agent 進行紅隊式否定審查
  ├── 每輪審核產出補充驗證指令
  ├── 執行補充指令後更新報告
  └── 輸出：Phase1_2_審核報告.md（初審 --> 二審 --> 三審）
```

