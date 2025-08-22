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
