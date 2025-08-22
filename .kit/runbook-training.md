# Runbook de Treinamento — Cleo

Este documento serve como guia prático para executar, monitorar e avaliar o treinamento do modelo do mundo.

## Infraestrutura
- Compute: GPU mínima recomendada (ex.: NVIDIA T4 ou superior)
- Quotas: 24h por experimento, 16GB RAM, 100GB storage
- Custos: estimar por hora conforme provedor (AWS, GCP, local)
- Acesso: credenciais via `.kit/secrets-template.md`

## Passos para Treinamento
1. Preparar dataset representativo em `data/worldmodel/validation.jsonl`
2. Rodar o trainer:
   ```
   python examples/train_worldmodel.py --batch_size 32 --epochs 10 --checkpoint artifacts/wm_checkpoint.npz
   ```
3. Calibrar thresholds:
   ```
   python -m tools.calibrate_thresholds --data data/worldmodel/validation.jsonl --percentile 95 --checkpoint artifacts/wm_checkpoint.npz
   ```
4. Validar modelo:
   ```
   python -m tools.validate_worldmodel --checkpoint artifacts/wm_checkpoint.npz --data data/worldmodel/validation.jsonl --thresholds services/worldmodel/THRESHOLDS.json
   ```
5. Exportar para ONNX (opcional):
   ```
   python examples/train_worldmodel.py --export_onnx artifacts/wm_checkpoint.onnx
   ```
6. Validar equivalência ONNX:
   ```
   python tools/tests/test_onnx_equivalence.py --checkpoint artifacts/wm_checkpoint.npz --onnx artifacts/wm_checkpoint.onnx
   ```

## Interpretação dos Artefatos
- `artifacts/metrics.json`: métricas de validação (MSE, RMSE, DTW)
- `services/worldmodel/THRESHOLDS.json`: thresholds calibrados
- `artifacts/wm_checkpoint.npz`: checkpoint do modelo
- `artifacts/wm_checkpoint.onnx`: exportação ONNX

## Critérios de promoção
- Métricas abaixo dos thresholds
- Equivalência ONNX validada
- Checklist de segurança e observabilidade revisada

## Rollback
- Restaurar checkpoint anterior
- Reverter thresholds
- Documentar no README e checklist

---
Adapte quotas e custos conforme o ambiente. Atualize este runbook sempre que o pipeline evoluir.
