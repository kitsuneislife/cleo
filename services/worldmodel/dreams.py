"""Simple 'dreams' generator for the worldmodel service.

Generates synthetic trajectories (sequences of state dicts) suitable for
local testing and small training experiments. Kept dependency-free so it runs
in CI without extra packages.
"""
from typing import List, Dict
import random
import time


def _random_pos(seed=None):
    return {
        'x': random.uniform(-10, 10),
        'y': random.uniform(0, 100),
        'z': random.uniform(-10, 10),
    }


def generate_dream(agent_id: str, length: int = 50) -> List[Dict]:
    """Generate a single trajectory (dream) for an agent.

    Each frame is a dict with keys: timestamp, agent_id, pos, metadata.
    """
    frames = []
    ts = int(time.time())
    for i in range(length):
        frame = {
            'timestamp': ts + i,
            'agent_id': agent_id,
            'pos': _random_pos(),
            'meta': {
                'step': i,
                'speed': random.uniform(0, 5),
            },
        }
        frames.append(frame)
    return frames


def generate_dreams(num_agents: int = 5, length: int = 50) -> List[List[Dict]]:
    """Generate multiple dreams (one per agent).

    Returns a list of trajectories.
    """
    dreams = []
    for n in range(num_agents):
        aid = f'agent-{n+1}'
        dreams.append(generate_dream(aid, length=length))
    return dreams


if __name__ == '__main__':
    import json
    ds = generate_dreams(3, 20)
    print(json.dumps(ds[:1], indent=2)[:1000])
