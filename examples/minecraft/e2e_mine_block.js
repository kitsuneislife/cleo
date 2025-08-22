// E2E bot script: navigate to a target block near spawn and mine it, then POST a completion marker to the adapter.
const mineflayer = require('mineflayer')
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder')
const Vec3 = require('vec3')
const axios = require('axios')
const net = require('net')

const BOT_HOST = process.env.MC_HOST || 'localhost'
const BOT_PORT = parseInt(process.env.MC_PORT || '25565')
const ADAPTER_URL = process.env.ADAPTER_URL || 'http://localhost:8001/observe'
const TARGET_REL = { x: 2, y: 0, z: 0 } // target block relative to spawn

let bot = null

function waitForPort(host, port, timeoutMs = 60000) {
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

async function run() {
  console.log('E2E: waiting for minecraft')
  try {
    await waitForPort(BOT_HOST, BOT_PORT, 120000)
  } catch (e) {
    console.error('minecraft did not open port:', e.message)
  }

  bot = mineflayer.createBot({ host: BOT_HOST, port: BOT_PORT, username: 'e2e_bot', auth: 'offline' })
  bot.loadPlugin(pathfinder)

  bot.once('spawn', async () => {
    console.log('E2E: bot spawned, finding spawn point')
    const spawn = bot.entity.position
    const targetPos = spawn.offset(TARGET_REL.x, TARGET_REL.y, TARGET_REL.z)
    console.log('E2E: target relative pos', TARGET_REL, '=>', targetPos)

    const mcData = require('minecraft-data')(bot.version)
    const defaultMove = new Movements(bot, mcData)
    bot.pathfinder.setMovements(defaultMove)

    try {
      const goal = new goals.GoalBlock(targetPos.x, targetPos.y, targetPos.z)
      console.log('E2E: moving to target')
      await bot.pathfinder.goto(goal)
      console.log('E2E: reached target, attempting to dig')

      // look at block and dig
      const block = bot.blockAt(targetPos)
      if (!block) {
        console.error('E2E: no block found at target')
      } else {
        console.log('E2E: block type:', block.name)
        await bot.dig(block)
        console.log('E2E: block mined')
      }

      // notify adapter with a completion marker
      try {
        await axios.post(ADAPTER_URL, { agent_id: 'e2e_bot', event: 'mined_block', coords: targetPos })
        console.log('E2E: posted completion to adapter')
      } catch (e) {
        console.warn('E2E: failed to post completion', e && e.message)
      }

      // exit after a short delay
      setTimeout(() => process.exit(0), 2000)
    } catch (e) {
      console.error('E2E: error during navigation/dig:', e && e.message)
      process.exit(2)
    }
  })

  bot.on('error', (err) => {
    console.error('Bot error', err && err.stack)
  })
}

run()
