## Sample 452

**Source**: `Reporter_v1\WORKSPACE\a02\AMR_Log_to_SQLite_遷移方案.md` L426

```
[瀏覽器] 匯出鈕
  --> POST /getlogzipfile/               (AGVWeb/webextjs.py:5935 getLogZipFile)
  --> Unix socket mysocket.s              (car_info/reset_connection/ReadSocket.py:13-27)
  --> ROS service LogGatherSrv(requestname, {startdate, enddate})
  --> syswork/scripts/loggathering.py LogGatherServer (line 545)
       兩個分支都會走相同 collect+zip 流程：
       ├─ TSCGatheringFile  分支 (line 554)  <-- 一般 log 匯出
       └─ GatheringFile     分支 (line 582)  <-- E84 完整匯出
       共同步驟：
       ├─ ReloadGatherLogPathFile  <-- 讀 loggather.json 白名單（用於來源檔案搜集）
       ├─ shutil.rmtree + mkdir(LogDestFolder)
       ├─ TSCCollectFile(start, end)  <-- 把符合 filter/fileextension 的檔案複製到 LogDestFolder
       └─ TSCZipFolder(LogDestFolder, ...) --> YYMMDD_YYMMDD_HHMMSS_$ROBOT.zip
  --> /getlogzipfilebyname/<name> 下載
```

