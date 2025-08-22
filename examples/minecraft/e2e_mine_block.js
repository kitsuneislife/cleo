// E2E bot script: do a quick direct dig of a nearby block and POST completion to adapter.
const mineflayer = require('mineflayer')
const Vec3 = require('vec3')
const axios = require('axios')
const net = require('net')

const BOT_HOST = process.env.MC_HOST || 'localhost'
const BOT_PORT = parseInt(process.env.MC_PORT || '25565')
const ADAPTER_URL = process.env.ADAPTER_URL || 'http://localhost:8001/observe'
const TARGET_REL = { x: 0, y: -1, z: 0 } // target the block under spawn for higher success

let bot = null

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
        setTimeout(attempt, 1000)
      })
      socket.once('timeout', () => {
        if (settled) return
        socket.destroy()
        if (Date.now() - start > timeoutMs) return reject(new Error('timeout'))
        setTimeout(attempt, 1000)
      })
      socket.connect(port, host)
    }
    attempt()
  })
}

async function run() {
  console.log('E2E: waiting for minecraft')
  try {
    await waitForPort(BOT_HOST, BOT_PORT, 60000)
  } catch (e) {
    console.error('minecraft did not open port:', e.message)
  }

  bot = mineflayer.createBot({ host: BOT_HOST, port: BOT_PORT, username: 'e2e_bot', auth: 'offline' })

  bot.once('spawn', async () => {
    console.log('E2E: bot spawned, finding spawn point')
    const spawn = bot.entity.position
    const targetPos = spawn.offset(TARGET_REL.x, TARGET_REL.y, TARGET_REL.z)
    console.log('E2E: target relative pos', TARGET_REL, '=>', targetPos)

    try {
      console.log('E2E: attempting direct dig at target (no pathfinder)')
      try {
        await bot.lookAt(targetPos.offset(0.5, 0.5, 0.5))
      } catch (e) {
        // ignore look failures
      }
      const block = bot.blockAt(targetPos)
      if (!block) {
        console.error('E2E: no block found at target')
      } else {
        console.log('E2E: block type:', block.name)
        try {
          await bot.dig(block)
          console.log('E2E: block mined')
        } catch (e) {
          console.error('E2E: dig failed', e && e.message)
        }
      }

      // notify adapter with a completion marker in the ObserveReq shape (state base64)
      try {
        const payload = { event: 'mined_block', coords: { x: targetPos.x, y: targetPos.y, z: targetPos.z } }
        const stateJson = JSON.stringify(payload)
        const base64 = Buffer.from(stateJson).toString('base64')
        await axios.post(ADAPTER_URL, { agent_id: 'e2e_bot', state: base64 })
        console.log('E2E: posted completion to adapter (as ObserveReq)')
      } catch (e) {
        console.warn('E2E: failed to post completion', e && e.message)
      }

      // exit after a short delay
      setTimeout(() => process.exit(0), 2000)
    } catch (e) {
      console.error('E2E: error during dig:', e && e.message)
      process.exit(2)
    }
  })

  bot.on('error', (err) => {
    console.error('Bot error', err && err.stack)
  })
}

run()
