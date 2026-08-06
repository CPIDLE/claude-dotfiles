# 團隊分享信（.tips）製作與發佈 SOP

`.tips/` 是寄給團隊的 Claude Code 使用心得分享信原稿資料夾，**本身不進 repo**（已 `.gitignore`，因含真實收件人名單）。這份文件是把 `.tips/README.md` 裡「怎麼做」的方法搬進 `docs/`，即使 `.tips/` 內容之後清空或改版，這套流程仍留在這裡可查。實際的收件名單、Drive 資料夾連結等個人化設定，只存在本機 `.tips/README.md`。

## 檔案結構與命名

```
.tips/
├── A01-slug.md                      <- 標準化 Markdown 稿（主要維護這個）
├── A01-slug.html                    <- Gmail draft 用的渲染 HTML
├── A01-slug-附件slug.md             <- 附件（範例報告、補充資料，同 prefix）
└── .template/
    ├── A01-claude-memory.md         <- 視覺基準原稿
    ├── [...].eml                    <- 視覺基準寄出版
    └── _TEMPLATE.html               <- HTML 樣式骨架，A03 起都以此為底
```

- **編號**：`A01`、`A02`... 依序遞增，不重用。
- **分類**（信件主旨用）：`環境` / `工作流` / `技巧` / `案例` / `其他`。
- **slug**：英文小寫短詞對應主題，例：`claude-memory`、`pm-review-redteam`。
- **附件**：跟主檔同 prefix 再加描述，一封信可有多個附件。

## 標準 Markdown 模板

```markdown
# [分享 A0N-分類] 標題

> GYRO SYSTEMS · INTERNAL SHARING
> 副標題 · YYYY-MM-DD
> 作者：<姓名>

---

Hi 團隊,

（一段話開場：做了什麼、為什麼分享、本文涵蓋什麼。）

## 一、XXX（中文數字做大章節）

內文 / 對照表 / ASCII 圖。

## 二、XXX

**① 粗體加圈號做要點**
說明。

## N、一句話總結

> **重點 A** 是 X，
> **重點 B** 是 Y ——
> 兩者配合的結論。

有興趣想深入討論，歡迎再找我聊。

Best,
**<姓名>**
GYRO SYSTEMS, INC.

---

**參考資料：**
- <https://...>
- 工具版本 / 關鍵資訊
```

## HTML 渲染規則

Gmail 渲染**必須走 inline styles**（`<style>` block 會被 Gmail 剝掉），見 [[feedback_gmail_inline_styles]]。做法：複製 `_TEMPLATE.html` 骨架 → 改檔名 `A0N-slug.html` → 把 `{{...}}` 佔位符換成內容 → 用 mailbox 專用 skill 建成 Gmail draft（`--html`）。

`_TEMPLATE.html` 是從最早一篇寄出版本反推出來的品牌樣式骨架，之後每篇一律沿用，不要重新發明：

- 主色深紅磚 + 橘色漸層（GYRO 品牌色）
- 卡片底灰、表格 zebra、code 反白
- max-width 760px，系統字體（`-apple-system` / `Segoe UI` / `Microsoft JhengHei`）
- Header 左邊條、H2 底邊框、表格 header 反白、三色建議卡片（① 主 / ② 中 / ③ 輔）

## 內容風格守則

1. **ASCII box-drawing only**：圖用 `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`，禁 Unicode 箭頭、emoji、厚框（見全域 CLAUDE.md「ASCII Art Diagrams」）。
2. **對照表用 Markdown table**，不要用空格硬排。
3. **圈號要點用 `① ② ③ ④ ⑤`**（信件風格的例外用法）。
4. **路徑/指令用反引號**標記。
5. **粗體標關鍵詞**，不要整段粗體。
6. **避免過時資訊**：版本號、連結寄出前重新確認。

## 發信流程

1. 寫 `A0N-slug.md` 並定稿。
2. **把定稿的 `.md`（連同附件）上傳到團隊共用的 Drive 資料夾**，信件內容固定帶這個資料夾連結。
   - **Why：** 信件轉寄進 mailing list（尤其訂閱者用 Digest 摘要模式的 Google Group）排版會整個跑掉，這是平台行為、寄件端無法避免。固定帶 Drive 資料夾連結，不管怎麼轉寄/摘要都還能點進去找到原始內容。
   - **傳 `.md` 不要 `.eml`**：`.eml` 在 Drive 只會顯示原始 MIME 原始碼、瀏覽器打不開；`.md` 點開就是純文字，不用額外工具。
   - Drive 資料夾連結是固定的，不用每篇另外產生專屬連結重傳。
3. 轉成 HTML 草稿（見上「HTML 渲染規則」）。
4. 從 Gmail 介面手動補附件、檢查、寄出。

## Mailbox fallback 順序

**預設用工作信箱**寄，失敗才 fallback 到個人信箱：

1. 先用工作信箱對應的 mailbox skill 建草稿。
2. 若工作信箱不通（OAuth 失效、Workspace 政策擋、API 錯誤等），改用個人信箱，並在回覆裡明確告知使用者「已 fallback 到個人信箱」。
3. 純測試/預覽用途仍可直接走個人信箱。
4. 寄工作版時 CC 自己（工作信箱）留存一份；寄個人版時 CC 個人信箱留存。

## 個人化設定（不進 repo）

以下只存在本機 `.tips/README.md`，**不寫進這份 SOP**（公開 repo，避免外洩真實聯絡資訊）：

- 實際收件人名單（姓名 + email）
- 共用 Drive 資料夾的實際連結
- 寄件/CC 用的真實信箱地址

新機或需要查這些設定時，直接讀本機 `.tips/README.md`；若該檔不存在（例如換了一台沒同步過 `.tips/` 的機器），比照 [[project_new_machine_install]] 的思路——這類個人化設定本來就不隨 install script 走，得手動補。

## 相關記憶

- [[project_tips_folder]] — Google Group Digest 轉寄跑版的原始 incident 記錄
- [[feedback_gmail_inline_styles]] — Gmail inline style 限制
- [[feedback_docs_consistency]] — README / email / docs 內容要跨管道一致
