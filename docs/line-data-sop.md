# 家庭 LINE 群組記錄查詢 SOP

家庭 LINE 群組（AnnSinHome bot）的訊息/媒體記錄存放位置、schema、怎麼查。原始專案：`AnnSinHome_v0`——這份文件是知識搬移，即使該 repo 或本機部署未來被刪，「怎麼建、怎麼查」這套方法仍留在這裡。

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
- **格式**：SQLite，WAL 模式

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

## 完整部署/設定（GAS 部署步驟、LINE Developers Console、token 輪替）

不在此重複——這份文件只保留「資料在哪、怎麼查」這種穩定不變的知識；部署細節會隨專案演進變動，見來源專案 `AnnSinHome_v0/README.md`（若當下仍存在）。
