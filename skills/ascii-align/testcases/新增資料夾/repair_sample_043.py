import unicodedata
import sys
from pathlib import Path

sys.path.append(r'C:\Users\benth\.claude\skills\ascii-align\scripts')
try:
    from sarasa_widths import WIDE_OVERRIDES
except ImportError:
    WIDE_OVERRIDES = set()

def char_cols(c):
    cp = ord(c)
    if cp in WIDE_OVERRIDES or unicodedata.east_asian_width(c) in ('F', 'W'):
        return 2
    return 1

def display_width(s):
    return sum(char_cols(c) for c in s)

def repair_content(lines):
    # 1. 找出最大寬度
    max_w = max(display_width(l) for l in lines)
    print(f"Aligning to max width: {max_w}")
    
    # 2. 補足空格
    fixed = []
    for l in lines:
        needed = max_w - display_width(l)
        fixed.append(l + (" " * needed))
    return fixed

def main():
    path = r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc\Nested_Container\sample_043.md'
    raw_lines = [
        "┌───────────┐    ┌─────────────────────────────┐    ┌─────┐",
        "│ API GW    │ →  │ ECS/Fargate                 │ ←→ │ S3  │",
        "│           │    │ Docker 容器                 │    │     │",
        "└───────────┘    │ FastAPI                     │    └─────┘",
        "                 │ Python 腳本                 │",
        "                 │                             │    ┌───────────────┐",
        "                 │ gemini client ──────────────│──→ │ Google Gemini │",
        "                 │                             │    │ - Embedding API │",
        "                 │                             │    │ - Chat/Gen API │",
        "                 └─────────────────────────────┘    │               │",
        "                                                    └───────────────┘"
    ]
    
    # 執行補齊
    fixed = repair_content(raw_lines)
    
    # 組合
    content = "## Sample 043\n\n**Source**: `Chat_bot_v1\\aws-migration-discussion.md` L109\n\n```\n"
    content += "\n".join(fixed)
    content += "\n```\n\n---\n"
    
    Path(path).write_text(content, encoding='utf-8')
    
    # 自我驗證
    print("--- Self Verification ---")
    for i, l in enumerate(fixed):
        w = display_width(l)
        print(f"L{i+6}: w={w}")

if __name__ == "__main__":
    main()
