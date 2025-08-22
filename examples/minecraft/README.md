# Example Mineflayer bot

Quickstart:

1. Start the full dev stack (recommended) using Docker Compose. This will start the Minecraft server, Python services and the example bot.

```powershell
cd ..\..  # repo root
docker compose up --build
```

If you prefer to run services locally, ensure `worldmodel`, `control`, `execution` and the `adapter` are running and healthy. The adapter exposes a `/health` endpoint on port 8001 that can be used by orchestrators and to verify readiness.

Install and run the bot locally (requires Node.js) if you want to iterate on the bot script:

```powershell
cd examples\minecraft
npm install
set ADAPTER_URL=http://localhost:8001/observe; node bot.js
```

The bot periodically sends a small state payload to the adapter and logs the decision. When using Docker Compose the example bot is started automatically.