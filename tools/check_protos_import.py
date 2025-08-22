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
