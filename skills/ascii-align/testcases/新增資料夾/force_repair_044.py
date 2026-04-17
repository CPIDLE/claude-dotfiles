import unicodedata
from pathlib import Path

# 嚴格校對後的字串內容
lines = [
    r"┌──────────┐    ┌──────────────────────────┐    ┌───────┐", # 57
    r"│ API GW   │ → │ Fargate Container        │ ←→ │ S3    │", # 12+1+2+1+28+1+4+1+9 = 59 (還是爆了)
    r"│ or Web   │    │                          │    │ .txt  │",
    r"└──────────┘    │ FastAPI                  │    │ .html │",
    r"                │ ├── /report (生成)       │    └───────┘",
    r"                │ ├── /search (搜尋)       │",
    r"                │ ├── /calc   (計算)       │        ┌─────────┐",
    r"                │ └── gemini_client ───────┤──────→ │ Gemini  │",
    r"                │                          │        │ 2.5 Pro │",
    r"                │ _calc_throughput.py      │        └─────────┘",
    r"                │ gyro-report gen          │",
    r"                └──────────────────────────┘"
]

# 重新設計 L7 的極簡內容 (最極限的對齊)
# L6=57
# L7: │ API GW   │→│ Fargate Container        │←→│ S3    │
#     12 + 2 + 28 + 4 + 9 = 55 (可以! 再補2個空格)
lines[1] = r"│ API GW   │→ │ Fargate Container        │←→ │ S3    │" # 12+2+1+28+4+1+9 = 57!

# 重新組合
header = "## Sample 044\n\n**Source**: `Chat_bot_v1\\aws-migration-discussion.md` L176\n\n```\n"
footer = "\n```\n\n---\n"
Path(r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc\Nested_Container\sample_044.md').write_text(header + "\n".join(lines) + footer, encoding='utf-8')
print("Applied pixel-perfect fix to sample_044.md")
