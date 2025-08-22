"""Calibrate thresholds for worldmodel validation from a dataset.

Usage: python -m tools.calibrate_thresholds --data path/to/validation.jsonl --percentile 95
This script computes MSE_h1, RMSE_h10 and DTW for each episode and writes the given
percentile value into `services/worldmodel/THRESHOLDS.json`.
"""
import argparse
import json
import numpy as np
import os

from tools.validate_worldmodel import load_jsonl_episodes, mse_h1, rollout_rmse, avg_dtw, build_params_from_npz


def compute_metrics_for_dataset(data_path, params=None):
    eps = load_jsonl_episodes(data_path)
    # If params not provided, we will use a zeroed toy model to compute metrics
    if params is None:
        # build trivial params with small random weights
        params = {'W1': np.zeros((4, 8), dtype=np.float32), 'b1': np.zeros(8, dtype=np.float32), 'W2': np.zeros((8, 4), dtype=np.float32), 'b2': np.zeros(4, dtype=np.float32)}
    m1 = []
    r10 = []
    dtw = []
    for ep in eps:
        try:
            m1.append(mse_h1(params, [ep]))
            r10.append(rollout_rmse(params, [ep], horizon=10))
            dtw.append(avg_dtw([ep], params))
        except Exception:
            continue
    return np.array(m1), np.array(r10), np.array(dtw)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=str, default='data/worldmodel/validation.jsonl')
    p.add_argument('--percentile', type=float, default=95.0)
    p.add_argument('--checkpoint', type=str, default=None)
    args = p.parse_args()

    params = None
    if args.checkpoint and os.path.exists(args.checkpoint):
        try:
            import numpy as _np
            ck = _np.load(args.checkpoint)
            params = build_params_from_npz(dict(ck))
        except Exception:
            params = None

    m1, r10, dtw = compute_metrics_for_dataset(args.data, params=params)

    def choose(arr):
        arr = arr[~np.isnan(arr)]
        if arr.size == 0:
            return None
        return float(np.percentile(arr, args.percentile))

    out = {}
    out['MSE_h1'] = choose(m1) or 0.5
    out['RMSE_h10'] = choose(r10) or 1.0
    out['DTW'] = choose(dtw) or 100.0

    os.makedirs('services/worldmodel', exist_ok=True)
    with open('services/worldmodel/THRESHOLDS.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('Wrote services/worldmodel/THRESHOLDS.json with:')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
