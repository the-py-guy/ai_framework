import asyncio, websockets, json, os, base64
from multiprocessing import Process, Pipe
from ai import ai
working_dir = os.path.dirname(os.path.abspath(__file__))+'/'

def srv_says(data):
	print('[SERVER]: '+data)

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

def set_code_signature():
	code = ''
	for x in os.listdir(working_dir+'../intents'):
		if '.json' in x:
			contents = open(working_dir+'../intents/'+x, 'r')
			for y in contents.readlines():
				code = code+y
		contents.close()

	with open(working_dir+'code_signature.txt','w') as f:
		code_signature = base64.b64encode(code.encode('utf-8'))
		f.write(code_signature.decode('utf-8'))
		f.close()

def compare_code_signature():
	code = ''
	for x in os.listdir(working_dir+'../intents'):
		if '.json' in x:
			contents = open(working_dir+'../intents/'+x, 'r')
			for y in contents.readlines():
				code = code+y
		contents.close()
	current_signature = base64.b64encode(code.encode('utf-8')).decode('utf-8')
	previous_signature = open(working_dir+'code_signature.txt','r').readlines()[0]
	if current_signature == previous_signature:
		return True
	else:
		return False

def server():
	asyncio.get_event_loop().run_until_complete(
		websockets.serve(handle_request, 'localhost', 8765))
	asyncio.get_event_loop().run_forever()

def main(parent_process):
	try:
		srv_says('checking for code_signature.txt')
		compare_code_signature()
	except:
		srv_says('code_signature.txt doesnt exist')
		srv_says('creating code_signature.txt')
		
		srv_says('training ai for the first time')
		ai.train_ai()
		set_code_signature()
		srv_says('done training ai for the first time')

	if compare_code_signature():
		srv_says('code signatures are the same ai will start normally')
		ai.normal_start()
		srv_says('ai started normally')
	else:
		srv_says('code signature didnt match')
		srv_says('updating code signature')
		set_code_signature()
		srv_says('updated code signature')
		srv_says('training ai')
		ai.train_ai()
		srv_says('trained ai')
		srv_says('starting ai normally')
		ai.normal_start()
	srv_says('starting server')
	parent_process.send(True)
	parent_process.close()
	server()
