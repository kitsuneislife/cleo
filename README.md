# Projeto Cleo — Estrutura inicial

Este repositório contém o esqueleto para o Projeto Overpowered (Cleo). Os documentos de projeto e protocolo estão em `.kit/`.

Objetivo deste scaffold
- Fornecer uma estrutura modular de microsserviços.
- Padrões para segurança, CI e integração por gRPC + protobuf.
- Exemplos e scripts para desenvolvimento local.

Layout principal
- `services/` — cada microsserviço (perception, worldmodel, control, etc.) tem seu próprio diretório e README.
- `proto/` — arquivos `.proto` e gerados.
- `infra/` — compose, k8s e infra de orquestração.
- `examples/` — pequenos scripts de demonstração.
- `.github/workflows/` — CI (lint/test/build).
- `.kit/` — documentação de alto nível (manifesto, protocolo).

Próximo passo: veja `infra/docker-compose.yml` para executar uma instância local simulada e `scripts/setup_dev.ps1` para preparar ambiente.
