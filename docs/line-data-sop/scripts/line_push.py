"""直接呼叫 LINE Messaging API 的 push endpoint，發訊息到指定 group_id/user_id。

只用 Python 標準庫（urllib），不需要 AnnSinHome_v0 repo 的 httpx/async 環境、不需要 docker。
憑證是 LINE_CHANNEL_ACCESS_TOKEN，這是「AnnSinHome bot」這個 LINE Messaging API channel 的 token
（跟 gas_query.py 用的 GAS_PULL_URL/GAS_TOKEN 是完全不同的兩組憑證，不要混用）。

**這不是唯讀工具，執行後果不可逆——動手前必讀 line-data-sop.md 的「發送訊息（push）」章節**：
  - 訊息會顯示是 AnnSinHome bot 帳號發的，不是使用者本人
  - LINE 沒有收回機制，發出去就送出去了
  - 每次要送都要先讓使用者看過最終文字內容並明確同意，不能因為前一次做過就當作長期授權

**預設是 dry-run**：不加 --send 只會印出「將會送出什麼」，不會真的打 API。
使用者確認內容沒問題、且明確同意要送之後，才加 --send 真的發出去。

Token 讀取優先序：
  1. 環境變數 LINE_CHANNEL_ACCESS_TOKEN
  2. ~/.claude/.env 的 ANNSINHOME_LINE_CHANNEL_ACCESS_TOKEN（尚未實際同步過，是長期可攜的路徑）
  3. 本機 AnnSinHome_v0 repo 的 .env（目前唯一有這個值的地方，只在跑 docker-compose 的那台 PC 上存在，
     路徑寫死 E:\\github\\AnnSinHome_v0\\.env——跟 line-data-sop.md 記錄的本機 SQLite 路徑是同一台機器）

用法：
    python line_push.py push <to> --text "<文字，<=4900字元>"
        # dry-run，只印出會送出的內容，不會真的發

    python line_push.py push <to> --text "<文字>" --send
        # 真的發送

    python line_push.py push <to> --file msg.txt --send
        # 從檔案讀文字（多行/含特殊字元時比 shell 參數安全），存在就送

    python line_push.py push <to> --send < msg.txt
        # 或用 stdin 餵文字

<to> 是 group_id（群組）或 user_id（1:1），對照表見 line-data-sop.md「已知 group_id/user_id 對照表」。
不知道某群的 group_id：先用 gas_query.py pull 撈一批看 groupId/groupName，或問使用者。
"""

import json
import os
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

_LOCAL_REPO_ENV = r"E:\github\AnnSinHome_v0\.env"


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


def load_local_repo_env():
    if not os.path.isfile(_LOCAL_REPO_ENV):
        return {}
    values = {}
    with open(_LOCAL_REPO_ENV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            values[key.strip()] = val.strip()
    return values


def get_token():
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if token:
        return token
    token = load_claude_env().get("ANNSINHOME_LINE_CHANNEL_ACCESS_TOKEN")
    if token:
        return token
    token = load_local_repo_env().get("LINE_CHANNEL_ACCESS_TOKEN")
    if token:
        return token
    print(
        "缺 LINE_CHANNEL_ACCESS_TOKEN——環境變數沒設、~/.claude/.env 裡沒有 "
        "ANNSINHOME_LINE_CHANNEL_ACCESS_TOKEN、本機 AnnSinHome_v0/.env 也讀不到。"
        "跟有這個值的機器要，或問使用者，不要用猜的。",
        file=sys.stderr,
    )
    sys.exit(1)


def push(token, to, text, dry_run):
    text = text[:4900]
    payload = {"to": to, "messages": [{"type": "text", "text": text}]}

    if dry_run:
        print("--- DRY RUN，尚未送出 ---")
        print(f"to: {to}")
        print(f"text ({len(text)} 字元):")
        print(text)
        print("--- 加 --send 才會真的發送 ---")
        return

    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"送出成功，HTTP {resp.status}")
            print(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"送出失敗，HTTP {e.code}", file=sys.stderr)
        print(e.read().decode(), file=sys.stderr)
        sys.exit(1)


def read_text(args):
    if "--text" in args:
        return args[args.index("--text") + 1]
    if "--file" in args:
        path = args[args.index("--file") + 1]
        with open(path, encoding="utf-8") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    print("沒給文字——用 --text \"...\"、--file <path>，或用 stdin 餵。", file=sys.stderr)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else None

    if cmd != "push" or len(args) < 2:
        print("用法: python line_push.py push <to> --text \"...\" [--send]", file=sys.stderr)
        sys.exit(1)

    to = args[1]
    text = read_text(args[2:])
    send = "--send" in args

    token = get_token()
    push(token, to, text, dry_run=not send)


if __name__ == "__main__":
    main()
