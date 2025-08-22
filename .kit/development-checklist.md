# Checklist de Desenvolvimento — Projeto Cleo

Objetivo: checklist orientada por etapas (Planejar → Implementar → Testar → Robustecer → Documentar) mapeada para as áreas do manifesto (`.kit/summary.md`) e seguindo o protocolo (`.kit/protocol.md`). Use esta lista como referência em PRs, reviews e ADRs.

Instruções rápidas
- Lembre-se de atualizar o status das tasks nesse arquivo SEMPRE.
- Para cada item marque [ ] quando pendente e [x] quando concluído.
- Crie um ADR para decisões arquiteturais importantes.
- Atualize o `README.md` do serviço e a checklist neste arquivo sempre que acrescentar um novo serviço ou mudança de contrato.

---

## Tabela de conteúdos (áreas)
- Núcleo Cognitivo
- Modelo do Mundo (V–M–C)
- Planeamento (HTN + GOAP)
- Motivação e Aprendizagem (ICM, antifragilidade)
- Fenómenos Cognitivos (Memórias, Criatividade)
- Arquitetura de Software (microsserviços, infra)
- Avaliação e Métricas
- Tarefas transversais (proto, CI, segurança, infra)

---

## Padrão de cada item (por componente)
Para cada componente aplicar as 5 etapas do protocolo:
1) Planejar — artefatos: requisitos, contratos `.proto`, plano de testes, Definition of Ready
2) Implementar — TDD, código limpo, geração de stubs, PRs com reviewers
3) Testar — unit, integração, E2E em ambiente orquestrado
4) Robustecer — profilings, retries, timeouts, logs/metrics, hardening
5) Documentar — README do serviço, exemplos em `examples/`, ADRs

---

## 1 Núcleo Cognitivo
- Planejar
  - [ ] Definir escopo do núcleo (módulos: perceção, procedural, declarativa, buffers)
  - [x] Especificar APIs entre `control` e planeadores (gRPC `.proto`)
  - [x] Criar Definition of Ready com critérios de aceitação e benchmarks iniciais
- Implementar
  - [x] Esqueleto do serviço `services/control` com servidor gRPC
  - [x] Implementar ciclo de decisão mínimo (percepção → proposta → seleção → ação)
  - [x] Tests unitários para o loop de decisão (simulações determinísticas)
- Testar
  - [x] Testes de integração: `control` ↔ `worldmodel` ↔ `execution` no `docker-compose` (smoke via local stubs)
  - [ ] E2E smoke: executar cenário de alto-nível (ex.: alcançar e minerar um bloco)
- Robustecer
  - [x] Instrumentar métricas (latência, taxa de decisões por segundo) (opt-in via ENABLE_METRICS)
  - [x] Adicionar circuit-breaker e retries para chamadas externas (basic retry logic present in worldmodel call handling)
  - [x] Definir limites de recursos para containers
- Documentar
  - [x] README com contrato do serviço e exemplos de chamadas
  - [x] ADR se a implementação divergir do design híbrido Soar/ACT-R

---

## 2 Modelo do Mundo (V–M–C)
- Planejar
  - [ ] Definir formato latente `z` e esquema de inputs/outputs (proto ou JSON compactado)
  - [ ] Planejar pipeline de treino (offline + sonhos) e datasets necessários
  - [ ] Documentar critérios de qualidade do modelo (MSE, likelihood, fidelidade de simulação)
- Implementar
  - [x] Implementar serviço `worldmodel` com endpoints gRPC para predição e simulação (toy predictor)
  - [ ] Implementar utilitário para gerar 'sonhos' (trajectórias simuladas)
  - [x] Tests unitários para modelos (shape/contratos) e integração com dados sintéticos
- Testar
  - [x] Validar que o controlador obtém previsões coerentes em cenários simples
  - [ ] Medir discrepância previsão vs realidade e registar como métrica
- Robustecer
  - [ ] Exportar modelo para ONNX e validar inferência equivalência
  - [ ] Adicionar cache e batch inference para throughput
  - [ ] Monitorar drift do modelo e pipeline de retraining automatizado
- Documentar
  - [ ] README com como treinar, exportar e usar o modelo (ex.: `examples/train_worldmodel.py`)

---

## 3 Planeamento Hierárquico (HTN + GOAP)
- Planejar
  - [ ] Definir linguagem de domínio para HTN e representação de objetivos para GOAP
  - [ ] Definir contratos entre HTN → GOAP → Control (proto)
- Implementar
  - [ ] Implementar HTN planner skeleton (gerar tasks de alto nível)
  - [ ] Implementar GOAP planner (operadores com precondições/efeitos e heurística A*)
  - [ ] Cobertura unitária dos decompositores e do buscador
- Testar
  - [ ] Integração HTN+GOAP com `control` em cenários variados (teste parametrizado)
  - [ ] Benchmarks de latência para planos táticos em diferentes tamanhos de estado
- Robustecer
  - [ ] Timeout e fallback strategy (se GOAP falhar, tentar operadores defensivos)
  - [ ] Persistir planos críticos e replan quando inconsistências surgirem
- Documentar
  - [ ] README e exemplos: como definir HTNs e operadores GOAP

---

## 4 Motivação Intrínseca, Antifragilidade e Aprendizagem
- Planejar
  - [ ] Especificar sinal de recompensa intrínseca (ICM) e métricas associadas
  - [ ] Planejar armazenamento de incidentes (AIID) e formato de logs/análises
- Implementar
  - [ ] Módulo ICM que computa recompensa a partir de erro de predição
  - [ ] Pipeline que alimenta reforço e atualiza utilidades/subsimbólicas
- Testar
  - [ ] Testes que mostrem exploração preferencial em ambientes de recompensa esparsa
  - [ ] Simular falhas e validar que AIID registra causas e ações
- Robustecer
  - [ ] Limitar taxa de exploração e controlar trade-off exploração/exploração
  - [ ] Adotar checkpoints e rollback para políticas perigosas
- Documentar
  - [ ] Documentar algoritmos, métricas e políticas de segurança/limites

---

## 5 Fenômenos Cognitivos Avançados
- Planejar
  - [ ] Priorizar quais módulos de memória e criatividade serão MVP
  - [ ] Definir interface para memória episódica/semântica (vetor DB) e procedural
- Implementar
  - [ ] Serviço de `memory` com operações básicas: store, query (RAG-friendly)
  - [ ] Módulo criativo com interface para gerar candidatos (offline)
- Testar
  - [ ] Validar recuperação de memórias relevantes (recall precision)
  - [ ] Testes de integração RAG → controlador
- Robustecer
  - [ ] Deduplicação, compactação e políticas de retenção de memória
  - [ ] Custo computacional do módulo criativo isolado (batching/worker)
- Documentar
  - [ ] Exemplos de uso e critérios de validade das memórias

---

## 6 Arquitetura de Software e Infra
- Planejar
  - [ ] Decidir políticas de segurança (mTLS, secret management, RBAC)
  - [ ] Definir infra alvo (docker-compose para dev, k8s para produção)
  - [ ] Criar ADRs para escolhas infra/observability
- Implementar
  - [ ] Dockerfile template por serviço
  - [ ] Helm chart / kustomize skeleton (opcional inicial)
  - CI: pipeline (status parcial)
    - [x] geração de stubs (protoc) no CI (`scripts/gen_protos.sh` + step)
    - [x] lint (ruff) no CI
    - [x] test (pytest) no CI
    - [ ] build image (docker build/publish) no CI
    - [x] scan (pip-audit) no CI (step presente; currently permissive)
- Testar
  - [x] Testes E2E em compose; smoke em cluster (se disponível) — verificado com `examples/minecraft` (bot spawnou e fluxo adapter→control→worldmodel observado)
  - [ ] Testes de resiliência (kill/restart serviços)
- Robustecer
  - [ ] Monitoramento (Prometheus + Grafana), tracing (OpenTelemetry)
  - [ ] Política de backups para DB vetorial e modelos críticos
- Documentar
  - [ ] How-to deploy, run and rollback; healthchecks; onboarding guide

---

## 7 Avaliação e Métricas
- Planejar
  - [ ] Definir benchmarks (tarefas e datasets) e métricas (C, E, B + qualitativas)
  - [ ] Ferramentas para coleta de dados (logs, traces, vetores de features)
- Implementar
  - [ ] Instrumentação nos serviços para expor métricas (Prometheus metrics)
  - [ ] Scripts para calcular métricas de similaridade e entropia de percurso
- Testar
  - [ ] Rodar benchmarks controlados e coletar baselines
- Robustecer
  - [ ] Painéis de observabilidade com alertas para regressões de performance
- Documentar
  - [ ] Processos de avaliação, templates de relatório e planos de experimentos

---

## Tarefas transversais e lista mínima inicial
 - [ ] Adicionar `Dependabot` / atualização automática de dependências
 - [x] Adicionar `pip-audit` ou scanner equivalente no CI (step incluído)
 - [x] Automatizar geração de stubs no CI (`protoc` step)
 - Adicionar linter/formatter no CI
   - [x] ruff (lint) — já incluído no CI
   - [ ] black / isort (formatter) — não incluído ainda
 - Criar Dockerfiles por serviço e Makefile
   - [ ] Dockerfiles por serviço
   - [x] Makefile com targets: `dev`, `test`, `build`
 - [ ] Criar templates de secrets e instruções para secret manager (ex.: HashiCorp Vault / AWS Secrets)
 - [ ] Implementar política de logs (Structured JSON) e evitar PII
 - [ ] Definir e documentar processo para ADRs

---

## Critérios de aceitação gerais (Definition of Done)
- Código com testes unitários cobrindo comportamento crítico
- Contratos `.proto` versionados e geradores automáticos no CI
- Documentação mínima: README do serviço, exemplos, ADRs para decisões relevantes
- Segurança: configuração de CI para scanner de dependências e não comitar secrets
- Observability mínima: métricas básicas e logs estruturados

---

## Notas finais
- Atualize esta checklist sempre que um novo serviço for adicionado ou quando um critério evoluir.
- Use PR templates que referenciem os itens relevantes desta checklist para garantir conformidade.

---

_End of checklist_
