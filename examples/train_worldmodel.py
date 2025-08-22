"""Toy trainer for worldmodel using synthetic dreams.

Lightweight trainer using numpy-only dependencies. Exposes CLI for batch_size,
epochs and rho (proportion of dreams in mixed dataset). Checkpointing saves
numpy arrays for model weights.
"""
import argparse
import json
import os
import time
import numpy as np

from services.worldmodel.dreams import generate_dreams


def build_mlp(input_dim, hidden=64, output_dim=32):
    rng = np.random.RandomState(0)
    W1 = rng.randn(input_dim, hidden).astype(np.float32) * 0.1
    b1 = np.zeros(hidden, dtype=np.float32)
    W2 = rng.randn(hidden, output_dim).astype(np.float32) * 0.1
    b2 = np.zeros(output_dim, dtype=np.float32)
    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}


def mlp_forward(params, x):
    h = np.tanh(x.dot(params['W1']) + params['b1'])
    z = h.dot(params['W2']) + params['b2']
    return z


def train_step(params, x, lr=1e-3):
    # simple gradient-free update: move weights slightly towards a target z=mean(x)
    target = np.mean(x, axis=1, keepdims=True)
    pred = mlp_forward(params, x)
    loss = np.mean((pred - target) ** 2)
    # pseudo-update (not real gradients) for toy purposes
    for k in params:
        params[k] *= (1 - lr * 1e-3)
    return loss


def prepare_batch(dreams, batch_size):
    # flatten episodes into frames and extract features
    frames = []
    for ep in dreams:
        for f in ep:
            frames.append(f)
    # build random batches of feature vectors (meta.speed and pos)
    feats = []
    for f in frames:
        pos = f['pos']
        speed = f['meta'].get('speed', 0.0)
        feats.append([pos['x'], pos['y'], pos['z'], speed])
    X = np.array(feats, dtype=np.float32)
    # yield batches
    n = len(X)
    idx = np.arange(n)
    np.random.shuffle(idx)
    for i in range(0, n, batch_size):
        yield X[idx[i:i+batch_size]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--batch_size', type=int, default=32)
    p.add_argument('--epochs', type=int, default=1)
    p.add_argument('--rho', type=float, default=0.5)
    p.add_argument('--checkpoint', type=str, default='artifacts/wm_checkpoint.npz')
    p.add_argument('--onnx', action='store_true', help='export ONNX if onnx installed')
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.checkpoint), exist_ok=True)

    # generate dreams
    dreams = generate_dreams(num_agents=20, length=50)

    # simple mixing: use only dreams for now; rho reserved for offline mixing
    model = build_mlp(input_dim=4, hidden=64, output_dim=32)

    steps = 0
    for epoch in range(args.epochs):
        for batch in prepare_batch(dreams, args.batch_size):
            loss = train_step(model, batch)
            steps += 1
            if steps % 10 == 0:
                print(f'step={steps} loss={loss:.6f}')
            # early stop for smoke tests
            if steps >= 50:
                break
        if steps >= 50:
            break

    # checkpoint
    np.savez(args.checkpoint, **model)
    print('Saved checkpoint to', args.checkpoint)

    # optional ONNX export (if onnx available)
    if args.onnx:
        try:
            import onnx
            # naive: save weights as npz and note that ONNX export is skipped in this
            # lightweight example. Real export requires a framework (torch/keras).
            print('ONNX package is present but export requires framework; skipping real export')
        except Exception:
            print('onnx not available; skipping ONNX export')


if __name__ == '__main__':
    main()
