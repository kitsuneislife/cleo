# Security policies (summary)

Decisions recommended
- Enforce mTLS between services in production.
- Use a secrets manager (HashiCorp Vault or cloud-native secrets) to store credentials.
- RBAC: least-privilege for service accounts and CI tokens.

Notes
- CI should use short-lived credentials; rotate keys monthly.
- Document required roles and policies for each cloud provider used.
