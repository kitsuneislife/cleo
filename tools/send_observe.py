import json
import base64
import urllib.request

url = 'http://localhost:8001/observe'
state = json.dumps({'hello':'world'})
state_b64 = base64.b64encode(state.encode('utf-8')).decode('ascii')
body = json.dumps({'agent_id':'bot1','state':state_b64}).encode('utf-8')
req = urllib.request.Request(url, data=body, headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print('status', resp.status)
        print(resp.read().decode('utf-8'))
except Exception as e:
    print('error', e)
