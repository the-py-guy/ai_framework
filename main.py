import asyncio, websockets, handler, json, os, time
from subprocess import Popen, PIPE, STDOUT


async def request(uri, data):
	async with websockets.connect(uri) as websocket:
		await websocket.send(data)
		return dict(json.loads(await websocket.recv()))

def ai_predict(data):
	return asyncio.get_event_loop().run_until_complete(
		request('ws://localhost:8765', data))

p = Popen(["python","ai/ai_server.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p.stdout.readline().rstrip()

while True:
	inp = input('you: ')
	response = ai_predict(inp)
	handler.response_handler(response)