import os
import hashlib
from collections import defaultdict
import argparse

def compute_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, PermissionError):
        return None

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def find_duplicates(directory):
    hash_map = defaultdict(list)
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_hash = compute_hash(file_path)
            if file_hash:
                hash_map[file_hash].append(file_path)
    return hash_map

def delete_duplicates(hash_map):
    removed_files = 0
    space_freed = 0
    for files in hash_map.values():
        if len(files) > 1:
            for file_path in files[1:]:
                try:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    removed_files += 1
                    space_freed += size
                except (OSError, PermissionError):
                    continue
    return removed_files, space_freed

def confirm_proceed():
    print("SELODesigns - Dedupe Script")
    print("\n⚠️ WARNING: This script will permanently delete duplicate files.")
    print("There is NO undo. Use at your own risk.\n")
    while True:
        answer = input("Are you sure you want to proceed? (y/n): ").strip().lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            print("Operation cancelled by user.")
            return False
        else:
            print("Please enter 'y' or 'n'.")

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate files in a directory by comparing hashes.")
    parser.add_argument("directory", help="Target directory to scan for duplicates")
    args = parser.parse_args()

    if not confirm_proceed():
        return

    print(f"🔍 Scanning '{args.directory}' for duplicates...")
    hash_map = find_duplicates(args.directory)
    removed_files, space_freed = delete_duplicates(hash_map)

    print(f"\n✅ Duplicate cleanup complete.")
    print(f"🗑️ Files removed: {removed_files}")
    print(f"💾 Space freed: {format_size(space_freed)}")

if __name__ == "__main__":
    main()
