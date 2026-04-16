## Sample 123

**Source**: `draft-draw\SESSION_NOTES.md` L18

```
C:\Users\benth\Documents\GitHub\draft-draw\
├── generate_images.py          # Gemini Imagen API image generation script
├── generate_prompts.py         # Gemini Vision API batch prompt generation script
├── filter_by_date.py           # Date filter: .images_full --> .images_main
├── SESSION_NOTES.md            # This file
├── .generate_prompts_checkpoint.json  # Prompt generation checkpoint/resume
├── .generate_prompts.log       # Prompt generation log file
├── .images_full/               # Original 188,431 images (READ-ONLY source)
│   ├── 00_其他/
│   ├── 01_產品介紹/
│   ├── 02_工程圖面/
│   ├── 03_技術規格/
│   ├── 04_認證標準/
│   ├── 05_電池充電/
│   ├── 06_系統軟體/
│   ├── 07_客戶提案/
│   ├── 08_安全規範/
│   ├── 09_操作手冊/
│   ├── 10_報告分析/
│   └── skipped_files.txt
├── .images_sample/             # 50 sample images + 50 .md prompts + 38 generated images
│   └── (same subdirectory structure)
├── detect_text_images.py        # Text/blank image detection and removal
├── .images_main/               # Filtered working directory: 73,058 visual images (2021+, text removed)
│   └── (same subdirectory structure)
├── .images_main_scan_results.csv  # Full scan classification results
├── .images_main_deleted.log       # Log of deleted file paths
└── .claude/
    └── settings.local.json
```

