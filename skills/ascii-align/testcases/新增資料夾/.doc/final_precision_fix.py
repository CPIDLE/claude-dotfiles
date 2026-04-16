import unicodedata

def get_width(s):
    overrides = {
        '─': 1, '│': 1, '┌': 1, '┐': 1, '└': 1, '┘': 1, '├': 1, '┤': 1, '┬': 1, '┴': 1, '┼': 1,
        '◄': 2, '►': 2, '↕': 2, '↔': 2, '→': 2, '←': 2, '↑': 2, '↓': 2,
        '×': 1,
    }
    width = 0
    for char in s:
        if char in overrides: width += overrides[char]
        elif unicodedata.east_asian_width(char) in ('F', 'W'): width += 2
        else: width += 1
    return width

def pad(s, target):
    w = get_width(s)
    return s + ' ' * (target - w)

# --- Sample 006 Precision ---
# Box 1 Width: 21 (─ count 19)
# Box 2 Width: 25 (─ count 23)
# Gap: 10
# Indent: 12
# Total: 12 + 21 + 10 + 25 = 68.
def gen_006():
    target = 70
    lines = [
        "                   正常狀態                          雪崩狀態",
        "            ┌───────────────────┐          ┌───────────────────────┐",
        "            │  loggingCarWork   │          │  loggingCarWork       │",
        "            │    = 0.01s        │          │    = 0.01s            │",
        "            │  (100Hz 排程)     │          │  (100Hz 排程)         │",
        "            └──────────┬────────┘          └──────────┬────────────┘",
        "                       ↓                              ↓",
        "            ┌───────────────────┐          ┌───────────────────────┐",
        "            │  log_work() 執行  │          │  log_work() 執行      │",
        "            │  耗時 5ms < 10ms  │          │  耗時 15ms > 10ms     │",
        "            │  ──> sleep 5ms    │          │  ──> 跳過 sleep       │",
        "            │  ──> 下一次排程   │          │  ──> 立即排下一次     │",
        "            └───────────────────┘          │  ──> 堆積 ──> 連續執行│",
        "                                           │  ──> CPU 100%         │",
        "            CPU: 69%                       └───────────────────────┘",
        "                                           CPU: 95~100%"
    ]
    res = []
    for l in lines:
        res.append(pad(l, target))
    return res

# --- Sample 015 Precision ---
# Box 1: 15, Gap: 19, Box 2: 16. Total 50.
def gen_015():
    target = 50
    lines = [
        "┌─────────────┐    /motor_cmd     ┌──────────────┐",
        "│             │ ────────────────> │              │",
        "│  gyro-ros   │    /motor_actual  │  ethercat /  │",
        "│  (主系統)   │ <──────────────── │  canopen     │",
        "│             │    /motorAlarm    │  (馬達控制)  │",
        "│             │ <──────────────── │              │",
        "└──────┬──────┘                   └──────────────┘",
        "       │                                          ",
        "       │  rosbridge (port 9090)                   ",
        "       ↕                                         ",
        "┌──────┴──────┐                                   ",
        "│   agvweb    │                                   ",
        "│   (Web UI)  │                                   ",
        "└─────────────┘                                   "
    ]
    res = []
    for l in lines:
        res.append(pad(l, target))
    return res

# --- Sample 042 Precision ---
def gen_042():
    target = 49
    lines = [
        "┌────────────────────┐     ┌────────────────────┐",
        "│  EC2 (運算)        │ <-> │  S3 (儲存)         │",
        "│  Python 腳本       │     │  .doc/ 知識庫      │",
        "│  FastAPI (可選)    │     │  報告輸出          │",
        "│  Claude API        │     │  _index.json       │",
        "└────────────────────┘     └────────────────────┘"
    ]
    res = []
    for l in lines:
        res.append(pad(l, target))
    return res

def write_file(filename, lines, title, source):
    path = f'E:/github/claude-dotfiles/skills/ascii-align/testcases/新增資料夾/.doc/Nested_Container/{filename}'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"## {title}\n\n")
        f.write(f"**Source**: `{source}`\n\n")
        f.write("```\n")
        for l in lines:
            f.write(l + "\n")
        f.write("```\n\n---\n\n---\n")

write_file('sample_006.md', gen_006(), 'Sample 006', 'AMRCoolDown_v0\\AMR_撞機事件根因分析.md` L168')
write_file('sample_015.md', gen_015(), 'Sample 015', 'AMRCoolDown_v0\\AMR_程式架構分析_v2.md` L441')
write_file('sample_042.md', gen_042(), 'Sample 042', 'Chat_bot_v1\\aws-migration-discussion.md` L93')
