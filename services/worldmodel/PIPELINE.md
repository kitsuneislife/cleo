# Planejamento do pipeline de treino — Worldmodel

Objetivo
-------
Descrever um pipeline de treino reprodutível para o serviço `worldmodel` que combine dados offline observados (logs/trajectórias reais) com dados sintéticos gerados pelos "sonhos" (trajectórias simuladas). O plano foca em entregáveis mínimos (MVP), métricas de validação, formatos de dados e etapas de CI/QA.

Visão geral do pipeline
-----------------------
- Fontes de dados:
  - Offline: logs de episódios coletados pelo sistema de execução (ex.: sequências de states/actions/timestamps).
  - Sonhos: datasets sintéticos gerados por `services.worldmodel.dreams.generate_dreams`.
- Objetivo do modelo: mapear InputState -> latent z (compact) e/ou previsões futuras (trajectórias) para uso pelo `control`.
- Entregáveis MVP:
  1. Data schema e gerador de dataset (JSONL) que mistura offline+sonhos.
  2. Script de treino mínimo (`examples/train_worldmodel.py` já criado) ampliado para treinar por n steps em CPU/GPU.
  3. Testes unitários + CI smoke run (treino por poucas iterações).
  4. Export ONNX e validação de inferência equivalência (smoke).

Formato de dados (canonical)
----------------------------
- Arquivo: JSONL (uma linha = um frame ou um episódio, conforme necessário)
- Exemplo (frame-level):

  {
    "agent_id": "agent-23",
    "timestamp": 1690000000,
    "features": [0.1, 0.2, ...],
    "action": 3,                # opcional, inteiro ou vetor one-hot
    "reward": 0.0,              # opcional
    "meta": {"env": "test"}
  }

- Exemplo (episode-level):

  {
    "agent_id": "agent-23",
    "episode": [ {frame}, {frame}, ... ]
  }

Notas:
- Para transporte compacto entre serviços, use `z` empacotado em bytes (proto `LatentZ.z`) ou base64 em JSON.
- O campo `features` deve ser um vetor float32; prefira normalização/min-max no preprocess.

Preprocessamento
-----------------
- Converter JSONL → TFRecords/NPZ/LMDB conforme volume (MVP: NPZ por episódio).
- Normalização: calcular média/desvio no conjunto de treino (salvar estatísticas).
- Opcional: extrair janelas (sliding windows) para modelos seq2seq.

Treino (MVP)
------------
- Modelo: encoder simples (MLP para features estáticas, RNN/Transformer leve para sequências) que produz `z` (dim z configurável, ex.: 32–128).
- Loss: MSE entre previsão e realidade para predição de features; KL/contrastive se for VAE.
- Hiperparâmetros iniciais:
  - batch_size: 64
  - lr: 1e-3 (Adam)
  - epochs/steps: configurável; CI smoke: 10 steps
  - dim(z): 64
- Checkpoints: salvar pesos e um manifesto (yaml/json) com argumentos e seed.

Mix: Offline + Sonhos
---------------------
- Estratégia MVP: amostragem mista por batch com `rho` = proporção de sonhos.
  - Exemplo inicial: rho = 0.5 (metade batches reais, metade sonhos).
  - Cronograma de curriculum: aumentar rho de sonhos com o tempo para explorar variantes.
- Alternativa: oversample rare events dos logs usando sonhos dirigidos.

Validação e métricas
--------------------
- Métricas primárias:
  - MSE de features futuras (horizon t+1,..,t+H)
  - Log-likelihood (se modelo probabilístico)
  - Discrepância previsão vs realidade (episódio) — agregada por agente
- Métricas operacionais:
  - Tempo por batch, throughput (samples/s)
  - Latência de inferência (P50/P90)

Testes e CI
-----------
- Unit tests:
  - shape/roundtrip tests (já criados para schema e dreams)
  - smoke train: executar `examples/train_worldmodel.py` por N small steps e checar saída
- CI job:
  - gerar protos (se necessário), rodar testes unitários e smoke train (CPU-only)

Export e inferência
-------------------
- Exportar modelo para ONNX em uma etapa final de pipeline e validar inferência equivalência com um conjunto de entradas de validação.
- Salvar artefatos (checkpoints, onnx, normalizers) em `artifacts/worldmodel/<run-id>/`.

Reprodutibilidade
-----------------
- Fixar seeds (numpy, random, torch) e salvar manifest.
- Registrar ambiente (`pip freeze` ou `requirements.txt`), e preferir `requirements-dev.txt` para dev deps.

Infra e armazenamento
----------------------
- Pequeno volume: armazenar datasets em `data/worldmodel/` (JSONL/NPZ). Para produção usar S3/MinIO.
- Logs e metadados: usar `runs/` com `run-id` e metadata JSON.

Cronograma e entregáveis mínimos (MVP)
-----------------------------------
1. Documento de pipeline (este arquivo) — hoje
2. Script de preprocess + converter dreams → dataset (1–2 dias)
3. Treino MVP script com checkpoint e smoke test (2–3 dias)
4. CI smoke training step e testes unitários (1 dia)
5. ONNX export + validação (1 dia)

Riscos e mitigação
------------------
- Risco: sonhos pouco realistas — mitigar usando curriculum e pesos adaptativos.
- Risco: custo compute — mitigar com smoke tests em CI e treino real em instância dedicada/spot.

Próximos passos (concretos)
--------------------------
1. Implementar `scripts/prepare_worldmodel_dataset.py` que mistura offline+dreams e gera NPZ/JSONL.
2. Ampliar `examples/train_worldmodel.py` para suportar argumentos CLI (batch_size, epochs, rho).
3. Adicionar CI smoke job que executa o train por 10–50 steps.
4. Documentar formato de artefatos e adicionar Makefile targets: `make data`, `make train`, `make export`.
