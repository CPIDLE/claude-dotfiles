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

## 發送訊息（push）——這個 bot 不是唯讀的

`AnnSinHome_v0/app/line_api.py` 有現成的 `push(to, text)` / `reply(reply_token, text)` async 函式，走 LINE Messaging API（`https://api.line.me/v2/bot/message/push`），憑證是 `LINE_CHANNEL_ACCESS_TOKEN`（跟 `gas_query.py` 用的 GAS 憑證是完全不同的兩組，不要混用）。`to` 填 `group_id`（見下方對照表）即可推到指定群組，文字上限 4900 字元。

**獨立腳本已包好**：`scripts/gas_query.py` 旁邊的 `scripts/line_push.py`（deploy 後在 `~/.claude/docs/line-data-sop/scripts/line_push.py`），純標準庫、不需要 repo 環境：

```bash
python scripts/line_push.py push <group_id> --text "<文字>"          # 預設 dry-run，只印出會送什麼，不會真的發
python scripts/line_push.py push <group_id> --text "<文字>" --send   # 確認過內容才加 --send 真的送出
python scripts/line_push.py push <group_id> --file msg.txt --send    # 多行/特殊字元時用 --file 比 shell 參數安全
```

Token 讀取順序：環境變數 `LINE_CHANNEL_ACCESS_TOKEN` → `~/.claude/.env` 的 `ANNSINHOME_LINE_CHANNEL_ACCESS_TOKEN`（尚未實際同步，長期可攜路徑）→ 本機 `AnnSinHome_v0/.env`（目前唯一有這個值的地方，只在跑 docker-compose 那台 PC 上）。

**重要限制，動手前一定要跟使用者確認過**（腳本預設 dry-run 就是為了這個）：
- 訊息會顯示是 **AnnSinHome bot 帳號**發的，不是使用者本人——群組成員看到的署名是 bot，不是本人
- LINE 沒有內建收回/刪除 API 給這個場景，**發出去就送出去了**，沒有事後補救的路
- 屬於「發訊息給他人／影響共享狀態」的高風險動作類別，每次要送都要先讓使用者看過最終文字內容並明確同意，不能因為前一次做過就當作長期授權——**不要因為腳本存在就跳過確認直接加 `--send`**

## 已知 group_id 對照表

`groups` 表的 `display_name` 欄位目前都是 `NULL`（沒有被寫入過），**不能**靠這欄位對應群組名稱。目前唯二可行的辨識方法：

1. **內容比對（土法）**：`SELECT group_id, COUNT(*), (取幾筆 text 樣本) FROM messages GROUP BY group_id`，人工看訊息內容猜是哪個群——這是本文件目前記錄下面對照表的方法，準確但費工
2. **官方 API（更可靠，尚未在任何腳本裡實際跑過）**：`line_api.py` 有 `get_group_summary(group_id)`，打 `GET /v2/bot/group/{group_id}/summary` 直接拿到真正的 `groupName`——如果 1 的土法對不準或要批次核對，優先用這個

已確認的對照範例格式（實際 ID/群組名屬個人資料，**不放公開 repo**——真實對照表維護在 `~/.claude/docs/line-data-sop.md` 本機版，查到新的就回填在那邊）：

| group_id | 群組 |
|---|---|
| `<group_id_1>` | （範例）某群組說明 |
| `<user_id 開頭是使用者，非 group_id>` | 個人 1:1 |

其餘 group_id 尚未核對，需要時用上面兩種方法之一辨認，**確認後回填本機版對照表**，別每次都重新猜。

## 已知 user_id 對照表

`users` 表的 `display_name` 有正常寫入（跟 `groups` 不同），可以直接 `SELECT user_id, display_name FROM users WHERE display_name LIKE '%關鍵字%'` 查，不需要土法比對。真實查到的 user_id/display_name 對照（同上，屬個人資料，**不放公開 repo**）維護在本機版：

| user_id | display_name |
|---|---|
| `<user_id_1>` | （範例）某成員說明 |

要撈某人風格範本（例如「他習慣怎麼分享文章」），用 `messages.user_id` + `group_id` 篩，只挑 `text LIKE '%http%'` 的訊息看格式（開場方式、有沒有摘要、連結放哪、有沒有 emoji），不用整批全讀。
