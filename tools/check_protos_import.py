"""Utility to verify generated Python protobuf stubs import correctly.

Run this locally or in CI to ensure the `proto` package and stubs are importable.
"""
import sys
import logging
import os

# Ensure repo root is on sys.path so `from proto import ...` works when this
# script is executed as `python tools/check_protos_import.py` from the repo root.
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

logger = logging.getLogger('cleo.tools.check_protos_import')
logging.basicConfig(level=logging.INFO)


def main():
    ok = True
    try:
        # Preferred import path when package is installed / in PYTHONPATH
        from proto import control_pb2, control_pb2_grpc  # type: ignore
        logger.info('Imported proto.control_pb2 and proto.control_pb2_grpc successfully')
    except Exception as e:
        logger.warning('Package import failed: %s', e)
        ok = False
    try:
        # Fallback: top-level generated modules
        import control_pb2  # type: ignore
        import control_pb2_grpc  # type: ignore
        logger.info('Imported top-level control_pb2 modules successfully')
    except Exception as e:
        logger.warning('Top-level import failed: %s', e)
        ok = ok or False

    if not ok:
        logger.error('Proto import checks failed; run `scripts/gen_protos.sh` and ensure generated files are on PYTHONPATH')
        sys.exit(2)
    print('OK')


if __name__ == '__main__':
    main()
"""Quick check that the generated proto package imports correctly.

Exit 0 on success, non-zero on failure.
"""
import sys
try:
    import proto
    from proto import control_pb2, control_pb2_grpc, worldmodel_pb2, worldmodel_pb2_grpc
except Exception as e:
    print('proto import failed:', e)
    sys.exit(2)
print('proto imports ok')
sys.exit(0)
