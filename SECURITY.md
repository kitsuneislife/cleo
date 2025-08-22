# Segurança

Siga estas práticas iniciais:

- Testes automático de dependências e atualizações (Dependabot).
- Scanner de vulnerabilidades em CI (ex.: `pip-audit`).
- Não commitar segredos. Use variáveis de ambiente e secret managers.
- Comunicação entre serviços via TLS (mTLS recomendado em produção).

Reportar vulnerabilidades: abra uma issue privada ou use o canal de segurança do projeto.
