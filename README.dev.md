# Desenvolvimento local — Guia rápido

1. Criar e ativar um virtualenv:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Instalar dependências

```powershell
pip install -r requirements.txt
```

3. Gerar stubs gRPC

```powershell
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/service.proto
```

4. Rodar o servidor de percepção (exemplo):

```powershell
python services\perception\server.py
```

5. Em outro terminal, rodar o cliente de exemplo:

```powershell
python services\perception\client.py
```

Notas
- Em produção, configure TLS e autenticação para gRPC.
- Use `docker-compose` em `infra/` para orquestrar múltiplos serviços locais.
