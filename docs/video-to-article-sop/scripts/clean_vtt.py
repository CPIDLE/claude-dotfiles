"""清理 YouTube 自動字幕 (VTT)。

YouTube 自動字幕是「捲動字幕」格式：同一句話會被拆成好幾個 cue block，
且每個 block 常包含「上一句的殘留 + 這句新增的幾個字」。
只取每個 block 的最後一行文字，並跳過與前一次輸出相同的重複行。

用法：python clean_vtt.py <輸入.vtt> <輸出.txt>
"""

import re
import sys


def parse_vtt(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"\n\n+", content)
    ts_re = re.compile(r"(\d\d:\d\d:\d\d\.\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d\.\d\d\d)")
    cues = []
    for block in blocks:
        m = ts_re.search(block)
        if not m:
            continue
        start = m.group(1)
        text_lines = [l for l in block.split("\n")
                      if not ts_re.search(l) and not l.strip().isdigit() and l.strip()]
        if not text_lines:
            continue
        last_line = re.sub(r"<[^>]+>", "", text_lines[-1]).strip()
        cues.append((start, last_line))
    return cues


def dedupe(cues):
    out, last = [], None
    for start, text in cues:
        if not text or text == last:
            continue
        out.append((start, text))
        last = text
    return out


if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    deduped = dedupe(parse_vtt(in_path))
    with open(out_path, "w", encoding="utf-8") as f:
        for start, text in deduped:
            f.write(f"[{start.split('.')[0]}] {text}\n")
    print(f"raw cues: -> clean lines: {len(deduped)}")
