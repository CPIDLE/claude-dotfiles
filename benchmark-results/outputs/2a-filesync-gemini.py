import os
import hashlib
import shutil
import argparse
import sys

def get_md5(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"Warning: Could not hash {file_path}: {e}")
        return None

def scan_dir(path):
    """Scan directory and return mapping of relative paths to MD5 hashes."""
    mapping = {}
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if os.path.islink(full_path):
                print(f"Warning: Skipping symlink {full_path}")
                continue
            rel_path = os.path.relpath(full_path, path)
            file_hash = get_md5(full_path)
            if file_hash:
                mapping[rel_path] = file_hash
    return mapping

def diff_dirs(source, target):
    """Compare two directories and return added, removed, and modified files."""
    src_files = scan_dir(source)
    tgt_files = scan_dir(target)
    
    src_keys = set(src_files.keys())
    tgt_keys = set(tgt_files.keys())
    
    diff = {
        "added": list(src_keys - tgt_keys),
        "removed": list(tgt_keys - src_keys),
        "modified": [p for p in (src_keys & tgt_keys) if src_files[p] != tgt_files[p]]
    }
    return diff

def sync_dirs(source, target, dry_run=False):
    """Synchronize source to target; return list of actions taken."""
    actions = []
    diff = diff_dirs(source, target)
    
    for rel_path in diff["added"] + diff["modified"]:
        src_path = os.path.join(source, rel_path)
        tgt_path = os.path.join(target, rel_path)
        actions.append(f"COPY/UPDATE: {rel_path}")
        if not dry_run:
            os.makedirs(os.path.dirname(tgt_path), exist_ok=True)
            shutil.copy2(src_path, tgt_path)
            
    for rel_path in diff["removed"]:
        tgt_path = os.path.join(target, rel_path)
        actions.append(f"DELETE: {rel_path}")
        if not dry_run:
            os.remove(tgt_path)
            
    return actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync two directories.")
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    if not os.path.isdir(args.source):
        print(f"Error: Source {args.source} is not a directory.")
        sys.exit(1)
    if not os.path.exists(args.target):
        os.makedirs(args.target)
        
    try:
        result = sync_dirs(args.source, args.target, args.dry_run)
        for action in result:
            print(action)
    except Exception as e:
        print(f"Sync failed: {e}")
        sys.exit(1)