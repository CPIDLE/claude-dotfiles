## Sample 192

**Source**: `personal-rag_v1\flow.md` L65

```
Frontend                          Backend (chat.py)
────────                          ─────────────────
輸入文字 + 附件         POST /chat
  v  (kb_mode, history,   ───>  收到 ChatRequest
     attachments)                v 
                            組裝 contents (history + user parts)
                            附加 KB mode system instruction
                                 v 
                            呼叫 Gemini (gemini-2.0-flash)
                                 v 
                           ┌─ 有 function_calls? ──┐
                           │  是                   │ 否
                           v                        v 
                      執行 function            直接回傳文字
                      (search/generate)
                           v 
                      回傳結果給 Gemini
                      (最多 3 輪)
                           v 
                      Post-check retry
                      (偵測遺漏圖片生成)
                           v 
                      回傳 ChatResponse
                      (reply, sources,
                       function_calls_made,
                       images)
```

