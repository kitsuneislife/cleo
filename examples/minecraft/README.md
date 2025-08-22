# Example Mineflayer bot

Quickstart:

1. Start Python services (worldmodel, control, execution) and the HTTP adapter:

```powershell
.\.venv\Scripts\Activate.ps1
# start worldmodel, control, execution, adapter in separate terminals
```

2. Install and run the bot (requires Node.js):

```powershell
cd examples\minecraft
npm install
set ADAPTER_URL=http://localhost:8001/observe; node bot.js
```

The bot periodically sends a small state payload to the adapter and logs the decision.