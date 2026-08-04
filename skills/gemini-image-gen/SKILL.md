---
name: gemini-image-gen
description: >
  Generate polished infographic-style images (especially dense Traditional
  Chinese text) via the Gemini API. Use when the user wants an infographic,
  diagram-as-image, or business-presentation-style graphic generated or
  iterated on programmatically instead of clicking through a chat UI.
  Trigger when: /gemini-image-gen, 生成資訊圖表, infographic, Gemini 生圖,
  Nano Banana Pro, 圖生圖.
argument-hint: "[--prompt-file p.md | --prompt \"text\"] --out out.png [--size 4K] [--ref ref.png]"
---

# gemini-image-gen

用 Gemini API 生成資訊圖表／簡報風格圖片，可程式化迭代（改 prompt 檔重跑，不用在瀏覽器裡重新點擊）。

## 關鍵發現

1. **模型要選對，不然中文會亂碼**：
   - `gemini-2.5-flash-image`（Nano Banana）：密集中文文字渲染會出現大量錯字/亂碼，**不能用**在文字量大的 infographic
   - `gemini-3-pro-image`（Nano Banana Pro，本 skill 預設）：文字渲染品質接近 gemini.google.com 網頁版，這才是對的選擇
   - 查詢一把 key 實際能用哪些模型：`GET https://generativelanguage.googleapis.com/v1beta/models?key=<KEY>`，篩 `supportedGenerationMethods` 含 `generateContent` 且名稱含 image/nano 的項目

2. **文字量要精簡，不然字級被迫縮小、模糊**：每張卡片條列壓到最多 2 條、案例最多 2 個，寧可少寫也不要塞滿——這比事後要求「加大字體」有效，因為版面空間是模型自己排的，塞太滿字級就會被自動縮小。

3. **解析度要另外指定，不然預設偏低、文字邊緣模糊**：本腳本用 `--size 4K` 帶 `generationConfig.imageConfig.imageSize`。4K 輸出約 5500×3100，檔案 5-8MB，文字邊緣清晰。已知部分第三方 proxy 會忽略這個欄位，直接打 REST API（本腳本做法）才可靠。

4. **風格要在 prompt 裡明講「像 ChatGPT/DALL-E 商業簡報圖」**，並具體描述「圖示要有柔和陰影、不要死板線框」——不然預設風格偏扁平，圖示質感明顯不如 ChatGPT 版。完整範例見 `references/example_prompt.md`。

## 用法

```bash
# 標準呼叫（4K，最終品質）
python ~/.claude/skills/gemini-image-gen/scripts/gemini_image_gen.py --prompt-file prompt.md --out out.png --size 4K

# 快速測試改動（不指定 --size，較快但解析度較低）
python ~/.claude/skills/gemini-image-gen/scripts/gemini_image_gen.py --prompt-file prompt.md --out draft.png

# 圖生圖／以現有圖為底做局部修改
python ~/.claude/skills/gemini-image-gen/scripts/gemini_image_gen.py --prompt-file p.md --out v2.png --ref 上一版.png

# 換模型（不建議換回 flash-image，中文會亂碼）
python ~/.claude/skills/gemini-image-gen/scripts/gemini_image_gen.py --prompt-file p.md --out out.png --model gemini-3-pro-image
```

Key 讀取順序：環境變數 `GEMINI_API_KEY` → 找不到就讀 `~/.claude/.env` 裡的 `GEMINI_API_KEY`。

## 迭代流程

1. 寫 / 改 prompt 檔（`references/example_prompt.md` 是完整結構範例：標題區／流程列／卡片區／底部列／配色與風格，換主題複製結構即可）
2. 不帶 `--size` 先跑一次快速看效果（省時間）
3. 確認方向對了，再帶 `--size 4K` 跑正式版
4. 檔名遞增版本號（`_v6`、`_v7`…），比對後把過時版本標成 archived，只留最新一版

## 已知的坑

- 瀏覽器下載按鈕點了沒反應：Chrome 下載預設路徑可能設在專案資料夾本身，不是系統 Downloads
- 想從頁面 JS 直接 fetch blob URL 抓圖：base64 大量資料抽取會觸發安全機制擋下，改用「使用者自己在瀏覽器下載」這條路才成功
- `gemini-2.5-flash-image` 是預設看起來最直覺的名字，但實際上是舊代、文字弱的那顆，容易誤用
