import argparse, json, random, string, base64, asyncio, websockets
from communication import interact

def confirm_deny_cancel(inp):
	prediction = ai_predict(inp)['prediction_data']
	if prediction['certainty'] > 0.7:
		print (prediction['tag'])
		if prediction['tag'] == 'cancel':
			print('exit script bruh')
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

def create_action(trigger):
	f_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	with open('intents/'+f_name+'.json','w') as f:
		data = {}
		data['intents'] = []
		data['intents'].append({'tag':f_name,'patterns':[trigger],'responses':['$action:'+f_name+'.py'],'context_set':""})
		json.dump(data, f)
	with open('action/'+f_name+'.py','a') as f:
		f.write('# saying: "'+trigger+'" will execute this script.\n')
		template = open('action/templates/action_template.py','r')
		for line in template.readlines():
			f.write(line)
		template.close()

def main(data):
	while True:
		interact.say('what action should i create?')
		action = interact.get_input()
		confirm_deny_cancel(action)
		interact.say('create action '+action+'?')
		inp = interact.get_input()
		if confirm_deny_cancel(inp) == 'confirm':
			create_action(action)
			interact.say('ok. i created a new action for you.')
			exit()
		elif confirm_deny_cancel(inp) == 'deny':
			interact.say('sorry. lets try that again.')
		

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True)
args = parser.parse_args()
wrapped = args.data
unwrapped = base64.b64decode(wrapped.encode('utf-8'))
call_json = json.loads(unwrapped.decode('utf-8'))
main(call_json)