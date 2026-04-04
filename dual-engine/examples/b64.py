import base64
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/b64.py [encode|decode]")
        sys.exit(1)

    command = sys.argv[1]
    input_data = sys.stdin.buffer.read()

    if command == "encode":
        encoded = base64.b64encode(input_data)
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.write(b'\n') # Usually, people want a newline for simple CLI outputs
    elif command == "decode":
        decoded = base64.b64decode(input_data)
        sys.stdout.buffer.write(decoded)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python examples/b64.py [encode|decode]")
        sys.exit(1)

if __name__ == "__main__":
    main()
