import sys

def c2f(c):
    return (c * 9/5) + 32

def f2c(f):
    return (f - 32) * 5/9

def c2k(c):
    return c + 273.15

def main():
    if len(sys.argv) < 3:
        print("Usage: python temp.py <mode> <value>")
        sys.exit(1)
    
    mode = sys.argv[1]
    try:
        val = float(sys.argv[2])
    except ValueError:
        print("Invalid value")
        sys.exit(1)
        
    if mode == "c2f":
        print(c2f(val))
    elif mode == "f2c":
        print(f2c(val))
    elif mode == "c2k":
        print(c2k(val))
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
