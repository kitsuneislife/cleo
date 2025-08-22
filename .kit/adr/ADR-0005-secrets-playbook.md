# ADR 0005 — Provisionamento seguro de segredos e padrão CI para artefatos

Status: Proposed

Context
- O projeto precisa de um padrão seguro e auditável para armazenar e fornecer credenciais (S3, MLflow, Vault, cloud secrets) para CI/CD e serviços em produção.
- Requisitos: least-privilege, rotação, audit trail, integração com CI sem long-lived secrets em repositório.

Decision
- Adotar um padrão híbrido:
  - Para infra pública/cloud: usar o provider nativo de secrets (AWS Secrets Manager / GCP Secret Manager / Azure Key Vault) com políticas IAM limitadas.
  - Para equipes que preferem centralização: usar HashiCorp Vault (se disponível) com auth por OIDC/Kubernetes.
  - CI (GitHub Actions): preferir OIDC provider para trocas temporárias de credenciais; quando não possível, usar secrets do GitHub com escopo mínimo e rotação obrigatória.

Consequences
- Integração OIDC evita armazenar chaves permanentes no CI e reduz risco de leaks.
- Exige configuração de roles/policies e documentação de onboarding para devs e CI.

Playbook (alto nível)
1. Decidir provedor primário (AWS/GCP/Azure) ou Vault.
2. Criar política de roles least-privilege para CI e service-accounts:
   - Role para upload S3 (put/get em prefix `cleo-artifacts/*`).
   - Role para escrita/leitura de artefacts no MLflow (se self-hosted) com token de curto prazo.
3. Provisionar secret engine (Secrets Manager / Vault) e criar entrys:
   - `artifacts/s3/bucket` (nome do bucket)
   - `artifacts/s3/role` (ARN/role to assume)
   - `mlflow/tracking_uri`
   - `mlflow/api_token` (rotacionável)
4. Configurar CI para usar OIDC (GitHub Actions) e mapear roles apropriadas.
5. Testar job CI em ambiente de staging com logs limitados (não imprimir secrets).
6. Documentar processo de rotação e revogação no playbook local.

Security controls
- Enforce KMS encryption for stored secrets.
- Audit logs enabled (CloudTrail / Vault audit device).
- Require MFA for manual secret accesses.
- Limit access via IP or VPC when possible.

Implementation notes
- Prefer short-lived credentials for MLflow and S3 via STS assume-role.
- For local dev, use Vault dev token or `aws-vault` patterns; never commit creds.
- Add a test job `ci/test-artifact-upload` that runs against a staging bucket.

Files and references
- Playbook operacional: `.kit/playbooks/provision_secrets_playbook.md`
- Templates de secrets: `.kit/secrets-template.md`
- CI example: `.github/workflows/ci_upload_artifacts.yml`
