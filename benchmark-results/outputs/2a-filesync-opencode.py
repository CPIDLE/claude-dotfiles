import os
import hashlib
import shutil
import argparse
import sys

def scan_dir(path):
    """
    Scans a directory and returns a mapping of relative paths to MD5 hashes.
    Skips symlinks with a warning. Handles permission errors.
    """
    file_map = {}
    path = os.path.abspath(path)
    
    if not os.path.isdir(path):
        return file_map

    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, path)
            
            if os.islink(full_path):
                print(f"Warning: Skipping symlink {rel_path}", file=sys.stderr)
                continue
                
            try:
                hasher = hashlib.md5()
                with open(full_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hasher.update(chunk)
                file_map[rel_path] = hasher.hexdigest()
            except PermissionError:
                print(f"Warning: Permission denied {rel_path}", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Could not hash {rel_path}: {e}", file=sys.stderr)
                
    return file_map

def diff_dirs(source, target):
    """
    Compares two directories and returns added, removed, and modified files.
    Paths are relative to the directory roots.
    """
    src_map = scan_dir(source)
    tgt_map = scan_dir(target)
    
    src_paths = set(src_map.keys())
    tgt_paths = set(tgt_map.keys())
    
    added = sorted(list(src_paths - tgt_paths))
    removed = sorted(list(tgt_paths - src_paths))
    modified = sorted([
        p for p in (src_paths & tgt_paths) 
        if src_map[p] != tgt_map[p]
    ])
    
    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }

def sync_dirs(source, target, dry_run=False):
    """
    Synchronizes source to target. Copies new, overwrites modified, and deletes removed.
    Returns a list of actions performed or planned.
    """
    if not os.path.isdir(source):
        raise ValueError(f"Source directory does not exist: {source}")
    if not os.path.exists(target):
        if not dry_run:
            os.makedirs(target)
    
    diff = diff_dirs(source, target)
    actions = []
    
    # Remove files in target not in source
    for rel_path in diff["removed"]:
        dest = os.path.join(target, rel_path)
        actions.append(f"DELETE {rel_path}")
        if not dry_run:
            try:
                os.remove(dest)
            except Exception as e:
                actions[-1] += f" (FAILED: {e})"

    # Copy/Overwrite files from source to target
    for rel_path in diff["added"] + diff["modified"]:
        src_file = os.path.join(source, rel_path)
        dest_file = os.path.join(target, rel_path)
        action_type = "COPY" if rel_path in diff["added"] else "OVERWRITE"
        actions.append(f"{action_type} {rel_path}")
        
        if not dry_run:
            try:
                dest_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copy2(src_file, dest_file)
            except Exception as e:
                actions[-1] += f" (FAILED: {e})"
                
    return actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync two directories.")
    parser.get_default('dry_run')
    parser.add_argument("source", help="Source directory")
    parser.add_argument("target", help="Target directory")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing")
    
    args = parser.parse_args()
    
    try:
        results = sync_dirs(args.source, args.target, dry_run=args.dry_run)
        if not results:
            print("Directories are already in sync.")
        for action in results:
            print(action)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)