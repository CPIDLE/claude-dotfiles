## Sample 192

**Source**: `personal-rag_v1\flow.md` L65

```
Frontend                          Backend (chat.py)
────────                          ─────────────────
輸入文字 + 附件         POST /chat
  ↓ (kb_mode, history,   ──→  收到 ChatRequest
     attachments)                ↓
                            組裝 contents (history + user parts)
                            附加 KB mode system instruction
                                 ↓
                            呼叫 Gemini (gemini-2.0-flash)
                                 ↓
                           ┌─ 有 function_calls? ─┐
                           │  是                   │ 否
                           ↓                       ↓
                      執行 function            直接回傳文字
                      (search/generate)
                           ↓
                      回傳結果給 Gemini
                      (最多 3 輪)
                           ↓
                      Post-check retry
                      (偵測遺漏圖片生成)
                           ↓
                      回傳 ChatResponse
                      (reply, sources,
                       function_calls_made,
                       images)
```

---

