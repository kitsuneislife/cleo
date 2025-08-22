# AIID — Incident storage and schema

Purpose: registrar incidentes e eventos de replan/falha com contexto mínimo para auditoria e debugging.

Schema (JSON)
- id: uuid
- timestamp: iso8601
- service: string
- level: ERROR|WARN|INFO
- context: dict (state snapshot minimal)
- plan_id: optional string
- actions_taken: list
- root_cause: optional string

Storage
- Store in append-only JSONL in object storage for long-term; short-term push to vector DB for search.
- Retention: 90 days hot, archive to cold storage.
