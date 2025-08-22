#!/usr/bin/env bash
set -euo pipefail

# Generate Python gRPC stubs from proto files into the proto/ package
OUT_DIR=./proto
mkdir -p ${OUT_DIR}

# Find .proto files relative to repo root
PROTO_FILES=$(find proto -name "*.proto" | tr '\n' ' ')

if [ -z "${PROTO_FILES}" ]; then
  echo "No .proto files found in proto/; exiting."
  exit 0
fi

python -m grpc_tools.protoc \
  -I=proto \
  --python_out=${OUT_DIR} \
  --grpc_python_out=${OUT_DIR} \
  ${PROTO_FILES}

# Fix generated imports to be package-friendly (simple sed-based adjustment)
# Replace: import proto.control_pb2 as control__pb2
# With: from proto import control_pb2 as control__pb2
for f in ${OUT_DIR}/*_pb2.py ${OUT_DIR}/*_pb2_grpc.py; do
  if [ -f "$f" ]; then
    sed -i "s/^import \(.*_pb2\) as/from proto import \1 as/" "$f" || true
  fi
done

echo "Generated stubs in ${OUT_DIR}"
