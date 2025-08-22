# Cleo: Manifesto para um Agente Cognitivo Generalista em Minecraft

## Sumário

- Introdução
- Seção 1 — O Núcleo Cognitivo
- Seção 2 — Construindo o Modelo do Mundo
- Seção 3 — Planeamento e Execução
- Seção 4 — Motivação, Antifragilidade e Aprendizagem
- Seção 5 — Fenómenos Cognitivos Avançados
- Seção 6 — Arquitetura de Software
- Seção 7 — Avaliação
- Conclusão

## Introdução

Redefinindo "Overpowered" — Uma visão para a inteligência emergente.

O termo "overpowered" (OP), no contexto da inteligência artificial, tem sido historicamente associado a uma eficiência de execução de tarefas que excede em muito as capacidades humanas. No entanto, esta definição é limitadora. Um agente verdadeiramente "overpowered" não deve ser medido apenas pela sua velocidade em minerar blocos ou pela sua precisão em combate, mas sim pela sua capacidade de exibir um conjunto de competências generalistas que conduzem a comportamentos emergentes, adaptativos e criativos.

O ambiente de Minecraft serve como o "recipiente de Petri digital" ideal para esta ambição. A sua natureza de mundo aberto (sandbox), as regras causais complexas e a necessidade de planeamento a longo prazo oferecem um campo de testes inigualável para o desenvolvimento e estudo de comportamentos semelhantes aos da Inteligência Artificial Geral (AGI). Este projeto não visa "resolver" o Minecraft, mas sim utilizá-lo como um ecossistema para fomentar e analisar uma inteligência emergente.

Objetivos centrais:

- Projetar um agente cognitivo capaz de operar autonomamente em horizontes temporais longos, sem instruções pré-definidas.
- Criar uma arquitetura que aprende continuamente com a experiência, incluindo com as suas falhas.
- Servir como plataforma de investigação para estudar motivação intrínseca, planeamento hierárquico e simulação cognitiva.

---

## Seção 1 — O Núcleo Cognitivo: Arquitetando uma Mente Digital

### 1.1 Defesa de uma Arquitetura Cognitiva Híbrida

Um agente com ambição de inteligência generalista não pode depender de um único modelo monolítico (por exemplo, um LLM puro). Arquiteturas cognitivas oferecem a infraestrutura para aquisição e utilização de conhecimento, fornecendo blocos de construção computacionais necessários para inteligência geral.

### 1.2 Integrando Soar e ACT-R

Em vez de ver Soar e ACT-R como concorrentes, propõe-se uma síntese que aproveite os pontos fortes de ambos:

- **Soar**: Hipótese do Espaço de Problemas; ciclo de decisão por proposta/avaliação/seleção/aplicação; mecanismo de impasses para gerar sub-objetivos.
- **ACT-R**: Design modular inspirado no cérebro (módulos perceptual-motor, memória declarativa, memória procedural) que comunicam por buffers; mistura simbólico/subsimbólico.

O plano é usar a modularidade do ACT-R como estrutura de alto nível e implementar o ciclo de decisão do Soar como o motor do módulo procedural central.

### 1.3 Ciclo de Decisão Proposto

O ciclo combina perceção, elaboração de operadores, avaliação/seleção, resolução de impasses e aprendizagem (chunking e reforço):

- Perceção: dados do jogo processados em buffers percetuais.
- Elaboração: regras procedurais ativadas para propor operadores.
- Avaliação/Seleção: utilidades subsimbólicas e preferências simbólicas determinam a escolha.
- Impasse/Ação: impasse cria sub-objetivo quando inseguro; caso contrário aplica a ação.
- Aprendizagem: chunking e atualização de utilidades por reforço.

### Tabela 1 — Comparação sintética

| Característica | Soar | ACT-R | Implementação Híbrida (Overpowered) |
|---|---:|---:|---|
| Princípio central | Espaço de Problemas (busca) | Teoria modular (buffers) | Arquitetura modular com decisão baseada em busca |
| Estrutura da memória | Memória de trabalho unificada + memórias de longo prazo | Módulos distintos (declarativa, procedural) | Memórias separadas + memória procedural central |
| Tomada de decisão | Proposta → seleção → aplicação; impasses | Seleção por correspondência + equações de utilidade | Ciclo do Soar com utilidades ACT-R |
| Aprendizagem | Chunking + reforço | Ajustes subsimbólicos (ativação/utilidade) | Chunking + aprendizagem subsimbólica |
| Simbólico/Subsimbólico | Predominantemente simbólico | Híbrido | Totalmente híbrido |

---

## Seção 2 — Construindo o Modelo do Mundo: Perceção, Previsão e Realidade Interna

### 2.1 Por que um modelo do mundo

Um agente precisa de um modelo interno que permita raciocinar, planear e prever resultados — isto transforma comportamento reativo em raciocínio orientado por modelos.

### 2.2 Arquitetura V–M–C

Três componentes interligados:

- **Visão (V)**: compressão dos dados sensoriais do jogo num vetor latente z.
- **Memória (M)**: modelo recorrente (ex.: LSTM) que aprende a dinâmica temporal e prevê z_{t+1}.
- **Controlador (C)**: toma decisões usando o estado latente e o estado recorrente, operando no espaço abstrato.

### 2.3 Treinar no "sonho"

O modelo M pode servir como um simulador interno ("sonho") para treinar o controlador rapidamente, gerando muitas trajetórias sem interação real com o jogo.

### 2.4 Mundo físico vs mundo mental

- Mundo físico: propriedades de objetos, leis físicas, affordances de ferramentas.
- Mundo mental: estados e intenções de outras entidades (Teoria da Mente).

O modelo do mundo funciona como motor de simulação generativa para imaginação e planeamento.

---

## Seção 3 — Dos Objetivos às Ações: Planeamento Hierárquico

### 3.1 Dois níveis de planeamento

Separar estratégia (longo prazo) de tática (curto prazo).

### 3.2 Camada estratégica — HTN (Hierarchical Task Networks)

HTNs decomõem tarefas abstratas em subtarefas; úteis para planos de longo prazo e conhecimento de domínio.

### 3.3 Camada tática — GOAP (Goal-Oriented Action Planning)

GOAP resolve objetivos imediatos por busca regressiva entre estado atual e estado-objetivo usando operadores com pré-condições e efeitos.

### 3.4 Integração HTN + GOAP

Fluxo proposto:

1. HTN gera plano estratégico de alto nível.
2. Tarefas primitivas da HTN são transformadas em objetivos para o GOAP.
3. GOAP encontra sequências concretas de ações para satisfazer cada objetivo no contexto atual.

Tabela 2 — Comparação HTN vs GOAP

| Característica | HTN | GOAP | Papel no sistema integrado |
|---|---:|---:|---|
| Abordagem | Top-down (decomposição) | Bottom-up (busca regressiva) | HTN = estratégia; GOAP = tática |
| Força | Estruturado, bom para planos longos | Flexível, emergente | Combina estabilidade e agilidade |
| Fraqueza | Pode ser rígido | Pode ser caro computacionalmente | Complementam-se |

---

## Seção 4 — Motivação Intrínseca, Antifragilidade e Aprendizagem ao Longo da Vida

### 4.1 Além de recompensas extrínsecas

Minecraft tem recompensas esparsas; motivação intrínseca é necessária para exploração e aquisição de competências intermédias.

### 4.2 Curiosidade (ICM)

Implementar um Módulo de Curiosidade Intrínseca (ICM) onde o erro de previsão entre modelo direto e observação gera recompensa intrínseca, incentivando exploração de estados novidadeiros.

### 4.3 Antifragilidade

Princípio: sistemas antifrágeis melhoram quando expostos à incerteza; falhas são oportunidades informacionais.

### 4.4 Aprender com falhas

Processo proposto:

- Deteção de falhas (discrepância previsão vs real).
- Análise causal via impasse e sub-objetivos.
- Reparação do conhecimento (criar/ajustar regras procedurais).
- AIID interno: registar incidentes e ações corretivas.

Combinar curiosidade e antifragilidade cria um ciclo de aprendizagem que incentiva riscos calculados.

---

## Seção 5 — Emulando Fenómenos Cognitivos Avançados

### 5.1 Memória de longo prazo

Camadas propostas:

- Memória de trabalho: contexto imediato.
- Memória episódica: Memory-Augmented Transformer para registos de experiências.
- Memória semântica: base de conhecimento vetorial para RAG.
- Memória procedural: regras de produção no núcleo cognitivo.

### 5.2 Criatividade

Módulo criativo baseado em GANs/cGANs treinadas em datasets de construções para gerar projetos condicionados por estilo; HTN usa esses planos para garantir funcionalidade.

### 5.3 Simular vieses cognitivos

Introduzir vieses intencionais (ancoragem, disponibilidade, custo irrecuperável) para produzir comportamento mais natural e credível.

---

## Seção 6 — A Forma Física: Arquitetura de Software Modular

### 6.1 Microsserviços orientados a agentes

Adotar microsserviços para refletir modularidade cognitiva: escalabilidade, resiliência e diversidade tecnológica.

### 6.2 Microsserviços centrais

Tabela 3 — Microsserviços propostos

| Serviço | Função | Tecnologias chave | Interage com |
|---|---|---|---|
| Serviço de Perceção | Interface com cliente Minecraft; processa dados brutos | Visão computacional, ONNX | Cliente do Jogo, Modelo do Mundo |
| Modelo do Mundo (V–M–C) | Representação interna e modelo preditivo | PyTorch/TensorFlow, LSTM, VAE, ONNX | Perceção, Controlo Cognitivo |
| Controlo Cognitivo | Ciclo Soar/ACT-R; orquestra decisões | C++/Python, gRPC | Todos os serviços |
| Planeamento HTN | Planeador estratégico | HTN, PDDL | Controlo Cognitivo |
| Planeamento GOAP | Planeador tático | GOAP, A* | Controlo Cognitivo, Modelo do Mundo |
| Memória Episódica | Armazenar experiências | Memory-Augmented Transformer, DB vetorial | Controlo Cognitivo |
| Memória Semântica | Base de conhecimento para RAG | LLM, DB vetorial (Milvus/Qdrant) | Controlo Cognitivo, Planeadores |
| Módulo Criativo | Gera designs (GANs/cGANs) | PyTorch/TensorFlow, ONNX | Planeamento HTN |
| Execução de Ações | Traduz ações para comandos do jogo | APIs do Minecraft, gRPC | Controlo Cognitivo, Cliente do Jogo |

### 6.3 Comunicação — gRPC

Usar gRPC (HTTP/2 + protobuf) para comunicação interna de baixa latência.

### 6.4 Interoperabilidade e otimizações

- Exportar modelos para ONNX para inferência portátil.
- Otimizar LLMs via destilação e quantização.

---

## Seção 7 — Medindo o Imensurável: Avaliação Multicamadas

### 7.1 Métricas quantitativas (o "quê")

Exemplos:

- **Conclusão (C)**: taxa média de sucesso em tasks variadas.
- **Eficiência (E)**: recursos e tempo por tarefa.
- **Equilíbrio (B)**: distribuição do tempo entre categorias de atividade.

### 7.2 Métricas comportamentais qualitativas (o "como")

- Similaridade de distribuição de ações vs jogadores humanos.
- Análise de movimento e percurso (fluidez vs optimalidade).
- "Impressão digital" do estilo de jogo (vetor de características).

### 7.3 Teste de Turing "Overpowered" (o "porquê")

Julgamento por especialistas humanos sobre intencionalidade percebida, adaptabilidade, criatividade e credibilidade dos erros.

### Tabela 4 — Estrutura de métricas

| Camada | Métrica | Descrição | Fonte de dados |
|---|---|---|---|
| Camada 1 | Taxa de conclusão (C) | % de tarefas concluídas no benchmark | Registos do benchmark |
| Camada 1 | Eficiência (E) | Tempo e recursos usados por tarefa | Registos do jogo |
| Camada 1 | Equilíbrio (B) | Distribuição do tempo por atividade | Registos de ações |
| Camada 2 | Similaridade de ações | Distância estatística entre distribuições | Registos de agentes/humanos |
| Camada 2 | Entropia do percurso | Imprevisibilidade do movimento | Dados de posição |
| Camada 3 | Intencionalidade percebida | Classificação por juízes humanos | Observação/inquéritos |

---

## Conclusão

Este manifesto propõe uma arquitetura interdisciplinar para o Projeto Overpowered: uma mente híbrida (Soar + ACT-R) integrada com um modelo do mundo (V–M–C), planeamento hierárquico (HTN + GOAP), motivação intrínseca e princípios antifrágeis, suportada por microsserviços e avaliada por métricas multicamadas. O objetivo não é apenas superar humanos em tarefas, mas criar um agente cuja cognição, criatividade e falhas sejam plausivelmente humanas, servindo como plataforma de investigação para AGI.

## Estado atual / Próximos passos

Aqui está um resumo prático do estado de implementação (baseado em `.kit/development-checklist.md`) e as pendências priorizadas para guiar o trabalho de desenvolvimento:

- Entregues (links úteis):
	- Checklist atual: `.kit/development-checklist.md` (itens marcados e notas sobre o dataset sintético).
	- Worldmodel: `examples/train_worldmodel.py`, `tools/validate_worldmodel.py`, `tools/calibrate_thresholds.py` — trainer, validador e calibrador já presentes.
	- Dados de validação (sintéticos): `data/worldmodel/validation.jsonl` (committed) — usar apenas como smoke test até substituir por dataset representativo.
	- Thresholds calibrados: `services/worldmodel/THRESHOLDS.json` — calibrado a partir do dataset sintético.
	- Métricas de discrepância persistidas: `artifacts/metrics.json` (fluxo de validação/CI produz este artefato).
	- CI: job `validate-and-promote` configurado em `.github/workflows/ci.yml` para rodar trainer + validator e promover checkpoints quando passar.

- Pendências prioritárias (recomendado order):
	1. Substituir `data/worldmodel/validation.jsonl` por um dataset representativo (ex.: conversão de subset MineRL) — RECOMENDADO antes de "large-scale training".
	2. Definir plano de armazenamento e promoção de artefatos (S3 / MLFlow) e adicionar templates de secrets em `.kit/` (necessita decisão humana: provedor/credentials).
	3. Habilitar métricas em staging (ENABLE_METRICS=1) e configurar scrape Prometheus para monitorar discrepância em produção/staging.
	4. Decidir e validar caminho ONNX (export + equivalence tests) — adicionar testes de regressão de inferência.
	5. Documentar runbook de treino e promoção (cotas de GPU, custos, rollback) em `.kit/`.

Pequenas notas:
- Os artefatos binários de treino (checkpoints) não são cometidos no repo; CI re-treina o modelo smoketest quando necessário.
- Mantenha as marcações na checklist (ex.: "synthetic") para deixar claro o status dos artefatos até substituição por dados representativos.

Se quiser, faço commits diretos com links e formatação adicional (tabelas por seção) — diga apenas `sim` para eu proceder.