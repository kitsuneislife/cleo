# Fase 1 — Definition of Ready: Núcleo Cognitivo (Control)

Critérios para começar a implementação do núcleo cognitivo (control):

- Requisitos funcionais claros:
  - O serviço deve expor `RequestDecision` e `ApplyAction` via gRPC.
  - Deve aceitar um estado abstrato serializado e retornar operadores candidatos com utilidade.
- Contratos definidos:
  - `proto/control.proto` presente e versionado.
- Plano de testes:
  - Tests unitários para a lógica de ranking de operadores.
  - Testes de integração smoke com `worldmodel`(stub) e `execution`(stub).
- Recursos e restrições:
  - Owner/author definido para a feature.
  - Benchmarks iniciais esperados (latência < 200ms em decisão simples).

Quando todos os itens acima estiverem marcados, a implementação pode começar.
