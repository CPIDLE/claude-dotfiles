## Sample 383

**Source**: `Reporter_v1\WORKSPACE\a01\13_win_drive_v0.md` L51

```
├── src/
│   ├── main.cpp
│   ├── mcp_server.cpp / .h       # MCP 協定實作
│   ├── tool_registry.cpp / .h    # 工具註冊
│   ├── tools/
│   │   ├── screenshot.cpp / .h   # 截圖
│   │   ├── mouse.cpp / .h        # 滑鼠
│   │   ├── keyboard.cpp / .h     # 鍵盤
│   │   ├── window.cpp / .h       # 視窗管理
│   │   ├── uia.cpp / .h          # UI Automation
│   │   ├── batch.cpp / .h        # 批次操作
│   │   ├── gemini.cpp / .h       # Gemini 分析
│   │   └── shared.h
│   └── util/
│       ├── logger.cpp / .h       # Logging 模組
│       ├── png_encode.cpp / .h
│       ├── screen_buffer.cpp / .h
│       ├── base64.h, env_loader.h, input_guard.h, json_helpers.h
├── vendor/
│   ├── nlohmann/json.hpp
│   └── stb_image_write.h
├── xmake.lua
├── CHANGELOG.md
└── README.md
```

---

