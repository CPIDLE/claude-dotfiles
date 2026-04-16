## Sample 179

**Source**: `opencode-bench\4090-SETUP.md` L23

```
opencode CLI
    │
    v 
fix-proxy :4001/v1        <-- 修正 Ollama tool_calls index bug
    │
    v 
LiteLLM :4000/v1          <-- OpenAI-compatible API + ollama_chat backend
    │
    v 
Ollama :11434              <-- 模型推理引擎（GPU）
    │
    v 
RTX 4090 24GB VRAM
```

