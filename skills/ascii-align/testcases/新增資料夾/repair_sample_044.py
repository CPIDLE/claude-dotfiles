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

def main():
    target_path = r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc\Nested_Container\sample_044.md'
    
    # 原始結構
    lines = [
        "┌──────────┐    ┌──────────────────────────┐    ┌───────┐",
        "│ API GW   │ →  │ Fargate Container        │ ←→ │ S3    │",
        "│ or Web   │    │                          │    │ .txt  │",
        "└──────────┘    │ FastAPI                  │    │ .html │",
        "                │ ├── /report (生成)       │    └───────┘",
        "                │ ├── /search (搜尋)       │",
        "                │ ├── /calc   (計算)       │        ┌─────────┐",
        "                │ └── gemini_client ───────┤──────→ │ Gemini  │",
        "                │                          │        │ 2.5 Pro │",
        "                │ _calc_throughput.py      │        └─────────┘",
        "                │ gyro-report gen          │",
        "                └──────────────────────────┘"
    ]
    
    # 1. 找出最大寬度
    widths = [display_width(l) for l in lines]
    target_w = max(widths)
    print(f"Target Width decided: {target_w}")
    
    # 2. 補齊
    fixed_block = []
    for l in lines:
        curr_w = display_width(l)
        needed = target_w - curr_w
        fixed_block.append(l + (" " * needed))
    
    # 3. 組合寫入
    header = "## Sample 044\n\n**Source**: `Chat_bot_v1\\aws-migration-discussion.md` L176\n\n```\n"
    footer = "\n```\n\n---\n"
    final_content = header + "\n".join(fixed_block) + footer
    Path(target_path).write_text(final_content, encoding='utf-8')
    
    # 4. 即時驗證
    for i, l in enumerate(fixed_block):
        print(f"L{i+6}: w={display_width(l)}")

if __name__ == "__main__":
    main()
