"""Run a rollout-based validation using the same lightweight checkpoint format.

This script wraps `tools.validate_worldmodel` and prints a human-friendly report.
"""
import subprocess
import json
import sys

def main():
    args = ['.venv\Scripts\python.exe', '-m', 'tools.validate_worldmodel', '--checkpoint', 'artifacts/wm_checkpoint.npz']
    try:
        print('Running validator...')
        res = subprocess.run(args, check=False, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print('Validation failed:', res.stderr, file=sys.stderr)
            sys.exit(res.returncode)
        print('Validation PASSED')
    except FileNotFoundError:
        print('Could not locate python executable or validator. Ensure virtualenv is set up.', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
