"""Example: convert prediction JSON (with base64 `z_b64`) to proto `Prediction` and back.

This script requires generated Python proto stubs under `proto/` (CI runs
`scripts/gen_protos.py`). If stubs are not present it will print a message
and exit gracefully.
"""
from services.worldmodel import schema

try:
    from proto import worldmodel_pb2
except Exception:
    print('Proto stubs not found. Run `python scripts/gen_protos.py` to generate them.')
    raise SystemExit(1)


def json_to_proto(pred_json):
    z_list = schema.z_from_base64(pred_json['z_b64'])
    # convert list of floats -> packed bytes
    packed = schema.z_to_proto_bytes(z_list)
    p = worldmodel_pb2.Prediction()
    p.z.z = packed
    p.score = pred_json.get('score', 1.0)
    return p


def proto_to_json(pred_proto):
    b = pred_proto.z.z
    z = schema.z_from_proto_bytes(b)
    return {"z_b64": schema.z_to_base64(z), "score": pred_proto.score}


def main():
    example = schema.prediction_to_json([0.5, -0.5, 1.0], score=0.8)
    print('Example JSON:', example)
    p = json_to_proto(example)
    print('Proto prediction:', p)
    j = proto_to_json(p)
    print('Back to JSON:', j)


if __name__ == '__main__':
    main()
