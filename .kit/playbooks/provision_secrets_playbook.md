# Playbook: Provisionamento de segredos e integração CI (S3 + MLflow)

Objetivo: passos práticos para infra/ops provisionarem secrets e configurar CI seguro.

Pré-requisitos
- Conta cloud com permissão de admin para criar roles/policies (ou Vault admin).
- Bucket S3 para `cleo-artifacts` ou endpoint S3-compatível.
- MLflow server (opcional) com endpoint e token de API.

Passos rápidos
1. Criar bucket S3 (ex.: `cleo-artifacts`) e aplicar política:
   - Prefixo permitido: `cleo-artifacts/{service}/{version}/*`
   - Bloquear acesso público
2. Criar role `cleo-ci-artifacts-uploader` com permissão STS assume-role que permite `s3:PutObject`, `s3:GetObject` apenas no prefixo acima.
3. Registrar a role no Secret Manager ou Vault como `artifacts/s3/role`.
4. Se usar MLflow self-hosted:
   - Criar token de API com escopo mínimo e armazenar em `mlflow/api_token`.
   - Registrar `mlflow/tracking_uri` no secret store.
5. Configurar OIDC no GitHub repo/org e mapear para a role criada (ex.: trust policy AWS).
6. Atualizar CI workflow (ex.: `ci_upload_artifacts.yml`) para assumir role via OIDC e executar upload.
7. Testar: executar job em branch `staging` que rode upload de artefato de teste e valide retorno.
8. Rotação: agendar rotação de MLflow token e revalidar CI jobs.

Checklist de segurança
- [ ] KMS habilitado para bucket
- [ ] Audit logs ativados
- [ ] Roles com menor privilégio possíveis
- [ ] Rotação mensal para tokens long-lived

Dicas para dev local
- Use `aws-vault` ou `direnv` para gerenciar credenciais locais.
- Para Vault, use `vault login -method=oidc` e `vault read secret/artifacts/s3/role`.
