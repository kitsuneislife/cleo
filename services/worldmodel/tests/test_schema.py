import time
from services.worldmodel import schema


def test_z_roundtrip():
    z = [0.1, -2.3, 4.5, 0.0]
    b64 = schema.z_to_base64(z)
    out = schema.z_from_base64(b64)
    # allow exact equality for small arrays of float32
    assert len(out) == len(z)
    for a, b in zip(z, out):
        assert abs(a - b) < 1e-6


def test_prediction_json():
    z = [1.0, 2.0]
    j = schema.prediction_to_json(z, score=0.9)
    assert "z_b64" in j
    assert abs(j["score"] - 0.9) < 1e-9
