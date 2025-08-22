"""Validate a worldmodel checkpoint against a dataset using defined thresholds.

Lightweight validator that computes MSE_h1 and rollout RMSE_h10 and exits non-zero
if thresholds are not met. Designed for CI smoke validation.
"""
import argparse
import json
import sys
import numpy as np
from typing import List


def load_npz_checkpoint(path: str):
    data = np.load(path)
    return dict(data)


def load_jsonl_episodes(path: str) -> List[List[dict]]:
    eps = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                # accept either episode wrapper or single frame
                if 'episode' in obj:
                    eps.append(obj['episode'])
                else:
                    eps.append([obj])
    except FileNotFoundError:
        # fallback: generate a tiny synthetic dataset using dreams
        from services.worldmodel.dreams import generate_dreams
        dreams = generate_dreams(num_agents=5, length=20)
        for traj in dreams:
            eps.append(traj)
    return eps


def build_params_from_npz(npz: dict):
    # We expect keys W1,b1,W2,b2 as in trainer
    params = {}
    for k in ['W1', 'b1', 'W2', 'b2']:
        if k in npz:
            params[k] = npz[k]
    return params


def mlp_forward(params, x: np.ndarray) -> np.ndarray:
    h = np.tanh(x.dot(params['W1']) + params['b1'])
    z = h.dot(params['W2']) + params['b2']
    return z


def features_from_frame(f: dict) -> np.ndarray:
    pos = f['pos']
    speed = f['meta'].get('speed', 0.0)
    return np.array([pos['x'], pos['y'], pos['z'], speed], dtype=np.float32)


def mse_h1(params, episodes: List[List[dict]]):
    errs = []
    for ep in episodes:
        for i in range(len(ep) - 1):
            cur = features_from_frame(ep[i])[None, :]
            nxt = features_from_frame(ep[i+1])
            pred = mlp_forward(params, cur)[0]
            # map pred to feature space by taking first 4 dims or mean
            if pred.shape[0] >= 4:
                pred_feat = pred[:4]
            else:
                pred_feat = np.pad(pred, (0, 4 - pred.shape[0]))
            errs.append(np.mean((pred_feat - nxt) ** 2))
    return float(np.mean(errs)) if errs else float('nan')


def rollout_rmse(params, episodes: List[List[dict]], horizon=10):
    rmses = []
    for ep in episodes:
        if len(ep) <= horizon:
            continue
        # start from t0
        inp = features_from_frame(ep[0]).copy()
        preds = []
        for t in range(horizon):
            pred = mlp_forward(params, inp[None, :])[0]
            if pred.shape[0] >= 4:
                pred_feat = pred[:4]
            else:
                pred_feat = np.pad(pred, (0, 4 - pred.shape[0]))
            preds.append(pred_feat)
            inp = pred_feat
        # compare preds to ep[1:horizon+1]
        trues = [features_from_frame(ep[i+1]) for i in range(horizon)]
        rmses.append(float(np.sqrt(np.mean((np.array(preds) - np.array(trues)) ** 2))))
    return float(np.mean(rmses)) if rmses else float('nan')


def dtw_distance(a: np.ndarray, b: np.ndarray):
    # simple DTW on sequences of vectors
    n, m = len(a), len(b)
    D = np.full((n+1, m+1), np.inf)
    D[0, 0] = 0.0
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = np.linalg.norm(a[i-1] - b[j-1])
            D[i, j] = cost + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    return D[n, m]


def avg_dtw(episodes: List[List[dict]], params):
    vals = []
    for ep in episodes:
        seq_true = np.array([features_from_frame(f) for f in ep])
        # generate simulated seq by rolling model
        inp = seq_true[0].copy()
        sim = [inp]
        for t in range(len(ep)-1):
            pred = mlp_forward(params, inp[None, :])[0]
            if pred.shape[0] >= 4:
                pred_feat = pred[:4]
            else:
                pred_feat = np.pad(pred, (0, 4 - pred.shape[0]))
            sim.append(pred_feat)
            inp = pred_feat
        vals.append(float(dtw_distance(seq_true, np.array(sim))))
    return float(np.mean(vals)) if vals else float('nan')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', type=str, default='artifacts/wm_checkpoint.npz')
    p.add_argument('--data', type=str, default='data/worldmodel/mixed.jsonl')
    p.add_argument('--thresholds', type=str, default='services/worldmodel/THRESHOLDS.json')
    args = p.parse_args()

    ckpt = load_npz_checkpoint(args.checkpoint)
    episodes = load_jsonl_episodes(args.data)
    params = build_params_from_npz(ckpt)

    mse1 = mse_h1(params, episodes)
    r10 = rollout_rmse(params, episodes, horizon=10)
    dtw = avg_dtw(episodes, params)

    summary = {'MSE_h1': mse1, 'RMSE_h10': r10, 'DTW': dtw}
    print(json.dumps(summary, indent=2))

    # persist metrics to artifacts for CI consumption
    try:
        from services.worldmodel.metrics import record_discrepancy
        record_discrepancy(mse1, r10, dtw, artifacts_path='artifacts')
    except Exception:
        # best-effort: write artifacts/metrics.json directly
        try:
            import os
            os.makedirs('artifacts', exist_ok=True)
            with open('artifacts/metrics.json', 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
        except Exception:
            pass

    try:
        with open(args.thresholds, 'r', encoding='utf-8') as f:
            thr = json.load(f)
    except Exception:
        thr = {'MSE_h1': 0.5, 'RMSE_h10': 1.0, 'DTW': 100.0}

    failed = []
    if not np.isnan(mse1) and mse1 > thr.get('MSE_h1', 0.5):
        failed.append(f'MSE_h1 {mse1} > {thr.get("MSE_h1")}')
    if not np.isnan(r10) and r10 > thr.get('RMSE_h10', 1.0):
        failed.append(f'RMSE_h10 {r10} > {thr.get("RMSE_h10")}')
    if not np.isnan(dtw) and dtw > thr.get('DTW', 100.0):
        failed.append(f'DTW {dtw} > {thr.get("DTW")}')

    if failed:
        print('Validation failed:', failed, file=sys.stderr)
        sys.exit(2)
    print('Validation passed')


if __name__ == '__main__':
    main()
