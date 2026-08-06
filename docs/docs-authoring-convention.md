# docs/ 靜態 SOP 撰寫規範

`docs/` 是 `/mem-skill` 搜尋的知識庫（見 `commands/mem-skill.md`）。那份文件講的是「怎麼搜」，這份講「怎麼寫」——目前的慣例是從既有檔案（`line-data-sop.md`、`video-to-article-sop.md`、`tips-sharing-sop.md`）歸納出來的隱性模式，沒有正式文件化過，這份把它寫死，之後新增 SOP 有依據可查。

## 什麼進 docs/，什麼不進

- **進 docs/**：跟 skill 同等知識密度的靜態內容——SOP、schema、查詢方法、設計文件。不常駐 context，不掛進 skill 清單，只靠 `/mem-skill` 手動全文搜尋觸發。
- **不進 docs/**：
  - 個人化設定／敏感資訊（真實姓名、email、內部連結、Drive/Sheet ID 等）——這個 repo 是 **public**，見 [[feedback_repo_no_personal_config]]、[[feedback_secrets_move_atomic]]。個人 ID 放 `~/.claude/.env`，不寫進任何會 commit 的檔。
  - 會頻繁變動的「進行中」狀態（進度、待辦、下一步）——這類屬於 memory 或 plan，不是靜態 SOP。

## 命名

- **知識搬移／操作流程類**：`<主題>-slug>-sop.md`（例：`line-data-sop.md`、`video-to-article-sop.md`、`tips-sharing-sop.md`）
- **純敘述型設計文件／清單**：不加 `-sop` 尾綴（例：`plugins.md`、`pm-guide.md`、`repo-health-checklist.md`）
- 帶時間快照性質的（一次性體檢、評估報告）可加日期尾綴：`<主題>-YYYY-MM-DD.md`（例：`ai-self-checkup-2026-06-22.md`）

## 開頭結構

1. **標題**（`# `）：一句話點出主題，這是 `/mem-skill` 搜尋時第一眼判斷相關性的依據。
2. **第一段**：主題範圍 + 一句「知識搬移」註記——原始出處是哪個專案/來源，並強調「即使該來源未來被刪，這份文件仍可用」。這條是刻意的：docs/ 存在的理由就是讓知識脫離會消失的專案生命週期獨立留存。
   > 範例（`video-to-article-sop.md`）：「原始出處：`Reporter_v1/WORKSPACE/a1j/製作流程.md`——這份是知識搬移，不綁定任何特定專案，即使來源專案未來被刪，流程本身仍在這裡可用。」

## 內文

- **可搜尋性優先**：`/mem-skill` 是全文 grep + 語意過濾，不依賴 frontmatter/tag，關鍵字自然落在標題、第一段、章節標題就夠，不用刻意堆關鍵字。
- **步驟型 SOP** 用「步驟一／步驟二...」章節切分，每步驟可獨立執行、可獨立驗證。
- **參照型文件**（schema、對照表）用 Markdown table，不用空格硬排。
- **相關記憶**：文末可加一節列 `[[memory-name]]` 連結，把 docs/（跨專案靜態知識）跟 memory（per-project 動態脈絡）互相牽起來，見主 memory body 結構規則。

## 腳本

若 SOP 需要配套腳本，另開 `<檔名不含副檔名>/scripts/` 子目錄放真正的 `.py`/`.sh` 檔，不把整段程式碼貼在 md 裡當程式碼區塊——deploy 後路徑是 `~/.claude/docs/<slug>/scripts/`，文件裡用相對路徑指過去即可（例：`video-to-article-sop/scripts/`）。

## 敏感內容的替代寫法

遇到「流程需要提及但內容敏感」的狀況（收件人名單、內部連結、真實 ID），不要略過不寫，也不要硬塞進 repo：

- 在 docs/ 裡寫清楚「這類設定存在哪裡」（例：`~/.claude/.env`、本機某個 gitignored 資料夾），但不寫實際值。
- 若該資訊只存在本機且不隨 install 走，比照 [[project_new_machine_install]] 的思路提醒「換機器要手動補」。

參考範例：`tips-sharing-sop.md` 的「個人化設定（不進 repo）」一節。

## 檢查清單（新增一份 docs/ SOP 前）

- [ ] 檔名符合命名規則，主題一看就懂
- [ ] 開頭有「知識搬移」註記（原始出處 + 脫離來源專案獨立留存）
- [ ] 全文沒有真實姓名/email/內部連結/ID 等敏感內容
- [ ] 配套腳本（若有）抽成真正的檔案，不整段貼 md
- [ ] 文末視情況補「相關記憶」連結

## 相關記憶

- [[feedback_repo_no_personal_config]] — repo 不放個人設定的原則
- [[feedback_secrets_move_atomic]] — 搬 ID／secrets 要同步改所有讀取端
- [[feedback_docs_consistency]] — README / email / docs 內容跨管道要一致
