import math
import sys

def format_output(n):
    if math.isfinite(n) and n == int(n):
        print(int(n))
    else:
        print(n)

def main():
    if len(sys.argv) != 4:
        print("Usage: python calc.py <op> <n1> <n2>")
        sys.exit(1)

    op = sys.argv[1]
    try:
        n1 = float(sys.argv[2])
        n2 = float(sys.argv[3])
    except ValueError:
        print("Error: arguments must be numbers")
        sys.exit(1)

    if op == "add":
        format_output(n1 + n2)
    elif op == "sub":
        format_output(n1 - n2)
    elif op == "mul":
        format_output(n1 * n2)
    elif op == "div":
        if n2 == 0:
            print("Error: division by zero")
            sys.exit(1)
        format_output(n1 / n2)
    else:
        print(f"Error: unknown operator {op}")
        sys.exit(1)

if __name__ == "__main__":
    main()
