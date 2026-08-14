# 家庭 LINE 群組記錄查詢 SOP

家庭 LINE 群組（AnnSinHome bot）的訊息/媒體記錄存放位置、schema、怎麼查。原始專案：`AnnSinHome_v0`——這份文件是知識搬移，即使該 repo 或本機部署未來被刪，「怎麼建、怎麼查」這套方法仍留在這裡。

**適用範圍不只家庭群**：同一份 log（同一個 Sheet、同一支 GAS）也收 bot 所在的**工作群組**訊息，查工作專案的群一樣走這份文件，差別只在 `group_id`。標題寫「家庭」是因為專案起源如此，不代表資料範圍。

## 架構概覽

```
LINE 群組 → Google Apps Script Web App（雲端 24/7，不受本機開關機影響）
              ├─ Google Sheet「AnnSinHome Log」：log / users / groups 三個 tab
              └─ 媒體即時抓取 → Google Drive AnnSinHome/{群名}/{年}/{月}/

本機 PC（docker compose 常駐，開機時跑）
  ├─ 每 5 分鐘 pull Sheet 新列 → 本機 SQLite
  └─ 每日備份 DB → Drive（保留 14 天）
```

PC 關機不影響接收——雲端 GAS 24/7 收訊，開機後 sync 自動補齊，只影響「多久才同步到本機 SQLite」。

## 資料庫位置與 Schema

- **路徑**：`<AnnSinHome_v0 repo>/data/annsinhome.db`（docker-compose 用 `./data:/app/data` volume 掛進容器，host 上直接讀這個檔案就是即時資料，不需要進容器）
- **格式**：SQLite，journal_mode=DELETE（單 worker + 寫入已用 lock 序列化，不需要 WAL；2026-08-06 前是 WAL，因 Docker Desktop for Windows 的 volume 會讓 WAL 的 `-wal`/`-shm` 檔案存取失效才改掉，見下方）

| 表 | 用途 | 關鍵欄位 |
|---|---|---|
| `messages` | 每則訊息 | `message_id`(PK) / `group_id` / `user_id` / `session_id` / `type` / `text` / `timestamp` / `reply_to_message_id` / `raw_event`（完整原始 JSON） |
| `sessions` | 對話段（同群組訊息間隔 > 30 分鐘切新 session） | `session_id`(PK) / `group_id` / `started_at` / `ended_at` / `message_count` / `summary` |
| `users` | 成員快取 | `user_id`(PK) / `display_name` / `picture_url` |
| `groups` | 群組 Drive 資料夾段快取 | `group_id`(PK) / `folder_seg`（首次見到就釘住，之後群組改名也沿用同資料夾）/ `display_name` |
| `files` | 媒體檔上傳狀態 | `message_id`(FK) / `drive_file_id` / `drive_web_link` / `drive_path` / `mime_type` / `upload_status`（pending/uploaded/failed/expired） |
| `meta` | key-value 設定快取 | `key` / `value` |

> **命名陷阱**：SQLite 端叫 `messages`/`sessions`，Google Sheet 端對應的 tab 叫 `log`——雲端跟本機落地用不同名字指同一份資料，別搞混。

## 常見查詢

```bash
# 某群組最新 N 則
sqlite3 <repo>/data/annsinhome.db \
  "SELECT timestamp, text FROM messages WHERE group_id='<id>' ORDER BY timestamp DESC LIMIT 20;"

# 關鍵字搜尋（例：「找 3 個月沒吃過但之前常吃的晚餐」這類問題的資料源）
sqlite3 <repo>/data/annsinhome.db \
  "SELECT timestamp, text FROM messages WHERE group_id='<id>' AND text LIKE '%晚餐%' ORDER BY timestamp;"

# 依對話 session 瀏覽摘要
sqlite3 <repo>/data/annsinhome.db \
  "SELECT started_at, ended_at, message_count, summary FROM sessions WHERE group_id='<id>' ORDER BY started_at DESC;"
```

- **多群組**：`group_id` 是分區鍵，多個家庭群組天生分開存，不用額外過濾
- **去重**：`message_id` 是 PK，LINE webhook redelivery 不會造成重複列
- **原始 JSON**：`messages.raw_event` 存完整 LINE event，schema 之外需要的欄位可以從這裡挖

## 本機 SQLite 找不到時（換一台電腦、或本機查詢失敗）

`data/annsinhome.db` **只存在跑 docker-compose 的那台 PC 上**（目前是主機那台，路徑 `AnnSinHome_v0/data/annsinhome.db`）。在其他電腦上找不到這個檔案是正常狀況，不是資料遺失——直接跳過本機 SQLite，去查雲端來源。這條路徑不需要 `AnnSinHome_v0` repo、不需要 docker，任何裝了 Python 的電腦都能跑：

- **文字訊息／對話記錄** → 直接打 GAS Web App 的 pull API（本機 sync 用的就是同一支），比本機 SQLite 更即時（本機每 5 分鐘才 sync 一次，Sheet 是 GAS 即時寫入）。用 `scripts/gas_query.py`（跟本文件同目錄，deploy 後在 `~/.claude/docs/line-data-sop/scripts/gas_query.py`）：
  ```bash
  python scripts/gas_query.py latest <group_id>      # 某群組最新一則
  python scripts/gas_query.py pull --after 1 --limit 200   # 原始分頁拉取，含 groupId/groupName 對照
  python scripts/gas_query.py health                 # 只想知道 log 表目前總列數
  ```
- **媒體檔（照片/影片/文件）** → Google Drive `AnnSinHome/{群名}/{年}/{月}/`，每群一個資料夾，可直接當相簿瀏覽，不用查資料庫
- 不知道 `group_id` 對應哪個群組：`pull` 結果每列都帶 `groupId` + `groupName`，掃一批就能對照
- GAS 的 302 轉址間歇性 404（Google 端已知 flaky 行為，同組請求連跑會時好時壞，跟哪個 HTTP client 無關）——`gas_query.py` 已內建 retry，正常不用管；萬一連 3 次都失敗才是真的異常

**這台電腦沒有 `GAS_PULL_URL`/`GAS_TOKEN` 這兩個值時**：`gas_query.py` 會自動讀 `~/.claude/.env` 的 `ANNSINHOME_GAS_PULL_URL` / `ANNSINHOME_GAS_TOKEN`（見 `.env.example`）——這份 `.env` 本來就是裝 claude-dotfiles 時該手動同步好的機密清單，不用為這兩個值另外想辦法。真的兩邊都沒設，跟有的那台要，或問使用者，不要用猜的或留空硬跑。

## 查詢報 `disk I/O error`

2026-08-06 曾因 WAL 模式在 Docker Desktop for Windows 的 volume 上失效而發生，已改成 `journal_mode=DELETE` 修掉根因（見上方 schema 說明）。若之後又出現同類錯誤：檢查 `PRAGMA journal_mode` 是不是又被改回 WAL；真的查不到才退回 Google Sheet/Drive（見上一節）。

## 完整部署/設定（GAS 部署步驟、LINE Developers Console、token 輪替）

不在此重複——這份文件只保留「資料在哪、怎麼查」這種穩定不變的知識；部署細節會隨專案演進變動，見來源專案 `AnnSinHome_v0/README.md`（若當下仍存在）。
