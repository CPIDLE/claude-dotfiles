import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def scan_dir(path: str) -> dict[str, str]:
    """Scan directory and return {relative_path: md5_hash} for all regular files."""
    result: dict[str, str] = {}
    root = Path(path)
    if not root.is_dir():
        print(f"Error: '{path}' is not a directory")
        sys.exit(1)

    for entry in root.rglob("*"):
        if entry.is_symlink():
            print(f"Warning: skipping symlink {entry}", file=sys.stderr)
            continue
        if not entry.is_file():
            continue
        rel = str(entry.relative_to(root))
        try:
            md5 = hashlib.md5(entry.read_bytes()).hexdigest()
            result[rel] = md5
        except PermissionError:
            print(f"Warning: permission denied {entry}", file=sys.stderr)
    return result


def diff_dirs(source: str, target: str) -> dict[str, list[str]]:
    """Compare source and target directories. Returns {added, removed, modified}."""
    src_map = scan_dir(source)
    tgt_map = scan_dir(target)

    added = [f for f in src_map if f not in tgt_map]
    removed = [f for f in tgt_map if f not in src_map]
    modified = [f for f in src_map if f in tgt_map and src_map[f] != tgt_map[f]]

    return {"added": sorted(added), "removed": sorted(removed), "modified": sorted(modified)}


def sync_dirs(source: str, target: str, dry_run: bool = False) -> list[str]:
    """Sync source to target. Returns list of actions taken."""
    diff = diff_dirs(source, target)
    actions: list[str] = []
    src_root = Path(source)
    tgt_root = Path(target)

    for f in diff["added"]:
        action = f"copy {f}"
        actions.append(action)
        if not dry_run:
            dest = tgt_root / f
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_root / f, dest)

    for f in diff["modified"]:
        action = f"overwrite {f}"
        actions.append(action)
        if not dry_run:
            shutil.copy2(src_root / f, tgt_root / f)

    for f in diff["removed"]:
        action = f"delete {f}"
        actions.append(action)
        if not dry_run:
            try:
                (tgt_root / f).unlink()
            except PermissionError:
                print(f"Warning: cannot delete {f}", file=sys.stderr)

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync two directories")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("target", help="Target directory")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: source '{args.source}' does not exist")
        sys.exit(1)

    os.makedirs(args.target, exist_ok=True)

    actions = sync_dirs(args.source, args.target, dry_run=args.dry_run)
    prefix = "[DRY RUN] " if args.dry_run else ""
    for a in actions:
        print(f"{prefix}{a}")
    if not actions:
        print("Already in sync.")


if __name__ == "__main__":
    main()
