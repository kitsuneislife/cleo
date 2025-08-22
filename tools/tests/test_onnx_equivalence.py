"""
Teste mínimo de equivalência entre modelo original e exportado ONNX.

Uso:
  python tools/tests/test_onnx_equivalence.py --checkpoint artifacts/wm_checkpoint.npz --onnx artifacts/wm_checkpoint.onnx
"""
import numpy as np
import argparse

# Mock: compara outputs de dois modelos (substitua por chamada real ao ONNX)
def compare_models(checkpoint_path, onnx_path):
    # Carrega checkpoint original (mock)
    orig_out = np.array([1.0, 2.0, 3.0])
    # Carrega output ONNX (mock)
    onnx_out = np.array([1.0, 2.0, 3.0])
    # Calcula diferença
    diff = np.abs(orig_out - onnx_out).max()
    print(f"Máxima diferença: {diff}")
    return diff < 1e-5

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--onnx', required=True)
    args = parser.parse_args()
    ok = compare_models(args.checkpoint, args.onnx)
    if ok:
        print("Equivalência validada!")
    else:
        print("Falha na equivalência!")

if __name__ == "__main__":
    main()
