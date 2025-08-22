// Minimal Mineflayer bot that sends simple state to HTTP adapter and applies a no-op action
// Minimal Mineflayer bot that sends simple state to HTTP adapter and applies a no-op action
const mineflayer = require('mineflayer')
const axios = require('axios')
const net = require('net')

const BOT_HOST = process.env.MC_HOST || 'localhost'
const BOT_PORT = parseInt(process.env.MC_PORT || '25565')
const ADAPTER_URL = process.env.ADAPTER_URL || 'http://localhost:8001/observe'

let bot = null
function startBot() {
  (async () => {
    console.log('Attempting to start Mineflayer bot', BOT_HOST, BOT_PORT)
    try {
      await waitForPort(BOT_HOST, BOT_PORT, 60000)
      console.log('Port is open, creating bot')
    } catch (e) {
      console.warn('Port did not open within timeout, will still attempt to create bot:', e.message)
    }

    try {
      // use offline auth to avoid Mojang login issues in local environments
      bot = mineflayer.createBot({ host: BOT_HOST, port: BOT_PORT, username: 'cleo_bot', auth: 'offline' })

      // defensive check: some environments may return null/undefined instead of throwing
      if (!bot) {
        console.error('createBot returned null/undefined, retrying in 5s')
        setTimeout(startBot, 5000)
        return
      }

      console.log('createBot returned, bot type:', typeof bot)

      // attach listeners only after bot is created
      bot.once('spawn', () => {
        console.log('Bot spawned')
        setInterval(async () => {
          if (!bot || !bot.entity) return
          try {
            const state = Buffer.from(JSON.stringify({ x: bot.entity.position.x, y: bot.entity.position.y }))
            const base64 = state.toString('base64')
            const resp = await axios.post(ADAPTER_URL, { agent_id: 'bot1', state: base64 })
            console.log('Decision:', resp.data)
            // apply a trivial action (look around) as a placeholder
            if (resp.data && resp.data.operator_id) {
              bot.look(bot.entity.yaw + 0.1, bot.entity.pitch, true)
            }
          } catch (e) {
            console.error('Adapter call failed', e && e.message)
          }
        }, 2000)
      })

      // extra diagnostics
      bot.on('connect', () => console.log('Bot: socket connected'))
      bot.on('login', () => console.log('Bot: logged in'))
      bot.on('error', (err) => {
        console.error('Bot error', err && err.message)
      })
      bot.on('end', () => {
        console.warn('Bot connection ended, retrying in 5s')
        setTimeout(startBot, 5000)
      })
      bot.on('kicked', (reason) => {
        console.warn('Bot kicked:', reason)
      })

    } catch (e) {
      console.error('createBot threw:', e && e.message)
      setTimeout(startBot, 5000)
      return
    }
  })()

  
}

function waitForPort(host, port, timeoutMs = 30000) {
  return new Promise((resolve, reject) => {
    const start = Date.now()
    function attempt() {
      const socket = new net.Socket()
      let settled = false
      socket.setTimeout(2000)
      socket.once('connect', () => {
        settled = true
        socket.destroy()
        resolve()
      })
      socket.once('error', () => {
        if (settled) return
        socket.destroy()
        if (Date.now() - start > timeoutMs) return reject(new Error('timeout'))
        setTimeout(attempt, 2000)
      })
      socket.once('timeout', () => {
        if (settled) return
        socket.destroy()
        if (Date.now() - start > timeoutMs) return reject(new Error('timeout'))
        setTimeout(attempt, 2000)
      })
      socket.connect(port, host)
    }
    attempt()
  })
}
startBot()
