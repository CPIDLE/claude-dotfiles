import argparse
import string
import secrets
import sys

def generate_password(length, use_symbols):
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += string.punctuation
    
    return "".join(secrets.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description="A simple password generator.")
    parser.add_argument("--length", type=int, default=16, help="Length of the password (default: 16)")
    parser.add_argument("--no-symbols", action="store_false", dest="use_symbols", help="Exclude symbols from the password")
    parser.set_defaults(use_symbols=True)
    
    args = parser.parse_args()
    
    if args.length <= 0:
        print("Error: Length must be greater than 0", file=sys.stderr)
        sys.exit(1)
        
    password = generate_password(args.length, args.use_symbols)
    print(password)

if __name__ == "__main__":
    main()
