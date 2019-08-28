import handler, websockets, asyncio, json
from multiprocessing import Process, Pipe
from ai import ai_server

async def request(uri, data):
	async with websockets.connect(uri) as websocket:
		await websocket.send(data)
		return dict(json.loads(await websocket.recv()))

def ai_predict(data):
	return asyncio.get_event_loop().run_until_complete(
		request('ws://localhost:8765', data))


parent_conn, child_conn = Pipe()
server = Process(target=ai_server.main, args=(child_conn,))
server.start()

if parent_conn.recv():
	while True:
		inp = input('you: ')
		response = ai_predict(inp)
		handler.response_handler(response)


