"""直接呼叫 AnnSinHome GAS Web App 的 pull API，查家庭 LINE 群組記錄。

只用 Python 標準庫（urllib），不需要 AnnSinHome_v0 repo、不需要 docker、不需要裝任何套件——
只要有 GAS_PULL_URL 和 GAS_TOKEN 兩個值就能跑，換到哪台電腦都一樣。

這兩個值本身是 secret。優先順序：
  1. 環境變數 GAS_PULL_URL / GAS_TOKEN（有設就用這個）
  2. ~/.claude/.env 裡的 ANNSINHOME_GAS_PULL_URL / ANNSINHOME_GAS_TOKEN

第 2 項是預設路徑——這份 .env 本來就是這台電腦裝 claude-dotfiles 時該手動填好的機密清單
（跟 CHAT_WEBHOOK_URL 那些放一起），不用每次額外 export。新機器上如果兩個管道都沒有，代表
這兩個值還沒同步過來，跟有的機器要，或問使用者，不要用猜的。

用法：
    python gas_query.py health
        # 回傳 {"status":"ok","lastRow":<目前 log 表總列數>}

    python gas_query.py latest <group_id> [--window 100]
        # 找某個 group_id 最新一則（往前掃 window 列，預設 100，找不到就加大）

    python gas_query.py pull --after 1 --limit 200
        # 原始分頁 pull（跟 app/sync.py 用的是同一個 API）

不知道 group_id 對應哪個群組：跑 pull 隨便抓一批，看 rows 裡的 groupId + groupName 欄位對照。
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Windows 主控台代碼頁常是 cp950/cp1252，不是 UTF-8——print() 預設用主控台代碼頁編碼，
# 會讓 CJK 輸出在別的機器/程式（假設 UTF-8）讀起來變 replacement char。強制 stdout 走 UTF-8，
# 讓輸出真的「換到哪台電腦都一樣」。
sys.stdout.reconfigure(encoding="utf-8")


def load_claude_env():
    path = os.path.expanduser("~/.claude/.env")
    values = {}
    if not os.path.isfile(path):
        return values
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            values[key.strip()] = val.strip()
    return values


def call(url, token, params, attempts=3, backoff=1.5):
    """GAS Web App 的 302 -> script.googleusercontent.com 轉址間歇性 404（Google 端已知
    flaky 行為，跟 client library 無關，同一組請求連跑會有時成功有時 404），失敗就重試。"""
    q = urllib.parse.urlencode({**params, "token": token})
    last_err = RuntimeError("call() ran with attempts=0")
    for i in range(attempts):
        try:
            with urllib.request.urlopen(f"{url}?{q}", timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(backoff * (i + 1))
    raise last_err


def main():
    claude_env = load_claude_env()
    url = os.environ.get("GAS_PULL_URL") or claude_env.get("ANNSINHOME_GAS_PULL_URL")
    token = os.environ.get("GAS_TOKEN") or claude_env.get("ANNSINHOME_GAS_TOKEN")
    if not url or not token:
        print("缺 GAS_PULL_URL/GAS_TOKEN——沒設環境變數，~/.claude/.env 裡也沒有 "
              "ANNSINHOME_GAS_PULL_URL/ANNSINHOME_GAS_TOKEN。跟有這兩個值的機器要，或問使用者。",
              file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "health"

    if cmd == "health":
        print(call(url, token, {"action": "health"}))
        return

    if cmd == "pull":
        args = sys.argv[2:]
        after = int(args[args.index("--after") + 1]) if "--after" in args else 1
        limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 200
        data = call(url, token, {"action": "pull", "after": after, "limit": limit})
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if cmd == "latest":
        group_id = sys.argv[2]
        window = int(sys.argv[sys.argv.index("--window") + 1]) if "--window" in sys.argv else 100
        last_row = call(url, token, {"action": "health"})["lastRow"]
        after = max(1, last_row - window)
        data = call(url, token, {"action": "pull", "after": after, "limit": window})
        rows = [r for r in data.get("rows", []) if r.get("groupId") == group_id]
        if not rows:
            print(f"最近 {window} 列裡沒找到這個 group_id，加大 --window 再試")
            return
        latest = max(rows, key=lambda r: r["ts"])
        print(json.dumps(latest, ensure_ascii=False, indent=2))
        return

    print(f"未知指令: {cmd}（health / pull / latest）", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
