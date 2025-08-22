# ADR 0002 — Infra target for Cleo (dev vs prod)

Status: Proposed

Decision
- Dev: `docker-compose` for local development and quick E2E smoke tests.
- Prod: Kubernetes (k8s) with Helm charts for deploy, autoscaling and observability.

Rationale
- `docker-compose` reduces onboarding friction for devs and CI smoke tests.
- k8s required for production features: scaling, resource limits, network policies and observability.

Consequences
- Need Helm chart skeleton and CI steps to build/push images and run canary deployments.
- Define resource requests/limits and add readiness/liveness checks per service.

Next steps
- Create `charts/` skeleton and a policy doc for image build/promotion.
