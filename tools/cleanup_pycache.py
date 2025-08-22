"""Small utility to remove __pycache__ folders and .pyc files under the repo.
Run this before pytest if import cache issues happen.
"""
import os
import sys

def remove_pycache(root):
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # remove __pycache__ directories
        if '__pycache__' in dirnames:
            path = os.path.join(dirpath, '__pycache__')
            try:
                for fn in os.listdir(path):
                    os.remove(os.path.join(path, fn))
                os.rmdir(path)
                removed += 1
            except Exception:
                pass
        # remove .pyc files
        for f in filenames:
            if f.endswith('.pyc'):
                try:
                    os.remove(os.path.join(dirpath, f))
                    removed += 1
                except Exception:
                    pass
    return removed

if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f"Cleaning pycache under {root}...")
    n = remove_pycache(root)
    print(f"Removed {n} items")
