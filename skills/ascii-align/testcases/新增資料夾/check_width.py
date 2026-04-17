import unicodedata
import sys
from pathlib import Path

# 加入 sarasa_widths 的路徑
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

def check_file(path):
    print(f"Checking: {path}")
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    in_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_block = not in_block
            continue
        if in_block:
            # 找到每一行中最後一個邊界字元的寬度，以此作為對齊依據
            w = display_width(line.rstrip())
            print(f"L{i+1}: w={w} | {line}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_file(sys.argv[1])
