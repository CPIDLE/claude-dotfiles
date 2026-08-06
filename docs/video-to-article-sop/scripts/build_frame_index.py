"""從 ffmpeg scene-detect log 建立候選截圖的時間戳索引 CSV。

用法：python build_frame_index.py <scene_log.txt> <frames/raw 目錄> <輸出.csv>
"""

import csv
import os
import re
import sys


def build_index(log_path, raw_dir, out_csv):
    with open(log_path, encoding="utf-8", errors="ignore") as f:
        pts = re.findall(r"pts_time:([0-9.]+)", f.read())
    files = sorted(f for f in os.listdir(raw_dir) if f.lower().endswith(".png"))
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["filename", "seconds", "timestamp"])
        for fname, t in zip(files, pts):
            secs = float(t)
            h, m, s = int(secs // 3600), int((secs % 3600) // 60), int(secs % 60)
            w.writerow([fname, f"{secs:.3f}", f"{h:02d}:{m:02d}:{s:02d}"])


if __name__ == "__main__":
    log_path, raw_dir, out_csv = sys.argv[1], sys.argv[2], sys.argv[3]
    build_index(log_path, raw_dir, out_csv)
