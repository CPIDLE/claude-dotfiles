# 影片轉圖文文章 SOP

把 YouTube 課程講座影片轉成一篇圖文並茂的繁體中文 Markdown 文章。本流程已在 Stanford CS329A 全系列 9 支影片上驗證過，可直接依此 SOP 執行。

> 原始出處：`Reporter_v1/WORKSPACE/a1j/製作流程.md`——這份是知識搬移，不綁定任何特定專案，即使來源專案未來被刪，流程本身仍在這裡可用。用到的兩支腳本已抽成真正的 `.py` 檔，放在同目錄的 `video-to-article-sop/scripts/`，不用從文件裡現拆現貼。

## 需求環境

- `yt-dlp`（下載影片與字幕）
- `ffmpeg`（場景偵測擷取截圖）
- `python3` + `PIL`（Pillow）+ `numpy`（清理字幕、建索引、去重用）
- 一個能派 `Agent` / `Workflow` 的 AI 助手（分段與逐段寫作用）

## 產出結構

```
partN/
├── article.md              # 最終產物：文章本體 + 內嵌圖片
└── frames/
    └── selected/            # 最終產物：文章實際引用的截圖
```

> 中間產物（`downloads/` 影片與字幕、`frames/raw/` 候選截圖、逐字稿、CSV 索引等）只在製作過程中需要，完成後全部刪除，見步驟八。

---

## 步驟一：下載影片與字幕

```bash
mkdir -p partN/downloads partN/frames/raw partN/frames/selected
cd partN/downloads
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" \
  --write-auto-sub --sub-lang en --convert-subs vtt \
  --merge-output-format mp4 -o "video.%(ext)s" "<影片網址>"
```

畫質 ≤1080p 已足夠看清投影片文字。若一次處理多支影片，下載可平行跑（背景執行時**不要**同時用 shell 的 `&` 又疊加工具自己的背景模式，兩者擇一，否則進度追蹤會失準）。

## 步驟二：清理逐字稿

YouTube 自動字幕是「捲動字幕」格式：同一句話會被拆成好幾個 cue block、且每個 block 常包含「上一句的殘留 + 這句新增的幾個字」。清理邏輯是**只取每個 block 的最後一行文字，並跳過與前一次輸出相同的重複行**——已寫成現成腳本 `scripts/clean_vtt.py`（跟本文件同目錄，deploy 後在 `~/.claude/docs/video-to-article-sop/scripts/clean_vtt.py`），直接執行不用重新現拆現貼：

```bash
python scripts/clean_vtt.py partN/downloads/video.en.vtt partN/downloads/transcript_clean.txt
```

一支 70 分鐘講座通常會從約 3000-3700 條原始 cue 清理成約 1800-1900 行乾淨逐字稿。

## 步驟三：擷取候選投影片截圖

```bash
ffmpeg -i partN/downloads/video.mp4 \
  -vf "select='gt(scene,0.35)',showinfo" -vsync vfr \
  partN/frames/raw/slide_%04d.png > partN/frames/scene_log.txt 2>&1
```

場景偵測（畫面變化幅度 > 0.35 才存檔）比固定間隔取樣更貼近「投影片換頁」的時機。正常情況下 70 分鐘影片會抓到約 50-150 張候選圖。

**已知例外**：若影片是 Zoom／瀏覽器錄影（畫面四周有大片黑邊、投影片只占中間一小塊），0.35 的門檻可能完全抓不到任何 scene change（黑邊稀釋了整體畫面差異）。若 `grep -c "pts_time:" scene_log.txt` 結果是 0，改用更低門檻重跑（例如 0.05、0.04），抓到 40-60 張左右即可，不需要精確調到某個數字。

再從 log 建立時間戳索引——已寫成現成腳本 `scripts/build_frame_index.py`：

```bash
python scripts/build_frame_index.py partN/frames/scene_log.txt partN/frames/raw partN/frames/frame_index.csv
```

## 步驟四：候選截圖去重（可選）

用感知雜湊（average hash，16x16 灰階 + 平均亮度二值化）比對每張候選圖與前一張**保留下來**的圖，Hamming 距離 ≤ 8 視為重複、捨棄。實務上場景偵測抓到的候選圖本來就已經是換頁瞬間，**這一步在絕大多數影片上不會刪掉任何東西**，可以視為安全網而非必要步驟——除非遇到步驟三提到的黑邊型影片，這種情況下全畫面比對會被黑邊主導、誤判大量正常換頁為重複，此時應**跳過去重、直接把完整候選清單交給下一步**。

## 步驟五：交給一個 agent 做分段

把清理過的逐字稿丟給一個 agent，請它讀完整份逐字稿、依主題切成 6-9 段，回傳 JSON：

```json
[{"title": "分段標題", "startTs": "HH:MM:SS", "endTs": "HH:MM:SS"}, ...]
```

不需要自己通讀逐字稿再手動切，交給 agent 判斷即可；多支影片的分段可以平行派多個 agent 同時做。

## 步驟六：平行生成段落文字與挑圖（Workflow）

用 `Workflow` 工具，把步驟五的分段結果**寫死成 JS 陣列直接放進腳本檔**（不要用 `args` 參數傳遞，實測會失敗），對每一段平行派一個 sub-agent，同時做兩件事：

1. 讀該段時間範圍內的逐字稿，重新組織寫成一段通順繁體中文（不是逐句翻譯，去掉口語贅字）
2. 讀該段時間範圍內的候選截圖，挑 1-2 張最能代表內容、畫面清晰的，複製到 `frames/selected/` 並依段落編號重新命名（如 `03_1.png`）

Workflow 腳本要點：
- 用 `schema` 參數強制 agent 回傳 `{paragraph, imagesUsed}` 的結構化 JSON
- 內建 `isValid()` 檢查：段落長度、是否為 "test" 等佔位文字、是否混入 `</parameter>` `</invoke>` 這類工具呼叫殘留字串
- 用 `try/catch` 包住 `agent()` 呼叫並搭配 `for` 迴圈重試（`MAX_ATTEMPTS = 3`）——`agent()` 內部的 schema 驗證重試上限（預設 5 次）用盡時會直接 throw，若不用 `try/catch` 接住，`parallel()` 會把該段結果靜默變成 `null`，必須額外處理才能被自訂重試邏輯抓到並重跑
- 完成後務必實際 `ls frames/selected/` 核對檔案數與 `imagesUsed` 是否一致，不要只信 agent 回傳的 JSON

## 步驟七：組裝文章

依段落順序,把每段文字 + 對應截圖組合進 `article.md`(Markdown,圖片用相對路徑指向 `frames/selected/`),開頭附上影片標題、講者、課程連結、課程網站等資訊。組裝前用腳本核對文章裡引用的每張圖片檔名,在 `frames/selected/` 底下都真的存在,避免有段落選了圖但檔案沒複製成功。

## 步驟八：完成後清理中間產物

確認 `article.md` 與所有截圖都沒問題後,只保留 `article.md` 與文章實際引用到的 `frames/selected/*.png`,其餘全部刪除：

```bash
rm -rf partN/downloads
rm -rf partN/frames/raw
rm -f partN/frames/*.csv partN/frames/*.txt partN/frames/*.log
# 順便清掉 frames/selected 裡沒被 article.md 引用到的圖（例如 agent 選了但後來沒用上的檔案）
```

刪除前務必先確認 `article.md` 存在且非空、圖片引用都對得上，再執行刪除，避免刪掉還沒完成的半成品。

---

## 已知問題與應對

| 問題 | 原因 | 應對 |
|---|---|---|
| Workflow 用 `args` 傳資料失敗 | 工具限制 | 資料寫死在腳本檔裡 |
| 平行 agent 回傳 "test" 等佔位文字 | 候選圖太多、agent 負擔過重，或單純隨機失誤 | Workflow 內建 `isValid()` + 自動重試 |
| `agent()` schema 驗證重試上限用盡直接 throw | 內部重試機制與自訂重試邏輯是兩層,不會自動被外層 catch | 外層加 `try/catch`，抓到後照樣重跑；若重跑仍失敗，改派一個不用 schema、純文字輸出的 `Agent` 補救 |
| 場景偵測在某支影片抓到 0 張候選圖 | Zoom／瀏覽器錄影黑邊稀釋畫面差異 | 降低 `scene` 門檻重跑（0.35 → 0.05 附近） |
| 感知雜湊去重誤刪大量候選圖 | 全畫面比對被黑邊主導 | 該類影片跳過去重步驟 |
| 段落文字混入 `</parameter>` 等殘留字串 | agent 生成內容時意外回聲工具呼叫語法 | `isValid()` 檢查排除，或組裝文章時人工去除 |
| 背景執行進度追蹤失準 | shell `&` 疊加工具自帶背景模式 | 兩者擇一，不要同時用 |

## 檢查清單

- [ ] `downloads/video.en.vtt` 清理後行數是否落在合理區間（約原始 cue 數的一半）
- [ ] 候選截圖數量是否落在合理區間（約 40-150 張／70 分鐘）；若為 0 需調整場景門檻
- [ ] 每個段落的 `imagesUsed` 是否都能在 `frames/selected/` 找到對應檔案
- [ ] `article.md` 全文讀過一次，確認無佔位文字、無工具呼叫殘留字串、圖文對應正確
- [ ] 完成後只剩 `article.md` + `frames/selected/`，其餘中間產物已刪除
