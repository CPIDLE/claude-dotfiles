# 長篇 Markdown 的可跳轉目錄（含 Notepad++ MarkdownPanel 對策）

給幾百行以上、章節多的 Markdown 檔（專案紀錄、SOP、會議逐則紀錄）加一份**點得動**的目錄。重點不在「產生目錄」——那部分很簡單——而在**anchor 在不同 renderer 下行為不一致**，尤其 Notepad++ 的 MarkdownPanel 外掛預設完全跳不動。

原始出處：某長篇專案紀錄檔的目錄需求（本機專案目錄，不進 repo）。這份是知識搬移，不綁定任何特定專案，即使來源專案未來被刪，做法本身仍在這裡可用。

配套腳本：`markdown-toc-sop/scripts/md_toc.py`（deploy 後為 `~/.claude/docs/markdown-toc-sop/scripts/md_toc.py`）。

## 為什麼不能只靠自動 anchor

多數 renderer 會替標題自動產生 id，但**產法各家不同**，中文標題尤其歧異：

| Renderer | 標題 id 怎麼來 | 中文標題的下場 |
|---|---|---|
| GitHub / GitLab | 小寫、去標點（含全形括號冒號）、空白轉 `-`、CJK 保留 | 可用，id 是中文 |
| VS Code 預覽 | 類似 GitHub，另有自己的標點清單 | 可用 |
| Notepad++ MarkdownPanel（Markdig） | `UseAdvancedExtensions` → AutoIdentifiers，**預設帶 `AllowOnlyAscii`** | **中文字被整串剝掉**，純中文標題退化成 `section` / `section-1` |

所以「照 GitHub 規則算 slug 寫進目錄」在 MarkdownPanel 下必然對不上。**解法是不要讓 renderer 決定 id ——自己把 `<a id="...">` 寫進標題。**

## MarkdownPanel 的第二層問題：連結被取消

就算 id 對上了，MarkdownPanel 仍然點不動。反組譯外掛的 `Webview2Viewer.dll` 可以看到兩個關鍵設計：

- 預覽內容是用 `document.body.innerHTML = '...'` 注入更新的
- `NavigationStarting` 事件會 `set_Cancel` ——外掛靠這個把外部連結攔下來丟系統瀏覽器

點 `#anchor` 在 WebView2 眼中就是一次 navigation → **被攔截取消 → 什麼都不會發生**。

連帶的推論：**在 md 裡塞 `<script>` 也救不了**。HTML 規範明訂經由 `innerHTML` 插入的 `<script>` 不執行，所以那條路在這個外掛下是死的。

可行的是 **inline event handler**——它是屬性，跟著 innerHTML 一起生效：

```html
- <a href="#thread-9" onclick="document.getElementById('thread-9').scrollIntoView();return false;">Thread 9：...</a>
```

`return false` 讓瀏覽器不觸發 navigation，改由 JS 直接捲動，繞過取消機制。同時保留 `href="#id"`，所以在 GitHub / VS Code（會把 `onclick` 濾掉）仍走原生 anchor —— **一份檔案兩邊都能點**。

## 做法

### 步驟一：產目錄 + 寫入 anchor

```bash
python ~/.claude/docs/markdown-toc-sop/scripts/md_toc.py FILE.md
```

腳本會：

1. 掃 h2~h3 標題（可用 `--max-level` 調整），**自動跳過 code fence 內的假標題**
2. 標題沒有 anchor 的補上 ` <a id="..."></a>`，**已經有的保留不動**
3. 在第一個標題前插入 `<!-- TOC -->` … `<!-- /TOC -->` 包住的目錄區塊

常用參數：

| 參數 | 用途 |
|---|---|
| `--max-level 2` | 只收 h2，章節多時目錄才不會爆長 |
| `--plain` | 只產純 Markdown 連結，不加 `onclick`（確定不用 MarkdownPanel 時） |
| `--dry-run` | 只印目錄不寫檔 |
| `--title 索引` | 改目錄標題文字（預設「目錄」） |

### 步驟二：把 id 改成看得懂的名字（選作，但建議）

純中文標題會拿到 `sec` / `sec-1` / `sec-2` 這種流水號 id（ASCII slug 算完是空的）。手動把它們改成語意化名稱會好用很多：

```
## 待辦 / 未回覆事項 <a id="todo"></a>
### A. 最高優先 <a id="todo-a"></a>
```

改完**再跑一次腳本**即可——它會認得既有 id 並沿用，目錄連結自動跟著更新。這也是為什麼腳本刻意不覆寫既有 anchor：**id 一旦被別的文件或訊息引用就不該再變**。

### 步驟三：改了標題之後重跑

新增/刪除/搬動章節後重跑同一行指令。目錄區塊被標記包住，會整塊重生；標題既有 anchor 不動，所以外部連結不會斷。

## 驗證

```python
import re
lines = open('FILE.md', encoding='utf-8').read().split('\n')
ids   = {m.group(1) for l in lines for m in re.finditer(r'<a id="([\w-]+)"></a>', l)}
links = {m.group(1) for l in lines for m in re.finditer(r'href="#([\w-]+)"', l)}
print('壞連結:', sorted(links - ids))
```

`壞連結` 應為空。實際點擊仍要在目標 renderer 裡確認一次——尤其換了 MarkdownPanel 版本之後。

## 已知限制

- **只處理 h2~h6**：h1 當作文件標題不收。
- **inline `onclick` 在嚴格 CSP 環境會被擋**。放進靜態網站（Jekyll/Hugo/Docusaurus）前先用 `--plain` 重產，那些環境的原生 anchor 本來就正常。
- **MarkdownPanel 的 `RenderingEngine`**：本做法在 `EDGE`（WebView2）下驗證過。切回 IE11 引擎的行為未測。
- 目錄區塊靠 `<!-- TOC -->` / `<!-- /TOC -->` 定位，**不要手動刪掉標記**，否則重跑會在檔案裡插入第二份目錄。

## 相關記憶

- [[feedback_docs_consistency]] — 同一份知識跨管道要一致
