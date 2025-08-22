"""Schema helpers for the worldmodel latent format and I/O serialization.

This module provides a compact JSON-friendly representation for the
latent `z` and utilities to encode/decode a base64-packed float32
array for compact transport when needed.
"""
from __future__ import annotations

import base64
import struct
from typing import List, Dict, Any
import importlib


def _try_import_proto():
    try:
        return importlib.import_module('proto.worldmodel_pb2')
    except Exception:
        return None


def z_to_bytes(z: List[float]) -> bytes:
    # Pack floats as little-endian float32
    return struct.pack(f"{len(z)}f", *z)


def z_to_base64(z: List[float]) -> str:
    return base64.b64encode(z_to_bytes(z)).decode("ascii")


def z_from_base64(s: str) -> List[float]:
    b = base64.b64decode(s)
    # infer length
    n = len(b) // 4
    return list(struct.unpack(f"{n}f", b))


def z_to_proto_bytes(z: List[float]) -> bytes:
    """Return bytes suitable to assign to the proto `LatentZ.z` field."""
    return z_to_bytes(z)


def z_from_proto_bytes(b: bytes) -> List[float]:
    n = len(b) // 4
    return list(struct.unpack(f"{n}f", b))


def inputstate_to_json(agent_id: str, timestamp: int, features: List[float]) -> Dict[str, Any]:
    return {"agent_id": agent_id, "timestamp": timestamp, "features": features}


def prediction_to_json(z: List[float], score: float = 1.0) -> Dict[str, Any]:
    return {"z_b64": z_to_base64(z), "score": score}
