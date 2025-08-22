# Template de Secrets — Cleo

Este arquivo serve como modelo para configuração de secrets necessários para storage/promoção de artefatos (S3, MLFlow, etc) e integração segura no CI/CD.

Preencha os campos conforme o provedor escolhido e armazene as credenciais em local seguro (ex.: GitHub Secrets, Vault, AWS Secrets Manager).

---

## S3 (AWS)
```
S3_BUCKET=cleo-artifacts
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
AWS_REGION=us-east-1
```

## MLFlow
```
MLFLOW_TRACKING_URI=https://mlflow.example.com
MLFLOW_TRACKING_TOKEN=xxxx
```

## GitHub Actions (CI)
```
GH_TOKEN=xxxx
```

## Observações
- Nunca comite este arquivo preenchido com valores reais.
- Adapte os campos conforme o provedor/infraestrutura utilizada.
- Documente no README e na checklist quando adicionar novos secrets.
