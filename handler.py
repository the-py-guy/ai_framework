import random, os, base64, json
from action.communication import interact

action_files_path = 'action/'

def response_handler(response):
	if response['prediction_data']['certainty'] > 0.7:
		action = None
		for x in response['prediction_data']['responses']:
			if '$action' in x:
				action = x
				break
		if action is not None:
			handle_action(response, action)
		else:
			interact.say(random.choice(response['prediction_data']['responses']))
	else:
		interact.say("im not sure what you mean by "+response['trigger_phrase'])

def handle_action(response, action):
	action = action.split(':')[1]
	wrapped = base64.b64encode(json.dumps(response).encode("utf-8"))
	command = "python "+action_files_path+action+" --data '"+wrapped.decode('utf-8')+"'"
	os.system(command)