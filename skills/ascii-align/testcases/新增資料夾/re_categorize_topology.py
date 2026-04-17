import os
import re
import shutil

def analyze_topology(content):
    # 統計結構字元
    junctions = len(re.findall(r'[┬┴┼]', content))
    horizontals = len(re.findall(r'[─]', content))
    verticals = len(re.findall(r'[│]', content))
    arrows_v = len(re.findall(r'[▼▲↓↑]', content))
    arrows_h = len(re.findall(r'[→←↔]', content))
    corners = len(re.findall(r'[┌┐└┘]', content))
    
    # 判定邏輯
    if junctions > 5 or (junctions > 2 and corners > 10):
        if junctions > 10 and corners > 20:
            return "Grid_Table"
        return "Branching_Tree"
    
    # 檢查嵌套 (簡單判定：同一行出現多個左邊界或多層結構)
    lines = content.split('\n')
    max_boxes_per_line = 0
    for line in lines:
        box_starts = len(re.findall(r'┌|│', line))
        max_boxes_per_line = max(max_boxes_per_line, box_starts)
    
    if max_boxes_per_line >= 4:
        return "Nested_Container"
    
    if arrows_h > arrows_v * 1.5:
        return "Horizontal_Connect"
    
    if arrows_v > 0 or verticals > 5:
        return "Linear_Pipeline"
        
    return "Simple_Box"

def re_categorize(doc_dir):
    # 先將所有檔案移回根目錄 (flatten)
    all_files = []
    for root, dirs, files in os.walk(doc_dir):
        if root == doc_dir: continue
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(doc_dir, f)
            if os.path.exists(dst): os.remove(dst)
            shutil.move(src, dst)
        os.rmdir(root)

    # 建立新資料夾
    categories = ["Linear_Pipeline", "Branching_Tree", "Grid_Table", "Nested_Container", "Horizontal_Connect", "Simple_Box"]
    for cat in categories:
        os.makedirs(os.path.join(doc_dir, cat), exist_ok=True)

    # 開始分析並搬移
    for filename in os.listdir(doc_dir):
        if not filename.endswith(".md") or filename == "000_header.md":
            continue
            
        file_path = os.path.join(doc_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cat = analyze_topology(content)
        shutil.move(file_path, os.path.join(doc_dir, cat, filename))
    
    print("Topological categorization complete.")

if __name__ == "__main__":
    doc_path = r"E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc"
    re_categorize(doc_path)
