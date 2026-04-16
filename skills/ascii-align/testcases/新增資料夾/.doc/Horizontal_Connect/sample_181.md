## Sample 181

**Source**: `opencode-bench\ARCHITECTURE.md` L79

```
opencode  ───>  fix-proxy :4001  ───>  LiteLLM :4000  ───>  Ollama :11434
                    │
          修正 tool_calls index
          (Ollama streaming 全送
           index:0，導致 @ai-sdk
           合併/丟失多個 tool calls)
```

