# Núcleo Cognitivo — Escopo (MVP)

Este documento descreve o escopo mínimo viável (MVP) do Núcleo Cognitivo para o projeto Cleo, suficiente para suportar integração com `control`, `worldmodel` e `execution` no ambiente de desenvolvimento.

Componentes e responsabilidades

1. Percepção (Perception)
   - Responsabilidade: transformar observações brutas (ex.: posição/estado do agente, eventos do ambiente) em um objeto de estado interno normalizado.
   - Entrada: payloads do adapter (JSON/base64) ou observadores simulados.
   - Saída: State proto (ex.: Position, Entities, Timestamps, AgentId).
   - Considerações: validação e sanitização; taxa de amostragem configurável; filtros básicos (e.g., deduplicação de eventos).

2. Procedural (Procedural memory / reactive policies)
   - Responsabilidade: regras reativas e operadores imediatos (ex.: seguir, olhar, pegar) que podem ser executados sem planejamento profundo.
   - Entrada: estado atual do mundo e eventos de percepção.
   - Saída: proposta de ações (ActionProposal) com prioridade/utility estimada.
   - Considerações: implementado inicialmente como uma lista ordenada de operadores com precondições simples e uma função de scoring.

3. Declarativa (Declarative memory / beliefs)
   - Responsabilidade: armazenamento simples de fatos e memórias de curto-prazo (ex.: últimos N observações, mapas simplificados).
   - API: store(key, value, ttl?), query(predicate) — infra leve em memória (LRU) e persistência opcional para debug.
   - Considerações: fornecer interfaces para recuperação rápida por control e planners.

4. Buffers (Working memory buffers)
   - Responsabilidade: interoperabilidade entre módulos — buffers para percepção, intención, contexto e resultados de planeamento.
   - Implementação: filas simples com capacidade limitada e políticas de substituição (FIFO/LRU configurável).

Interfaces e Contratos
- gRPC/proto shapes (MVP):
  - State proto: agent_id, timestamp, position{ x,y,z }, entities[], raw_blob
  - ActionProposal proto: operator_id, params (map<string,string>), utility (float)
  - DecisionRequest / DecisionResponse (existente entre adapter/control)

Erro e Resiliência
- Timeouts e retries para chamadas externas.
- Validação de entrada com fallback (estado mínimo) quando percepção falhar.

Métricas iniciais
- Latência de processamento por módulo (perception, procedural, declarative)
- Número de proposals geradas por segundo
- Taxa de falhas/validações de entrada

Critério de aceitação do MVP
- Perception converte observações do bot.js em State proto e entrega para control
- Procedural gera pelo menos 3 operadores básicos e envia ActionProposal válidas
- Declarative buffer armazena as últimas 50 observações e responde a queries básicas
- Todos os contratos documentados no `proto/` e exemplos em `examples/`


---

Commit checklist: marcar `1 Núcleo Cognitivo -> Planejar -> Definir escopo do núcleo` como concluído.
