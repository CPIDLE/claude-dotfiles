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

def smart_repair(path):
    print(f"Repairing: {path}")
    content = Path(path).read_text(encoding='utf-8')
    lines = content.splitlines()
    
    new_lines = []
    in_block = False
    block_lines = []
    
    for line in lines:
        if line.strip().startswith('```'):
            if not in_block:
                # 進入區塊
                in_block = True
                new_lines.append(line)
                block_lines = []
            else:
                # 離開區塊，執行對齊
                in_block = False
                if block_lines:
                    # 1. 找出區塊內內容的最大寬度
                    max_w = max(display_width(l) for l in block_lines)
                    # 2. 補齊
                    for bl in block_lines:
                        needed = max_w - display_width(bl)
                        new_lines.append(bl + (" " * needed))
                new_lines.append(line)
        else:
            if in_block:
                block_lines.append(line)
            else:
                new_lines.append(line)
    
    Path(path).write_text("\n".join(new_lines) + "\n", encoding='utf-8')
    print(f"Done.")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        smart_repair(p)
