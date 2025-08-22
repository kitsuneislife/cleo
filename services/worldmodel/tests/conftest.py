import sys
from pathlib import Path


def pytest_configure(config):
    # Ensure repository root is on sys.path so tests can import generated proto package
    repo_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(repo_root))
