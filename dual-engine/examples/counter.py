import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="A simple JSON counter.")
    parser.add_argument("--reset", action="store_true", help="Reset the counter to 0.")
    args = parser.parse_args()

    counter_file = os.path.join(os.path.dirname(__file__), ".counter.json")

    count = 0
    if os.path.exists(counter_file):
        try:
            with open(counter_file, "r") as f:
                data = json.load(f)
                count = data.get("count", 0)
        except (json.JSONDecodeError, IOError):
            count = 0

    if args.reset:
        count = 0
    else:
        count += 1

    with open(counter_file, "w") as f:
        json.dump({"count": count}, f)

    print(f"Count: {count}")

if __name__ == "__main__":
    main()
