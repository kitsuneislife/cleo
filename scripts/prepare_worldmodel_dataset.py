"""Prepare worldmodel dataset by mixing offline JSONL with synthetic dreams.

Output options: JSONL (frame per line) or NPZ per-episode bundle.
"""
import argparse
import json
import os
from services.worldmodel.dreams import generate_dreams


def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


def write_jsonl(path, items):
    with open(path, 'w', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(it) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--offline', type=str, help='path to offline JSONL (optional)')
    p.add_argument('--out', type=str, default='data/worldmodel/mixed.jsonl')
    p.add_argument('--num-dreams', type=int, default=100)
    p.add_argument('--length', type=int, default=50)
    p.add_argument('--rho', type=float, default=0.5, help='proportion of dreams')
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    dreams = generate_dreams(num_agents=args.num_dreams, length=args.length)
    dream_items = []
    for traj in dreams:
        dream_items.append({'agent_id': traj[0]['agent_id'], 'episode': traj})

    offline_items = []
    if args.offline:
        offline_items = list(load_jsonl(args.offline))

    # Mix: proportion rho dreams as episodes, rest offline frames (simple scheme)
    mixed = []
    n_dreams = int(len(dream_items) * args.rho)
    mixed.extend(dream_items[:n_dreams])
    # flatten offline frames into episode wrappers
    for i, frame in enumerate(offline_items):
        mixed.append({'agent_id': frame.get('agent_id', f'offline-{i}'), 'episode': [frame]})

    write_jsonl(args.out, mixed)
    print('Wrote', args.out, 'with', len(mixed), 'items')


if __name__ == '__main__':
    main()
