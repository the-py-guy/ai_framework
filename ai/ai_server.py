import asyncio, websockets, ai, argparse, json



def payload_constructor(inp,prediction):
	json_data = {}
	json_data['trigger_phrase'] = inp
	json_data['prediction_data'] = {}
	for x in prediction:
		json_data['prediction_data'][x] = prediction[x]
	return json.dumps(json_data)

async def handle_request(websocket, path):
	async for request in websocket:
		prediction = ai.predict_response(request)
		await websocket.send(payload_constructor(request, prediction))

parser = argparse.ArgumentParser()
parser.add_argument("--train", action = 'store_true')
args = parser.parse_args()

if args.train:
	ai.train_ai()
else:
	ai.normal_start()
	asyncio.get_event_loop().run_until_complete(
		websockets.serve(handle_request, 'localhost', 8765))
	asyncio.get_event_loop().run_forever()