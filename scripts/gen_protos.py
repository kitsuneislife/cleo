"""Generate Python gRPC stubs from .proto files into the `proto/` package.

This is a cross-platform replacement for `scripts/gen_protos.sh` that works on
Windows and in CI using the project's Python environment.
"""
import os
import sys
import glob
import subprocess
from grpc_tools import protoc


OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
os.makedirs(OUT_DIR, exist_ok=True)

proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
proto_files = glob.glob(os.path.join(proto_dir, '*.proto'))
if not proto_files:
    print('No .proto files found in proto/; exiting.')
    sys.exit(0)

args = [
    'protoc',
    f'-I={proto_dir}',
    f'--python_out={OUT_DIR}',
    f'--grpc_python_out={OUT_DIR}',
]
args.extend(proto_files)

print('Running protoc with args:', args)
res = protoc.main(args)
if res != 0:
    print('protoc failed with code', res)
    sys.exit(res)

# Fix imports in generated files to use package imports (from proto import ...)
for path in glob.glob(os.path.join(OUT_DIR, '*_pb2.py')) + glob.glob(os.path.join(OUT_DIR, '*_pb2_grpc.py')):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
        if 'from proto import' in src:
            continue
        src = src.replace('\nfrom . import ', '\nfrom proto import ')
        # replace 'import control_pb2 as control__pb2' to 'from proto import control_pb2 as control__pb2'
        import_pattern = '\nimport '
        lines = src.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('import ') and line.endswith('_pb2 as ' + lines[i].split()[-1]):
                lines[i] = 'from proto import ' + line[len('import '):]
        new_src = '\n'.join(lines)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_src)
    except Exception as e:
        print('warning: failed to patch', path, e)

print('Generated stubs in', OUT_DIR)
