# Protocolo de Ciclo de Vida de Desenvolvimento

## Preâmbulo

Este documento define o processo padrão a ser seguido para cada nova funcionalidade, módulo ou microsserviço dentro do Projeto Overpowered. O objetivo é garantir que cada componente seja bem projetado, implementado de forma robusta, rigorosamente testado e claramente documentado.

A adesão a este ciclo de vida de 5 etapas — **Planejar**, **Implementar**, **Testar**, **Robustecer**, **Documentar** — é fundamental para a qualidade, manutenibilidade e sucesso a longo prazo do projeto.

---

## Etapa 1 — Planejar (A Arquitetura da Ideia)

**Filosofia:** "Meça duas vezes, corte uma vez." Nenhum código de implementação é escrito nesta fase. O foco é transformar uma ideia ou requisito em um plano técnico detalhado e acionável.

### Atividades principais

- **Definição de requisitos**
  - Descrever claramente o que a funcionalidade deve fazer.
  - Definir os critérios de aceitação: Como saberemos que a funcionalidade está "pronta"?

- **Design da arquitetura**
  - Determinar onde a nova lógica se encaixará na arquitetura de microsserviços existente.
  - Decidir: será um novo serviço ou uma adição a um serviço existente?
  - Criar diagramas simples (sequência, componentes) para visualizar interações.

- **Definição da interface (o contrato)**
  - Para novos serviços ou APIs, definir o contrato formal usando *Protocol Buffers* (`.proto`) para **gRPC**.
  - Especificar requisições, respostas e métodos; isto é crítico para baixo acoplamento entre serviços.

- **Elaboração do plano de teste**
  - Tests unitários: quais classes/funções precisam de testes isolados?
  - Tests de integração: como testaremos a interação com outros serviços (ex.: chamadas gRPC)?
  - Testes end-to-end (E2E): descrever um cenário completo que valide a funcionalidade do ponto de vista do agente.

**Definition of Ready:** a implementação pode começar quando o plano está completo, as interfaces estão definidas e o plano de teste foi revisado e acordado.

---

## Etapa 2 — Implementar (A Tradução para o Código)

**Filosofia:** Escrever código limpo, testável e que adira ao plano.

### Atividades principais

- **Desenvolvimento orientado a testes (TDD) ou testes concorrentes**
  - Escrever os testes unitários definidos no plano antes ou junto com o código.
  - Garantir cobertura adequada para o novo código.

- **Codificação e boas práticas**
  - Implementar seguindo princípios de código limpo (nomes claros, funções pequenas, responsabilidade única).
  - Gerar o código servidor/cliente gRPC a partir dos arquivos `.proto`.

- **Revisão de código (Code Review)**
  - Todo código deve ser revisado por pelo menos outro membro da equipe.
  - Revisões visam identificar bugs, melhorar legibilidade e garantir conformidade com a arquitetura.

**Definition of Done:** o código está completo, todos os testes unitários passam e a revisão de código foi aprovada.

---

## Etapa 3 — Testar (Validação no Sistema)

**Filosofia:** "Confie, mas verifique." O código funciona isoladamente; agora provamos que funciona no sistema como um todo.

### Atividades principais

- **Execução dos testes de integração**
  - Validar a comunicação entre serviços (ex.: o Controlo Cognitivo chama o Serviço de Memória via gRPC e recebe resposta válida).

- **Execução dos testes end-to-end (E2E)**
  - Executar o cenário completo definido no plano (normalmente em um ambiente orquestrado, por exemplo `docker-compose`).

- **Registro de bugs**
  - Qualquer falha ou comportamento inesperado é registrado formalmente como bug, priorizado e corrigido.

**Definition of Done:** todos os testes de integração e E2E planejados passam; não há bugs críticos ou impeditivos conhecidos.

---

## Etapa 4 — Robustecer (Preparação para Produção)

**Filosofia:** Fazer funcionar é o começo; fazer funcionar de forma confiável e eficiente é a meta.

### Atividades principais

- **Profiling de performance**
  - Usar ferramentas de profiling para analisar consumo de CPU/memória.
  - Identificar e otimizar gargalos que afetem performance em tempo real.

- **Tratamento de erros e resiliência**
  - Garantir que o serviço lida graciosamente com falhas (ex.: serviço dependente indisponível).
  - Implementar retries com *exponential backoff* para chamadas de rede.

- **Logging e monitoramento**
  - Adicionar logs estruturados (ex.: JSON) que facilitem diagnóstico e análise.
  - Instrumentar métricas relevantes (latência, taxa de erro, throughput).

**Definition of Done:** a funcionalidade atende requisitos de performance, é resiliente a falhas comuns e produz logs/ métricas informativos.

---

## Etapa 5 — Documentar e Exemplificar (Transferência de Conhecimento)

**Filosofia:** "Código bem escrito explica como ele funciona. Documentação bem escrita explica por que ele existe."

### Atividades principais

- **Documentação técnica**
  - Atualizar o `README.md` do microsserviço com propósito, como executar e como consumir a API.
  - Atualizar diagramas de arquitetura relevantes.

- **Criação de exemplos de uso**
  - Incluir scripts de exemplo auto-contidos, ex.: `examples/use_memory_service.py` que demonstrem interações de cliente.

- **Registro de decisões arquiteturais (ADR)**
  - Para decisões significativas (ex.: escolha de gRPC vs REST), escrever um ADR que registre o raciocínio.

**Definition of Done:** documentação completa e precisa; um novo desenvolvedor pode entender a funcionalidade e como usá-la sem ler todo o código-fonte.

---

## Notas finais

Seguir este protocolo torna o trabalho previsível, testável e auditável. Para cada nova feature, verifique a checklist de desenvolvimento em `.kit/development-checklist.md` e acrescente observações específicas do componente no repositório (README, ADRs, exemplos e testes).