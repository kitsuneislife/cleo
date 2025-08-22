# ADR 0003 — Logging format and backup policy

Decision
- Logs: structured JSON with fields: timestamp, service, level, msg, ctx (dict), trace_id, span_id.
- Backups: vector DB and model artifacts: daily snapshot to object storage; retention 30 days hot + 1 year cold.

Rationale
- Structured logs simplify alerts and parsing; trace fields enable distributed tracing correlation.
- Regular backups mitigate model/DB corruption.

Implementation notes
- Add structured logging helper in `services/common/logging.py`.
- Backup job: daily job that snapshots vectors and uploads to S3.
