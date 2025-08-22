# Benchmarks and metrics — guide

- Define tasks (e.g., minerar bloco, coletar recurso, navegar 10m) and datasets.
- Measure latency, plan length, success rate, resource usage.
- Store benchmark results as JSONL under `artifacts/benchmarks/` with versioned metadata.

Try it
- use `services/htn/tests/test_benchmark.py` as a starting point for latency microbenchmarks.
