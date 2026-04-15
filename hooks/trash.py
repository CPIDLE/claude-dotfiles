#!/usr/bin/env python3
"""trash.py — Move files/directories to OS trash (Recycle Bin on Windows).

Usage: python trash.py file1 [file2 ...]
"""

import sys
from pathlib import Path
from send2trash import send2trash


def main():
    if len(sys.argv) < 2:
        print("Usage: trash.py file1 [file2 ...]", file=sys.stderr)
        sys.exit(1)

    for f in sys.argv[1:]:
        p = Path(f).resolve()
        if p.exists():
            send2trash(str(p))
            print(f"Trashed: {f}")
        else:
            print(f"Not found: {f}", file=sys.stderr)


if __name__ == "__main__":
    main()
