// Minimal Mineflayer bot that sends simple state to HTTP adapter and applies a no-op action
const mineflayer = require('mineflayer')
const axios = require('axios')

const BOT_HOST = process.env.MC_HOST || 'localhost'
const BOT_PORT = parseInt(process.env.MC_PORT || '25565')
const ADAPTER_URL = process.env.ADAPTER_URL || 'http://localhost:8001/observe'

const bot = mineflayer.createBot({ host: BOT_HOST, port: BOT_PORT, username: 'cleo_bot' })

bot.once('spawn', () => {
  console.log('Bot spawned')
  setInterval(async () => {
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
      console.error('Adapter call failed', e.message)
    }
  }, 2000)
})
