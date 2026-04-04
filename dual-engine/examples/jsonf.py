import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='JSON Formatter')
    parser.add_argument('json_str', nargs='?', help='JSON string to format')
    parser.add_argument('--compact', action='store_true', help='Compact output')
    args = parser.parse_args()

    if args.json_str:
        input_data = args.json_str
    else:
        input_data = sys.stdin.read()

    if not input_data.strip():
        return

    try:
        data = json.loads(input_data)
        if args.compact:
            print(json.dumps(data, separators=(',', ':')))
        else:
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
