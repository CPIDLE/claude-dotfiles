import sys
from pathlib import Path

# 加入 sarasa_widths 的路徑
sys.path.append(r'C:\Users\benth\.claude\skills\ascii-align\scripts')
try:
    from sarasa_widths import WIDE_OVERRIDES
except ImportError:
    WIDE_OVERRIDES = set()

import unicodedata

def char_cols(c):
    cp = ord(c)
    if cp in WIDE_OVERRIDES or unicodedata.east_asian_width(c) in ('F', 'W'):
        return 2
    return 1

def display_width(s):
    return sum(char_cols(c) for c in s)

def main():
    path = r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc\Nested_Container\sample_044.md'
    
    # 基準行: L7 (┌──────────┐    ┌──────────────────────────────┐    ┌───────┐)
    # 我們要對齊的是中間方框的右邊界。
    # 這裡直接定義每一行的「原始組成」，由腳本計算補齊。
    
    # 格式: (前綴, 中間內容, 中間右邊界, 右側箭頭/內容)
    # 目標是讓「中間右邊界」的 display_width 累積值相同。
    
    # L6: ┌──────────┐    ┌──────────────────────────────┐
    # L7: │ API GW   │ →  │ Fargate Container            │
    
    target_mid_border_col = 12 + 4 + 32 # 48
    
    lines_parts = [
        # (L6) 57寬度的頂邊
        r"┌──────────┐    ┌──────────────────────────────┐    ┌───────┐",
        # (L7)
        (r"│ API GW   │ →  │ Fargate Container", r"│"),
        # (L8)
        (r"│ or Web   │    │", r"│"),
        # (L9)
        (r"└──────────┘    │ FastAPI", r"│"),
        # (L10)
        (r"                │  ├── /report (生成)", r"│"),
        # (L11)
        (r"                │  ├── /search (搜尋)", r"│"),
        # (L12)
        (r"                │  ├── /calc   (計算)", r"│"),
        # (L13)
        (r"                │  └── gemini_client ──────────┼──→", r"│ Gemini  │"),
        # (L14)
        (r"                │", r"│", r"│ 2.5 Pro │"),
        # (L15)
        (r"                │ _calc_throughput.py", r"│", r"└─────────┘"),
        # (L16)
        (r"                │ gyro-report gen", r"│"),
        # (L17)
        r"                └──────────────────────────────┘"
    ]
    
    # ... 這裡邏輯太複雜，我直接寫出完美對齊的字串列表 (手工計算寬度) ...
    fixed_lines = [
        r"┌──────────┐    ┌──────────────────────────────┐    ┌───────┐", # 57
        r"│ API GW   │ →  │ Fargate Container            │ ←→ │ S3    │", # 12+4+32=48, 48+4+9=61
        r"│ or Web   │    │                              │    │ .txt  │", 
        r"└──────────┘    │ FastAPI                      │    │ .html │",
        r"                │  ├── /report (生成)          │    └───────┘",
        r"                │  ├── /search (搜尋)          │",
        r"                │  ├── /calc   (計算)          │    ┌─────────┐",
        r"                │  └── gemini_client ──────────┼──→ │ Gemini  │",
        r"                │                              │    │ 2.5 Pro │",
        r"                │ _calc_throughput.py          │    └─────────┘",
        r"                │ gyro-report gen              │",
        r"                └──────────────────────────────┘"
    ]
    
    # 檢驗 fixed_lines 中間邊界對齊度
    # 我們讓每一行在 48 列出現 │
    
    content = "## Sample 044\n\n**Source**: `Chat_bot_v1\\aws-migration-discussion.md` L176\n\n```\n"
    content += "\n".join(fixed_lines)
    content += "\n```\n\n---\n"
    
    Path(path).write_text(content, encoding='utf-8')
    print("Repaired sample_044.md with manual character counting logic.")

if __name__ == "__main__":
    main()
