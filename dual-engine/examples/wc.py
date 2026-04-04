import sys
import os

def main():
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print(f"Usage: python {sys.argv[0]} [FILE]")
        sys.exit(1)

    input_data = ""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()

    lines = input_data.splitlines()
    line_count = len(lines)
    word_count = len(input_data.split())
    char_count = len(input_data)

    print(f"Lines: {line_count}")
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")

if __name__ == "__main__":
    main()
