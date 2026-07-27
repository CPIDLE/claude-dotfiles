# To Spec — 共識綜合成 spec

把已經談定的共識**純綜合**成一份 spec（動工前把「要蓋什麼」寫死），不再訪談。Matt Pocock 主 flow 第二棒，接在 `/grill-me` 之後。

> 源自 Matt Pocock 的 `to-spec`。設計成跑在 `/grill-me` **同一 session**（不 compact / clear），吃同一串已對齊的 context。到得了這一步，代表對齊工作已做完——這裡只負責寫下來。

## 觸發

`/to-spec [主題]`，手動。前提是當前 context 已有談定的共識（通常來自 `/grill-me`）。

## 核心規則

1. **零訪談、純綜合**。不再逐題問。從當前 context（共識）+ 探程式碼，綜合出 spec。
2. **讀什麼 / 不讀什麼**：
   - ✅ 探當前程式碼、respect 現有 ADR（這是**當前系統的事實**）。
   - ❌ **不讀 `specs/` 下任何既有 spec / PRD**（那是**過期的意圖表述**，讀了會錨定污染、悄悄復活已推翻的決策）。
3. **唯一互動點 = seam 確認**。探碼後選 testing seam（取**最高架構層**、優先沿用現有 seam），**寫 spec 前**把 seam 方案丟給使用者確認一次，確認後才寫。除此之外全程不問。
4. **輸出 `specs/<slug>.md`**。`<slug>` 從 change 主題自動生、開頭讓使用者確認一次；重跑**覆蓋同 slug**（spec 是可重生的 destination）。無 `specs/` 目錄則建立。
5. **不動手實作**。只寫 spec，不寫 code。

## spec 模板（Matt 7 段）

```markdown
---
slug: <slug>
status: ready
created: <當前系統日期 YYYY-MM-DD>
---
# <spec 標題>

## 問題陳述
<使用者視角的問題>

## 解法
<使用者視角的做法>

## User Stories
1. As an X, I want Y, so that Z
2. ...

## 實作決策
<模組 / 介面 / 架構 / schema / API 契約；**不含檔路徑**；可放決策豐富的 snippet>

## 測試決策
<外部行為導向、testing seam、模組覆蓋、prior art>

## Out of Scope
<明確排除的東西>

## 備註
<其他 context>
```

> `created` 用當前系統日期，不硬編。

## INDEX 整合

寫檔後 `hooks/index-append.py` 自動 append 進 INDEX.md；cc 順手補 用途=`spec`、狀態=`active`（沿用全域 CLAUDE.md 的 INDEX 規則，不需使用者指示）。

## 收尾

印一行：spec 路徑 + 段落數 + 「下一棒可接 `/pm-review` 審實作是否符合 spec（或日後 `/to-tickets` 拆票）」。

## 反模式

- ❌ 又開始逐題訪談（這一步是綜合，不是 grill）。
- ❌ 去讀 `specs/` 舊 spec 來「參考 / 合併」。
- ❌ seam 沒跟使用者確認就直接寫 spec。
- ❌ spec 裡塞檔路徑當實作決策。
- ❌ 順手把 code 也寫了。
