"""Toy predictive model for Phase 2 POC.

Keeps deterministic, lightweight behavior suitable for tests.
"""
from hashlib import sha256


class ToyModel:
    """Simple deterministic predictor: hashes the state bytes and returns a short token.

    Methods:
    - predict(state_bytes) -> bytes
    """

    def predict(self, state_bytes: bytes) -> bytes:
        if state_bytes is None:
            state_bytes = b''
        h = sha256(state_bytes).digest()
        # return first 8 bytes as compact prediction
        return b'pred:' + h[:8]


def make_default_model() -> ToyModel:
    return ToyModel()
