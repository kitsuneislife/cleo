# Critérios de Qualidade do Modelo — Worldmodel

Este documento descreve métricas objetivas e procedimentos mínimos para avaliar a
qualidade do `worldmodel`. O objetivo é ter critérios reproduzíveis para aceitar
checkpoints e decidir se um modelo pode ser promovido para produção ou usado pelo
`control`.

1) Métricas numéricas primárias
--------------------------------
- MSE (Mean Squared Error)
  - O que: erro quadrático médio entre features previstas e reais em horizon t+1 (ou t+H).
  - Como medir: por frame e por episódio; reportar média e desvio.
  - Aceitação (exemplo MVP): MSE_h1 < 0.05 sobre validação (normalizado)

- NLL / Log-likelihood (se modelo probabilístico)
  - O que: verossimilhança média das observações segundo a distribuição predita.
  - Como medir: negativa média da log-probabilidade por sample; útil para modelos VAE/flow.

2) Fidelidade de simulação (trajectória)
----------------------------------------
- Rollout error (episódio)
  - O que: executar o modelo em modo auto-regressivo por H passos e comparar a série com a realidade.
  - Métricas: RMSE por horizon, DTW (Dynamic Time Warping) para medir desvio temporal/estrutural.
  - Aceitação (exemplo MVP): RMSE_h10 < 0.2; DTW relativo < 1.2

- Eventos e propriedades (qualitativas mensuráveis)
  - O que: avaliar se eventos críticos (ex.: colisão, mudança de estado) são preservados.
  - Como medir: precisão/recall para detecção de eventos em rollouts.

3) Robustez e calibração
-------------------------
- Calibration / Sharpness
  - O que: avaliar se as incertezas preditas refletem o erro observado (reliability diagrams).

- Sensibilidade a inputs ruidosos
  - O que: adicionar ruído gaussian e medir degradação de MSE; modelo robusto não deve degradar abruptamente.

4) Métricas operacionais
------------------------
- Latência de inferência (P50/P90)
  - Onde medir: serviço `worldmodel` em modo servidor.
  - SLA exemplo: P90 < 50ms para chamadas single-shot (CPU em dev).

- Throughput (inferences/s) e uso de memória

5) Procedimento de validação e aceitação (MVP)
---------------------------------------------
1. Gerar dataset de validação separado (offline + sonhos), fixar seed.
2. Rodar validação: calcular MSE_h1/h10, NLL (se aplicável), rollout RMSE e DTW.
3. Executar 10 rollouts em episódios reais e medir eventos críticos (precision/recall).
4. Se todas as métricas passam thresholds definidos, promover checkpoint e exportar ONNX.

6) Artefatos e relatórios
-------------------------
- Salvar um `report.json` com métricas, seed, commit-id, dataset hash e tempo de execução.
- Salvar `artifacts/<run-id>/metrics.json` e `artifacts/<run-id>/onnx-check.npz` contendo validação de inferência (entrada/saída comparadas).

7) Ferramentas e comandos úteis
-------------------------------
- Script de validação (exemplo): `python tools/validate_worldmodel.py --checkpoint <file> --data data/val.jsonl`
- Para rollouts: reusar `examples/train_worldmodel.py` ou criar `examples/rollout_validate.py` que carrega checkpoint e compara trajectories.

Notas finais
------------
- Os thresholds acima são sugestões iniciais; ajuste com base na distribuição dos dados e nas necessidades do `control`.
- Sempre registrar resultados (report.json) e anexar aos PRs de modelos.
