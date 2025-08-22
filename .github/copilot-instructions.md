## Copilot instructions for the Cleo repo

This file gives concise, actionable guidance to an AI coding agent to be productive in this repository. It focuses on the repo-specific architecture, developer workflows, conventions, and concrete examples you can follow.

1) Big-picture architecture (what to read first)
- Top-level: `README.md` (repo layout) and `.kit/` for project protocol/decisions.
- Services: microservices live under `services/` (e.g. `control`, `worldmodel`, `perception`, `htn`, `goap`, `memory`, `execution`, `integration`). Each service has a `README.md` — read these for service-specific contracts and quickstarts.
- Dataflow: `control` calls `worldmodel` (gRPC) to get predictions/simulations; adapters in `services/integration` bridge external systems (e.g., Mineflayer bot) to `control` via HTTP/gRPC. `proto/` contains protobuf contracts and generated stubs used across services.

2) Key developer workflows (commands to run)
- Setup Python venv and install dev deps (from repo root):
  - PowerShell: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
- Run unit tests for a service (example worldmodel):
  - `pytest services/worldmodel/tests/test_dreams.py -q`
- Train the toy worldmodel (local smoke trainer):
  - ` .\.venv\Scripts\python.exe examples\train_worldmodel.py --batch_size 8 --epochs 1`
- Calibrate thresholds and validate a checkpoint (worldmodel CI flow):
  - ` .\.venv\Scripts\python.exe -m tools.calibrate_thresholds --data data/worldmodel/validation.jsonl --percentile 95 --checkpoint artifacts/wm_checkpoint.npz`
  - ` .\.venv\Scripts\python.exe -m tools.validate_worldmodel --checkpoint artifacts/wm_checkpoint.npz --data data/worldmodel/validation.jsonl --thresholds services/worldmodel/THRESHOLDS.json`
- CI: see `.github/workflows/ci.yml` — CI runs proto generation, ruff, pytest, a smoke trainer, and a `validate-and-promote` job that creates a GitHub Release when validation passes.

3) Project-specific conventions & patterns
- Services are lightweight Python packages; prefer small, explicit CLIs under `examples/` and `tools/` for experiments and validation.
- Opt-in metrics are guarded by an `ENABLE_METRICS` env var and expose Prometheus metrics (see `services/worldmodel/metrics.py`). Don't assume metrics are always on.
- Non-binary artifacts (datasets, thresholds JSON) are tracked in the repo when small and reviewable (see `data/worldmodel/validation.jsonl` on branch `ci/smoke-valid`), but large binary checkpoints are intentionally excluded — CI re-trains smoke models instead.
- Protobuf-first contracts: update `.proto` in `proto/`, then run the repo's protogen flow (CI uses `scripts/gen_protos.sh`). Tests and services import generated stubs under `proto/`.

4) Integration points and external dependencies
- gRPC services: `worldmodel` and `control` expect proto-based RPCs. See `proto/worldmodel.proto` and generated stubs under `proto/` for method names and message shapes.
- External systems: the `examples/minecraft` adapter uses a Node.js mineflayer bot that talks to `services/integration/adapter.py` via HTTP; adapters translate external events into `control` RPCs.
- Artifact promotion: CI uses a `validate-and-promote` job that will create a GitHub Release for a validated checkpoint. The repo leaves S3/MLFlow decision for humans and stores small artifacts (thresholds, JSONL) in-tree for reproducibility.

5) Where to look for concrete examples
- Worldmodel: `examples/train_worldmodel.py`, `tools/validate_worldmodel.py`, `tools/calibrate_thresholds.py`, `services/worldmodel/dreams.py` demonstrate the full local train → calibrate → validate flow used in CI.
- E2E / adapter: `examples/minecraft/` contains the Mineflayer harness and shows how the adapter translates game events into control actions and health/readiness endpoints.
- CI pipeline: `.github/workflows/ci.yml` demonstrates gating (validate-and-promote), proto generation, and test steps.

6) Typical edits an AI may be asked to do (and where)
- Add a new RPC or message: edit `proto/*.proto`, update any README examples, and adjust service server/client code under `services/*/` and add/update tests in `services/*/tests/`.
- Add a small tooling script: place under `tools/` or `scripts/`, include a short CLI with argparse, and add a unit test under `tools/tests/` or `services/<svc>/tests/`.
- Update CI to store artifacts externally: modify `.github/workflows/ci.yml` and add templated secret names in `.kit/` docs; do not commit secrets.

7) Code patterns to follow when editing
- Keep changes minimal and localized: prefer adding small utility functions or scripts rather than large refactors in a single PR.
- When introducing runtime flags, follow the `ENABLE_METRICS` pattern (env var guarded) and document in the service README.
- When editing `.kit/` docs or the checklist, preserve the checklist formatting and add concise notes when marking tasks done (see existing entries for example phrasing).

8) Quick sanity checks before committing
- Run unit tests for touched services: `pytest services/<svc>/tests -q`.
- Run `python -m tools.check_protos_import` to ensure generated protobuf imports are valid.
- Lint with `ruff` (CI runs linting): `ruff services/ tests/`.

9) When you need to ask the human
- Only ask for human input when it involves secrets, budget/infra decisions (S3 vs MLFlow), or selecting representative datasets. For implementation choices, prefer the small, safe default used in the repo (synthetic dataset, smoke trainer, percentiles for thresholds) and document the choice in `.kit/` or the README.

If anything in this file is unclear or missing examples you need, tell me which section to expand and I'll update the file.

Tone and address
- The repo owner prefers to be addressed in Portuguese with a sweet and gentle tone: use short, kind sentences, avoid blunt or bureaucratic phrasing, and prefer empathetic language when asking for confirmations or giving instructions. Keep messages concise and practical while remaining polite.


## Agent interaction model (repo owner's preference)

The repository owner prefers minimal interruptions: AI agents should decide the next concrete step autonomously and present it at the end of each message as a single-line proposal. The agent must then pause and wait for the human to reply with the single word `sim` (Portuguese for "yes") before executing the proposed step.

Rules for the agent:
- At the end of each reply include exactly one proposed next step (short, actionable, 1 line). Example: `Proposed next step: run worldmodel calibrator and commit updated thresholds`.
- Do not execute the proposed step until the user replies with `sim` or `Continue` alone on a line.
- If the user replies with any other content, treat it as new instructions and respond accordingly.
- Only ask the human for help when absolutely necessary (secrets, permissions, or choices that cannot be inferred from `.kit/`).

Follow this interaction model strictly when operating in this repository unless explicitly instructed otherwise by the repo owner.
