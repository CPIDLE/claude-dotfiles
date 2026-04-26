"""Batch entry point for ascii-render.

Equivalent to `render.py <dir>` — kept as a separate file for parity
with the SCOPE spec and to allow future divergence (parallelism, glob
patterns, multi-source merge).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from render import run


def main() -> None:
    ap = argparse.ArgumentParser(prog="ascii-render-pipeline")
    ap.add_argument("path", type=Path, help="Directory or file to scan")
    ap.add_argument("--normalize", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    base = args.path if args.path.is_dir() else args.path.parent
    out_dir = args.out or (base / ".render")
    sys.exit(run(args.path, out_dir, args.normalize, args.check, args.strict))


if __name__ == "__main__":
    main()
