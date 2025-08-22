# Control Service

Minimal control service (Núcleo Cognitivo) for Cleo.

Purpose:
- Expose gRPC `ControlService` with two RPCs: `RequestDecision` and `ApplyAction`.
- Provide a decision loop that can query `worldmodel` and select operators.

Quickstart (development):

1. Install dependencies and generate protos:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m grpc_tools.protoc -Iproto --python_out=./proto --grpc_python_out=./proto proto/control.proto
```

2. Run the service locally:

```powershell
setx ENABLE_METRICS 1; setx CONTROL_METRICS_PORT 8000
python services\control\server.py
```

Notes:
- Metrics are optional, enabled via `ENABLE_METRICS=1` and exposed on `CONTROL_METRICS_PORT`.
- The service persists decisions to `services/control/control.db` by default.
# Serviço de Controlo Cognitivo

Função: implementar o ciclo Soar/ACT-R, orquestrar planeadores e executar decisões.
Tecnologias sugeridas: C++/Python, gRPC para comunicação com outros serviços.
