# Artifact decision summary

Chosen pattern: S3 for binaries + MLflow for run metadata.

Why
- S3 scales for large files; MLflow adds experiment tracking.

How to use
- CI: upload artifacts to S3 and add MLflow run with `artifact_uri`.
- Use `.kit/secrets-template.md` for required secrets.
