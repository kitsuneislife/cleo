# Segurança e hardening (pontos de atenção)

- Comunicação: exigir TLS; usar autenticação mútua (mTLS) entre microsserviços.
- Secrets: não guardar segredos no repositório; usar secret manager.
- Dependências: auditar e pinnear versões críticas.
- Isolamento: rodar serviços com usuários não privilegiados e quotas de recursos.
- Contenção: usar timeouts e circuit-breakers para chamadas externas.
- Logs: evitar informação sensível em logs.
