"""Example: consume dreams and run a toy training loop.

This script demonstrates how to use `services.worldmodel.dreams` to produce
synthetic trajectories and run a minimal 'training' pass that computes simple
statistics. It's intended as documentation and an example for the README.
"""
from services.worldmodel.dreams import generate_dreams
import statistics
import json


def summarize(dreams):
    stats = []
    for traj in dreams:
        speeds = [f['meta']['speed'] for f in traj]
        stats.append({'mean_speed': statistics.mean(speeds), 'len': len(traj)})
    return stats


def main():
    dreams = generate_dreams(num_agents=4, length=30)
    s = summarize(dreams)
    print(json.dumps(s, indent=2))


if __name__ == '__main__':
    main()
