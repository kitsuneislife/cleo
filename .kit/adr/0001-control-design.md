# ADR 0001 — Control service: persistence, metrics and contracts

Status: Accepted

Context
-------
For Phase 1 we needed a minimal, testable control loop (Núcleo Cognitivo) that:

- Uses gRPC contracts in `proto/` to interoperate with `worldmodel` and `execution`.
- Persists recent decisions to allow deterministic ranking with light historical bias.
- Exposes optional operational metrics without making the dependency mandatory for tests.

Decision
--------

1. Use gRPC (.proto) as primary contract mechanism for inter-service APIs.
2. Use a simple SQLite-backed `DecisionStore` for Phase 1 persistence. This is file-based and easy to reason about in local dev and tests.
3. Make Prometheus metrics opt-in via environment variable `ENABLE_METRICS=1` and `CONTROL_METRICS_PORT`. If the `prometheus_client` package is unavailable the server continues without metrics.

Consequences
------------

- SQLite provides low-friction persistence but is not appropriate for heavy write loads or distributed multi-node deployments. Plan to replace/augment with an async writer and a durable store (e.g., PostgreSQL or vector DB) in Phase 2/3.
- Making metrics optional prevents test flakiness and avoids binding extra ports in CI unless explicitly requested.
- gRPC contracts must be versioned; enforce automatic stub generation in CI as next step.
