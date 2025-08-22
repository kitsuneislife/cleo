# Worldmodel — Dreams generator

This package contains a small utilities module used to generate synthetic "dreams" (trajectories) for the worldmodel service. The dreams generator is intentionally lightweight and deterministic-friendly so it can be used in unit tests, examples and toy training loops.

Files
- `dreams.py` — functions to generate single-agent and multi-agent trajectories (`generate_dream`, `generate_dreams`). Each frame is a simple dict with `timestamp`, `agent_id`, `pos` and optional `meta`.
- `tests/test_dreams.py` — unit tests validating shapes and agent ids.
- `examples/train_worldmodel.py` — a tiny consumer example that loads generated dreams, computes simple statistics (e.g., average speed) and demonstrates how to wire the generator into a training flow.

Usage

Basic usage from Python:

```python
from services.worldmodel.dreams import generate_dreams

# generate 5 agents each with length-100 trajectories
dreams = generate_dreams(num_agents=5, length=100)
for traj in dreams:
    print(traj[0]['agent_id'], 'len=', len(traj))
```

Run the example script:

1. From the repository root run (uses the repo Python):

```bash
python examples/train_worldmodel.py
```

What to expect
- The example prints some simple statistics about the synthetic trajectories (mean speed per agent).
- The unit tests exercise basic shape/contract assertions and should pass in CI.

Testing

Run the worldmodel unit tests with pytest (from repo root):

```bash
pytest services/worldmodel/tests/test_dreams.py -q
```

Notes
- The generator is a toy utility. For production or research experiments you may want to replace the trajectory schema with a typed dataclass, add random seeds, richer physics, and a serialization format (e.g., Protobuf or JSONL). The current schema was chosen for clarity and testability.
# WorldModel Service

Stub and development notes for the WorldModel service used by `control` in Phase 2.

Quickstart (dev):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m grpc_tools.protoc -Iproto --python_out=./proto --grpc_python_out=./proto proto/worldmodel.proto
python services\worldmodel\server.py
```

The Phase 2 implementation will provide two main RPCs: `Predict` (single-step prediction) and `Simulate` (rollout / trajectory generation).
# Serviço Modelo do Mundo

Função: manter estado internalizado (V–M–C) e expor simulações/sonhos para treino.
Tecnologias sugeridas: PyTorch/TensorFlow, LSTM/VAE, ONNX e gRPC.
