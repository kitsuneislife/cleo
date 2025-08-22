# Phase 2 — Modelo do Mundo (Definition of Ready)

This Definition of Ready lists acceptance criteria and required artifacts before implementing the `worldmodel` service.

Acceptance criteria
- Proto contract for worldmodel (`proto/worldmodel.proto`) exists and defines Predict and Simulate RPCs.
- Synthetic dataset or generator for basic trajectories (toy data) is available under `examples/`.
- Inference API surface documented in `services/worldmodel/README.md` with quickstart for running locally.
- Lightweight integration test that verifies `control` can call `worldmodel` and receive a prediction.

Non-functional criteria
- Initial performance target: prediction latency < 50ms for trivial models in dev environment.
- Provide a plan for model persistence and versioning (ONNX export target).

DoR tasks
- Add `services/worldmodel/README.md` (quickstart + contract usage)
- Add a small synthetic data generator `examples/generate_trajectories.py` (optional first cut)
- Add integration test scaffold `services/worldmodel/tests/test_inference.py`
