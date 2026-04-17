import os
import re
import shutil

def categorize_samples(doc_dir):
    categories = {
        "Flow_Stream": ["Stream", "tee\(\)", "▼", "↓", "→", "pipe", "Flow"],
        "Topology_Network": ["Gateway", "TSC", "MCS", "IPC", "AMR", "E-Rack", "Network", "Protocol", "┼", "┴"],
        "Map_Grid": ["A\d+-\d+", "Stocker", "Sorter", "Map", "Grid"],
        "Hardware_Memory": ["GPU", "DDR", "Memory", "Buffer", "Register", "Hardware"],
        "Process_State": ["Phase", "State", "Step", "Process", "Algorithm"],
    }
    
    # Create category directories
    for cat in categories.keys():
        os.makedirs(os.path.join(doc_dir, cat), exist_ok=True)
    os.makedirs(os.path.join(doc_dir, "Other"), exist_ok=True)
    
    for filename in os.listdir(doc_dir):
        if not filename.endswith(".md") or filename == "000_header.md":
            continue
            
        file_path = os.path.join(doc_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        found_cat = "Other"
        for cat, keywords in categories.items():
            if any(re.search(kw, content, re.IGNORECASE) for kw in keywords):
                found_cat = cat
                break
        
        shutil.move(file_path, os.path.join(doc_dir, found_cat, filename))
        
    print("Categorization complete.")

if __name__ == "__main__":
    doc_path = r"E:\github\claude-dotfiles\skills\ascii-align\testcases\新增資料夾\.doc"
    categorize_samples(doc_path)
