import os
import re

def split_markdown(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根據 "## Sample " 進行拆分
    samples = re.split(r'(?=## Sample \d+)', content)
    
    # 第一部分通常是標題或說明
    header = samples[0]
    if header.strip():
        with open(os.path.join(output_dir, "000_header.md"), 'w', encoding='utf-8') as f:
            f.write(header)
            
    for i, sample in enumerate(samples[1:], 1):
        # 提取 Sample 編號作為檔名
        match = re.search(r'## Sample (\d+)', sample)
        sample_num = match.group(1) if match else f"{i:03d}"
        file_name = f"sample_{sample_num.zfill(3)}.md"
        
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
            f.write(sample)
    
    print(f"Split {len(samples)-1} samples into {output_dir}")

if __name__ == "__main__":
    source = r"E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\Ascii_sample_2026-04-15.md"
    target = r"E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc"
    split_markdown(source, target)
