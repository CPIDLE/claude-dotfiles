import os
from pathlib import Path
import sys

# 載入對齊工具
sys.path.append(r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾')
from smart_repair import smart_repair

def batch_process(directory):
    mapping = {
        '→': '->',
        '←→': '<->',
        '▼': 'v',
        '▲': '^',
        '❌': '[X]',
        '⚠️': '[!]',
        '✅': '[v]'
    }
    
    files = [f for f in os.listdir(directory) if f.endswith('.md')]
    for fname in files:
        path = Path(directory) / fname
        content = path.read_text(encoding='utf-8')
        
        # 1. 符號替換
        for k, v in mapping.items():
            content = content.replace(k, v)
        path.write_text(content, encoding='utf-8')
        
        # 2. 數值對齊
        try:
            smart_repair(str(path))
        except Exception as e:
            print(f"Error processing {fname}: {e}")

if __name__ == "__main__":
    batch_process(r'E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc\Nested_Container')
