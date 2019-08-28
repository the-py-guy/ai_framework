import argparse, base64, json, asyncio, websockets

def confirm_deny_cancel(inp):
	prediction = ai_predict(inp)['prediction_data']
	if prediction['certainty'] > 0.7:
		if prediction['tag'] == 'cancel':
			exit()
		else:
			return prediction['tag']

async def request(uri, data):
	async with websockets.connect(uri) as websocket:
		await websocket.send(data)
		return dict(json.loads(await websocket.recv()))

def ai_predict(data):
	return asyncio.get_event_loop().run_until_complete(
		request('ws://localhost:8765', data))


def main(data):
	print('looks like you havent programmed me to do this yet. heres some data: '+str(data))
		

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True)
args = parser.parse_args()
wrapped = args.data
unwrapped = base64.b64decode(wrapped.encode('utf-8'))
call_json = json.loads(unwrapped.decode('utf-8'))
main(call_json)