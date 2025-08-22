const axios = require('axios');

const adapterUrl = process.env.ADAPTER_URL || 'http://adapter:8001/observe';

async function loop() {
  try {
    const state = Buffer.from(JSON.stringify({ hello: 'world', t: Date.now() })).toString('base64');
    const resp = await axios.post(adapterUrl, { state });
    console.log('Adapter response:', resp.data);
  } catch (err) {
    console.error('Error sending observation', err.message || err);
  }
}

setInterval(loop, 2000);
console.log('Mock bot started, sending observations to', adapterUrl);
