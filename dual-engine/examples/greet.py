import argparse
import sys
from typing import Dict

GREETINGS: Dict[str, str] = {
    "en": "Hello",
    "zh": "你好",
    "ja": "こんにちは",
}

def greet(name: str = "World", lang: str = "en") -> str:
    """回傳問候字串。lang 不在支援清單時 raise ValueError。"""
    if lang not in GREETINGS:
        raise ValueError(f"Unsupported language code: {lang}")
    return f"{GREETINGS[lang]}, {name}!"

def main() -> None:
    """argparse CLI entry point。
    --name: 姓名，預設 "World"
    --lang: 語言代碼 (en/zh/ja)，預設 "en"
    """
    parser = argparse.ArgumentParser(description="Multilingual greeting CLI tool")
    parser.add_argument("--name", default="World", help="Name to greet (default: World)")
    parser.add_argument("--lang", default="en", help="Language code (en/zh/ja, default: en)")

    args = parser.parse_args()
    
    try:
        print(greet(args.name, args.lang))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
