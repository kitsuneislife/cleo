# Serviço de Perceção

Função: interface com o cliente Minecraft e normalização dos dados sensoriais.
Tecnologias sugeridas: Python, gRPC, ONNX para modelos de visão.

Entradas/saídas:
- Recebe Observations via gRPC (ver `proto/service.proto`).
- Publica eventos para `worldmodel` ou persiste em fila.
