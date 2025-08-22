"""Decision utilities for Control service.
Provides deterministic ranking of a small set of operators for MVP.
This module supports optional lightweight persistence-based biasing.
"""
import hashlib
from typing import Optional


def rank_operators(state_bytes: bytes, agent_id: Optional[str] = None, store=None):
    """Return a list of operators ranked by utility.

    If `store` is provided, historical utilities for the agent will slightly
    bias the returned utilities (simple averaging heuristic).
    """
    # Deterministic base scores from state
    h = hashlib.sha256(state_bytes or b"").digest()
    score_base = h[0] / 255.0
    ops = [
        {"id": "op_move", "description": "move towards target", "utility": 0.8 + 0.2 * score_base},
        {"id": "op_mine", "description": "mine block", "utility": 0.6 + 0.3 * (1 - score_base)},
    ]

    # If historical data exists, compute average past utility per operator id
    if store is not None and agent_id is not None:
        try:
            recent = store.get_recent(agent_id, limit=20)
            # recent is list of operator-lists
            hist = {}
            counts = {}
            for entry in recent:
                for o in entry:
                    oid = o.get('id')
                    util = o.get('utility', 0)
                    hist[oid] = hist.get(oid, 0) + util
                    counts[oid] = counts.get(oid, 0) + 1
            avg = {k: (hist[k] / counts[k]) for k in hist}
            # apply small bias: 10% of historical average
            for o in ops:
                if o['id'] in avg:
                    o['utility'] = o['utility'] * 0.9 + avg[o['id']] * 0.1
        except Exception:
            # fail-safe: ignore storage issues
            pass

    ops.sort(key=lambda o: o['utility'], reverse=True)
    return ops
