"""直接呼叫 AnnSinHome GAS Web App 的 pull API，查家庭 LINE 群組記錄。

只用 Python 標準庫（urllib），不需要 AnnSinHome_v0 repo、不需要 docker、不需要裝任何套件——
只要有 GAS_PULL_URL 和 GAS_TOKEN 兩個值就能跑，換到哪台電腦都一樣。

這兩個值本身是 secret，存在 AnnSinHome_v0/.env（不在 git 裡）。這台電腦如果沒有
AnnSinHome_v0 這個 repo，代表也沒有這兩個值——跟有這兩個值的機器要，或問使用者。

用法：
    export GAS_PULL_URL=...
    export GAS_TOKEN=...

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
import urllib.parse
import urllib.request


def call(url, token, params):
    q = urllib.parse.urlencode({**params, "token": token})
    with urllib.request.urlopen(f"{url}?{q}", timeout=30) as resp:
        return json.loads(resp.read())


def main():
    url = os.environ.get("GAS_PULL_URL")
    token = os.environ.get("GAS_TOKEN")
    if not url or not token:
        print("缺 GAS_PULL_URL / GAS_TOKEN 環境變數（見 AnnSinHome_v0/.env，或跟有這兩個值的機器要）",
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
