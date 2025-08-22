# ADR 0001 — Artifact storage and promotion

Status: Proposed

Context
- We need a repeatable, low-cost, and secure way to store model artifacts (checkpoints, ONNX, thresholds) and a promotion process for validated artifacts.

Decision
- Recommend primary storage in S3-compatible object storage (AWS S3 or S3-compatible bucket) for binary artifacts, plus MLflow (or equivalent) to track runs/metadata.
- Promotion workflow: validated artifact -> store in S3 under `s3://cleo-artifacts/{service}/{version}`; write metadata to MLflow run (artifact URI, thresholds, validation metrics). Create GitHub Release with small artifacts and thresholds JSON when promoting to release.

Consequences
- Easy large-file storage, lifecycle policies and cross-region replication available via S3.
- Metadata + lineage in MLflow helps reproducibility and search.
- Requires secrets (access keys) and IAM policies; use secrets manager (Vault) to provision CI/CD access.

Alternatives considered
- Only MLflow artifact store (works for small/medium artifacts but less flexible for large checkpoints). Rejected as primary.
- External artifact registries (S3 + Artifactory) — more infra and cost.

Implementation notes
- CI: add steps to upload artifacts to S3 and log run in MLflow; add `ARTIFACTS_S3_BUCKET` and `MLFLOW_TRACKING_URI` as secrets.
- Templates: `.kit/secrets-template.md` updated with `ARTIFACTS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `MLFLOW_TRACKING_URI`, `MLFLOW_API_TOKEN`.
